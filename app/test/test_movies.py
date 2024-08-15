import pytest



@pytest.mark.parametrize("username, full_name, phone_number, password", 
                         [("newuser1", "newName1", "0901999444", "newpassword1")])
def test_create_movie(client, setup_db, username, full_name, phone_number, password):
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
    token = response.json()["access_token"]
   
    # Then, listing a movie
    movie_data = {
        "title": "NewMovie", "director": "new director", "genre": "Action", "release_year": "2024"
    }
    response = client.post("/Movies/movies", json= movie_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code ==201
    data = response.json()
    assert data["title"] =="NewMovie"
    assert data["director"] == "new director"
    assert data["genre"] == "Action"


# Test for get_movies endpoint
@pytest.mark.parametrize("title",  [("somemovies"),])
def test_get_users(client, setup_db, title):
    response = client.get(f"/Movies/movies/")
    assert response.status_code == 200
    data = response.json()
    response_data = data[0]


# Test for get_a_movie by id endpoint
@pytest.mark.parametrize("username, full_name, phone_number, password", 
                         [("newuser21", "newName1", "09019994448", "newpassword1")])
def test_get_movie(client, setup_db, username, full_name, phone_number, password):
    # Signing up a user
    new_user_data = {
        "username": username,
        "full_name": full_name,
        "phone_number": phone_number,
        "password": password
    }
    response = client.post("/Users/user/", json=new_user_data)
    assert response.status_code == 201

    # Login the user
    response = client.post("/login", data={"username": username, "password": password})
    assert response.status_code == 200
    token = response.json()["access_token"]

    # Create a movie
    new_movie_data = {
        "title": "NewMovie1", "director": "new director", "genre": "Action", "release_year": "2023"
    }
    response = client.post("/Movies/movies", json=new_movie_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "NewMovie1"
    assert data["director"] == "new director"
    assert data["genre"] == "Action"

    # get a movie by id
    movie_id = data["id"]
    response = client.get(f"/Movies/movie/{movie_id}") 
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["title"] == "NewMovie1"
    assert response_data["director"] == "new director"
    assert response_data["genre"] == "Action"

# Testing movie id not found
@pytest.mark.parametrize("movie_id", [13, 25, 49])
def test_get_movie_not_found(client, setup_db, movie_id):
    response = client.get(f"/Movies/movie/{movie_id}")
    
    assert response.status_code == 404
    assert response.json() == {"detail": "Movie not found"}


# Test for Update a Movie
@pytest.mark.parametrize("movie_data, update_data", [
    (
        {"title": "Old Title", "director": "Old Director", "genre": "Action", "release_year": 2023},
        {"title": "Updated Title", "director": "Updated Director", "genre": "Drama", "release_year": 2025}
    )
])
def test_update_movie(client, setup_db, movie_data, update_data):
    # Create a user and log in
    user_data = {
        "username": "testuser",
        "full_name": "Test User",
        "phone_number": "1234567890",
        "password": "testpassword"
    }
    client.post("/Users/user/", json=user_data)
    login_response = client.post("/login", data={"username": "testuser", "password": "testpassword"})
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    # Create a movie
    create_response = client.post("/Movies/movies", json=movie_data, headers={"Authorization": f"Bearer {token}"})
    assert create_response.status_code == 201
    movie_id = create_response.json()["id"]

    # Update the movie
    response = client.put(
        f"/Movies/movies/{movie_id}",
        json=update_data,
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    updated_movie = response.json()
    assert updated_movie["title"] == update_data["title"]
    assert updated_movie["director"] == update_data["director"]
    assert updated_movie["genre"] == update_data["genre"]
    assert updated_movie["release_year"] == update_data["release_year"]

# Testing for movie not found
@pytest.mark.parametrize("movie_id", [109]) 
def test_update_movie_not_found(client, setup_db, movie_id):

    user_data = {
        "username": "testuser",
        "full_name": "Test User",
        "phone_number": "1234567890",
        "password": "testpassword"
    }
    client.post("/Users/user/", json=user_data)
    login_response = client.post("/login", data={"username": "testuser", "password": "testpassword"})
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    # Sample update data
    update_data = {
        "title": "Updated Title",
        "director": "Updated Director",
        "genre": "Drama",
        "release_year": 2025
    }

    response = client.put(
        f"/Movies/movies/{movie_id}",
        json=update_data,
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Movie not found or not authorized"}



# Testing for Delete endpoint
@pytest.mark.parametrize("movie_data", [
    {"title": "Movie to Delete", "director": "Some Director", "genre": "Comedy", "release_year": 2023}
])
def test_delete_movie(client, setup_db, movie_data):
    # Create a user and log in
    user_data = {
        "username": "testuser",
        "full_name": "Test User",
        "phone_number": "1234567890",
        "password": "testpassword"
    }
    client.post("/Users/user/", json=user_data)
    login_response = client.post("/login", data={"username": "testuser", "password": "testpassword"})
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    # Create a movie
    create_response = client.post("/Movies/movies", json=movie_data, headers={"Authorization": f"Bearer {token}"})
    assert create_response.status_code == 201
    movie_id = create_response.json()["id"]

    # Delete the movie
    delete_response = client.delete(f"/Movies/movies/{movie_id}", headers={"Authorization": f"Bearer {token}"})
    assert delete_response.status_code == 200
    deleted_movie = delete_response.json()
    assert deleted_movie["title"] == movie_data["title"]
    assert deleted_movie["director"] == movie_data["director"]
    assert deleted_movie["genre"] == movie_data["genre"]
    assert deleted_movie["release_year"] == movie_data["release_year"]
 
# Test delete movie not found
@pytest.mark.parametrize("movie_id", [111]) 
def test_delete_movie_not_found(client, setup_db, movie_id):
  
    user_data = {
        "username": "testuser",
        "full_name": "Test User",
        "phone_number": "1234567890",
        "password": "testpassword"
    }
    client.post("/Users/user/", json=user_data)
    login_response = client.post("/login", data={"username": "testuser", "password": "testpassword"})
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    # Attempt to delete a non-existent movie
    response = client.delete(f"/Movies/movies/{movie_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Movie not found or not authorized"}
