import os
import django
import random

# 1. 设置 Django 环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myblog.settings')
django.setup()

from django.contrib.auth import get_user_model
from core.models import Category, Tag, Post, Comment

User = get_user_model()

# 2. 准备一些假数据素材
CATEGORY_NAMES = ['Python教程', '生活感悟', '旅行日记', '美食分享', '科技前沿']
TAG_NAMES = ['Django', '学习', '周末', '快乐', 'Bug修复', '风景', '打卡']
USER_NAMES = ['Alice', 'Bob', 'Charlie', 'David', 'Eva']

TITLES = [
    "为什么 Django 是最好的 Web 框架？",
    "今天天气真不错，去公园散步了",
    "Python 学习笔记：列表推导式",
    "我的第一次独自旅行",
    "如何用 Python 批量处理 Excel",
    "推荐一家超好吃的火锅店！",
    "程序员的自我修养",
    "2025年最新科技趋势解读",
    "解决 Django 数据库迁移报错的方法",
    "周末躺平指南",
]

CONTENT_TEMPLATE = """
这里是文章的开头，**Markdown 语法测试**。

## 第一章：背景
这是一个测试段落，用来展示{topic}的相关内容。Django 真的很有趣！

- 列表项 1
- 列表项 2

> 这是一个引用块，用来测试样式。

### 结论
希望大家喜欢这篇文章。欢迎在评论区留言！
"""


def run():
    print("🚀 开始生成测试数据...")

    # --- 1. 创建分类 ---
    categories = []
    for name in CATEGORY_NAMES:
        cat, _ = Category.objects.get_or_create(name=name)
        categories.append(cat)
    print(f"✅ 创建了 {len(categories)} 个分类")

    # --- 2. 创建标签 ---
    tags = []
    for name in TAG_NAMES:
        tag, _ = Tag.objects.get_or_create(name=name)
        tags.append(tag)
    print(f"✅ 创建了 {len(tags)} 个标签")

    # --- 3. 创建用户 ---
    users = []
    for name in USER_NAMES:
        # 密码统一设为 123456
        if not User.objects.filter(username=name).exists():
            u = User.objects.create_user(username=name, email=f"{name.lower()}@example.com", password='123456')
            u.bio = f"我是 {name}，热爱分享生活！"
            u.save()
            users.append(u)
        else:
            users.append(User.objects.get(username=name))
    print(f"✅ 创建了 {len(users)} 个测试用户 (密码均为 123456)")

    # --- 4. 创建文章 ---
    print("✍️ 正在疯狂写文章...")
    for i in range(20):
        author = random.choice(users)
        title = random.choice(TITLES) + f" (No.{i + 1})"
        cat = random.choice(categories)
        is_draft = (i % 5 == 0)  # 每5篇设为一篇草稿

        post = Post.objects.create(
            title=title,
            content=CONTENT_TEMPLATE.format(topic=cat.name),
            author=author,
            category=cat,
            is_draft=is_draft,
            views=random.randint(10, 500)
        )

        # 随机添加 1-3 个标签
        post_tags = random.sample(tags, k=random.randint(1, 3))
        post.tags.set(post_tags)

    # --- 5. 创建评论 ---
    print("🗣️ 正在生成评论...")
    all_posts = Post.objects.filter(is_draft=False)
    for _ in range(30):
        post = random.choice(all_posts)
        user = random.choice(users)
        Comment.objects.create(
            post=post,
            user=user,
            content=f"这篇文章写得太好了！我是 {user.username}，给你点赞！👍"
        )

    print("-" * 30)
    print("🎉 全部完成！测试数据已就绪。")


if __name__ == '__main__':
    run()