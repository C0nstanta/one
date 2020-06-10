import mongoengine as me
import datetime
from seeder_lib import *
me.connect('Blog')


class Tag(me.Document):
    """Реализовать модель тег."""
    tag_body = me.ListField(me.StringField(max_length=256))

# Tag.objects
# [obj.tag for obj in Tag.objects] - выдернуть теги


class Author(me.Document):

    """Реализовать модель автор (имя, фамилия, кол-во публикаций автора)."""

    auth_name = me.StringField(max_length=40, required=True)
    auth_surname = me.StringField(max_length=40)
    num_post = me.IntField(min_value=0)


class Post(me.Document):

    """Реализовать модель Пост (название, содержание, дата публикации, автор, кол-во просмотров, тег)."""

    author = me.ReferenceField(Author)
    tag = me.ReferenceField(Tag)

    header = me.StringField(max_length=256, required=True)
    body = me.StringField(max_length=4056)
    created = me.DateTimeField(default=datetime.datetime.utcnow())
    views = me.IntField(min_value=1)


# Добавить валидацию ко всем полям.
if __name__ == "__main__":
    dbmanager = DBManager()
    dbmanager.seed_posts(1)  # Это сидер постов( количество которых передаем в метод класса). Сидятся посты и теги
    # одновременно. Авторы берутся из существующих

    dbmanager.seed_authors(1)  # Это сидер авторов( количество которых передаем в метод класса)
