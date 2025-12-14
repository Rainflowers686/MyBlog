import pymysql

# --- 配置区 ---
MYSQL_PASSWORD = 'lidagezuishuai66'  # <--- 【必改】这里填你刚才测试成功的那个正确密码！
# ----------------

print("正在连接 MySQL...")
try:
    # 连接到 MySQL 服务（不指定数据库）
    conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password=MYSQL_PASSWORD
    )
    cursor = conn.cursor()

    # 创建数据库
    print("正在创建数据库 my_blog_db ...")
    cursor.execute("CREATE DATABASE IF NOT EXISTS my_blog_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")

    print("✅ 成功！数据库已创建。")
    conn.close()

except Exception as e:
    print(f"❌ 出错了: {e}")