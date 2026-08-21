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
    res = client.get('/posts')
    
    assert res.status_code == 401