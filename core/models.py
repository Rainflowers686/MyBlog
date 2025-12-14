from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor_uploader.fields import RichTextUploadingField  # 确保安装了 django-ckeditor


# 1. 用户模型 (升级：包含个性化设置)
class User(AbstractUser):
    # 基础信息
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="头像")
    bio = models.TextField(blank=True, verbose_name="个人简介")

    # 👇 新增：个性化博客设置 👇
    blog_title = models.CharField(max_length=50, default="我的个人空间", verbose_name="个人博客标题")
    blog_bg = models.ImageField(upload_to='user_bg/', blank=True, null=True, verbose_name="个人背景图")

    THEME_CHOICES = [
        ('blue', '☁️ 天空之城 (默认天蓝)'),
        ('purple', '🔮 赛博朋克 (霓虹紫)'),
        ('dark', '🌙 深夜模式 (极简黑)'),
        ('green', '🍃 森之秘境 (清新绿)'),
        ('pink', '🌸 樱花烂漫 (柔和粉)'),  # 多加一个颜色
    ]
    theme_color = models.CharField(max_length=20, choices=THEME_CHOICES, default='blue', verbose_name="主题风格")

    show_live2d = models.BooleanField(default=True, verbose_name="显示看板娘")

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = "用户管理"


# 2. 分类与标签
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="分类名称")

    def __str__(self): return self.name

    class Meta: verbose_name = "文章分类"; verbose_name_plural = "文章分类"


class Tag(models.Model):
    name = models.CharField(max_length=100, verbose_name="标签名称")

    def __str__(self): return self.name

    class Meta: verbose_name = "文章标签"; verbose_name_plural = "文章标签"


# 3. 博客文章 (使用富文本)
class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name="标题")
    # 使用 CKEditor 的富文本字段
    content = RichTextUploadingField(verbose_name="内容", help_text="支持图片、代码、视频")

    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="作者")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="分类")
    tags = models.ManyToManyField(Tag, blank=True, verbose_name="标签")

    is_draft = models.BooleanField(default=False, verbose_name="设为草稿")
    views = models.PositiveIntegerField(default=0, verbose_name="阅读量")
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True, verbose_name="点赞用户")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "文章"
        verbose_name_plural = "文章管理"


# 4. 评论系统
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(verbose_name="评论内容")
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    likes = models.ManyToManyField(User, related_name='liked_comments', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta: verbose_name = "评论"; verbose_name_plural = "评论管理"


# 5. 通知系统
class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    url = models.CharField(max_length=200)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta: ordering = ['-created_at']; verbose_name = "消息通知"; verbose_name_plural = "消息通知"


# ... (上面的代码保持不变) ...

# 6. 系统设置 (升级版：支持背景图和主题切换)
class SiteSetting(models.Model):
    site_name = models.CharField(max_length=50, default="我的云端世界", verbose_name="博客名称")
    site_desc = models.CharField(max_length=200, default="记录代码，分享生活", verbose_name="博客描述")
    owner_name = models.CharField(max_length=50, default="站长", verbose_name="站长昵称")
    contact_email = models.EmailField(blank=True, verbose_name="联系邮箱")
    seo_keywords = models.CharField(max_length=200, blank=True, default="Django, Blog, Python",
                                    verbose_name="SEO关键词")

    # 👇 新增：自定义背景和主题 👇
    site_background = models.ImageField(upload_to='site_bg/', blank=True, null=True,
                                        verbose_name="自定义背景图(覆盖主题色)")

    THEME_CHOICES = [
        ('blue', '☁️ 天空之城 (默认天蓝)'),
        ('purple', '🔮 赛博朋克 (霓虹紫)'),
        ('dark', '🌙 深夜模式 (极简黑)'),
        ('green', '🍃 森之秘境 (清新绿)'),
    ]
    theme_color = models.CharField(max_length=20, choices=THEME_CHOICES, default='blue', verbose_name="博客主题风格")

    class Meta:
        verbose_name = "系统设置"
        verbose_name_plural = "系统设置"

    def __str__(self):
        return "站点配置"

    def save(self, *args, **kwargs):
        if not self.pk and SiteSetting.objects.exists():
            return
        super().save(*args, **kwargs)