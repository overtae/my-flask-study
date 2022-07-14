from flask import Flask, url_for, request, redirect

app = Flask(__name__)

users = [
    {'id': 1, 'name': '홍길동', 'age': 20, 'msg': '플라스크를 공부 중인 홍길동입니다.'},
    {'id': 2, 'name': '고영희', 'age': 28, 'msg': '고양이 아닙니다. 고영희입니다.'},
    {'id': 3, 'name': '이철수', 'age': 22, 'msg': '"철수야 철수하자" 드립치면 법정에서 뵙겠습니다.'},
]

next_id = len(users) + 1  # user의 마지막 id 값 저장


def template(contents, content, id=None):
    contextUI = ''
    if id != None:
        contextUI = f'''
            <li><a href="/update/{id}/">update</a></li>
            <li><form action="/delete/{id}/" method="POST"><input type="submit" value="delete"></form></li>
        '''
    return f'''<!doctype html>
    <html>
        <body>
            <h1>Menu</h1>
            <ul>
                <li><a href="{url_for("index")}">Main</a></li>
                <li><a href="{url_for("about_page")}">About this page</a></li>
                <li><a href="{url_for("create")}">Create user</a></li>
            </ul>
            <hr>
            <h1>Users</h2>
            <ol>
                {contents}
            </ol>
            <hr>
            {content}
            <ul>
                {contextUI}
            </ul>
        </body>
    </html>
    '''


def get_users():
    li_tags = ''
    for user in users:
        li_tags = li_tags + \
            f'<li><a href="/read/{user["id"]}/">{user["name"]}</a></li>'
    return li_tags


@app.route('/')
def index():
    return 'This is Home page.' \
           f'<p><a href="{url_for("index")}">Main</a></p>' \
           f'<p><a href="{url_for("about_page")}">About this page</a></p>' \
           f'<p><a href="{url_for("create")}">Create user</a></p>'


@app.route('/about_page')
def about_page():
    return template(get_users(), '<h1>This is ...</h1> User Information Page')


@app.route('/read/<int:id>/')
def read(id):
    name = ''
    msg = ''
    for user in users:
        if id == user['id']:
            name = user['name']
            age = user['age']
            msg = user['msg']
            break
    return template(get_users(), f'<h2 style="display:inline;">{name}</h2> ({age} 세)</p> {msg}', id)


@app.route('/create/', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        content = '''
            <form action="/create/" method="POST">
                <p><input type="text" name="name" placeholder="name"></p>
                <p><input type="number" name="age" placeholder="age"></p>
                <p><textarea name="msg" placeholder="msg"></textarea></p>
                <p><input type="submit" value="create"></p>
            </form>
        '''
        return template(get_users(), content)
    elif request.method == 'POST':
        global next_id
        name = request.form['name']
        age = request.form['age']
        msg = request.form['msg']
        newuser = {'id': next_id, 'name': name, 'age': age, 'msg': msg}
        users.append(newuser)
        url = '/read/' + str(next_id) + '/'
        next_id = next_id + 1
        return redirect(url)


@app.route('/update/<int:id>/', methods=['GET', 'POST'])
def update(id):
    if request.method == 'GET':
        name = ''
        msg = ''
        for user in users:
            if id == user['id']:
                name = user['name']
                msg = user['msg']
                break
        content = f'''
            <form action="/update/{id}/" method="POST">
                <p><input type="text" name="name" placeholder="name" value="{name}"></p>
                <p><textarea name="msg" placeholder="msg">{msg}</textarea></p>
                <p><input type="submit" value="update"></p>
            </form>
        '''
        return template(get_users(), content)
    elif request.method == 'POST':
        global next_id
        name = request.form['name']
        msg = request.form['msg']
        for user in users:
            if id == user['id']:
                user['name'] = name
                user['msg'] = msg
                break
        url = '/read/'+str(id)+'/'
        return redirect(url)


@app.route('/delete/<int:id>/', methods=['POST'])
def delete(id):
    for user in users:
        if id == user['id']:
            users.remove(user)
            break
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
