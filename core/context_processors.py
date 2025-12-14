from .models import Notification, SiteSetting


def global_context(request):
    context = {}

    if request.user.is_authenticated:
        context['notifications'] = Notification.objects.filter(recipient=request.user, is_read=False)

    # 获取设置
    setting = SiteSetting.objects.first()
    if not setting:
        setting = SiteSetting.objects.create()

    context['SITE_TITLE'] = setting.site_name
    context['SITE_DESC'] = setting.site_desc
    context['SITE_OWNER'] = setting.owner_name
    context['SEO_KEYWORDS'] = setting.seo_keywords

    # 👇 传递主题和背景 👇
    context['CURRENT_THEME'] = setting.theme_color
    if setting.site_background:
        context['SITE_BG_URL'] = setting.site_background.url
    else:
        context['SITE_BG_URL'] = None

    return context