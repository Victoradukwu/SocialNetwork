import discord
import os
import requests

from dotenv import load_dotenv

load_dotenv()

client = discord.Client()

host = os.getenv('APP_HOST')
users = []
posts = []
BOT_CONFIGS = {
    'number_of_users': 5,
    'max_posts_per_user': 5,
    'max_likes_per_user': 10
}


def create_users(session):
    for cnt in range(1, BOT_CONFIGS['number_of_users'] + 1):
        user_data = {
          'email': f'user{cnt}@social.com',
          'phoneNumber': f'10000{cnt}',
          'firstName': f'User{cnt}F',
          'lastName': f'User{cnt}L',
          'password': f'user{cnt}',
          'confirmPassword': f'user{cnt}'
        }
        resp = session.post(f'http://{host}:8000/auth/register/', json=user_data, headers={})
        json_resp = resp.json()
        user = json_resp['user']
        user['password'] = user_data['password']
        user['token'] = json_resp['accessToken']
        users.append(user)
    created_users = [user['email'] for user in users]
    print('Created users: ', created_users)


def create_posts(session):
    for user in users:
        for cnt in range(1, BOT_CONFIGS['max_posts_per_user'] + 1):
            post_data = {
                'topic': f'Post Number{cnt}-{user["email"]}',
                'content': f'This is the content for Post Number{cnt}'
              }
            resp = session.post(f'http://{host}:8000/posts/',
                                json=post_data,
                                headers={'Authorization': f'Token {user["token"]}'}
                                )
            post = resp.json()
            posts.append(post)
    created_posts = [post['topic'] for post in posts]
    print('Created posts: ', created_posts)


def like_posts(session):
    global users
    users = sorted(users, key=lambda x: len(x['posts']), reverse=True)
    posts_to_like = [post for post in posts if not post['likes']]
    user_iter = iter(users)
    while posts_to_like:
        user = next(user_iter)
        while len(user['likedPosts']) < BOT_CONFIGS['max_likes_per_user']:
            possible_posts = [post for post in posts_to_like if post['owner'] != user['id']]
            if not possible_posts:
                break
            for post in possible_posts:
                resp = session.get(f'http://{host}:8000/posts/like/{post["id"]}/',
                                   headers={'Authorization': f'Token {user["token"]}'})
                if resp.ok:
                    user['likedPosts'].append(post['id'])
                posts_to_like.remove(post)
    token = users[0]["token"]
    post_resp = session.get(f'http://{host}:8000/posts/', headers={'Authorization': f'Token {token}'})
    print('Posts after likings', post_resp.json())


def social_activities():
    with requests.Session() as session:
        session.headers.update({'Content-Type': 'application/json'})
        create_users(session)
        create_posts(session)
        like_posts(session)


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('$social'):
        social_activities()
        await message.channel.send('Done')

client.run(os.getenv('TOKEN'))
