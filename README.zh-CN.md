<div align="center">

# **MyBlog**

大学程序设计课程中的 Django 博客项目。

用富文本编写文章，按分类与标签整理内容，并提供个人主页、评论和消息通知。

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](requirements.txt) [![Django](https://img.shields.io/badge/Django-5.2.8-092E20?logo=django&logoColor=white)](requirements.txt) [![MySQL](https://img.shields.io/badge/database-MySQL-4479A1)](#配置说明)

[English](README.md) · [简体中文](README.zh-CN.md)

[功能](#功能) · [本地运行](#本地运行) · [配置说明](#配置说明) · [仓库内容](#仓库内容) · [参与贡献](#参与贡献)

</div>

## 项目状态

课程项目仓库，保存 Django 5.2.8 应用、站点设置和数据脚本，主要供本地学习与演示。
面向公网部署前，需要进一步检查认证、上传处理和部署配置。

当前富文本依赖包含已停止维护的 CKEditor 4.22.1，Django 检查会提示
`ckeditor.W001`。正式部署前需要替换编辑器，或选用仍受支持的发行版。

## 功能

- 富文本文章、草稿、分类、标签、搜索和分页。
- 个人头像、博客标题、背景与主题设置。
- 评论与回复、点赞、消息通知和作者主页。
- Django 管理后台、django-allauth 账号路由和只读文章 API。

源码配置了 GitHub 与 Google 登录提供方，实际使用时需要自行配置应用凭据和站点信息。

## 本地运行

需要 Python 3.10 或更新版本，以及本地 MySQL 服务。在仓库根目录建立虚拟环境：

~~~powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
~~~

在同一个终端中设置配置。下面会生成新的开发密钥，并询问本地数据库账号的密码：

~~~powershell
$env:DJANGO_SECRET_KEY = python -c "import secrets; print(secrets.token_urlsafe(64))"
$env:DJANGO_DEBUG = "1"
$env:DJANGO_ALLOWED_HOSTS = "127.0.0.1,localhost"
$env:DB_NAME = "my_blog_db"
$env:DB_USER = "myblog"
$env:DB_PASSWORD = [System.Net.NetworkCredential]::new("", (Read-Host "MySQL password" -AsSecureString)).Password
~~~

使用 MySQL 管理工具创建数据库，并为该账号授予所需权限，然后运行：

~~~powershell
python manage.py check
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
~~~

打开 `http://127.0.0.1:8000/`。博客列表位于 `/blog/`，管理后台位于 `/admin/`，
只读文章 API 位于 `/api/posts/`。

原课程依赖清单漏列的运行时包已补齐，但原环境中的具体版本
没有记录。恢复环境后应验证并保存实际解析到的版本，再把它作为可复现的课程环境。

## 配置说明

[.env.example](.env.example)列出了不含真实凭据的配置项。它只是参考文件，程序读取
进程环境变量，不会自动加载 `.env`。

| 变量 | 用途 |
| --- | --- |
| `DJANGO_SECRET_KEY` | 必填的新密钥，至少 50 个字符；拒绝沿用旧的开发密钥格式 |
| `DJANGO_DEBUG` | 默认 `0`；仅本地开发时设为 `1` |
| `DJANGO_ALLOWED_HOSTS` | 逗号分隔的主机名，默认只包含本地回环名称 |
| `DB_NAME`、`DB_USER`、`DB_PASSWORD` | 数据库名称、账号与必填密码 |
| `DB_HOST`、`DB_PORT` | MySQL 地址，默认为 `127.0.0.1:3306` |
| `EMAIL_*`、`DEFAULT_FROM_EMAIL` | 邮件配置；默认把邮件内容输出到控制台 |
| `MYBLOG_DEMO_PASSWORD_RESET` | 默认 `0`；直接展示重置链接还要求 `DJANGO_DEBUG=1` |

真实用户环境必须关闭演示重置选项。它会在浏览器里直接显示重置链接，仅供隔离的课堂
演示。正常密码重置走邮件流程，控制台邮件适合本地查看。

仓库源码曾保存开发密钥与数据库密码，并跟踪了可携带旧配置的 Python 字节码。
如果使用过这些值，需要更换。清理当前文件不会撤销凭据，也不会清除 Git 历史，具体见[安全说明](SECURITY.md)。

## 数据脚本

对任何数据库执行前，先检查这些脚本：

- `myblog/setup_db.py`：显式运行时创建配置的数据库，需要账号具有建库权限。
- `populate_db.py`：添加演示数据。新建演示账号没有可登录密码；本次修改不会重置
  数据库中已有账号的密码。
- `fix_site.py`：修改 Django Site 记录并清除社交应用关联，属于维护操作，不是常规
  启动步骤。
- `local_settings.py`：保存站点展示文字；凭据由环境变量单独提供。

## 仓库内容

| 路径 | 内容 |
| --- | --- |
| `manage.py` | Django 命令行入口 |
| `myblog/` | 配置、路由、应用入口和建库辅助脚本 |
| `core/` | 模型、视图、模板和数据库迁移 |
| `requirements.txt` | Python 依赖声明 |
| `.env.example` | 不含秘密的配置参考 |

## 参与贡献

[贡献指南](CONTRIBUTING.md)说明本地检查和数据处理要求。普通问题可在 Issues 中附上
复现步骤与脱敏后的错误信息；敏感问题请按[安全说明](SECURITY.md)报告。

## 许可证

仓库目前未声明统一的许可证。第三方依赖和外部资源保留各自条款；再分发前需要明确
相关内容的复用权利。
