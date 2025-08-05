# Users Endpoints Test Plan

This document outlines a comprehensive test plan for the users endpoints in `backend/app/api/v1/endpoints/users.py`.

## Overview

The users endpoints provide CRUD functionality for managing users, as well as retrieving posts and comments associated with specific users. There are 7 endpoints:

1. `POST /users/` - Create a new user
2. `GET /users/` - Retrieve users with pagination
3. `GET /users/{user_id}` - Get a specific user by id
4. `PATCH /users/{user_id}` - Update a user
5. `DELETE /users/{user_id}` - Delete a user
6. `GET /users/{user_id}/posts` - Get all posts by a specific user
7. `GET /users/{user_id}/comments` - Get all comments by a specific user

## Test Structure

Following the existing patterns in the codebase:
- Unit tests in `backend/app/tests/unit/`
- Integration tests in `backend/app/tests/integration/`
- Use pytest with pytest-asyncio for async support
- Separate unit and integration tests
- Use mocking for database operations in unit tests
- Use TestClient for integration tests
- Follow existing naming conventions

## Test Files to Create

1. `backend/app/tests/unit/test_users.py` - Unit tests for users endpoints
2. `backend/app/tests/integration/test_users.py` - Integration tests for users endpoints

## Detailed Test Cases

### 1. POST /users/ - Create a new user

#### Unit Tests

**test_create_user_success**
- Mock `user_crud.get_user_by_email` to return None (no existing user)
- Mock `user_crud.create_user` to return a mock user
- Call the endpoint with valid user data
- Verify:
  - Response status code is 201
  - Response contains user data matching the mock user
  - `user_crud.get_user_by_email` was called with correct parameters
  - `user_crud.create_user` was called with correct parameters

**test_create_user_duplicate_email**
- Mock `user_crud.get_user_by_email` to return an existing user
- Call the endpoint with user data that conflicts with existing user
- Verify:
  - Response status code is 400
  - Error message indicates user with this email already exists
  - `user_crud.create_user` was not called

**test_create_user_invalid_data**
- Call the endpoint with invalid user data
- Verify:
  - Response status code is 422
  - Error message indicates validation errors
  - `user_crud.get_user_by_email` and `user_crud.create_user` were not called

#### Integration Tests

**test_create_user_success**
- Call the endpoint with valid user data
- Verify:
  - Response status code is 201
  - Response contains user data matching the input
  - User is actually stored in the database
  - Password is properly hashed

**test_create_user_duplicate_email**
- Create a user in the database
- Call the endpoint with user data that has the same email as the existing user
- Verify:
  - Response status code is 400
  - Error message indicates user with this email already exists

### 2. GET /users/ - Retrieve users with pagination

#### Unit Tests

**test_read_users_success**
- Mock `user_crud.get_multi_user` to return a list of mock users
- Call the endpoint with skip and limit parameters
- Verify:
  - Response status code is 200
  - Response contains correct number of users based on pagination
  - `user_crud.get_multi_user` was called with correct parameters

**test_read_users_empty**
- Mock `user_crud.get_multi_user` to return an empty list
- Call the endpoint
- Verify:
  - Response status code is 200
  - Response contains an empty list

#### Integration Tests

**test_read_users_success**
- Create multiple users in the database
- Call the endpoint with skip and limit parameters
- Verify:
  - Response status code is 200
  - Response contains correct number of users based on pagination
  - Users match those stored in the database

**test_read_users_empty**
- Call the endpoint when no users exist in the database
- Verify:
  - Response status code is 200
  - Response contains an empty list

### 3. GET /users/{user_id} - Get a specific user by id

#### Unit Tests

**test_read_user_by_id_success**
- Mock `user_crud.get_user` to return a mock user
- Call the endpoint with a valid user_id
- Verify:
  - Response status code is 200
  - Response contains user data matching the mock user
  - `user_crud.get_user` was called with correct parameters

**test_read_user_by_id_not_found**
- Mock `user_crud.get_user` to return None
- Call the endpoint with a non-existent user_id
- Verify:
  - Response status code is 404
  - Error message indicates "User not found"
  - `user_crud.get_user` was called with correct parameters

