from flask import (
    Flask,
    request,
    render_template,
    redirect,
    make_response,
    abort
    )
from flask_restful import Api
from telebot.types import Update

from .my_resources import (
    CategoryResource,
    ProductResource,
    TempDataResource,
    UsersResource,
    AdminResource,
    StatusResource
    )
from webshop.bot.main import bot
from webshop.bot import config
from .authorization import Authorization


app = Flask(__name__)
api = Api(app)

api.add_resource(CategoryResource, '/tg/category/all', '/tg/category/all/<string:id_key>')
api.add_resource(ProductResource, '/tg/products/all', '/tg/products/all/<string:id_key>')
api.add_resource(TempDataResource, '/tg/tempdata/all', '/tg/tempdata/all/<string:id_key>')
api.add_resource(UsersResource, '/tg/users/all', '/tg/users/all/<string:id_key>')
api.add_resource(AdminResource, '/tg/admin/all', '/tg/admin/all/<string:id_key>')
api.add_resource(StatusResource, '/tg/status/all', '/tg/status/all/<string:id_key>')


@app.route(config.WEBHOOK_PATH, methods=['GET', 'POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        abort(403)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


@app.route('/tg/admin/', methods=["GET", "POST"])
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
