import sqlite3

class SQL:
    def __init__(self, query):
        self.query = query
        self.method = query.split(" ")[0]

    def execute(self):
        dbname = 'database.db'
        # データベース接続とカーソル生成
        con = sqlite3.connect(dbname)
        cur = con.cursor()
        con.text_factory = str

        results = []
        if self.method == "insert":
            # SQL文（insert）の作成と実行
            cur.execute(self.query)
            con.commit()
        elif self.method == "update":
            # SQL文（insert）の作成と実行
            cur.execute(self.query)
            con.commit()
        elif self.method == "select":
            # SQL文（select）の作成
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