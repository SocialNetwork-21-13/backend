import sys
sys.path.insert(0, 'src/')
from fastapi.testclient import TestClient
from src.main import app as user_app
import pytest
from src.repositories.user import UserRepository

client = TestClient(user_app)

users = UserRepository()

jwt_token = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NjYzNzEyMzQsImlhdCI6MTY2NjM2OTQzNCwic2NvcGUiOiJhY2Nlc3NfdG9rZW4iLCJzdWIiOiJ0ZXN0In0.YPiVbQEu25asw7RrGDz-9nopMyqN81oXtpEluJkQ7jQ"
user_id = ""

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
    u_id = response.json()["_id"]
    global user_id
    user_id = u_id
    user = users.get_by_id(user_id)
    assert response.status_code == 200
    assert response.json() == user

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
    global user_id
    user = users.get_by_id(user_id)
    assert response.json() == user
    assert response.status_code == 200

@pytest.mark.skip(reason="Not working")
def test_update_profile_image():
    response = client.put("/users/profile_image",
                        headers={"accept": "application/json",
                                "Authorization": jwt_token,
                                "Content-Type": "multipart/form-data",
                                },
                        files="file=@1_change.png;type=image/png"
                        )
    assert response.status_code == 200

def test_update_name_surname():
    response = client.put("/users/name_surname?name=third&surname=fourh",
                        headers={"accept": "application/json",
                                "Authorization": jwt_token},
                        )
    global user_id
    user = users.get_by_id(user_id)
    assert response.json() == user
    assert response.status_code == 200

def test_update_username():
    response = client.put("/users/username?username=test",
                        headers={"accept": "application/json",
                                "Authorization": jwt_token},
                        )
    global user_id
    user = users.get_by_id(user_id)
    assert response.json() == user
    assert response.status_code == 200

def test_update_bio():
    response = client.put("/users/bio?bio=testic",
                        headers={"accept": "application/json",
                                "Authorization": jwt_token},
                        )
    global user_id
    user = users.get_by_id(user_id)
    assert response.json() == user
    assert response.status_code == 200

def test_subscribe():
    response = client.put("/users/subscribe?sub_id=80647541-c473-426b-aa7b-6f2d4a69efbd",
                        headers={"accept": "application/json",
                                "Authorization": jwt_token},
                        )
    assert response.status_code == 200

def test_unsibscribe():
    response = client.put("/users/unsubscribe?sub_id=80647541-c473-426b-aa7b-6f2d4a69efbd",
                        headers={"accept": "application/json",
                                "Authorization": jwt_token},
                        )
    assert response.status_code == 200

def test_get_subscribers():
    response = client.get("/users/get_subscribers",
                        headers={"accept": "application/json",
                                "Authorization": jwt_token},
                        )
    global user_id
    subs = users.get_subscribers(user_id)
    assert response.json() == subs
    assert response.status_code == 200

def test_get_subscriptions():
    response = client.get("/users/get_subscriptions",
                        headers={"accept": "application/json",
                                "Authorization": jwt_token},
                        )
    global user_id
    subs = users.get_subscriptions(user_id)
    assert response.json() == subs
    assert response.status_code == 200