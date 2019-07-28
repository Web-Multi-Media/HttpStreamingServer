from django.contrib import admin
from StreamServerApp.models import Video
from StreamServerApp.utils import delete_DB_Infos, populate_db_from_local_folder
from django.conf import settings


def reload_video(modeladmin, request, queryset):
    selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
    data = request.POST.copy()
    if len(selected) == 0 and data['action'] in ('reload_video'):
        delete_DB_Infos()
        populate_db_from_local_folder(settings.VIDEO_ROOT, settings.VIDEO_URL)
        reload_video.short_description = "Reload videos"
    else:
        return super(VideoAdmin, self).response_action(request, queryset)


class VideoAdmin(admin.ModelAdmin):
    actions = []

admin.site.register(Video, VideoAdmin)
admin.site.add_action(reload_video)