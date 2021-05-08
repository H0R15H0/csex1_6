def html_body():
    body = ''

    # HTML（入力フォーム部分）
    body += '<body>\n' \
            '<div class="form1">\n' \
                f'<form action="/users" method="post">\n' \
                '学生番号　（整数） 　<input type="number" name="user_student_id"><br>\n' \
                '氏名　　　（文字列） <input type="text" name="user_name"><br>\n' \
                '<input type="submit" value="登録">\n' \
                '</form>\n' \
                '</div>\n' \
            '</body>\n'
    return body
