from app import schemas
import pytest

def test_get_all_posts(authorized_client, put_posts):
    res = authorized_client.get('/posts/')
    # print(res.json())
    
    def validate(post):
        return schemas.VotePost(**post)
    posts_map = map(validate, res.json())
    print(list(posts_map))
    
    assert len(res.json()) == len(put_posts)
    assert res.status_code == 200 
    
def test_unauthorized_client_get_all_post(client):
    res = client.get('/posts/')
    
    assert res.status_code == 401
    
def test_unauthorized_client_get_one_post(client, put_posts):    
    res = client.get(f'/posts/{put_posts[0].id}')
    
    assert res.status_code == 401

def test_unauthorized_client_get_one_post_not_exist(authorized_client, put_posts):    
    res = authorized_client.get(f'/posts/9')
    
    assert res.status_code == 404

def test_get_one_post(authorized_client, put_posts):
    res = authorized_client.get(f'/posts/{put_posts[0].id}')
    print(res.json())
    post = schemas.VotePost(**res.json())
    
    assert post.Post.id == put_posts[0].id
    assert post.Post.content == put_posts[0].content
    
@pytest.mark.parametrize("title, content, published ", argvalues=[
    ("i'm back", "mfers we up", True),
    ("i'm back dad", "mfers we up, dad", True),
    ("i'm back ooo", "mfers we u oop", False),
])
def test_create_post(authorized_client, put_posts, login_user, title, content, published):
    res = authorized_client.post('/posts/', json={"title": title, "content": content, 
                                                  "published": published})
    
    created_post = schemas.Post(**res.json())
    
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == login_user['id']
    
def test_create_post_default_published_true(authorized_client, login_user, put_posts):
    res = authorized_client.post(
        "/posts/", json={"title": "arbitrary title", "content": "aasdfjasdf"})

    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == "arbitrary title"
    assert created_post.content == "aasdfjasdf"
    assert created_post.published == True
    assert created_post.owner_id == login_user['id']


def test_unauthorized_user_create_post(client, login_user, put_posts):
    res = client.post(
        "/posts/", json={"title": "arbitrary title", "content": "aasdfjasdf"})
    assert res.status_code == 401


def test_unauthorized_user_delete_Post(client, login_user, put_posts):
    res = client.delete(
        f"/posts/{put_posts[0].id}")
    assert res.status_code == 401


def test_delete_post_success(authorized_client, login_user, put_posts):
    res = authorized_client.delete(
        f"/posts/{put_posts[0].id}")

    assert res.status_code == 204


def test_delete_post_non_exist(authorized_client, login_user, put_posts):
    res = authorized_client.delete(
        f"/posts/8000000")

    assert res.status_code == 404


def test_delete_other_user_post(authorized_client, login_user, put_posts):
    res = authorized_client.delete(
        f"/posts/{put_posts[2].id}")
    assert res.status_code == 204


def test_update_post(authorized_client, login_user, put_posts):
    data = {
        "title": "updated title",
        "content": "updatd content",
        "id": put_posts[0].id

    }
    res = authorized_client.put(f"/posts/{put_posts[0].id}", json=data)
    updated_post = schemas.Post(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']


# def test_update_other_user_post(authorized_client, test_user, test_user2, test_posts):
#     data = {
#         "title": "updated title",
#         "content": "updatd content",
#         "id": test_posts[3].id

#     }
#     res = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)
#     assert res.status_code == 403


# def test_unauthorized_user_update_post(client, test_user, test_posts):
#     res = client.put(
#         f"/posts/{test_posts[0].id}")
#     assert res.status_code == 401


# def test_update_post_non_exist(authorized_client, test_user, test_posts):
#     data = {
#         "title": "updated title",
#         "content": "updatd content",
#         "id": test_posts[3].id

#     }
#     res = authorized_client.put(
#         f"/posts/8000000", json=data)

#     assert res.status_code == 404