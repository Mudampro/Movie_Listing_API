import pytest




# TESTING CREATE RATING ENDPOINT
@pytest.mark.parametrize("movie_data, rating_data", [
    (
        {"title": "Test Movie", "director": "Director", "genre": "Drama", "release_year": 2023},
        {"rating": 8}
    )
])
def test_create_rating(client, setup_db, movie_data, rating_data):
    # Create a user and log in
    user_data = {
        "username": "testuser",
        "full_name": "Test User",
        "phone_number": "0897090989",
        "password": "testpassword"
    }
    client.post("/Users/user/", json=user_data)
    login_response = client.post("/login", data={"username": "testuser", "password": "testpassword"})
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    # Create a movie
    create_movie_response = client.post("/Movies/movies", json=movie_data, headers={"Authorization": f"Bearer {token}"})
    assert create_movie_response.status_code == 201
    movie_data_response = create_movie_response.json()
    movie_id = movie_data_response["id"]
    print(f"Created movie with ID: {movie_id}")

    # Create a rating for the movie
    create_rating_response = client.post(
        f"/Ratings/movies/{movie_id}/ratings/",
        json=rating_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert create_rating_response.status_code == 200
    rating = create_rating_response.json()
    assert rating["rating"] == rating_data["rating"]
    assert rating["movie_id"] == movie_id

# Testing for invalid movie ID when rating a movie
@pytest.mark.parametrize("movie_id", [9912]) 
def test_create_rating_invalid_movie(client, setup_db, movie_id):
  
    user_data = {
        "username": "testuser",
        "full_name": "Test User",
        "phone_number": "08089898778",
        "password": "testpassword"
    }
    client.post("/Users/user/", json=user_data)
    login_response = client.post("/login", data={"username": "testuser", "password": "testpassword"})
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    # Attempt to create a rating for a non-existent movie
    rating_data = {"rating": 8}
    response = client.post(
        f"/Ratings/movies/{movie_id}/ratings/",
        json=rating_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Invalid Movie Id or Movie not found"}

# Test for Rating with Invalid Rating value
@pytest.mark.parametrize("rating_data", [
    {"rating": 0},  # Below valid range
    {"rating": 11}  # Above valid range
])
def test_create_rating_invalid_value(client, setup_db, rating_data):
    # Create a movie and user
    movie_data = {"title": "Valid Movie", "director": "Director", "genre": "Drama", "release_year": 2023}
    user_data = {
        "username": "testuser",
        "full_name": "Test User",
        "phone_number": "90989809876",
        "password": "testpassword"
    }

    client.post("/Users/user/", json=user_data)
    login_response = client.post("/login", data={"username": "testuser", "password": "testpassword"})
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    create_movie_response = client.post("/Movies/movies", json=movie_data, headers={"Authorization": f"Bearer {token}"})
    assert create_movie_response.status_code == 201
    movie_id = create_movie_response.json()["id"]

    # Attempt to create a rating with invalid value
    response = client.post(
        f"/Ratings/movies/{movie_id}/ratings/",
        json=rating_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Ratings of a movie must not be less than 1 and greater than 10"}

# Test for User Re-Rating the Same Movie
@pytest.mark.parametrize("movie_data, rating_data", [
    (
        {"title": "Another Movie", "director": "Another Director", "genre": "Action", "release_year": 2023},
        {"rating": 7}
    )
])
def test_create_rating_user_already_rated(client, setup_db, movie_data, rating_data):
    # Create a user and log in
    user_data = {
        "username": "testuser",
        "full_name": "Test User",
        "phone_number": "9080980090",
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

    # Create a rating for the movie
    create_rating_response = client.post(
        f"/Ratings/movies/{movie_id}/ratings/",
        json=rating_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert create_rating_response.status_code == 200

    # Attempt to rate the same movie again
    response = client.post(
        f"/Ratings/movies/{movie_id}/ratings/",
        json=rating_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "User has already rated this movie"}


# TESTING FOR GET RATINGS ENDPOINT
@pytest.mark.parametrize("rating",  [9])
def test_get_ratings(client, setup_db, rating):
    response = client.get(f"/Ratings/ratings/")
    assert response.status_code == 200
    data = response.json()
    response_data = data[0]


# TESTING FOR GET RATING BY ID ENDPOINT
@pytest.mark.parametrize("movie_data, rating_data", [
    (
        {"title": "Test Movie", "director": "Director", "genre": "Drama", "release_year": 2023},
        {"rating": 8}
    )
])
def test_get_rating(client, setup_db, movie_data, rating_data):
    # Create a user and log in
    user_data = {
        "username": "testuser",
        "full_name": "Test User",
        "phone_number": "090998987",
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

    # Create a rating for the movie
    create_rating_response = client.post(
        f"Ratings/movies/{movie_id}/ratings/",
        json=rating_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert create_rating_response.status_code == 200
    rating_id = create_rating_response.json()["id"]

    # Retrieve the rating
    get_rating_response = client.get(f"/Ratings/ratings/{rating_id}")
    assert get_rating_response.status_code == 200
    retrieved_rating = get_rating_response.json()
    assert retrieved_rating["id"] == rating_id
    assert retrieved_rating["rating"] == rating_data["rating"]


# TESTING FOR GET RATING BY ID NOT FOUND ENDPOINT
@pytest.mark.parametrize("rating_id", [97987])
def test_get_rating_not_found(client, setup_db, rating_id):
    
    # Attempt to retrieve a non-existent rating
    get_rating_response = client.get(f"/Ratings/ratings/{rating_id}")
    assert get_rating_response.status_code == 404
    assert get_rating_response.json() == {"detail": "Rating not found"}


# TESTING FOR UPDATE RATING ENDPOINT
@pytest.mark.parametrize("movie_data, rating_data, update_data", [
    (
        {"title": "Test Movie", "director": "Director", "genre": "Drama", "release_year": 2023},
        {"rating": 9},
        {"rating": 8}
    )
])
def test_update_rating(client, setup_db, movie_data, rating_data, update_data):
    # Create a user and log in
    user_data = {
        "username": "testuser",
        "full_name": "Test User",
        "phone_number": "9898989877",
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

    # Create a rating for the movie
    create_rating_response = client.post(
        f"/Ratings/movies/{movie_id}/ratings/",
        json=rating_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert create_rating_response.status_code == 200
    rating_id = create_rating_response.json()["id"]

    # Update the rating
    update_rating_response = client.put(
        f"/Ratings/ratings/{rating_id}",
        json=update_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert update_rating_response.status_code == 200
    updated_rating = update_rating_response.json()
    assert updated_rating["id"] == rating_id
    assert updated_rating["rating"] == update_data["rating"]

# Testing For Test Updating a Non-existent or Unauthorized Rating
@pytest.mark.parametrize("rating_id", [9999, 10000, 12345])
def test_update_rating_not_found(client, setup_db, rating_id):
    # Create a user and log in
    user_data = {
        "username": "testuser",
        "full_name": "Test User",
        "phone_number": "89909004",
        "password": "testpassword"
    }
    client.post("/Users/user/", json=user_data)
    login_response = client.post("/login", data={"username": "testuser", "password": "testpassword"})
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    # Attempt to update a non-existent or unauthorized rating
    update_data = {"rating": 5}
    update_rating_response = client.put(
        f"Ratings/ratings/{rating_id}",
        json=update_data, headers={"Authorization": f"Bearer {token}"}
    )
    assert update_rating_response.status_code == 404
    assert update_rating_response.json() == {"detail": "Rating not found or not authorized"}


# Testing for Updating a Rating with Invalid Value
@pytest.mark.parametrize("invalid_rating_value", [-1, 0, 11, 100])
def test_update_rating_invalid_value(client, setup_db, invalid_rating_value):
    # Create a user and log in
    user_data = {
        "username": "testuser",
        "full_name": "Test User",
        "phone_number": "867857585",
        "password": "testpassword"
    }
    client.post("/Users/user/", json=user_data)
    login_response = client.post("/login", data={"username": "testuser", "password": "testpassword"})
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    # Create a movie
    movie_data = {"title": "Test Movie", "director": "Director", "genre": "Drama", "release_year": 2023}
    create_movie_response = client.post("/Movies/movies", json=movie_data, headers={"Authorization": f"Bearer {token}"})
    assert create_movie_response.status_code == 201
    movie_id = create_movie_response.json()["id"]

    # Create a rating for the movie
    rating_data = {"rating": 7}
    create_rating_response = client.post(
        f"/Ratings/movies/{movie_id}/ratings/",
        json=rating_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert create_rating_response.status_code == 200
    rating_id = create_rating_response.json()["id"]

    # Attempt to update the rating with an invalid value
    update_data = {"rating": invalid_rating_value}
    update_rating_response = client.put(
        f"Ratings/ratings/{rating_id}",
        json=update_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert update_rating_response.status_code == 400
    assert update_rating_response.json() == {"detail": "Ratings of a movie must not be less than 1 and greater than 10"}



# TESTING FOR DELETE RATING ENDPOINT
@pytest.mark.parametrize("movie_data, rating_data", [
    (
        {"title": "Test Movie", "director": "Director", "genre": "Drama", "release_year": 2023},
        {"rating": 7}
    )
])
def test_delete_rating_success(client, setup_db, movie_data, rating_data):
    # Create a user and log in
    user_data = {
        "username": "testuser",
        "full_name": "Test User",
        "phone_number": "867585744",
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

    # Create a rating for the movie
    create_rating_response = client.post(
        f"/Ratings/movies/{movie_id}/ratings/",
        json=rating_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert create_rating_response.status_code == 200
    rating_id = create_rating_response.json()["id"]

    # Delete the rating
    delete_rating_response = client.delete(
        f"/Ratings/ratings/{rating_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert delete_rating_response.status_code == 200
    deleted_rating = delete_rating_response.json()
    assert deleted_rating["id"] == rating_id

# Testing to Check unauthorized or Non-existent Delete Rating
@pytest.mark.parametrize("rating_id", [9345])
def test_delete_rating_not_found(client, setup_db, rating_id):
    # Create a user and log in
    user_data = {
        "username": "testuser",
        "full_name": "Test User",
        "phone_number": "088875757",
        "password": "testpassword"
    }
    client.post("/Users/user/", json=user_data)
    login_response = client.post("/login", data={"username": "testuser", "password": "testpassword"})
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    # Attempting to delete a non-existent or unauthorized rating
    delete_rating_response = client.delete(
        f"/Ratings/ratings/{rating_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert delete_rating_response.status_code == 404
    assert delete_rating_response.json() == {"detail": "Rating not found or not authorized"}

    