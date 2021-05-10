import sqlite3

DBNAME = 'database.db'

class SQL:
    def __init__(self, query):
        self.query = query
        self.method = query.split(" ")[0]

    @classmethod
    def initialize_db(cls):
        con = sqlite3.connect(DBNAME)
        cur = con.cursor()
        query = 'create table if not exists users (id int, name varchar(64))'
        cur.execute(query)
        query = 'create table if not exists authors (id int, name varchar(64))'
        cur.execute(query)
        query = 'create table if not exists books (id int, title varchar(64), class_name varchar(64), published_at varchar(64), author_id int)'
        cur.execute(query)
        query = 'create table if not exists users_books_comments (user_id int, book_id int, message varchar(64))'
        cur.execute(query)
        con.commit()
        cur.close()
        con.close()

    def execute(self):
        # データベース接続とカーソル生成
        con = sqlite3.connect(DBNAME)
        cur = con.cursor()
        con.text_factory = str

        results = []
        # SQL文（insert, update）の実行
        if self.method == "insert" or self.method == "update":
            cur.execute(self.query)
            con.commit()
        # SQL文（select）の実行
        elif self.method == "select":
            for row in cur.execute(self.query):
                results.append(row)
        # カーソルと接続を閉じる
        cur.close()
        con.close()
        # タプルで帰ってる時は2以上になる。
        # 配列で帰ってる時は多次元配列に直す。
        # 検索結果が一個しかない時の対応
        if len(results) == 1:
            results = results[0]
        return results