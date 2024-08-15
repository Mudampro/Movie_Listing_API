import pytest




# Testing Create Comment Endpoint
@pytest.mark.parametrize("movie_data, comment_data", [
    (
        {"title": "Test Movie", "director": "Director", "genre": "Drama", "release_year": 2023},
        {"comment_text": "Great movie!"} 
    )
])
def test_create_comment(client, setup_db, movie_data, comment_data):
    # Create a user and log in
    user_data = {
        "username": "testuser",
        "full_name": "Test User",
        "phone_number": "08099898721",
        "password": "testpassword"
    }
    client.post("/Users/user/", json=user_data)
    login_response = client.post("/login", data={"username": "testuser", "password": "testpassword"})
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    # Create a movie
    create_movie_response = client.post("/Movies/movies", json=movie_data, headers={"Authorization": f"Bearer {token}"})
    assert create_movie_response.status_code == 201
    movie_id = create_movie_response.json()["id"]

    # Create a comment for the movie
    create_comment_response = client.post(
        f"/Comments/movies/{movie_id}/comments/",
        json=comment_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert create_comment_response.status_code == 200
    created_comment = create_comment_response.json()

    # Verify the comment text in the response matches the one sent in the request
    assert created_comment["comment_text"] == comment_data["comment_text"]


# Testing E
@pytest.mark.parametrize("movie_data, comment_data, reply_data", [
    (
        {"title": "Test Movie", "director": "Director", "genre": "Drama", "release_year": 2023},
        {"comment_text": "Great movie!"},
        {"comment_text": "I agree, fantastic!"}
    )
])
def test_create_reply(client, setup_db, movie_data, comment_data, reply_data):
    # Create a user and log in
    user_data = {
        "username": "testuser",
        "full_name": "Test User",
        "phone_number": "08099898721",
        "password": "testpassword"
    }
    client.post("/Users/user/", json=user_data)
    login_response = client.post("/login", data={"username": "testuser", "password": "testpassword"})
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    # Create a movie
    create_movie_response = client.post("/Movies/movies", json=movie_data, headers={"Authorization": f"Bearer {token}"})
    assert create_movie_response.status_code == 201
    movie_id = create_movie_response.json()["id"]

    # Create a comment for the movie
    create_comment_response = client.post(
        f"/Comments/movies/{movie_id}/comments/",
        json=comment_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert create_comment_response.status_code == 200
    created_comment = create_comment_response.json()
    comment_id = created_comment["id"]

    # Create a reply to the comment
    create_reply_response = client.post(
        f"/Comments/comments/{comment_id}/replies/",
        json=reply_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert create_reply_response.status_code == 200
    created_reply = create_reply_response.json()

    assert created_reply["comment_text"] == reply_data["comment_text"]


@pytest.mark.parametrize("comments",  [("comecomments"),])
def test_get_comments(client, setup_db, comments):
    response = client.get(f"/Comments/comments/")
    assert response.status_code == 200
    data = response.json()
    response_data = data[0]



import pytest

@pytest.mark.parametrize("movie_data, comment_data", [
    (
        {"title": "Test Movie", "director": "Director", "genre": "Drama", "release_year": 2023},
        {"comment_text": "Great movie!"}
    )
])
def test_get_comment(client, setup_db, movie_data, comment_data):
    # Create a user and log in
    user_data = {
        "username": "testuser",
        "full_name": "Test User",
        "phone_number": "08099898721",
        "password": "testpassword"
    }
    client.post("/Users/user/", json=user_data)
    login_response = client.post("/login", data={"username": "testuser", "password": "testpassword"})
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    # Create a movie
    create_movie_response = client.post("/Movies/movies", json=movie_data, headers={"Authorization": f"Bearer {token}"})
    assert create_movie_response.status_code == 201
    movie_id = create_movie_response.json()["id"]

    # Create a comment for the movie
    create_comment_response = client.post(
        f"/Comments/movies/{movie_id}/comments/",
        json=comment_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert create_comment_response.status_code == 200
    comment_id = create_comment_response.json()["id"]

    # Get the specific comment by ID
    get_comment_response = client.get(f"Comments/comments/{comment_id}")
    assert get_comment_response.status_code == 200
    retrieved_comment = get_comment_response.json()

    assert retrieved_comment["comment_text"] == comment_data["comment_text"]

# Get comment with an invalid ID or Id not in db
@pytest.mark.parametrize("comment_id", [999])
def test_get_comment_not_found(client, setup_db, comment_id):
    get_comment_response = client.get(f"Comments/comments/{comment_id}")
    assert get_comment_response.status_code == 404
    assert get_comment_response.json() == {"detail": "Comment not found"}


# Testing Update enpoint

import pytest

@pytest.mark.parametrize("comment_id, update_data, expected_status, expected_detail", [
    (1, {"comment_text": "Updated comment!"}, 200, None),  # Successful update
    (9999, {"comment_text": "Updated comment!"}, 404, "Comment not found or not authorized"),  # Non-existent comment
    (1, {"comment_text": "Unauthorized update!"}, 404, "Comment not found or not authorized"),  # Unauthorized user
])
def test_update_comment(client, setup_db, comment_id, update_data, expected_status, expected_detail):
    # Create a user and log in
    user_data = {
        "username": "testuser",
        "full_name": "Test User",
        "phone_number": "08099898721",
        "password": "testpassword"
    }
    client.post("/Users/user/", json=user_data)
    login_response = client.post("/login", data={"username": "testuser", "password": "testpassword"})
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    # Create a movie
    create_movie_response = client.post(
        "/Movies/movies",
        json={"title": "Test Movie", "director": "Director", "genre": "Drama", "release_year": 2023},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert create_movie_response.status_code == 201
    movie_id = create_movie_response.json()["id"]

    # Create a comment for the movie
    create_comment_response = client.post(
        f"/Comments/movies/{movie_id}/comments/",
        json={"comment_text": "Original comment"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert create_comment_response.status_code == 200
    created_comment = create_comment_response.json()
    created_comment_id = created_comment["id"]  # Use the ID of the created comment

    # Adjust the comment_id based on the parameterized test case
    comment_id = created_comment_id if comment_id == 1 else 9999

    # If we are testing unauthorized access, create a second user and log in as that user
    if update_data["comment_text"] == "Unauthorized update!":
        user_data2 = {
            "username": "unauthorizeduser",
            "full_name": "Unauthorized User",
            "phone_number": "08012345678",
            "password": "anotherpassword"
        }
        client.post("/Users/user/", json=user_data2)
        login_response2 = client.post("/login", data={"username": "unauthorizeduser", "password": "anotherpassword"})
        assert login_response2.status_code == 200
        token2 = login_response2.json()["access_token"]

    # Attempt to update the comment
    update_comment_response = client.put(
        f"/Comments/comments/{comment_id}/",
        json=update_data,
        headers={"Authorization": f"Bearer {token}" if update_data["comment_text"] != "Unauthorized update!" else f"Bearer {token2}"}
    )

    # Verify the status code and response details
    assert update_comment_response.status_code == expected_status
    if expected_status == 200:
        updated_comment = update_comment_response.json()
        assert updated_comment["comment_text"] == update_data["comment_text"]
    else:
        assert update_comment_response.json() == {"detail": expected_detail}


import pytest

@pytest.mark.parametrize("comment_text, expected_status", [
    ("Comment to delete", 200),
])
def test_delete_comment_success(client, setup_db, comment_text, expected_status):
    # Create a user and log in
    user_data = {
        "username": "testuser",
        "full_name": "Test User",
        "phone_number": "08099898721",
        "password": "testpassword"
    }
    client.post("/Users/user/", json=user_data)
    login_response = client.post("/login", data={"username": "testuser", "password": "testpassword"})
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    # Create a movie
    create_movie_response = client.post(
        "/Movies/movies",
        json={"title": "Test Movie", "director": "Director", "genre": "Drama", "release_year": 2023},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert create_movie_response.status_code == 201
    movie_id = create_movie_response.json()["id"]

    # Create a comment for the movie
    create_comment_response = client.post(
        f"/Comments/movies/{movie_id}/comments/",
        json={"comment_text": comment_text},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert create_comment_response.status_code == 200
    created_comment = create_comment_response.json()
    created_comment_id = created_comment["id"]

    # Delete the comment
    delete_comment_response = client.delete(
        f"/Comments/comments/{created_comment_id}/",
        headers={"Authorization": f"Bearer {token}"}
    )

    # Verify the status code
    assert delete_comment_response.status_code == expected_status
    if expected_status == 200:
        # Verify the response
        deleted_comment = delete_comment_response.json()
        assert deleted_comment["id"] == created_comment_id
        assert deleted_comment["comment_text"] == comment_text


import pytest

@pytest.mark.parametrize("comment_id, expected_status, expected_detail", [
    (9999, 404, "Comment not found or not authorized"),
])
def test_delete_comment_not_found(client, setup_db, comment_id, expected_status, expected_detail):
    # Create a user and log in
    user_data = {
        "username": "testuser",
        "full_name": "Test User",
        "phone_number": "08099898721",
        "password": "testpassword"
    }
    client.post("/Users/user/", json=user_data)
    login_response = client.post("/login", data={"username": "testuser", "password": "testpassword"})
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    # Attempt to delete a non-existent comment
    delete_comment_response = client.delete(
        f"/Comments/comments/{comment_id}/",
        headers={"Authorization": f"Bearer {token}"}
    )

    # Verify the status code and response details
    assert delete_comment_response.status_code == expected_status
    assert delete_comment_response.json() == {"detail": expected_detail}



import pytest

@pytest.mark.parametrize("comment_id, expected_status, expected_detail", [
    (1, 404, "Comment not found or not authorized"),
])
def test_delete_comment_unauthorized(client, setup_db, comment_id, expected_status, expected_detail):
    # Create two users
    user1_data = {
        "username": "testuser1",
        "full_name": "Test User 1",
        "phone_number": "08099898722",
        "password": "testpassword1"
    }
    client.post("/Users/user/", json=user1_data)
    login_response1 = client.post("/login", data={"username": "testuser1", "password": "testpassword1"})
    assert login_response1.status_code == 200
    token1 = login_response1.json()["access_token"]

    user2_data = {
        "username": "testuser2",
        "full_name": "Test User 2",
        "phone_number": "08099898723",
        "password": "testpassword2"
    }
    client.post("/Users/user/", json=user2_data)
    login_response2 = client.post("/login", data={"username": "testuser2", "password": "testpassword2"})
    assert login_response2.status_code == 200
    token2 = login_response2.json()["access_token"]

    # Create a movie
    create_movie_response = client.post(
        "/Movies/movies",
        json={"title": "Test Movie", "director": "Director", "genre": "Drama", "release_year": 2023},
        headers={"Authorization": f"Bearer {token1}"}
    )
    assert create_movie_response.status_code == 201
    movie_id = create_movie_response.json()["id"]

    # Create a comment for the movie with user1
    create_comment_response = client.post(
        f"/Comments/movies/{movie_id}/comments/",
        json={"comment_text": "Comment to delete"},
        headers={"Authorization": f"Bearer {token1}"}
    )
    assert create_comment_response.status_code == 200
    created_comment = create_comment_response.json()
    created_comment_id = created_comment["id"]

    # Attempt to delete the comment with user2 (unauthorized)
    delete_comment_response = client.delete(
        f"/Comments/comments/{created_comment_id}/",
        headers={"Authorization": f"Bearer {token2}"}
    )

    # Verify the status code and response details
    assert delete_comment_response.status_code == expected_status
    assert delete_comment_response.json() == {"detail": expected_detail}
