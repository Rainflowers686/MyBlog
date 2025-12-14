from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from core.views import DemoPasswordResetView
from rest_framework.routers import DefaultRouter
from core import views

router = DefaultRouter()
router.register(r'posts', views.PostViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),

    # --- 找回密码流程 ---
    path('accounts/password/reset/', DemoPasswordResetView.as_view(), name="account_reset_password"),
    path('accounts/password/reset/confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='account/password_reset_from_key.html'),
         name='password_reset_confirm'),
    path('accounts/password/reset/complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='account/password_reset_from_key_done.html'),
         name='password_reset_complete'),

    path('accounts/', include('allauth.urls')),

    # 页面路由
    path('', views.landing, name='landing'),
    path('blog/', views.home, name='home'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('create/', views.create_edit_post, name='create_post'),
    path('edit/<int:pk>/', views.create_edit_post, name='edit_post'),
    path('delete/<int:pk>/', views.delete_post, name='delete_post'),
    path('like/<int:pk>/', views.like_post, name='like_post'),
    path('like/comment/<int:pk>/', views.like_comment, name='like_comment'),
    path('profile/', views.profile, name='profile'),
    path('author/<int:pk>/', views.author_detail, name='author_detail'),
    path('notif/<int:pk>/', views.mark_read, name='mark_read'),

    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('api/', include(router.urls)),

]
# 👇 关键修复：这两行必须在 urlpatterns 列表的外面，用 + 号连接！
# 只有加了这句，你上传的头像才能在网页上显示出来
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)