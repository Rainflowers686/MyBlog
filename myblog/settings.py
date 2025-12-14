import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# 生产环境请修改密钥
SECRET_KEY = 'django-insecure-dynamic-sky-blue-theme-key'
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ckeditor',
    'ckeditor_uploader', # 用于上传图片

    # 关键：必须有这个，后台才会有 Sites
    'django.contrib.sites',

    # 第三方库
    'core',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.github',
    'rest_framework', # 新增
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'myblog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',  # Allauth 需要
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.global_context',  # 我们的通知小红点

            ],
        },
    },
]

WSGI_APPLICATION = 'myblog.wsgi.application'

# 数据库 (请确保密码正确！！！)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'my_blog_db',
        'USER': 'root',
        'PASSWORD': 'lidagezuishuai66',  # <--- 【必改】这里一定要填你 MySQL 的真实密码
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

# 用户认证与登录
AUTH_USER_MODEL = 'core.User'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# 站点ID
SITE_ID = 1
ACCOUNT_EMAIL_VERIFICATION = 'none'

# 国际化设置 (中文)
LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_TZ = True

# 静态文件
STATIC_URL = 'static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- CKEditor 富文本编辑器配置 ---
CKEDITOR_UPLOAD_PATH = "uploads/" # 图片上传路径
CKEDITOR_IMAGE_BACKEND = "pillow"

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',  # 开启全功能工具栏
        'height': 400,
        'width': '100%',
        # 开启代码块、图片上传、Youtube视频插入等插件
        'extraPlugins': ','.join([
            'codesnippet',
            'uploadimage',
            'div',
            'autolink',
            'autoembed',
            'embedsemantic',
            'widget',
        ]),
    },
}


# --- 邮件配置 (开发模式) ---
# 将邮件打印到终端，而不是真的发送 (防止报错)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = 'Webmaster <webmaster@localhost>'