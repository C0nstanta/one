# Категория - отдельная таблица с категориями, продукты из других таблиц будут ссылаться на айди с категорией
#Скрипт работает следующим образом:  смотреть категории, количество товара и информацию по товару мы можем свободно.
#Для того, что бы попасть в админку ,где мы можем изменять наш товар - мы должны войти на страницу администратора (/admin)
# и там ввести логин - пароль администратора. (admin:123) если все верно - мы попадаем дальше на страницу с вводом
# товара и категорий.
#Проверка на права доступа отсуществляется следующим образом...
# Мы при вводе логин-пароль проверяемся в бд на право доступа на страницу, если такое право запиcано в бд для этого
# пользователя - нам разрешается вход и об этом идет запись к нам в кукисы. Дальшейшее попадание на страницу - через кукисы.
# Нет записи - доступ запрещен. Можно реализовать время валидности кукисов и смену ключа раз в сколько то времени.
# Ну это уже частности, реализован сам принцип.


from flask import Flask, request, url_for, render_template, redirect, make_response
from dbmanager import DBManager
from authorization import Authorization


app = Flask(__name__)
dbmanager = DBManager()


@app.route('/<cat_name>')
def category(cat_name):
    if cat_name in dbmanager.get_category_name():
#Отсылаем запрос с категорией, которую выбрали, в БД. И в ответ получаем список товара, доступен - не доступен.
        print(cat_name)
        goods_list = dbmanager.get_category_info(cat_name)
        print(goods_list)
        return render_template('second_page.html', category = cat_name, goods=goods_list)

@app.route('/<cat_name>/<id>')
def get_info(cat_name, id):
    goods_info = dbmanager.get_goods_info(id)
    print(goods_info)
    return render_template('third_page.html', about_good=goods_info)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


@app.route('/admin/', methods=["GET", "POST"])
def admin_authorization():
    cookies = request.cookies
    print(cookies)

    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        admin = Authorization(username, password)

        if admin.check_log_pass_registration():
            category_list = dbmanager.get_category_name()
            print(category_list)
            resp = make_response(redirect('/admin/db_access/'))
            resp.set_cookie('secret_key', dbmanager.secret_key)
            return resp
        else:
            return render_template('admin.html', error = "Wrong data. Try again!")
    else:
        return render_template('admin.html')


@app.route('/admin/db_access/', methods=["GET", "POST"])
def db_page():
    category_list = dbmanager.get_category_name()
    if request.cookies['secret_key'] == dbmanager.secret_key:
        print("Secret_key good")
        if request.method == "POST":
            if request.form['action'] == 'Add item':
                brand = request.form['brand']
                model = request.form['model']
                quantity = request.form['quantity']
                description = request.form['description']
                category = (request.form['category'])
                dbmanager.add_item(category, brand, model, quantity, description)
            elif request.form['action'] == 'Add category':
                new_category = request.form['new_category']
                dbmanager.add_category(new_category)
                print(f'new_category:{new_category}')
            else:
                print("Please fill all data")

        return render_template("admin_manager.html", category_list= category_list )
    else:
        return render_template("admin.html", admin_access = "Enter your login:password again")


@app.route('/')
def start():
    category_list = dbmanager.get_category_name()
    print(category_list)
    return render_template('index.html', category_list=category_list)




if __name__ == "__main__":
    app.run(debug=True, port=8000)