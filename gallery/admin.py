from django.contrib import admin
from gallery.models import Image, Album, Gallery, Secret, AgentInviteInfo

@admin.register(Image)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ['id', 'url', 'tag', 'status']
    list_editable = ['url', 'status']

@admin.register(Album)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ['id', 'album_name', 'title', 'desc', 'status']
    list_editable = ['album_name', 'status']

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ['id', 'gallery_name', 'invite_code', 'status']
    list_editable = ['gallery_name', 'status']

