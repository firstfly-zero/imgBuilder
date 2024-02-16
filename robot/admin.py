from django.contrib import admin
from robot.models import Config, LarkBotInfo, WxSdtask, LarkSdtask, WxMjtask, LarkMjtask, WxImage

@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):
    list_display = ['id', 'key', 'value', 'desc', 'type', 'content']
    list_editable = ['key', 'value', 'desc', 'type', 'content']

@admin.register(LarkBotInfo)
class LarkBotInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'desc', 'app_id', 'app_secret', 'type', 'extra_config']
    list_editable = ['desc', 'app_id', 'app_secret', 'type', 'extra_config']

@admin.register(WxSdtask)
class WxSdtaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'status']
    list_editable = ['status']

@admin.register(LarkSdtask)
class LarkSdtaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'status']
    list_editable = ['status']

@admin.register(WxMjtask)
class WxMjtaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'status']
    list_editable = ['status']

@admin.register(LarkMjtask)
class LarkMjtaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'status']
    list_editable = ['status']

@admin.register(WxImage)
class WxImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'url']
    list_editable = ['url']
