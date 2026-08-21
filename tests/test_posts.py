from app import schemas

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