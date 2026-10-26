"""Create the configured development database when invoked explicitly."""

import os
import re
import sys

import pymysql


def main():
    password = os.environ.get("DB_PASSWORD")
    if not password:
        print("Set DB_PASSWORD before creating the database.", file=sys.stderr)
        return 1
    database = os.environ.get("DB_NAME", "my_blog_db")
    if not re.fullmatch(r"[A-Za-z0-9_]+", database):
        print("DB_NAME may contain only letters, numbers and underscores.", file=sys.stderr)
        return 1
    try:
        connection = pymysql.connect(
            host=os.environ.get("DB_HOST", "127.0.0.1"),
            port=int(os.environ.get("DB_PORT", "3306")),
            user=os.environ.get("DB_USER", "myblog"),
            password=password,
            charset="utf8mb4",
        )
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    f"CREATE DATABASE IF NOT EXISTS `{database}` "
                    "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
                )
        print("Database is ready.")
        return 0
    except (pymysql.MySQLError, ValueError) as error:
        print(f"Database setup failed ({type(error).__name__}); check the local MySQL configuration.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
