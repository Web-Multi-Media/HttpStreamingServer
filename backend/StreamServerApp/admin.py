from django.contrib import admin
from StreamServerApp.models import Video, Movie, Series, Subtitle
from StreamServerApp.database_utils import delete_DB_Infos, populate_db_from_local_folder, update_db_from_local_folder
from django.conf import settings


class VideoAdmin(admin.ModelAdmin):
    search_fields = ['Name']

admin.site.register(Video, VideoAdmin)
admin.site.register(Movie)
admin.site.register(Series)
admin.site.register(Subtitle)
