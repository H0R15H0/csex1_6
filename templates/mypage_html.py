def html_body():
    body = ''

    # HTML（入力フォーム部分）
    body += '<div style="margin: 10px 0 0 10px;"> \n' \
            '<form action="/users" method="post"> \n' \
            '<div class="form-group"> \n' \
            '<label for="student_id">学生番号</label> \n' \
            '<input type="text" class="form-control" id="student_id" name="student_id" placeholder="登録している学生番号を入力してください" style="width:40%;"> \n' \
            '</div> \n' \
            '<div class="form-group"> \n' \
            '<label for="name">名前</label> \n' \
            '<input type="text" class="form-control" id="name" name="name" placeholder="変更後の名前を入れてください" style="width:40%;"> \n' \
            '</div> \n' \
            '<button type="submit" class="btn btn-success">登録</button> \n' \
            '</form> \n' \
            '</div> \n'
    return body
