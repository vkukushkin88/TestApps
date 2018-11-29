import uuid
import json
import random
import argparse
import configparser
from urllib.parse import urljoin
from types import SimpleNamespace

import django
import factory
import factory.fuzzy
import requests


django.setup()


from django.contrib.auth.models import User


DEFAULT_INPUT_FILE_PATH = 'test_conf.ini'
SERVER_LOCALHOST = 'http://localhost:8000'


class MethodError(Exception):
    pass


class BaseData(SimpleNamespace):
    def add(self, new_attrs: dict):
        for k, v in new_attrs.items():
            setattr(self, k, v)


User = Post = BaseData


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: 'user%s' % str(uuid.uuid4())[:7])
    email = factory.LazyAttribute(lambda obj: '%s@example.com' % obj.username)
    password = factory.Sequence(lambda n: 'password%d' % n)


def __do_request(*,
                 method: ['POST', 'GET'],
                 url: str,
                 data: dict=None,
                 token: str=None) -> dict:

    headers = {'Authorization': 'JWT '+ token} if token else {}
    url = urljoin(SERVER_LOCALHOST, url)

    if method == 'POST':
        headers['Content-Type'] = 'application/json'
        res = requests.post(url, data=json.dumps(data), headers=headers)
    elif method == 'GET':
        res = requests.get(url, headers=headers)
    else:
        raise MethodError('Only GET|POST are allowed')

    try:
        res.raise_for_status()
    except requests.exceptions.HTTPError:
        print(res.text)
        raise

    return res.json()


def signup_users(*, number_of_users: int) -> list:
    users = []
    for i in range(number_of_users):
        user = User()
        new_user = UserFactory()
        user.add(__do_request(method='POST', url='users/', data={
            'username': new_user.username,
            'email': new_user.email,
            'password': new_user.password,
        }))
        print('Created new user: ', user.username)
        user.password = new_user.password
        users.append(user)
    return users


def login_user(*, user: User):
    print('Login user %s' % user.email)
    user.token = __do_request(
        method='POST', url='users/auth/api-token-auth/', data={
            'password': user.password,
            'username': user.username
        }
    )['token']


def create_posts(*, user: User, max_posts: int):
    num_posts = random.randint(1, max_posts)
    user.num_posts = num_posts
    posts = []
    print('Do %d posts by user: %s' % (num_posts, user.username))
    for i in range(num_posts):
        post = Post()
        post.add(__do_request(
            method='POST', url='posts/', data={
                'text': str(factory.fuzzy.FuzzyText())
            }, token=user.token
        ))
        post.likes = 0
        posts.append(post)

    user.posts = posts


def do_like(*, user: User, post: Post):
    print('Do like post %s by user %s' % (post.id, user.username))
    (__do_request(
        method='POST', url='posts/{}/like/'.format(post.id), data={
            'text': str(factory.fuzzy.FuzzyText())
        }, token=user.token
    ))
    post.likes += 1


def run_bot(config):
    users = signup_users(
        number_of_users=int(config['DEFAULT']['number_of_users']))
    for user in users:
        user.likes = 0
        login_user(user=user)
        create_posts(user=user,
                     max_posts=int(config['DEFAULT']['max_posts_per_user']))

    max_likes = int(config['DEFAULT']['max_likes_per_user'])
    while True:
        users_to_like = [user for user in users if user.likes < max_likes]
        if not users_to_like:
            print('All users exceed max likes')
            break
        users_to_like.sort(key=lambda x: len(x.posts), reverse=True)

        posts_to_like = []
        for user in users:
            if not all([post.likes for post in user.posts]):
                posts_to_like.extend(user.posts)

        if not posts_to_like:
            print('No more posts to like')
            break
        post_to_like = random.choice(posts_to_like)
        do_like(user=users_to_like[0], post=post_to_like)
        users_to_like[0].likes += 1
        post_to_like.likes += 1


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help='Input file path',
                        default=DEFAULT_INPUT_FILE_PATH)
    return parser.parse_args()


def main():
    args = parse_args()

    config = configparser.ConfigParser()
    config.read(args.input)

    run_bot(config)


if __name__ == '__main__':
    main()
