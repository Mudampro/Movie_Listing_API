import pytest


@pytest.mark.parametrize("username, full_name, phone_number, password", 
                         [("newuser", "newName", "090999444", "newpassword")])
def test_login(client, setup_db, username, full_name, phone_number, password):
    # Signing up a user
    new_user_data = {
        "username": username,
        "full_name": full_name,
        "phone_number": phone_number,
        "password": password
    }
    response = client.post("/Users/user/", json=new_user_data )
    assert response.status_code == 201

    # Login in the user
    response = client.post("/login", data= {"username": username, "password": password})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


# Test data for create_user endpoint
@pytest.mark.parametrize("username, full_name, phone_number, password", [
    ('someuser', 'somename', '090999', 'somepassword'),
   
])
def test_create_user(client, setup_db, username, full_name, phone_number, password):
    user_data = {
        "username": username,
        "full_name": full_name,
        "phone_number": phone_number,
        "password": password
    }
    response = client.post("/Users/user/", json=user_data )
    print(response.json())
    assert response.status_code == 201
    response_data = response.json()
    assert response_data["username"] == username
    assert "id" in response_data

# Test create user with existing username
@pytest.mark.parametrize("username, full_name, phone_number, password", [
    ('someuser', 'anothername', '090888', 'anotherpassword'),
])
def test_create_user_with_existing_username(client, setup_db, username, full_name, phone_number, password):
    
    initial_user_data = {
        "username": "uniqueuser",
        "full_name": "initialname",
        "phone_number": "090777",
        "password": "initialpassword"
    }
    response = client.post("/Users/user/", json=initial_user_data)
    assert response.status_code == 201

    # Attempting to create another user with the same username as above
    user_data = {
        "username": "uniqueuser",
        "full_name": full_name,
        "phone_number": phone_number,
        "password": password
    }
    response = client.post("/Users/user/", json=user_data)
    
    assert response.status_code == 400
    response_data = response.json()
    assert response_data["detail"] == "Username already registered"


# Test data for get_users endpoint
@pytest.mark.parametrize("username",  [("someuser"),])
def test_get_users(client, setup_db, username):
    response = client.get(f"/Users/users/")
    assert response.status_code == 200
    data = response.json()
    response_data = data[0]
 


# Test data for get_user by id endpoint
@pytest.mark.parametrize("user_id, username", [
    (1, 'someuser'),
])
def test_get_user(client, setup_db, user_id, username):
    response = client.get(f"/Users/users/{user_id}")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["id"] == user_id


@pytest.mark.parametrize("user_id", [101]) 
def test_get_user_not_found(client, setup_db, user_id):
    response = client.get(f"/Users/users/{user_id}")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


# Test data for update_user endpoint
@pytest.mark.parametrize("user_id, update_data", [
    (1, {"full_name": "updatedname", "phone_number": "070688"}),
])
def test_update_user(client, setup_db, user_id, update_data):
    response = client.put(f"/Users/users/{user_id}", json=update_data)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["id"] == user_id
    assert response_data["id"] == user_id
   

@pytest.mark.parametrize("user_id", [111])
def test_update_user_not_found(client, setup_db, user_id):
    update_data = {"full_name": "updatedname", "phone_number": "070688"}
    response = client.put(f"/Users/users/{user_id}", json=update_data)
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


# Test data for delete_user endpoint
@pytest.mark.parametrize("user_id", [1])
def test_delete_user(client, setup_db, user_id):
    response = client.delete(f"/Users/users/{user_id}")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["id"] == user_id

@pytest.mark.parametrize("user_id", [112]) 
def test_delete_user_not_found(client, setup_db, user_id):
    response = client.delete(f"/Users/users/{user_id}")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}
