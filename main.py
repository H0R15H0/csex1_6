#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
# CGIモジュールをインポート
import cgi
import cgitb

# SQL関連コマンドのImport
from sql import SQL
# HTML関連ファイルのImport
import templates
# POSTパラメーター整形用
import urllib.parse
# 正規表現用
import re

cgitb.enable()


# テーブルの作成
SQL.initialize_db()

def application(environ,start_response):
    # HTML（共通ヘッダ部分）NavBarもここで作成
    html = '<html lang="ja">\n' \
        '<head>\n' \
        '<meta charset="UTF-8">\n' \
        '<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.2.1/css/bootstrap.min.css" integrity="sha384-GJzZqFGwb1QTTN6wy59ffF1BuGJpLSa9DkKMp0DgiMDm4iYMj70gZWKYbI706tWS" crossorigin="anonymous">' \
        '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.4.1/font/bootstrap-icons.css">' \
        '<link rel="icon" href="data:,"> \n' \
        '<title>{title}</title>\n' \
        '</head>\n' \
        '<nav class="navbar navbar-primary bg-light"> \n' \
        '<a class="navbar-brand" href="/books">青空</a> \n' \
        '<form class="form-inline" action="/books" method="get"> \n' \
        '<input class="form-control mr-sm-2" type="search" placeholder="検索" name="book_title"> \n' \
        '<button class="btn btn-outline-success my-2 my-sm-0" type="submit">検索</button> \n' \
        '<a class="navbar-brand" href="/mypage" style="margin: 5px;"><i class="bi bi-person-circle"></i></a> \n' \
        '</form> \n' \
        '</nav> \n' 

    if environ['PATH_INFO'] == '/':
        # タイトルの設定
        html = html.format(title='ようこそ！')
        # HTMLを読み込む
        html += templates.index_html.html_body()
        html += '</html>\n'
        html = html.encode('utf-8')

        # レスポンス
        start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8'),
            ('Content-Length', str(len(html))) ])
        return [html]
    
    elif environ['PATH_INFO'] == '/mypage':
        # タイトルの設定
        html = html.format(title='登録情報の変更')
        # HTMLを読み込む
        html += templates.mypage_html.html_body()
        html += '</html>\n'
        html = html.encode('utf-8')

        # レスポンス
        start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8'),
            ('Content-Length', str(len(html))) ])
        return [html]
        
    elif environ['PATH_INFO'] == '/books':
        # タイトルの設定
        html = html.format(title='本一覧')
        # クエリパラメーター(book_title)の取得
        query_params = urllib.parse.parse_qs(environ["QUERY_STRING"])
        search_book_title = ''
        if len(query_params):
            search_book_title = query_params['book_title'][0]

        # SQL文の実行とその結果のHTML形式への変換
        query = 'select books.id, books.title, books.published_at, authors.id, authors.name from books JOIN authors ON books.author_id=authors.id '
        # クエリパラメーター(book_title)が存在している時、部分一致検索。存在していない時、全体検索。
        query += 'where books.title LIKE "%{}%";'.format(search_book_title) if len(search_book_title) else ';'
        query = SQL(query)
        results = query.execute()

        # HTMLを読み込む
        html += templates.books_index_html.html_body(results, search_book_title)
        html += '</html>\n'
        html = html.encode('utf-8')

        # レスポンス
        start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8'),
            ('Content-Length', str(len(html))) ])
        return [html]

    elif environ['REQUEST_METHOD'] == 'POST' and environ['PATH_INFO'] == '/users':
        # POSTリクエストボディの取得
        body = environ['wsgi.input'].read(int(environ.get('CONTENT_LENGTH', 0))).decode('utf-8')
        form = urllib.parse.parse_qs(body)

        # すでにUserが存在していれば取得
        query = SQL('select * from users where id = {};'.format(form['student_id'][0]))
        user = query.execute()

        # ↑で存在していたらUPDATE処理、存在していなかったらCREATE処理
        if user:
            query = SQL('update users set name="{}" where id={}'.format(form['name'][0], user[0]))
            query.execute()
        else:
            query = SQL('insert into users(id, name) values ({},"{}")'.format(int(form['student_id'][0]), form['name'][0]))
            query.execute()

        # /books 本の一覧ページにリダイレクトさせる。
        start_response('301 Moved', [('Location','/books')])
        return ''

    # /books/{id}/users_books_comments のルーティング
    elif environ['REQUEST_METHOD'] == 'POST' and re.compile('/books/(?P<book_id>\d+)/users_books_comments').fullmatch(environ['PATH_INFO']):
        # 正規表現で{id}の取得
        book_id = re.compile('/books/(?P<book_id>\d+)/users_books_comments').match(environ['PATH_INFO']).groupdict()["book_id"]
        # POSTリクエストボディの取得
        body = environ['wsgi.input'].read(int(environ.get('CONTENT_LENGTH', 0))).decode('utf-8')
        form = urllib.parse.parse_qs(body)
        # コメントの作成
        query = SQL('insert into users_books_comments(user_id, book_id, message) values ({},{},"{}")'.format(int(form['user_student_id'][0]), book_id, form['message'][0]))
        query.execute()

        # /books/{id} 本の詳細ページにリダイレクト
        start_response('301 Moved', [('Location','/books/{}'.format(book_id))])
        return ''

    # /books/{id} のルーティング
    elif re.compile('/books/(?P<book_id>\d+)').fullmatch(environ['PATH_INFO']):
        # タイトルの設定
        html = html.format(title='本の詳細')
        # 正規表現で{id}の取得
        book_id = re.compile('/books/(?P<book_id>\d+)').match(environ['PATH_INFO']).groupdict()["book_id"]

        # SQL文の実行とその結果のHTML形式への変換
        query = SQL('select books.id, books.title, books.published_at, books.class_name, authors.id, authors.name from books JOIN authors ON books.author_id=authors.id where books.id={};'.format(book_id))
        book = query.execute()
        query = SQL('select users.name, users_books_comments.message from users_books_comments JOIN users ON users_books_comments.user_id=users.id where users_books_comments.book_id={};'.format(book_id))
        comments = query.execute()
        # commentsが一つの時tupleがかえって来るのでarrayで包む
        if type(comments) is tuple:
            comments = [comments] 

        # HTMLを読み込む
        html += templates.books_show_html.html_body(book, comments)
        html += '</html>\n'
        html = html.encode('utf-8')

        # レスポンス
        start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8'),
            ('Content-Length', str(len(html))) ])
        return [html]

    # どのルーティングにもマッチしなかった時、'404 Not Found'を返す
    else:
        html = html.format(title='Not found')
        html += '<h1>404 Not Found</h1>'
        html = html.encode('utf-8')
        start_response('404 Not Found', [('Content-type', 'text/html; charset=utf-8'), 
            ('Content-Length', str(len(html))) ])
        return [html]


# リファレンスWEBサーバを起動
#  ファイルを直接実行する（python3 main.py）と，
#  リファレンスWEBサーバが起動し，http://localhost:8080 にアクセスすると
#  このサンプルの動作が確認できる．
#  コマンドライン引数にポート番号を指定（python3 main.py ポート番号）した場合は，
#  http://localhost:ポート番号 にアクセスする．
from wsgiref import simple_server
if __name__ == '__main__':
    port = 8080
    if len(sys.argv) == 2:
        port = int(sys.argv[1])

    server = simple_server.make_server('', port, application)
    server.serve_forever()