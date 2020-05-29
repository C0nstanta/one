import sqlite3
import os


class MyDBManager:
    base_dir = '/Users/admin/PycharmProjects/8Lesson/8Lesson-rebuild/'#os.getcwd()
    db_path = os.path.join(base_dir, "8lessondb.db")

    def __init__(self, db):
        self._db = db

    def __enter__(self):
        self.conn = sqlite3.connect(self._db)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()
        if exc_val:
            raise Exception("MyDBManager error!")


class DBManager(object):

    db_path = MyDBManager.db_path
    secret_key = 'somesecretkeyhereitcanbeasahash'

    def get_category_name(self):
        row_query = "SELECT cat_name FROM categories_tbl"
        category_list = []
        with MyDBManager(self.db_path) as conn:
            cursor = conn.cursor()
            res = cursor.execute(row_query)
            for record in res:
                category_list.append((str(record[0]).upper()))
            return category_list

    def get_category_info(self, cat_name):
        if cat_name in self.get_category_name():
            cat_name = cat_name.lower()
            row_query= f"SELECT id, name, model, quantity, on_sale, in_stock from goods_tbl where goods_tbl.category_id " \
                f"=(SELECT id FROM categories_tbl WHERE categories_tbl.cat_name='{cat_name}')"
        with MyDBManager(self.db_path) as conn:
            cursor = conn.cursor()
            res = cursor.execute(row_query)
            print("Here is the full information about categories.")
            return res.fetchall()

    def get_goods_info(self, id):
        row_query = f"SELECT id, name, model, quantity, on_sale, in_stock, description FROM goods_tbl  " \
                        "where id = ?"
        with MyDBManager(self.db_path) as conn:
            cursor = conn.cursor()
            value_query = (id,)
            res = cursor.execute(row_query, value_query)
            print("Here is the full information about goods staff.")
            return res.fetchall()

    def add_item(self,category, brand, model, quantity, description):
        print(category)
        print(self.get_category_name())
        if category in self.get_category_name():
            category = category.lower()
            with MyDBManager(self.db_path) as conn:
                cursor = conn.cursor()
                row_query1 = "SELECT id from categories_tbl WHERE categories_tbl.cat_name=?"
                value_query1 = (category,)
                res1 = cursor.execute(row_query1, value_query1)
                for record in res1:
                    cat_id = record[0]
                row_query = f"INSERT INTO  goods_tbl ('name', 'model', 'quantity', 'on_sale', 'in_stock', " \
                    f"'description', 'category_id') VALUES (?, ?, ?, ?, ?, ?, ?)"
                value_query = (brand, model, quantity, 1, 1, description, cat_id)
                cursor.execute(row_query, value_query)
                conn.commit()
                print(f'{brand}:{model} added to DB')
        else:
            print("Wrong category name!")

    def add_category(self, new_category):
        row_query = f"INSERT INTO 'categories_tbl'('id','cat_name') VALUES (NULL, '{new_category}')"
        with MyDBManager(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(row_query)
            conn.commit()
