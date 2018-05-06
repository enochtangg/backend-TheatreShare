from django.contrib import admin
from .models import Theatre


admin.site.register(
    Theatre,
    list_display=["id", "name", "youtube_url"],
    list_display_links=["id", "name"],
)