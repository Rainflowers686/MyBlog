import pymysql

# 初始化 PyMySQL
pymysql.install_as_MySQLdb()

# --- 新增：版本欺骗补丁 ---
# 这一步是为了骗过 Django 的版本检测
import MySQLdb
MySQLdb.version_info = (2, 2, 1, 'final', 0)