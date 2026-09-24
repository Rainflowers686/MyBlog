# MyBlog

*大学程序设计课程中的 Django 博客项目。*


[English](README.md) | [简体中文](README.zh-CN.md)

**导航：**[状态](#项目状态) · [本地运行](#本地运行) · [仓库内容](#仓库内容)


MyBlog 是为大学编程课程编写的 Django 5.2.8 博客项目。

## 项目状态

课程项目仓库，保留应用源码、本地配置和数据脚本。

## 本地运行

建议使用 Python 虚拟环境，在仓库根目录安装 requirements.txt 中的依赖，再启动 Django 开发服务器：

~~~powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py runserver
~~~

项目包含本地设置和数据脚本。运行前先检查其内容，并妥善保护密码、数据库内容和机器专属设置。

## 仓库内容

- manage.py：Django 命令行入口
- myblog/ 和 core/：应用代码
- requirements.txt：Python 依赖
