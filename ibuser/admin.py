from django.contrib import admin
from ibuser.models import IBUser, IBUserInviter, IBUserShare, IBVerificationCode

@admin.register(IBUser)
class IBUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'role']
    list_editable = ['username', 'role']

@admin.register(IBUserInviter)
class IBUserInviterAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'inviter']
    list_editable = ['user', 'inviter']

@admin.register(IBUserShare)
class IBUserShareAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'share_type']

@admin.register(IBVerificationCode)
class IBVerificationCodeAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'code']
    list_editable = ['email', 'code']
