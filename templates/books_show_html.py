def html_body(book, comments):
    body = ''

    body += '<body>\n' \
                '<a href="/books">< 一覧に戻る</a> \n' \
                '<div style="margin: 10px 10px;"> \n' \
                '<h1>' + book[1] + '</h1>\n'  \
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
                '<td>' + book[5] + '</td> \n' \
                '</tr> \n'
    body +=     '</tbody> \n' \
                '</table> \n'
    # コメント部分
    body += '<h2>コメント一覧</h2>\n' 
    body +=     '<hr size="10">\n' \
                '<form action="/books/'+str(book[0])+'/users_books_comments" method="post">\n' \
                '<div class="form-group"> \n' \
                    '<label for="user_student_id">学生番号</label> \n' \
                    '<input type="text" class="form-control" id="user_student_id" name="user_student_id" aria-describedby="emailHelp" placeholder="学生番号を入力してください" style="width:40%;"> \n' \
                '</div> \n' \
                '<div class="form-group"> \n' \
                    '<label for="user_name">名前</label> \n' \
                    '<input type="text" class="form-control" id="user_name" name="user_name" placeholder="名前を入力してください" style="width:40%;"> \n' \
                '</div> \n' \
                '<div class="form-group"> \n' \
                    '<label for="message">コメント</label> \n' \
                    '<textarea type="text" class="form-control" id="message" name="message" placeholder="すごいおもしろい！" style="width:90%;"></textarea> \n' \
                '</div> \n' \
                    '<button type="submit" class="btn btn-success">コメントする</button> \n' \
                '</form> \n' \
                '<hr size="10">\n' 
    for row in comments:
        body += '<h3>' + '<i class="bi bi-person-circle"></i>&nbsp;' + str(row[0]) + '</h3>\n' \
                '<p style="margin: 10px;">' + row[1] + '</p>' \
                '<hr> \n'
    body +=     '</div>\n' \
            '</body>\n'
    return body
