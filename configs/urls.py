from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic.base import RedirectView
from django.views import static
from django.conf import settings

urlpatterns = [
    # admin 后台
    path("admin/", admin.site.urls),
    # 静态资源访问
    re_path(r'^static/(?P<path>.*)$', static.serve, {'document_root': settings.STATIC_ROOT}, name='static'),
    # 用户相关路由
    path("api/v1/user/", include("ibuser.urls")),
    # 机器人相关路由
    path("api/v1/robot/", include("robot.urls")),
    # 图库相关路由
    path("api/v1/gallery/", include("gallery.urls")),
    # 兜底路由，指向首页
    path('', RedirectView.as_view(url='/static/main/index.html')),
]
