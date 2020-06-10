import os
import random
from models import *


class DBManager:

    script_path = os.getcwd()
    file_path = script_path + '/randombase/'

    fname_list = []
    surname_list = []
    tag_list = []
    author_dict = {}
    header_list = []
    body_list = []

    def seed_authors(self, num_seed=1):  # Сиидер рендомными авторами документа author
        with open(self.file_path + 'fname.txt', encoding='utf-8', mode='r') as fname:
            for name in fname:
                self.fname_list.append(name.replace('\n', ''))

        with open(self.file_path + 'lname.txt', encoding='utf-8', mode='r') as sname:
            self.surname_list = [x.replace('\n', '') for x in sname]
            i = 0
            while i < num_seed:
                fname_rand = random.choice(self.fname_list)
                surname_rand = random.choice(self.surname_list)
                author = Author.objects.create(auth_name=f'{fname_rand}', auth_surname=f'{surname_rand}', num_post=0)
                print(f'Author_id:{author.id}, name:{fname_rand} surname:{surname_rand} was added')
                i += 1

#  Для того, что бы сидить посты, мы должны сначала получить список наших авторов.
#  Так как сидить новыми рендомными авторами посты посчитал не сильно хорошо, сидим на основе уже существующих авторов
#  При создании поста, автору увеличиваем количество созданных постов.
    def seed_posts(self, num_seed=None):
        with open(self.file_path + 'tag.txt', encoding='utf-8', mode='r') as tagfile:
            self.tag_list = [x.replace('\n', '') for x in tagfile]

        with open(self.file_path + 'body.txt', encoding='utf-8', mode='r') as bodyfile:
            self.body_list = [x.replace('\n', '') for x in bodyfile]

        with open(self.file_path + 'title.txt', encoding='utf-8', mode='r') as titlefile:
            self.header_list = [x.replace('\n', '') for x in titlefile]

        for author in Author.objects():
            self.author_dict[str(author.id)] = list([author.auth_name, author.auth_surname])

        i = 0
        while i < num_seed:
            auth_id_rand = random.choice(list(self.author_dict))
            tag_rand = random.choice(self.tag_list)
            body_text_rand = random.choice(self.body_list)
            title_text_rand = random.choice(self.header_list)

            rand_author = Author.objects(id=auth_id_rand).get()
            tag = Tag.objects.create(tag_body=[tag_rand])
            post = Post.objects.create(author=rand_author, header=title_text_rand, body=body_text_rand, views=1,
                                       tag=tag)

            for auth in Author.objects(id=auth_id_rand):
                Author.objects(id=auth.id).update_one(inc__num_post=1)
            print(f'Post:{post.id} created.')
            i += 1
