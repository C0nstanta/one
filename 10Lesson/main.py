# TODO:
#  1) Написать REST для блога (использовать валидацию).
# - Реализовать модель Пост (название, содержание, дата публикации, автор, кол-во просмотров, тег).
# - Реализовать модель тег.
# - Реализовать модель автор (имя, фамилия, кол-во публикаций автора).
# - Добавить валидацию ко всем полям.
# - Реализовать модуль заполнения всех полей БД валидными (адекватными данными :) ).
# - Добавить вывод всех постов по тегу, при каждом обращении к конкретному посту увеличовать кол-во просмотров на 1.
# - При обращении к автору, выводить все его публикации.
"""
- Реализовать модель Пост: models.Post()
- Реализовать модель тег: models.Tag
- Реализовать модель автор: models.Author
- Добавить вывод всех постов по тегу: Составляем запрос вида /blog/tagsearch/<string:tag_value>, где tag_value - тег
    увеличение просмотра поста на 1 тут: my_resources.SearchTag.get()
- При обращении к автору, выводить все его публикации:
  Составляем запрос вида /blog/asearch/<string:fname>/<string:surname>', где fname, surname - Имя, Фамилия автора.
- Написать REST для блога (использовать валидацию):
    -  /blog/all - вывод всех постов в кучу
    -  /blog/get/<string:id_key> - вывод конкретного поста по указанному id.
    - /blog/add - добавление поста. Данные передаем в json формате.
    - /blog/update/<string:id_key> - обновление данных по указанному id
    - /blog/delete/<string:id_key> - удаление поста по указанному id
- Реализовать модуль заполнения всех полей БД валидными (адекватными данными :) ). - Добавлена схема.
    - Сам класс для заполнения лежит в модуле seeder_lib
    - Сидить нужно посредством запуска файла models.py
"""


from flask import Flask
from flask_restful import Api
from my_resources import (
                            BlogResource,
                            SearchTag,
                            SearchAuthor,
                            PostView
                         )

app = Flask(__name__)
api = Api(app)

api.add_resource(BlogResource, '/blog/all', endpoint='get_all', methods=['GET'])
api.add_resource(BlogResource, '/blog/get/<string:id_key>', endpoint='get_by_id', methods=['GET'])
api.add_resource(BlogResource, '/blog/add', endpoint='post', methods=['POST'])
api.add_resource(BlogResource, '/blog/update/<string:id_key>', endpoint='put', methods=['PUT'])
api.add_resource(BlogResource, '/blog/delete/<string:id_key>', endpoint='delete', methods=['DELETE'])
api.add_resource(SearchTag, '/blog/tagsearch/<string:tag_value>', endpoint='search_by_tag', methods=['GET'])
api.add_resource(SearchAuthor, '/blog/asearch/<string:fname>/<string:surname>', methods=['GET'])
api.add_resource(PostView, '/blog/postview/<string:post_id>', methods=['GET'])


if __name__ == '__main__':
    app.run(debug=True)
