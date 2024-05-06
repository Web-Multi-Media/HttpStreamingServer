from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.search import TrigramSimilarity
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from StreamServerApp.subtitles import get_subtitles
from StreamServerApp.media_processing import convert_subtitles_to_webvtt, resync_subtitle
from StreamServerApp.media_management.fileinfo import createfileinfo, readfileinfo
import os
import subprocess
import shutil

import logging 

logger = logging.getLogger("root")


class SearchManager(models.Manager):
    def search_trigramm(self, model_field, query):
        queryset = self.annotate(similarity=TrigramSimilarity(model_field, query)) \
            .filter(similarity__gte=0.01) \
            .order_by('-similarity')
        return queryset


class CommonInfo(models.Model):
    title = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = SearchManager()

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class Movie(CommonInfo):
    pass


class Series(CommonInfo):
    thumbnail = models.CharField(max_length=300, default="")

    @property
    def season_list(self):
        return list(set(self.video_set.values_list('season', flat=True)))

    def return_season_episodes(self, season):
        return self.video_set.filter(season=season).order_by('episode')


class Video(models.Model):

    name = models.CharField(max_length=200)
    video_codec = models.CharField(max_length=100, default="")
    height = models.IntegerField(default=0)
    width = models.IntegerField(default=0)
    audio_codec = models.CharField(max_length=100, default="")
    metadata = models.CharField(max_length=100, blank=True, default="")
    video_url = models.CharField(max_length=300, default="")
    video_folder = models.CharField(max_length=300, default="")
    audio_path = models.CharField(max_length=300, default="")
    thumbnail = models.CharField(max_length=300, default="")

    # Relations to series and movies
    # on_delete=SET_NULL keeps videos indexed if we remove a serie or a video it belongs to
    series = models.ForeignKey(Series, blank=True, null=True, on_delete=models.SET_NULL)
    movie = models.ForeignKey(Movie, blank=True, null=True, on_delete=models.SET_NULL)

    # For series & movie episodes and series seasons
    episode = models.PositiveSmallIntegerField(default=None, blank=True,  null=True, db_index=True)
    season = models.PositiveSmallIntegerField(default=None, blank=True, null=True, db_index=True)

    history = models.ManyToManyField(User, through='UserVideoHistory')

    objects = SearchManager()
    
    @property
    def next_episode(self):
        if self.series:
            try:
                return self.series.video_set.get(episode=self.episode+1, season=self.season).id
            except ObjectDoesNotExist:
                try:
                    return self.series.video_set.get(episode=1, season=self.season+1).id
                except ObjectDoesNotExist:
                    return None

    def return_user_time_history(self, user):
        video_history = self.uservideohistory_set.filter(user=user)
        if video_history.count() > 0:
            return video_history.first().time
        else:
            return 0

    def get_subtitles(self, video_path, remote_url):
        """ # get subtitles for the current instance of video.
            Args:
            ov_subtitles: boolean (True if input has subtitles, False if not).
        """
        video_infos = []
        fileinfos_path = "{}/fileinfo.json".format(
            os.path.split(self.video_folder)[0])
        if os.path.isfile(fileinfos_path):
            video_infos = readfileinfo(fileinfos_path)
            if not video_infos:
                logger.debug("video infos are empty, don't add subs")
                return 0
        else:
            logger.debug("{} is not a file ".format(fileinfos_path))
            return 0

        subtitles_list = get_subtitles(video_infos["video_full_path"])

        webvtt_subtitles_full_path = subtitles_list[0]
        srt_subtitles_full_path = subtitles_list[1]
        webvtt_subtitles_remote_path = {}
        for language_str, srt_subtitle_url in webvtt_subtitles_full_path.items():
            webvtt_subtitles_remote_path[language_str] = ''
            vtt_subtitle_url = webvtt_subtitles_full_path[language_str]
            if srt_subtitle_url and vtt_subtitle_url:
                webvtt_subtitles_relative_path = os.path.relpath(
                    vtt_subtitle_url, video_path)
                newsub = Subtitle()
                newsub.video_id = self
                newsub.vtt_path = vtt_subtitle_url
                if srt_subtitles_full_path.get(language_str):
                    newsub.srt_path = srt_subtitles_full_path[language_str]
                newsub.webvtt_subtitle_url = os.path.join(
                    remote_url, webvtt_subtitles_relative_path)
                newsub.language = language_str
                newsub.save()

    def __str__(self):
        return '{}'.format(self.name)


class UserVideoHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    time = models.IntegerField()   # time in sec
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)


class Subtitle(models.Model):
    webvtt_subtitle_url = models.CharField(max_length=300, default="")
    webvtt_sync_url = models.CharField(max_length=300, default="")
    srt_path = models.CharField(max_length=300, default="")
    srt_sync_path = models.CharField(max_length=300, default="")
    vtt_path = models.CharField(max_length=300, default="")
    vtt_sync_path = models.CharField(max_length=300, default="")
    FRENCH = 'fra'
    ENGLISH = 'eng'
    OV = 'OV'
    LANGUAGE_CHOICES = [
        (FRENCH, 'French'),
        (ENGLISH, 'English'),
        (OV, 'Original Version'),
    ]
    language = models.CharField(
        max_length=3,
        choices=LANGUAGE_CHOICES,
        default=ENGLISH,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    video_id = models.ForeignKey(Video, related_name='subtitles', on_delete=models.CASCADE)
    uploaded_data = models.FileField(upload_to='uploads/', default='')

    def resync(self):
        """ # resync current instance of sub
            Args:
            subtitle_id: subtitles id
        """
        video_path = self.video_id.audio_path
        subtitle_path = self.srt_path
        webvtt_path = self.vtt_path.replace('.vtt', '_sync.vtt')
        sync_subtitle_path = subtitle_path.replace('.srt', '_sync.srt')
        resync_subtitle(video_path, subtitle_path, sync_subtitle_path)
        convert_subtitles_to_webvtt(sync_subtitle_path, webvtt_path)
        self.srt_sync_path = sync_subtitle_path
        self.vtt_sync_path = webvtt_path
        if settings.VIDEO_ROOT in webvtt_path:
            self.webvtt_sync_url = os.path.join(settings.VIDEO_URL, webvtt_path.split(settings.VIDEO_ROOT)[1])
            self.save()
        elif "/usr/torrent/" in webvtt_path:
            self.webvtt_sync_url = os.path.join("/torrents", webvtt_path.split("/usr/torrent/")[1])
            self.save()
        else:
            logger.error("Something went wrong during resync")

    def __str__(self):
        return 'lang = {},\
webvtt_subtitle_url = {} \
webvtt_sync_url = {} \
srt_path = {} \
srt_sync_path = {} \
vtt_path = {} \
vtt_sync_path = {} \
'.format(self.language,
         self.webvtt_subtitle_url,
         self.webvtt_sync_url,
         self.srt_path, self.srt_sync_path, self.vtt_path, self.vtt_sync_path)


def delete_subtitle(sub: Subtitle) -> None:
    if os.path.isfile(sub.srt_path):
        os.remove(sub.srt_path)
    if os.path.isfile(sub.vtt_path):
        os.remove(sub.vtt_path)
    if os.path.isfile(sub.vtt_sync_path):
        os.remove(sub.vtt_sync_path)
    if os.path.isfile(sub.srt_sync_path):
        os.remove(sub.srt_sync_path)


#This function should be called before Video instance deletion
def delete_video_related_assets(Video_input: Video) -> None:
    playlistdir = os.path.split(Video_input.video_folder)[0]
    if os.path.isdir(playlistdir):
        logger.debug("removing directory: {}".format(playlistdir))
        shutil.rmtree(playlistdir, ignore_errors=True)
    logger.debug("removing audio ", Video_input.audio_path)
    if os.path.isfile(Video_input.audio_path):
        os.remove(Video_input.audio_path)
    logger.debug("removing subtitles")
    subs = Subtitle.objects.filter(video_id=Video_input)
    for sub in subs:
        delete_subtitle(sub)
