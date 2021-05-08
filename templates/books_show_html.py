def html_body(book, comments):
    body = ''

    body += '<body>\n' \
                '<a href="/books">< 一覧に戻る</a> \n' \
                '<div style="margin: 0 5vw;"> \n' \
                f'<h1>{book[0]}, {book[1]}, {book[2]}</h1>\n'  \
                '<table class="table" style="width: 20vw;"> \n' \
                '<tbody> \n' \
                '<tr> \n' \
                '<th scope="row">' + 'id' + '</th> \n' \
                '<td>' + str(book[0]) + '</td> \n' \
                '</tr> \n' \
                '<tr> \n' \
                '<th scope="row">' + 'タイトル' + '</th> \n' \
                '<td>' + book[1] + '</td> \n' \
                '</tr> \n' \
                '<tr> \n' \
                '<th scope="row">' + '分類番号' + '</th> \n' \
                '<td>' + book[3] + '</td> \n' \
                '</tr> \n' \
                '<tr> \n' \
                '<th scope="row">' + '公開日' + '</th> \n' \
                '<td>' + book[2] + '</td> \n' \
                '</tr> \n' \
                '<tr> \n' \
                '<th scope="row">' + '著者' + '</th> \n' \
                '<td>' + f'<a href="/authors/{book[4]}/books">{book[5]}</a>' + '</td> \n' \
                '</tr> \n'
    body +=     '</tbody> \n' \
                '</table> \n'
    # コメント部分
    body += '<h2>コメント</h2>\n' 
    body +=     '<div class="form1">\n' \
                f'<form action="/books/{book[0]}/users_books_comments" method="post">\n' \
                '学生番号　（整数） 　<input type="number" name="user_student_id"><br>\n' \
                '氏名　　　（文字列） <input type="text" name="user_name"><br>\n' \
                'コメント　（文字列） <input type="text" name="comment"><br>\n' \
                '<input type="submit" value="登録">\n' \
                '</form>\n' \
                '</div>\n' 
    for row in comments:
        body += '<h3>' + str(row[0]) + ',' + row[1] + '</h3>\n'
    body +=     '</div>\n' \
            '</body>\n'
    return body
