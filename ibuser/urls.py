from django.urls import path
import ibuser.views.userView as userView

urlpatterns = [
    # 用户相关
    path("verify", userView.verify),
    path("register", userView.register),
    path("login", userView.login),
    path("logout", userView.logout),
    path("info", userView.info),
    path("updateInviterInfo", userView.update_inviter),

    # 分享相关
    path("createShare", userView.create_share),
    path("getShare", userView.get_share),

]