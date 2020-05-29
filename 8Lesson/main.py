
categories - > phones tbl (usual inquiry)
----------------
SELECT   phones_tbl.name, phones_tbl.model, phones_tbl.quantity, phones_tbl.on_sale, phones_tbl.in_stock FROM categories LEFT JOIN phones_tbl ON categories.phones = phones_tbl.id


categories - > laptop tbl (usual inquiry)
----------------
SELECT  laptop_tbl.name , laptop_tbl.model, laptop_tbl.quantity, laptop_tbl.on_sale, laptop_tbl.in_stock  FROM categories LEFT JOIN laptop_tbl ON categories.laptops = laptop_tbl.id

categories - > tablet tbl (usual inquiry)
----------------
SELECT  tablet_tbl.name , tablet_tbl.model, tablet_tbl.quantity, tablet_tbl.on_sale, tablet_tbl.in_stock  FROM categories LEFT JOIN tablet_tbl ON categories.tablets = tablet_tbl.id

Задача
1) Создать базу данных товаров, у товара есть: Категория (связанная
таблица), название, есть ли товар в продаже или на складе, цена, кол-во
единиц.Создать html страницу. На первой странице выводить ссылки на все
категории, при переходе на категорию получать список всех товаров в
наличии ссылками, при клике на товар выводить его цену, полное описание и
кол-во единиц в наличии.
2) Создать страницу для администратора, через которую он может добавлять
новые товары и категории.


