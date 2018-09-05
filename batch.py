"""
    初期設定を行うためのPythonファイルです.
    データベースのセットアップを行います.
"""
import sqlite3

dbname = "database.db"

conn = sqlite3.connect(dbname)

c = conn.cursor()

create_table = """
CREATE TABLE posts (
  filename VARCHAR(16),
  body VARCHAR(512),
  created_at DATETIME
)
"""
c.execute(create_table)

