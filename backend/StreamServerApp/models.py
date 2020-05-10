from django.db import models
from django.contrib.postgres.search import TrigramSimilarity
from django.core.exceptions import ObjectDoesNotExist


class SearchManager(models.Manager):
    def search_trigramm(self, model_field, query):
        queryset = self.annotate(similarity=TrigramSimilarity(model_field, query)) \
                .filter(similarity__gte=0.01) \
                .order_by('-similarity')
        return queryset


class Movie(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title

    objects = SearchManager()


class Series(models.Model):
    title = models.CharField(max_length=200)
    thumbnail = models.CharField(max_length=300, default="")

    def __str__(self):
        return self.title

    objects = SearchManager()

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
    metadata = models.CharField(max_length=100, default="")
    video_url = models.CharField(max_length=300, default="")
    video_folder = models.CharField(max_length=300, default="")
    thumbnail = models.CharField(max_length=300, default="")
    fr_subtitle_url = models.CharField(max_length=300, default="")
    en_subtitle_url = models.CharField(max_length=300, default="")
    # This field describes the path to the subtitle shipped with the input video
    ov_subtitle_url = models.CharField(max_length=300, default="")

    # Relations to series and movies
    # on_delete=SET_NULL keeps videos indexed if we remove a serie or a video it belongs to
    series = models.ForeignKey(Series, null=True, on_delete=models.SET_NULL)
    movie = models.ForeignKey(Movie, null=True, on_delete=models.SET_NULL)

    # For series & movie episodes and series seasons
    episode = models.PositiveSmallIntegerField(default=None, null=True)
    season = models.PositiveSmallIntegerField(default=None, null=True)

    objects = SearchManager()
    
    @property
    def next_episode(self):
        if self.series:
            try:
                return self.series.video_set.get(episode=self.episode+1, season=self.season).id
            except ObjectDoesNotExist:
                return None
