def html_body(results):
    body = ''

    body += '<body>\n' \
            '<div class="ol1">\n' \
            '<ol>\n'
    for row in results:
        body += '<li>' + str(row[0]) + ',' + row[1] + ',' + row[2] + ',' + f'<a href="/authors/{row[3]}/books">{row[4]}</a>' + '</li>\n'
    body += '</ol>\n' \
            '</div>\n' \
            '</body>\n'
    return body
