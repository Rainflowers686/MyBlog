from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from rest_framework import viewsets, serializers

# 引入你的模型和表单
from .models import Post, Comment, Category, Tag, Notification, User
from .forms import PostForm  # 确保你之前创建了 forms.py

import markdown  # 虽然现在用了 CKEditor，为了兼容旧数据可以留着，或者直接删掉


# --- API 相关 (满足 PDF 技术栈) ---
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'created_at', 'views']


class PostViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Post.objects.filter(is_draft=False)
    serializer_class = PostSerializer


# --- 视图函数 ---

# 1. 新增：独立落地页
def landing(request):
    return render(request, 'landing.html')

# 1. 首页 (含搜索、筛选、分页)
def home(request):
    # 获取参数
    query = request.GET.get('q')
    cat_id = request.GET.get('cat')
    tag_id = request.GET.get('tag')

    # 基础查询
    posts = Post.objects.filter(is_draft=False)

    # 搜索逻辑
    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()

    # 筛选逻辑
    if cat_id:
        posts = posts.filter(category_id=cat_id)
    if tag_id:
        posts = posts.filter(tags__id=tag_id)

    # 排序逻辑
    sort_by = request.GET.get('sort', 'date')
    if sort_by == 'popularity':
        posts = posts.order_by('-views')
    else:
        posts = posts.order_by('-created_at')

    # 分页逻辑 (每页 5 篇)
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'home.html', {
        'page_obj': page_obj,
        'categories': Category.objects.all(),
        'tags': Tag.objects.all()
    })


# 2. 文章详情 (含评论发布、通知)
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.views += 1
    post.save()

    # 处理评论提交
    if request.method == 'POST' and request.user.is_authenticated:
        content = request.POST.get('content')
        parent_id = request.POST.get('parent_id')

        parent_comment = None
        if parent_id:
            parent_comment = Comment.objects.get(id=parent_id)

        # 创建评论
        comment = Comment.objects.create(post=post, user=request.user, content=content, parent=parent_comment)

        # 发送通知
        target_user = parent_comment.user if parent_comment else post.author
        if target_user != request.user:
            Notification.objects.create(
                recipient=target_user,
                message=f"{request.user.username} 在《{post.title}》中回复了你",
                url=f"/post/{pk}/"
            )
        return redirect('post_detail', pk=pk)

    return render(request, 'post_detail.html', {
        'post': post,
        'theme_owner': post.author  # <--- 关键！告诉前端用作者的主题
    })


# 3. 写文章/编辑文章 (使用 CKEditor 表单)
@login_required
def create_edit_post(request, pk=None):
    post = get_object_or_404(Post, pk=pk) if pk else None

    if post and post.author != request.user:
        return redirect('home')

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        title = request.POST.get('title')
        cat_name = request.POST.get('category')
        tags_str = request.POST.get('tags')
        is_draft = request.POST.get('is_draft') == 'on'

        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.title = title
            new_post.is_draft = is_draft

            # 分类
            category, _ = Category.objects.get_or_create(name=cat_name) if cat_name else (None, False)
            new_post.category = category

            new_post.save()

            # 标签
            new_post.tags.clear()
            if tags_str:
                for t_name in tags_str.split(','):
                    tag, _ = Tag.objects.get_or_create(name=t_name.strip())
                    new_post.tags.add(tag)

            return redirect('home')

    else:
        form = PostForm(instance=post)

    return render(request, 'post_form.html', {'post': post, 'form': form})


# 4. 删除文章
@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author == request.user:
        post.delete()
    return redirect('profile')


# 5. 文章点赞
@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        is_liked = False
    else:
        post.likes.add(request.user)
        is_liked = True
    return JsonResponse({'liked': is_liked, 'count': post.likes.count()})


# 6. 评论点赞 (就是这里！你之前缺了这个！)
@login_required
def like_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user in comment.likes.all():
        comment.likes.remove(request.user)
        is_liked = False
    else:
        comment.likes.add(request.user)
        is_liked = True
    return JsonResponse({'liked': is_liked, 'count': comment.likes.count()})


# 7. 个人中心
@login_required
def profile(request):
    if request.method == 'POST':
        # 1. 基础信息
        request.user.first_name = request.POST.get('nickname')
        request.user.bio = request.POST.get('bio')

        # 2. 头像 (必须处理 FILES)
        if request.FILES.get('avatar'):
            request.user.avatar = request.FILES['avatar']

        request.user.blog_title = request.POST.get('blog_title')

        # 👇 关键：获取 theme_color，如果前端没传，保持原样，不要覆盖成默认值
        new_theme = request.POST.get('theme_color')
        if new_theme:
            request.user.theme_color = new_theme

        if request.FILES.get('blog_bg'):
            request.user.blog_bg = request.FILES['blog_bg']

        # 4. 👇 修复看板娘开关逻辑 👇
        # HTML复选框机制：选中=提交'on'，没选中=什么都不提交
        # 所以我们判断 'show_live2d' 这个键是否在 request.POST 字典里即可
        request.user.show_live2d = 'show_live2d' in request.POST

        request.user.save()

        # 增加一个成功提示，确保你知道保存成功了
        from django.contrib import messages
        messages.success(request, '✨ 个人设置已更新！')

    user_posts = Post.objects.filter(author=request.user)
    return render(request, 'profile.html', {'user_posts': user_posts})

# 8. 标记通知已读
@login_required
def mark_read(request, pk):
    n = get_object_or_404(Notification, pk=pk, recipient=request.user)
    n.is_read = True
    n.save()
    return redirect(n.url)


# ... 保持前面的代码不变 ...

# 9. 公开的作者个人主页 (新增)
def author_detail(request, pk):
    author = get_object_or_404(User, pk=pk)
    # 获取该作者已发布的所有文章
    posts = Post.objects.filter(author=author, is_draft=False).order_by('-created_at')

    return render(request, 'author_detail.html', {
        'author_user': author,
        'posts': posts,
        'theme_owner': author  # <--- 关键！告诉前端用作者的主题
    })


# ... (上面的代码保持不变) ...

# 👇 底部新增：演示专用重置密码视图 👇
from django.conf import settings
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth import get_user_model


# ... 保持上面的 imports 不变 ...

class DemoPasswordResetView(PasswordResetView):
    success_url = reverse_lazy("account_reset_password_done")
    email_template_name = "account/password_reset_email.txt"
    subject_template_name = "account/password_reset_subject.txt"
    template_name = 'account/password_reset.html'

    def form_valid(self, form):
        if not (settings.DEBUG and settings.MYBLOG_DEMO_PASSWORD_RESET):
            return super().form_valid(form)
        # 1. 正常发邮件 (保持流程完整)
        opts = {
            'use_https': self.request.is_secure(),
            'token_generator': self.token_generator,
            'from_email': self.from_email,
            'email_template_name': self.email_template_name,
            'subject_template_name': self.subject_template_name,
            'request': self.request,
            'html_email_template_name': self.html_email_template_name,
        }
        form.save(**opts)

        # 2. 演示模式：手动生成链接
        email = form.cleaned_data['email']
        User = get_user_model()
        user = User.objects.filter(email=email).first()

        if user:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            # ⚠️ 修正：这里的格式必须和 urls.py 里的 <uidb64>/<token>/ 严格对应！
            # 旧代码（错误）：.../key/{uid}-{token}/
            # 新代码（正确）：.../confirm/{uid}/{token}/
            reset_url = f"/accounts/password/reset/confirm/{uid}/{token}/"

            return render(self.request, 'account/demo_reset_jump.html', {
                'reset_url': reset_url,
                'email': email
            })

        return super().form_valid(form)