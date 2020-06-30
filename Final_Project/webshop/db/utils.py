# Инициализация текстов  в БД
from models import Text, Status, Users, Admin


def init_texts():
    Text.objects.create(title=Text.TITLES['greetings'], body='Рады приветствовать вас в нашем магазине')
    Text.objects.create(title=Text.TITLES['cart'], body='Вы перешли в корзину')


def init_test_user():
    status = Status.objects.create(user_status=3, user_chat_id='11111test11111')

    Users.objects.create(
        status=status,
        fname="FirstBuyerName",
        phonenumber="testphonenumber",
        email="testemail@email.com",
        address="Some address here 9a",
        comments="This is a test user bot",
        total_summ=445.33
    )


def init_admin():
    Admin.objects.create(username="admin", password="123")


if __name__ == "__main__":
    init_texts()
    init_test_user()
#    init_admin()

