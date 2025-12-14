from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Category, Tag, Post, Comment, Notification, SiteSetting



# 1. 用户管理 (支持封禁)
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_active')  # 右侧筛选栏：只看被封禁的用户
    search_fields = ('username', 'email')
    actions = ['disable_user', 'enable_user']

    @admin.action(description='❌ 封禁选中用户')
    def disable_user(self, request, queryset):
        queryset.update(is_active=False)

    @admin.action(description='✅ 解封选中用户')
    def enable_user(self, request, queryset):
        queryset.update(is_active=True)


# 2. 文章管理
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'is_draft', 'views', 'created_at')
    list_filter = ('is_draft', 'category', 'created_at')  # 筛选：只看草稿、只看某分类
    search_fields = ('title', 'content')  # 搜索：搜内容
    date_hierarchy = 'created_at'


# 3. 评论管理 (审核与删除)
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'short_content', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('content', 'user__username')

    def short_content(self, obj):
        return obj.content[:20] + "..." if len(obj.content) > 20 else obj.content

    short_content.short_description = "评论摘要"


# 4. 其他基础配置
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Notification)

# 后台标题美化 (满足 PDF 系统设置需求)
admin.site.site_header = "云端博客管理后台"
admin.site.site_title = "Blog Admin"
admin.site.index_title = "欢迎回来，管理员"

@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'site_desc', 'owner_name')
    # 限制只能有一个配置，禁止添加多个
    def has_add_permission(self, request):
        return not SiteSetting.objects.exists()