#### Integration Tests

**test_read_user_by_id_success**
- Create a user in the database
- Call the endpoint with the user's ID
- Verify:
  - Response status code is 200
  - Response contains user data matching what was stored
  - All required fields are present in the response
  - Password field is not included in the response

**test_read_user_by_id_not_found**
- Call the endpoint with a non-existent user ID
- Verify:
  - Response status code is 404
  - Error message indicates "User not found"

### 4. PATCH /users/{user_id} - Update a user

#### Unit Tests

**test_update_user_success**
- Mock `user_crud.get_user` to return an existing mock user
- Mock `user_crud.update_user` to return an updated mock user
- Call the endpoint with valid user update data
- Verify:
  - Response status code is 200
  - Response contains updated user data
  - `user_crud.get_user` was called with correct parameters
  - `user_crud.update_user` was called with correct parameters

**test_update_user_not_found**
- Mock `user_crud.get_user` to return None
- Call the endpoint with user update data
- Verify:
  - Response status code is 404
  - Error message indicates user not found
  - `user_crud.update_user` was not called

**test_update_user_invalid_data**
- Mock `user_crud.get_user` to return an existing mock user
- Call the endpoint with invalid update data
- Verify:
  - Response status code is 422
  - Error message indicates validation errors
  - `user_crud.update_user` was not called

#### Integration Tests

**test_update_user_success**
- Create a user in the database
- Call the endpoint with valid update data
- Verify:
  - Response status code is 200
  - Response contains updated user data
  - User data in database has been updated correctly

**test_update_user_not_found**
- Call the endpoint with update data and a non-existent user ID
- Verify:
  - Response status code is 404
  - Error message indicates user not found

**test_update_user_partial**
- Create a user in the database
- Call the endpoint with partial update data (only username, not email)
- Verify:
  - Response status code is 200
  - Response contains updated username but unchanged email
  - Only the specified field was updated in the database

### 5. DELETE /users/{user_id} - Delete a user

#### Unit Tests

**test_delete_user_success**
- Mock `user_crud.delete_user` to return True
- Call the endpoint with a valid user_id
- Verify:
  - Response status code is 204
  - Response body is empty
  - `user_crud.delete_user` was called with correct parameters

**test_delete_user_not_found**
- Mock `user_crud.delete_user` to return False
- Call the endpoint with a non-existent user_id
- Verify:
  - Response status code is 404
  - Error message indicates "User not found"

#### Integration Tests

**test_delete_user_success**
- Create a user in the database
- Call the endpoint with the user's ID
- Verify:
  - Response status code is 204
  - Response body is empty
  - User no longer exists in the database

**test_delete_user_not_found**
- Call the endpoint with a non-existent user ID
- Verify:
  - Response status code is 404
  - Error message indicates "User not found"

### 6. GET /users/{user_id}/posts - Get all posts by a specific user

#### Unit Tests

**test_get_user_posts_success**
- Mock `get_posts_by_author` to return a list of mock posts
- Call the endpoint with a valid user_id
- Verify:
  - Response status code is 200
  - Response contains list of posts by the user
  - `get_posts_by_author` was called with correct parameters

**test_get_user_posts_empty**
- Mock `get_posts_by_author` to return an empty list
- Call the endpoint with a valid user_id
- Verify:
  - Response status code is 200
  - Response contains an empty list

#### Integration Tests

**test_get_user_posts_success**
- Create a user and posts by that user in the database
- Call the endpoint with the user's ID
- Verify:
  - Response status code is 200
  - Response contains list of posts by the user
  - All posts in response actually belong to the specified user

**test_get_user_posts_empty**
- Create a user but no posts by that user in the database
- Call the endpoint with the user's ID
- Verify:
  - Response status code is 200
  - Response contains an empty list

### 7. GET /users/{user_id}/comments - Get all comments by a specific user

#### Unit Tests

**test_get_user_comments_success**
- Mock `get_comments_by_user` to return a list of mock comments
- Call the endpoint with a valid user_id
- Verify:
  - Response status code is 200
  - Response contains list of comments by the user
  - `get_comments_by_user` was called with correct parameters

