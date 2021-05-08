def html_body():
    body = ''

    # HTML（入力フォーム部分）
    body += '<body>\n' \
            '<div class="form1">\n' \
            '<form>\n' \
            '学生番号（整数） <input type="text" name="v1"><br>\n' \
            '氏名　（文字列） <input type="text" name="v2"><br>\n' \
            '<input type="submit" value="登録">\n' \
            '</form>\n' \
            '</div>\n' \
            '</body>\n'
    return body
