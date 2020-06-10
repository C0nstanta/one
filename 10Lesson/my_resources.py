from flask.views import MethodView
from models import Post, Tag, Author
from flask import jsonify, request
from schemas import BlogSchema
from marshmallow import ValidationError
import json


class BlogResource(MethodView):

    @staticmethod
    def get(id_key=None):
        if id_key:
            for post in Post.objects(id=id_key):
                print(f'post.id:{post.id}, post.body:{post.body}, post.views:{post.views}')
                return BlogSchema().dumps(post)
        else:
            post_dict = {}
            for post in Post.objects():
                print(f'post.id:{post.id}, post.body:{post.body}, post.views:{post.views}')
                post_dict[str(post.id)] = post.body
            return BlogSchema(many=True).dumps(Post.objects().all())

    @staticmethod
    def post():
        data = BlogSchema().loads(json.dumps(request.json))
        try:
            if data['auth_name'] and data['auth_surname'] and data['header'] and data['body'] and data['tag_body']:
                author = Author.objects.create(auth_name=data['auth_name'], auth_surname=data['auth_surname'])
                tag = Tag.objects.create(tag_body=data['tag_body'])
                Post.objects.create(author=author, header=data['header'], body=data['body'], tag=tag)
        except ValidationError as e:
            return e.messages
        return data

    """В этом методе хочу пояснить, почему куча if, ведь логичнее было бы сделать так update(**data). Но у меня 
    апдейтиться может как только пост, автор или тэг. То есть тут часть данных не надо импортировать при апдейте. А в 
    словаре они идут на прием кучей."""
    @staticmethod
    def put(id_key=None):
        data = BlogSchema().loads(json.dumps(request.json))
        try:
            changes_list = []
            if data.get('auth_name'):
                Author.objects(id=id_key).update_one(set__auth_name=data['auth_name'])
                changes_list.append(f'auth_name:{data["auth_name"]} changed.')
            if data.get('auth_surname'):
                Author.objects(id=id_key).update_one(set__auth_surname=data['auth_surname'])
                changes_list.append(f'auth_surname:{data["auth_surname"]} changed.')
            if data.get('header'):
                Post.objects(id=id_key).update_one(set__header=data['header'])
                changes_list.append(f'header:{data["header"]} changed.')
            if data.get('body'):
                Post.objects(id=id_key).update_one(set__body=data['body'])
                changes_list.append(f'body:{data["body"]} changed.')
            if data.get('tag_body'):
                Post.objects(id=id_key).update_one(set__tag_body=data['tag_body'])
                changes_list.append(f'tag_body:{data["tag_body"]} changed.')
        except ValidationError as e:
            return f"{e.messages}:Wrong data dictionary"
        return changes_list

    @staticmethod
    def delete(id_key=None):
        for post in Post.objects(id=id_key):
            post.delete()
            print(f'post.id:{post.id} was deleted.')
            return BlogSchema().dumps(post)


class SearchTag(MethodView):

    @staticmethod
    def get(tag_value=None):
        post_dict = {}
        try:
            for tag in Tag.objects(tag_body=tag_value):
                print(f'tag.id:{tag.id} tag_body:{tag.tag_body}')
                for post in Post.objects(tag=tag.id):
                    Post.objects(id=post.id).update_one(inc__views=1)  # Увеличение просмотренных постов на 1
                    print(f'post.id:{post.id}, post.body:{post.body}, post.views:{post.views}')
                    post_dict[str(post.id)] = post.body
        except ValidationError as e:
            return e.messages
        return post_dict


class SearchAuthor(MethodView):

    @staticmethod
    def get(fname=None, surname=None):
        post_dict = {}
        for author in Author.objects(auth_name=fname.capitalize(), auth_surname=surname.capitalize()):
            print(f'author.id:{author.id}')
            for post in Post.objects(author=author.id):
                print(f'post.id:{post.id}, post.body:{post.body}')
                post_dict[str(post.id)] = post.body
        return post_dict


class PostView(MethodView):

    @staticmethod
    def get(post_id):
        for post in Post.objects(id=post_id):
            print(f'post.id:{post.id}, title:{post.header}, content:{post.body}, views:{post.views}')
        return f'post.id:{post.id}, title:{post.header}, content:{post.body}, views:{post.views}'
