import os
import django

# 设置 Django 环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myblog.settings')
django.setup()

from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp

print("🔍 正在执行【强力解绑】修复...")

target_domain = '127.0.0.1:8000'
target_name = 'MyBlog'

# 1. 找到那个占着茅坑的站点 (通常是 ID=2)
existing_site = Site.objects.filter(domain=target_domain).first()

if existing_site:
    print(f"ℹ️ 找到目标站点: ID={existing_site.id} | 域名={existing_site.domain}")

    # --- 关键步骤：解除关联 ---
    # 这步操作会删除该站点与所有 SocialApp 的连接记录，解决 IntegrityError
    print("🔗 正在解除与社交账号的绑定（防止报错）...")
    existing_site.socialapp_set.clear()

    # 2. 如果 ID 不是 1，强行改成 1
    if existing_site.id != 1:
        print(f"🔄 正在将 ID 从 {existing_site.id} 修改为 1 ...")

        # 确保 ID=1 的位置是空的
        Site.objects.filter(id=1).delete()

        # 强行更新 ID
        Site.objects.filter(id=existing_site.id).update(id=1)
        print("✅ ID 修改成功！")
    else:
        print("✅ ID 已经是 1 了，无需修改。")

else:
    # 如果完全找不到，就新建
    print("⚠️ 未找到站点，正在新建 ID=1 ...")
    Site.objects.filter(id=1).delete()  # 确保坑位干净
    Site.objects.create(id=1, domain=target_domain, name=target_name)

print("-" * 30)
print("🚀 修复完成！现在的站点列表：")
for s in Site.objects.all():
    print(f"ID: {s.id} | 域名: {s.domain}")

print("-" * 30)
print("⚠️ 重要提示：")
print("因为刚才执行了解绑，请登录后台 (http://127.0.0.1:8000/admin/)")
print("进入 'Social applications'，重新把 Google/GitHub 和站点关联一下！")