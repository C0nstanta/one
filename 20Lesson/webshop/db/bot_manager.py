from .models import Users, Status, TempData, Products, MyCart
from marshmallow import ValidationError


class DBManager:

    @staticmethod
    def check_status(chat_id: [int, str]) -> int:
        for status in Status.objects:
            if str(chat_id) == str(status.user_chat_id):
                stat_id = status.user_status
                return stat_id
        Status.objects.create(user_status=1, user_chat_id=str(chat_id))
        return 1

    @staticmethod
    def check_data(chat_id: [int, str], **kwargs):
        for status in Status.objects(user_chat_id=str(chat_id)):
            if status.user_status >= 2:
                temp_user = TempData.objects.get(status=status.id)
                if kwargs.get('temp_fname'):
                    return temp_user.temp_fname
                elif kwargs.get('temp_phonenumber'):
                    return temp_user.temp_phonenumber
                elif kwargs.get('temp_email'):
                    return temp_user.temp_email
                elif kwargs.get('temp_address'):
                    return temp_user.temp_address
            if status.user_status == 1:
                return False
            else:
                return False

    @staticmethod
    def create_data(chat_id: int, **kwargs):
        status = Status.objects.get(user_chat_id=str(chat_id))
        if status.user_status == 1:

            if kwargs.get('temp_new_name'):
                TempData.objects.create(status=status, temp_fname=kwargs.get('temp_new_name'), temp_phonenumber='',
                                        temp_email='', temp_address='', temp_comments='')
                Status.objects(user_chat_id=str(chat_id)).update(user_status=2)
                return True
            else:
                return False
        if status.user_status >= 2:
            if kwargs.get('temp_new_name'):
                TempData.objects(status=status.id).update(temp_fname=kwargs.get('temp_new_name'))
                return True
            elif kwargs.get('temp_phonenumber'):
                TempData.objects(status=status.id).update(temp_phonenumber=kwargs.get('temp_phonenumber'))
                return True
            elif kwargs.get('temp_email'):
                TempData.objects(status=status.id).update(temp_email=kwargs.get('temp_email'))
                return True
            elif kwargs.get('temp_address'):
                TempData.objects(status=status.id).update(temp_address=kwargs.get('temp_address'))
                return True
            else:
                return False

    @staticmethod
    def check_phone_number(chat_id: [int, str]):
        status = Status.objects.get(user_chat_id=str(chat_id))
        temp_user = TempData.objects.get(status=status.id)
        try:
            if temp_user.temp_phonenumber:
                return True
        except ValidationError as e:
            print(e)
            return False

    def create_user(self, chat_id: [int, str]):
        for status in Status.objects:
            if str(chat_id) == str(status.user_chat_id):
                stat_id = status.id
                temp_user = TempData.objects.get(status=stat_id)
                if status.user_status == 3:
                    user = Users.objects.get(status=stat_id)
                    order_summ = self.total_cart(chat_id)
                    total_summ = user.total_summ + order_summ
                    user.update(fname=temp_user.temp_fname, phonenumber=temp_user.temp_phonenumber,
                                email=temp_user.temp_email, address=temp_user.temp_address, total_summ=total_summ)
                    status.update(user_status=3)
                    self.del_cart(chat_id)
                if status.user_status <= 2:
                    Users.objects.create(status=stat_id, fname=temp_user.temp_fname,
                                         phonenumber=temp_user.temp_phonenumber, email=temp_user.temp_email,
                                         address=temp_user.temp_address, total_summ=self.total_cart(chat_id))
                    status.update(user_status=3)
                    self.del_cart(chat_id)

    @staticmethod
    def get_user_data(chat_id: [int, str]):
        status = Status.objects.get(user_chat_id=str(chat_id))
        temp_user = TempData.objects.get(status=status.id)
        return temp_user.temp_fname, temp_user.temp_phonenumber, temp_user.temp_email, temp_user.temp_address

    @staticmethod
    def add_my_cart(product_id, chat_id: [int, str]):
        product = Products.objects.get(id=product_id)
        status = Status.objects.get(user_chat_id=str(chat_id))
        temp_user = TempData.objects.get(status=status.id)

        if not MyCart.objects(user=temp_user.id, product=product.id):
            MyCart.objects.create(user=temp_user, product=product, quantity=1)
            return 1, product.title
        else:
            cart = MyCart.objects(user=temp_user.id, product=product.id)[0]
            MyCart.objects(user=temp_user.id, product=product.id).update(quantity=(cart.quantity + 1))
            return (cart.quantity + 1), product.title

    @staticmethod
    def min_my_cart(product_id, chat_id: [int, str]):
        product = Products.objects.get(id=product_id)
        status = Status.objects.get(user_chat_id=str(chat_id))
        temp_user = TempData.objects.get(status=status.id)

        if not MyCart.objects(user=temp_user.id, product=product.id):
            return 0, product.title
        mycart = MyCart.objects(user=temp_user.id, product=product.id)[0]
        if mycart.quantity <= 0:
            return 0, product.title
        else:
            cart = MyCart.objects(user=temp_user.id, product=product.id)[0]
            MyCart.objects(user=temp_user.id, product=product.id).update(quantity=(cart.quantity - 1))
            return (cart.quantity - 1), product.title

    @staticmethod
    def del_cart_product(product_id, chat_id: [int, str]):
        product = Products.objects.get(id=product_id)
        status = Status.objects.get(user_chat_id=str(chat_id))
        temp_user = TempData.objects.get(status=status.id)

        if not MyCart.objects(user=temp_user.id, product=product.id):
            return f"{product.title} нет в корзине"

        else:
            MyCart.objects(user=temp_user.id, product=product.id).delete()
            return f"{product.title} удален из корзины"

    def del_cart(self, chat_id: [int, str]):
        status = Status.objects.get(user_chat_id=str(chat_id))
        temp_user = TempData.objects.get(status=status.id)

        if not MyCart.objects(user=temp_user.id):
            return "Ваша корзина пустая."
        else:
            MyCart.objects(user=temp_user.id).delete()
            return "Корзина очищена"

    def total_cart(self, chat_id: [int, str]):
        status = Status.objects.get(user_chat_id=str(chat_id))
        temp_user = TempData.objects.get(status=status.id)
        total = 0
        for cart in MyCart.objects(user=temp_user.id):
            product = Products.objects.get(id=cart.product.id)
            disc_price = product.price - (product.price / 100 * product.discount)
            total += disc_price * cart.quantity
        return total

    @staticmethod
    def check_my_cart(chat_id: [int, str]):
        try:
            status = Status.objects.get(user_chat_id=str(chat_id))
            temp_user = TempData.objects.get(status=status.id)
            return temp_user.id
        except ValidationError as e:
            print(e)
        return False
