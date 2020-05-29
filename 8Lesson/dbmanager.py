import sqlite3
import os


class MyDBManager:

    base_dir = "/Users/admin/Google Drive/Colab Notebooks/ITEA/Lesson8/"
    db_path = os.path.join(base_dir, "db8.db")

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
            row_query = f"SELECT  {cat_name}_tbl.id, {cat_name}_tbl.name , {cat_name}_tbl.model, " \
                f"{cat_name}_tbl.quantity, {cat_name}_tbl.on_sale, {cat_name}_tbl.in_stock  FROM  {cat_name}_tbl "
        with MyDBManager(self.db_path) as conn:
            cursor = conn.cursor()
            res = cursor.execute(row_query)
            print("Here is the full information about categories.")
            return res.fetchall()

    def get_goods_info(self, cat_name, id):
        if cat_name in self.get_category_name():
            row_query = f"SELECT id, name, model, quantity, on_sale, in_stock, description FROM {cat_name}_tbl  " \
                        "where id = ?"
        with MyDBManager(self.db_path) as conn:
            cursor = conn.cursor()
            value_query = (id,)
            res = cursor.execute(row_query, value_query)
            print("Here is the full information about goods staff.")
            return res.fetchall()

    def add_item(self,category, brand, model, quantity, description):
        print("Hello from DB!")
        print(category)
        print(self.get_category_name())
        if category in self.get_category_name():
            category = category.lower()
            with MyDBManager(self.db_path) as conn:
                cursor = conn.cursor()
                row_query = f"INSERT INTO  {category}_tbl ('name', 'model', 'quantity', 'on_sale', 'in_stock', " \
                    f"'description', 'category_id') VALUES (?, ?, ?, ?, ?, ?, ?)"
                value_query = (brand, model, quantity, 1, 1, description, 1)
                cursor.execute(row_query, value_query)
                conn.commit()
                print(f'{brand}:{model} added to DB')

        else:
            print("Wrong category name!")

    def add_category(self, new_category):
        row_query = f"CREATE TABLE '{new_category}_tbl'('id' INTEGER PRIMARY KEY AUTOINCREMENT, 'name' TEXT NOT NULL, " \
            f"'model' TEXT NOT NULL, 'quantity' INTEGER NOT NULL, 'on_sale' INTEGER NOT NULL, 'in_stock' " \
            f"INTEGER NOT NULL, 'description' TEXT, 'category_id' INTEGER, FOREIGN KEY('category_id') REFERENCES " \
            f"'categories_tbl'('id') )"
        row_query2 = f"INSERT INTO 'main'.'categories_tbl'('id', 'cat_name') VALUES(NULL, '{new_category}')"
        with MyDBManager(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(row_query)
            conn.commit()
            cursor.execute(row_query2)
            conn.commit()