**test_get_user_comments_empty**
- Mock `get_comments_by_user` to return an empty list
- Call the endpoint with a valid user_id
- Verify:
  - Response status code is 200
  - Response contains an empty list

#### Integration Tests

**test_get_user_comments_success**
- Create a user and comments by that user in the database
- Call the endpoint with the user's ID
- Verify:
  - Response status code is 200
  - Response contains list of comments by the user
  - All comments in response actually belong to the specified user

**test_get_user_comments_empty**
- Create a user but no comments by that user in the database
- Call the endpoint with the user's ID
- Verify:
  - Response status code is 200
  - Response contains an empty list

## Test Data and Fixtures

### Required Test Data

1. **Test Users Fixture**
   - Users with username, email, and password for testing user operations
   - Valid user data that matches the User model schema

2. **Test Posts Fixture**
   - Posts associated with users for testing the get user posts endpoint
   - Posts with various authors for comprehensive testing

3. **Test Comments Fixture**
   - Comments associated with users for testing the get user comments endpoint
   - Comments with various authors for comprehensive testing

4. **Test Database Session**
   - Mock database session for unit tests
   - Real database session for integration tests (if needed)

### Mocking Strategies

1. **Database Operations**
   - Mock `user_crud.get_user_by_email` function for user creation
   - Mock `user_crud.get_user` function for user retrieval and update
   - Mock `user_crud.create_user` function for user creation
   - Mock `user_crud.get_multi_user` function for user listing
   - Mock `user_crud.update_user` function for user update
   - Mock `user_crud.delete_user` function for user deletion
   - Mock `get_posts_by_author` function for getting posts by user
   - Mock `get_comments_by_user` function for getting comments by user
   - Use `unittest.mock.patch` to mock specific CRUD functions

2. **Dependencies**
   - Mock `get_session` dependency to return mock database sessions
   - Mock password hashing functions if needed

## Expected Responses and Status Codes

### Success Responses

1. `POST /users/` - 201 Created with `UserRead` object
2. `GET /users/` - 200 OK with list of `UserRead` objects
3. `GET /users/{user_id}` - 200 OK with `UserRead` object
4. `PATCH /users/{user_id}` - 200 OK with `UserRead` object
5. `DELETE /users/{user_id}` - 204 No Content with empty response body
6. `GET /users/{user_id}/posts` - 200 OK with list of `PostRead` objects
7. `GET /users/{user_id}/comments` - 200 OK with list of `CommentRead` objects

### Error Responses

1. **400 Bad Request**
   - User with this email already exists during creation

2. **404 Not Found**
   - User not found when retrieving, updating, or deleting by ID
   - User not found when getting posts or comments by user

3. **422 Unprocessable Entity**
   - Validation errors in user data
   - Missing required fields in request body

## Test Execution

### Unit Tests
- Run with: `pytest backend/app/tests/unit/test_users.py`
- Focus on testing individual functions in isolation
- Use mocking to simulate database and external dependencies

### Integration Tests
- Run with: `pytest backend/app/tests/integration/test_users.py`
- Test complete endpoint workflows
- May require a test database depending on implementation

## Implementation Notes

1. **Test File Structure**
   - Follow the existing pattern in `test_media.py` for both unit and integration tests
   - Use `@pytest.mark.asyncio` for async test functions
   - Use `TestClient` from `fastapi.testclient` for integration tests

2. **Mocking Approach**
   - Use `unittest.mock.patch` to mock specific CRUD functions
   - Mock at the level of CRUD functions rather than database sessions where possible
   - Use `AsyncMock` for async functions

3. **Test Data Generation**
   - Create helper functions to generate test users, posts, and comments
   - Use `uuid.uuid4()` for generating unique IDs
   - Ensure test data matches the expected schemas

4. **Database Considerations**
   - For unit tests, fully mock database operations
   - For integration tests, either use a separate test database or fully mock as well
   - Ensure tests don't affect the development or production databases

5. **Security Considerations**
   - Follow security best practices in tests (don't hardcode sensitive data)
   - Test both positive and negative security scenarios
   - Ensure error messages don't leak sensitive information
   - Verify that passwords are properly hashed and not exposed in responses