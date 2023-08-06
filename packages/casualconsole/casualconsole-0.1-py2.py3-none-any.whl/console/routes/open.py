from flask import request, Blueprint, make_response, jsonify, session, redirect, flash, render_template, url_for

from console.config.config import Config

b_open = Blueprint("b_open", __name__)


def read_users():
    users = []
    with open(Config.USERS_PATH, "r") as infile:
        for line in infile.readlines():
            user = line.split("=")
            users.append({"uname":user[0], "pw":user[1]})
    return users


@b_open.route("/login", methods=["GET"])
def login_view():
    return render_template("login.html")

@b_open.route("/logout", methods=["GET"])
def logout():
    try:
        session.pop('logged_in_user')
        return redirect(url_for('b_open.login_view'))
    except Exception as e:
        return redirect(url_for('b_open.login_view'))


@b_open.route("/login", methods=["POST"])
def login_post():
    users = read_users()
    uname = request.form['username']
    pw = request.form['password']
    for user in users:
        if user['uname'] == uname and user['pw'] == pw:
            session['logged_in_user'] = user['uname']
            return redirect(url_for("b_routes.console"))
    else:
        flash(u'wrong username or password', 'login_error')
        return render_template("login.html")



