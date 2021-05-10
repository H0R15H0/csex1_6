def html_body(results, search_book_title):
    body = ''

    body += '<body>\n' \
            '<div style="margin: 10px 10px;"> \n' 
    if search_book_title:
        body += f'<h1>"{search_book_title}"の検索結果です！</h1>\n' 
    else:
        body += f'<h1>本の一覧ページです！</h1>\n' 
    body += '<table class="table"> \n' \
                '<thead> \n' \
                '<tr> \n' \
                '<th scope="col">id</th> \n' \
                '<th scope="col">タイトル</th> \n' \
                '<th scope="col">公開日</th> \n' \
                '<th scope="col">著者名</th> \n' \
                '</tr> \n' \
                '</thead> \n' \
                '<tbody> \n' 
    for row in results:
        body += '<tr> \n' \
                '<th scope="row">' + str(row[0]) + '</th> \n' \
                '<td style="width: 30vw;">' + f'<a href="/books/{row[0]}">{row[1]}</a>' + '</td> \n' \
                '<td>' + row[2] + '</td> \n' \
                '<td>' + row[4] + '</td> \n' \
                '</tr> \n'
    body +=     '</tbody> \n' \
                '</table> \n' \
                '</div> \n' \
            '</body>\n'
    return body
