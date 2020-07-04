from .authorization import Authorization
from flask import (
    Blueprint,
    request,
    render_template,
    redirect,
    make_response
)


auth_bp = Blueprint('auth_bp', __name__)


@auth_bp.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


@auth_bp.route('/tg/admin/', methods=["GET", "POST"])
def admin_authorization():
    cookies = request.cookies
    print(cookies)

    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        admin = Authorization(username, password)

        if admin.check_log_pass_registration():
            print("yes. you are  admin!")
            resp = make_response(redirect('/tg/admin/'))
            resp.set_cookie('secret_key', admin.secret_key)
            return render_template('admin.html', error="Yes. You are admin.")
        else:
            return render_template('admin.html', error="Wrong data. Try again!")
    else:
        return render_template('admin.html')
