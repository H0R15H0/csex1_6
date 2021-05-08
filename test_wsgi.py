#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
# CGIモジュールをインポート
import cgi
import cgitb

import re
from sql import SQL
import templates
# POSTパラメーター整形用
import urllib

cgitb.enable()

# sqlite3（SQLサーバ）モジュールをインポート
import sqlite3

# データベースファイルのパスを設定
dbname = 'database.db'
#dbname = ':memory:'

# テーブルの作成
con = sqlite3.connect(dbname)
cur = con.cursor()
create_table = 'create table if not exists users (id int, name varchar(64))'
cur.execute(create_table)
con.commit()
cur.close()
con.close()

def application(environ,start_response):
    # HTML（共通ヘッダ部分）
    html = '<html lang="ja">\n' \
        '<head>\n' \
        '<meta charset="UTF-8">\n' \
        '<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.2.1/css/bootstrap.min.css" integrity="sha384-GJzZqFGwb1QTTN6wy59ffF1BuGJpLSa9DkKMp0DgiMDm4iYMj70gZWKYbI706tWS" crossorigin="anonymous">' \
        '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.4.1/font/bootstrap-icons.css">' \
        '<title>{title}</title>\n' \
        '</head>\n'

    if environ['PATH_INFO'] == '/':
        html = html.format(title='ようこそ！')
        # フォームデータを取得
        form = cgi.FieldStorage(environ=environ,keep_blank_values=True)
        if ('v1' not in form) or ('v2' not in form):
            # 入力フォームの内容が空の場合（初めてページを開いた場合も含む）

            # HTML（入力フォーム部分）
            html += templates.index_html.html_body()
        else:
            # 入力フォームの内容が空でない場合

            # フォームデータから各フィールド値を取得
            v1 = form.getvalue("v1", "0")
            v2 = form.getvalue("v2", "0")

            # データベース接続とカーソル生成
            con = sqlite3.connect(dbname)
            cur = con.cursor()
            con.text_factory = str

            # SQL文（insert）の作成と実行
            sql = 'insert into users (id, name) values (?,?)'
            cur.execute(sql, (int(v1),v2))
            con.commit()

            # SQL文（select）の作成
            sql = 'select * from users'

            # SQL文の実行とその結果のHTML形式への変換
            html += '<body>\n' \
                    '<div class="ol1">\n' \
                    '<ol>\n'
            for row in cur.execute(sql):
                html += '<li>' + str(row[0]) + ',' + row[1] + '</li>\n'
            html += '</ol>\n' \
                    '</div>\n' \
                    '<a href="/">登録ページに戻る</a>\n' \
                    '</body>\n'

            # カーソルと接続を閉じる
            cur.close()
            con.close()


        html += '</html>\n'
        html = html.encode('utf-8')

        # レスポンス
        start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8'),
            ('Content-Length', str(len(html))) ])
        return [html]
        
    elif environ['PATH_INFO'] == '/books':
        html = html.format(title='本一覧')

        # SQL文の実行とその結果のHTML形式への変換
        query = SQL('select books.id, books.title, books.published_at, authors.id, authors.name from books JOIN authors ON books.author_id=authors.id;')
        results = query.execute()

        html += templates.books_index_html.html_body(results)

        html += '</html>\n'
        html = html.encode('utf-8')

        # レスポンス
        start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8'),
            ('Content-Length', str(len(html))) ])
        return [html]

    elif environ['REQUEST_METHOD'] == 'POST' and environ['PATH_INFO'] == '/users':
        body = environ['wsgi.input'].read(int(environ.get('CONTENT_LENGTH', 0))).decode('utf-8')
        form = urllib.parse.parse_qs(body)

        query = SQL('insert into users(id, name) values ({},"{}")'.format(int(form['student_id'][0]), form['name'][0]))
        query.execute()

        start_response('301 Moved', [('Location','/books')])
        return ''

    elif environ['REQUEST_METHOD'] == 'POST' and re.compile('/books/(?P<book_id>\d+)/users_books_comments').fullmatch(environ['PATH_INFO']).groupdict()["book_id"]:
        book_id = re.compile('/books/(?P<book_id>\d+)/users_books_comments').match(environ['PATH_INFO']).groupdict()["book_id"]
        body = environ['wsgi.input'].read(int(environ.get('CONTENT_LENGTH', 0))).decode('utf-8')
        form = urllib.parse.parse_qs(body)
        print(form)
        query = SQL('insert into users_books_comments(user_id, book_id, message) values ({},{},"{}")'.format(int(form['user_student_id'][0]), book_id, form['message'][0]))
        query.execute()

        start_response('301 Moved', [('Location','/books/{}'.format(book_id))])
        return ''

    elif re.compile('/books/(?P<book_id>\d+)').fullmatch(environ['PATH_INFO']).groupdict()["book_id"]:
        html = html.format(title='本の詳細')
        book_id = re.compile('/books/(?P<book_id>\d+)').match(environ['PATH_INFO']).groupdict()["book_id"]

        # SQL文の実行とその結果のHTML形式への変換
        query = SQL(f'select books.id, books.title, books.published_at, books.class_name, authors.id, authors.name from books JOIN authors ON books.author_id=authors.id where books.id={book_id};')
        book = query.execute()
        query = SQL(f'select users.name, users_books_comments.message from users_books_comments JOIN users ON users_books_comments.user_id=users.id where users_books_comments.book_id={book_id};')
        comments = query.execute()
        # commentsが一つの時tupleがかえって来るのでarrayで包む
        if type(comments) is tuple:
            comments = [comments] 


        html += templates.books_show_html.html_body(book, comments)
        html += '</html>\n'
        html = html.encode('utf-8')

        # レスポンス
        start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8'),
            ('Content-Length', str(len(html))) ])
        return [html]

    else:
        html = html.format(title='Not found')
        html += '<h1>404 Not Found</h1>'
        html = html.encode('utf-8')
        start_response('404 Not Found', [('Content-type', 'text/html; charset=utf-8'), 
            ('Content-Length', str(len(html))) ])
        return [html]


# リファレンスWEBサーバを起動
#  ファイルを直接実行する（python3 test_wsgi.py）と，
#  リファレンスWEBサーバが起動し，http://localhost:8080 にアクセスすると
#  このサンプルの動作が確認できる．
#  コマンドライン引数にポート番号を指定（python3 test_wsgi.py ポート番号）した場合は，
#  http://localhost:ポート番号 にアクセスする．
from wsgiref import simple_server
if __name__ == '__main__':
    port = 8080
    if len(sys.argv) == 2:
        port = int(sys.argv[1])

    server = simple_server.make_server('', port, application)
    server.serve_forever()