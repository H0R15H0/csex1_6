def html_body(results):
    body = ''

    body += '<body>\n' \
            '<table class="table"> \n' \
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
                '<td>' + row[1] + '</td> \n' \
                '<td>' + row[2] + '</td> \n' \
                '<td>' + f'<a href="/authors/{row[3]}/books">{row[4]}</a>' + '</td> \n' \
                '</tr> \n'
    body +=     '</tbody> \n' \
                '</table> \n' \
            '</body>\n'
    return body
