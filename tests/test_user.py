import sys
sys.path.insert(0, 'src/')
from fastapi.testclient import TestClient
from src.main import app as user_app
import pytest

client = TestClient(user_app)

jwt_token = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NjYzNjczNDksImlhdCI6MTY2NjM2NTU0OSwic2NvcGUiOiJhY2Nlc3NfdG9rZW4iLCJzdWIiOiJ0ZXN0In0.hbUH18lVA31SdEocDk_bMYWcR6sDE8mu9PdzT_f38cc"

@pytest.mark.skip(reason="Already signed up")
def test_sign_up():
    response = client.post("/auth/signup?username=test&password=testtest",
                         headers={"accept": "application/json"},
                        )
    assert response.status_code != 200

def test_login():
    response = client.post("/auth/login?username=test&password=testtest",
                         headers={"accept": "application/json"},
                        )
    assert response.status_code == 200

# @pytest.mark.skip(reason="Already get")
def test_get_user():
    response = client.get("/auth/user",
                        headers={"accept": "application/json",
                                "Authorization": jwt_token},
                        )
    assert response.status_code == 200
    '''
    user = {
        "_id": "80647541-c473-426b-aa7b-6f2d4a69efbd",
        "profile_image": "63503dac5b3eee2fd67f100d",
        "name": "testic",
        "surname": "testic",
        "bio": "testi",
        "email": "testic@example.com",
        "hashed_password": "$2b$12$No3QJXzW7qac8.r6wYb8G.zpKO8.I8VNWFsSemQ9244Dx1ZiV.f8i",
        "username": "test",
        "gender": "woman",
        "age": "2022-10-19",
        "liked_posts": [
            "080f63fd-542e-4085-8a49-92925f007b2a",
            "a5865168-eb03-4a25-aae4-aa0bd146523d"
        ],
        "subscriptions": [],
        "subscribers": [
            "8631fd7a-940a-46b4-9d72-cb42585d790d"
        ],
        "created_at": "2022-10-19T18:22:04.754528",
        "updated_at": "2022-10-19T18:22:04.754532"
    }
    assert response.json() == user '''

def test_get_users():
    response = client.get("/users/",
                        headers={"accept": "application/json",
                                "Authorization": jwt_token,
                                },
                        )
    assert response.status_code == 200

def test_update_user():
    update_data = {
        "name": "test",
        "surname": "test",
        "bio": "test form test",
        "email": "test@test.com",
        "gender": "test",
        "age": "2022-10-21",
    }
    response = client.put("/users/update",
                        headers={"accept": "application/json",
                                "Authorization": jwt_token,
                                "Content-Type": "application/json",
                                },
                        json=update_data
                        )
    assert response.status_code == 200

def test_update_profile_image():
    response = client.put("/users/profile_image",
                        headers={"accept": "application/json",
                                "Authorization": jwt_token,
                                "Content-Type": "multipart/form-data",

                                },
                        )