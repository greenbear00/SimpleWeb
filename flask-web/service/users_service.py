import bcrypt
from flask import request, jsonify, abort, render_template, redirect, url_for, session, flash
from common.log import logger_info
from common.database import session_scope
from model.users import Users
from datetime import datetime

def login():
    if request.method == "GET":
        return render_template("login_form.html")
    else:
        user_id = request.form.get('id')
        pw = request.form.get('pw').encode('utf-8')
        logger_info(f"login user_id = {user_id}")
        with session_scope() as db_session:
            result = db_session.query(Users).filter_by(id=user_id).first()

            if result:
                check_password = bcrypt.checkpw(pw, result.passwd.encode('utf-8'))
                logger_info(check_password)
                if check_password:
                    session['loggin_id'] = result.id
                    logger_info(f"session is... {session.get('loggin_id')}")
                    logger_info(f"user({user_id}) logined")
                    return redirect(url_for('hello.index'))
                else:
                    logger_info("login failed because wrong password.")
                    flash("wrong password!!")
                    return render_template('login_form.html')
            else:
                logger_info(f"login failed because user_id doesn't exist.")
                flash("wrong user_id!!")
                return render_template('login_form.html')

def signup():
    """
        curl -d '{"name":"greenbear", "id":"greenbear", "passwd": "greenbear"}' -H "Content-Type: application/json" -X POST http://localhost:5000/users/signup
        - 만약, create_user가 있다면 singup으로 redirect => 신규 id 생성으로 요청
        - 그렇지 않다면, user 생성 후, login 페이지로 redirect
        :return:
        """

    logger_info(f"[{request.remote_addr}] {request.method}")
    if request.method == "POST":
        logger_info(f"request.json: {request.json}")
        logger_info(f"request.form: {request.form}")
        if request.json:
            if not request.json or not 'id' in request.json:
                logger_info(f"400 error : {request}")
                abort(400)
                logger_info(f"request params: {request.json}")

        with session_scope() as db_session:
            if request.json:
                user_id = request.json.get('id')
                user_name = request.json.get('name')
                user_pw = request.json.get('pw')
            else:
                user_id = request.form.get('id')
                user_name = request.form.get('name')
                user_pw = request.form.get('pw')
            user = db_session.query(Users).filter_by(id=user_id).first()
            if user:
                # 만약 기존 user가 있다면, 신규 ID로 user를 생성할 수 있도록 다시 redirect
                logger_info(f"{user._asdict()} is already. try signup with new_user")
                flash("user id already exists.")
                return redirect(url_for('users.signup'))

            user_pw = (bcrypt.hashpw(user_pw.encode('UTF-8'), bcrypt.gensalt())).decode('utf-8')
            cret_dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            new_user = Users(user_id, user_name, user_pw, cret_dt)
            db_session.add(new_user)
            logger_info(f"create new_user: {new_user.id}")
            return redirect(url_for('users.login'))
    elif request.method == "GET":
        return render_template("signup_form.html")

def logout():
    session.pop('loggin_id', None)
    logger_info(f"logout session = {session}")
    return redirect(url_for('hello.index'))
