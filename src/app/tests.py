import json

from django.urls import reverse
from model_bakery import baker

from app.models import Post, User


def test_user_registration(db, api_client):
    user = baker.prepare(User)
    user_data = {
        "email": user.email,
        "phoneNumber": "1000",
        "firstName": user.first_name,
        "lastName": user.last_name,
        "password": "password",
        "confirmPassword": "password"
        }
    url = reverse('app:register')
    resp = api_client.post(
            url,
            data=json.dumps(user_data),
            content_type="application/json"
        )
    assert resp.status_code == 201
    assert resp.json()['user']['firstName'] == user.first_name


def test_user_login(db, api_client):
    user = baker.prepare(User)
    user_data = {
        "email": user.email,
        "phoneNumber": "1000",
        "firstName": user.first_name,
        "lastName": user.last_name,
        "password": "password",
        "confirmPassword": "password"
    }
    url = reverse('app:register')
    api_client.post(
        url,
        data=json.dumps(user_data),
        content_type="application/json"
    )
    login_url = reverse('app:login')
    login_data = {'email': user.email, 'password': 'password'}
    resp = api_client.post(
            login_url,
            data=json.dumps(login_data),
            content_type="application/json"
        )
    assert resp.status_code == 200
    assert 'accessToken' in resp.json()


def test_create_post(db, api_client_with_token):
    post = baker.prepare(Post)
    post_data = {
        "topic": post.topic,
        "content": post.content,
        }
    url = reverse('app:post_list')
    resp = api_client_with_token.post(
            url,
            data=json.dumps(post_data),
            content_type="application/json"
        )
    assert resp.status_code == 201
    assert resp.json()['topic'] == post.topic


def test_retrieve_post(db, api_client_with_token):
    post = baker.make(Post)
    url = reverse('app:post_detail', kwargs={"id": post.id})
    resp = api_client_with_token.get(url, content_type="application/json")
    assert resp.status_code == 200
    assert resp.json()['topic'] == post.topic


def test_list_posts(db, api_client_with_token):
    baker.make(Post, 10)
    url = reverse('app:post_list')
    resp = api_client_with_token.get(url, content_type="application/json")

    assert resp.status_code == 200
    assert len(resp.json()) == 10


def test_delete_post(db, api_client_with_token):
    posts = baker.make(Post, 10)
    url = reverse('app:post_detail', kwargs={"id": posts[1].id})
    resp = api_client_with_token.delete(url, content_type="application/json")
    assert resp.status_code == 204
    assert len(api_client_with_token.get(reverse('app:post_list'), content_type="application/json").json()) == 9


def test_user_cannot_like_their_own_post(db, api_client_with_token, user):
    post = baker.make(Post, owner=user)
    url = reverse('app:like_post', kwargs={"post_id": post.id})
    resp = api_client_with_token.get(url, content_type="application/json")

    assert resp.status_code == 400
    assert resp.json()['detail'] == 'You are not allowed to like your own post'


def test_user_can_like_their_own_post(db, api_client_with_token):
    post = baker.make(Post)
    url = reverse('app:like_post', kwargs={"post_id": post.id})
    resp = api_client_with_token.get(url, content_type="application/json")

    assert resp.status_code == 200
