# Admin Endpoints Test Plan

This document outlines a comprehensive test plan for the admin endpoints in `backend/app/api/v1/endpoints/admin.py`.

## Overview

The admin endpoints provide administrative functionality for managing users and posts. There are 5 endpoints:

1. `GET /admin/stats` - Get detailed admin statistics
2. `GET /admin/users` - List all users with pagination
3. `DELETE /admin/users/{user_id}` - Delete any user
4. `GET /admin/posts` - List all posts with pagination
5. `DELETE /admin/posts/{post_id}` - Delete any post

All endpoints require admin authentication via the `get_admin_user` dependency.

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

1. `backend/app/tests/unit/test_admin.py` - Unit tests for admin endpoints
2. `backend/app/tests/integration/test_admin.py` - Integration tests for admin endpoints

## Detailed Test Cases

### 1. GET /admin/stats - Get detailed admin statistics

#### Unit Tests

**test_get_admin_statistics_success**
- Mock `stat_crud.get_site_stats` to return sample statistics
- Mock `get_admin_user` dependency to return a mock admin user
- Call the endpoint
- Verify:
  - Response status code is 200
  - Response contains expected statistics fields
  - `stat_crud.get_site_stats` was called with correct parameters

**test_get_admin_statistics_db_error**
- Mock `stat_crud.get_site_stats` to raise an exception
- Mock `get_admin_user` dependency to return a mock admin user
- Call the endpoint
- Verify:
  - Appropriate error response is returned
  - Exception is handled properly

#### Integration Tests

**test_get_admin_statistics_success**
- Create a test admin user with admin role
- Generate a valid JWT token for the admin user
- Call the endpoint with valid authorization header
- Verify:
  - Response status code is 200
  - Response contains expected statistics fields
  - Values are reasonable (e.g., non-negative)

**test_get_admin_statistics_non_admin_forbidden**
- Create a test user without admin role
- Generate a valid JWT token for the non-admin user
- Call the endpoint with valid authorization header
- Verify:
  - Response status code is 403 (Forbidden)
  - Error message indicates admin privileges required

**test_get_admin_statistics_unauthorized**
- Call the endpoint without authorization header
- Verify:
  - Response status code is 401 (Unauthorized)
  - Error message indicates credentials validation failure

### 2. GET /admin/users - List all users with pagination

#### Unit Tests

**test_list_all_users_success**
- Mock `user_crud.get_multi_user` to return sample users
- Mock `get_admin_user` dependency to return a mock admin user
- Call the endpoint with default pagination parameters
- Verify:
  - Response status code is 200
  - Response contains expected user list with pagination info
  - `user_crud.get_multi_user` was called with correct parameters

**test_list_all_users_with_pagination**
- Mock `user_crud.get_multi_user` to return sample users
- Mock `get_admin_user` dependency to return a mock admin user
- Call the endpoint with custom skip and limit parameters
- Verify:
  - Response status code is 200
  - Response contains expected user list with correct pagination info
  - `user_crud.get_multi_user` was called with correct skip/limit parameters

**test_list_all_users_empty_result**
- Mock `user_crud.get_multi_user` to return empty list
- Mock `get_admin_user` dependency to return a mock admin user
- Call the endpoint
- Verify:
  - Response status code is 200
  - Response contains empty user list with correct pagination info

#### Integration Tests

**test_list_all_users_success**
- Create a test admin user with admin role
- Create several test users
- Generate a valid JWT token for the admin user
- Call the endpoint with valid authorization header
- Verify:
  - Response status code is 200
  - Response contains expected user list with pagination info
  - All created users are in the response

**test_list_all_users_with_pagination**
- Create a test admin user with admin role
- Create several test users (more than default limit)
- Generate a valid JWT token for the admin user
- Call the endpoint with custom skip and limit parameters
- Verify:
  - Response status code is 200
  - Response contains expected user list with correct pagination info
  - Pagination works correctly (correct page, size, total)

**test_list_all_users_non_admin_forbidden**
- Create a test user without admin role
- Generate a valid JWT token for the non-admin user
- Call the endpoint with valid authorization header
- Verify:
  - Response status code is 403 (Forbidden)
  - Error message indicates admin privileges required

**test_list_all_users_unauthorized**
- Call the endpoint without authorization header
- Verify:
  - Response status code is 401 (Unauthorized)
  - Error message indicates credentials validation failure

### 3. DELETE /admin/users/{user_id} - Delete any user

#### Unit Tests

**test_delete_any_user_success**
- Mock `user_crud.get_user_by_id` to return a mock user
- Mock `user_crud.delete_user` to return True
- Mock `get_admin_user` dependency to return a mock admin user
- Call the endpoint with a valid user ID
- Verify:
  - Response status code is 204 (No Content)
  - `user_crud.get_user_by_id` was called with correct parameters
  - `user_crud.delete_user` was called with correct parameters

**test_delete_any_user_not_found**
- Mock `user_crud.get_user_by_id` to return None
- Mock `get_admin_user` dependency to return a mock admin user
- Call the endpoint with a non-existent user ID
- Verify:
  - Response status code is 404 (Not Found)
  - Error message indicates user not found

**test_delete_any_user_db_error**
- Mock `user_crud.get_user_by_id` to return a mock user
- Mock `user_crud.delete_user` to return False
- Mock `get_admin_user` dependency to return a mock admin user
- Call the endpoint with a valid user ID
- Verify:
  - Response status code is 404 (Not Found)
  - Error message indicates user not found

**test_delete_any_user_self_deletion_forbidden**
- Mock `user_crud.get_user_by_id` to return a mock user with same ID as admin
- Mock `get_admin_user` dependency to return a mock admin user with same ID
- Call the endpoint with the admin user's own ID
- Verify:
  - Response status code is 400 (Bad Request)
  - Error message indicates user cannot delete themselves

#### Integration Tests

**test_delete_any_user_success**
- Create a test admin user with admin role
- Create another test user to be deleted
- Generate a valid JWT token for the admin user
- Call the endpoint with the user ID to be deleted
- Verify:
  - Response status code is 204 (No Content)
  - User is actually deleted from database

**test_delete_any_user_not_found**
- Create a test admin user with admin role
- Generate a valid JWT token for the admin user
- Call the endpoint with a non-existent user ID
- Verify:
  - Response status code is 404 (Not Found)
  - Error message indicates user not found

**test_delete_any_user_self_deletion_forbidden**
- Create a test admin user with admin role
- Generate a valid JWT token for the admin user
- Call the endpoint with the admin user's own ID
- Verify:
  - Response status code is 400 (Bad Request)
  - Error message indicates user cannot delete themselves

**test_delete_any_user_non_admin_forbidden**
- Create two test users (neither with admin role)
- Generate a valid JWT token for the first user
- Call the endpoint with the second user's ID
- Verify:
  - Response status code is 403 (Forbidden)
  - Error message indicates admin privileges required

**test_delete_any_user_unauthorized**
- Create a test user
- Call the endpoint with the user ID without authorization header
- Verify:
  - Response status code is 401 (Unauthorized)
  - Error message indicates credentials validation failure

### 4. GET /admin/posts - List all posts with pagination

#### Unit Tests

**test_list_all_posts_success**
- Mock database execute to return sample posts with relationships
- Mock `get_admin_user` dependency to return a mock admin user
- Call the endpoint with default pagination parameters
- Verify:
  - Response status code is 200
  - Response contains expected post list with pagination info
  - Database execute was called with correct query

**test_list_all_posts_with_pagination**
- Mock database execute to return sample posts with relationships
- Mock `get_admin_user` dependency to return a mock admin user
- Call the endpoint with custom skip and limit parameters
- Verify:
  - Response status code is 200
  - Response contains expected post list with correct pagination info
  - Database execute was called with correct query and pagination

**test_list_all_posts_empty_result**
- Mock database execute to return empty result
- Mock `get_admin_user` dependency to return a mock admin user
- Call the endpoint
- Verify:
  - Response status code is 200
  - Response contains empty post list with correct pagination info

#### Integration Tests

**test_list_all_posts_success**
- Create a test admin user with admin role
- Create several test posts
- Generate a valid JWT token for the admin user
- Call the endpoint with valid authorization header
- Verify:
  - Response status code is 200
  - Response contains expected post list with pagination info
  - All created posts are in the response

**test_list_all_posts_with_pagination**
- Create a test admin user with admin role
- Create several test posts (more than default limit)
- Generate a valid JWT token for the admin user
- Call the endpoint with custom skip and limit parameters
- Verify:
  - Response status code is 200
  - Response contains expected post list with correct pagination info
  - Pagination works correctly (correct page, size, total)

**test_list_all_posts_non_admin_forbidden**
- Create a test user without admin role
- Generate a valid JWT token for the non-admin user
- Call the endpoint with valid authorization header
- Verify:
  - Response status code is 403 (Forbidden)
  - Error message indicates admin privileges required

**test_list_all_posts_unauthorized**
- Call the endpoint without authorization header
- Verify:
  - Response status code is 401 (Unauthorized)
  - Error message indicates credentials validation failure

### 5. DELETE /admin/posts/{post_id} - Delete any post

#### Unit Tests

**test_delete_any_post_success**
- Mock `post_crud.get_post_by_id` to return a mock post
- Mock `post_crud.delete_post` to return True
- Mock `get_admin_user` dependency to return a mock admin user
- Call the endpoint with a valid post ID
- Verify:
  - Response status code is 204 (No Content)
  - `post_crud.get_post_by_id` was called with correct parameters
  - `post_crud.delete_post` was called with correct parameters

**test_delete_any_post_not_found**
- Mock `post_crud.get_post_by_id` to return None
- Mock `get_admin_user` dependency to return a mock admin user
- Call the endpoint with a non-existent post ID
- Verify:
  - Response status code is 404 (Not Found)
  - Error message indicates post not found

**test_delete_any_post_db_error**
- Mock `post_crud.get_post_by_id` to return a mock post
- Mock `post_crud.delete_post` to return False
- Mock `get_admin_user` dependency to return a mock admin user
- Call the endpoint with a valid post ID
- Verify:
  - Response status code is 404 (Not Found)
  - Error message indicates post not found

#### Integration Tests

**test_delete_any_post_success**
- Create a test admin user with admin role
- Create a test post to be deleted
- Generate a valid JWT token for the admin user
- Call the endpoint with the post ID to be deleted
- Verify:
  - Response status code is 204 (No Content)
  - Post is actually deleted from database

**test_delete_any_post_not_found**
- Create a test admin user with admin role
- Generate a valid JWT token for the admin user
- Call the endpoint with a non-existent post ID
- Verify:
  - Response status code is 404 (Not Found)
  - Error message indicates post not found

**test_delete_any_post_non_admin_forbidden**
- Create a test user without admin role
- Create a test post
- Generate a valid JWT token for the non-admin user
- Call the endpoint with the post ID
- Verify:
  - Response status code is 403 (Forbidden)
  - Error message indicates admin privileges required

**test_delete_any_post_unauthorized**
- Create a test post
- Call the endpoint with the post ID without authorization header
- Verify:
  - Response status code is 401 (Unauthorized)
  - Error message indicates credentials validation failure

## Test Data and Fixtures

### Required Test Data

1. **Admin User Fixture**
   - User with admin role for testing admin endpoints
   - Valid JWT token for admin user

2. **Regular User Fixture**
   - User without admin role for testing permission restrictions
   - Valid JWT token for regular user

3. **Sample Users**
   - Multiple users for testing pagination in user listing

4. **Sample Posts**
   - Multiple posts for testing pagination in post listing
   - Posts with various relationships (author, category, tags, etc.)

5. **Test Database Session**
   - Mock database session for unit tests
   - Real database session for integration tests (if needed)

### Mocking Strategies

1. **Database Operations**
   - Mock CRUD functions for unit tests
   - Use `unittest.mock.patch` to mock specific functions
   - For SQLAlchemy operations, mock the `execute` method on database sessions

2. **Dependencies**
   - Mock `get_admin_user` dependency to return test users
   - Mock `get_session` dependency to return mock database sessions

3. **External Services**
   - Mock JWT token decoding in security functions if needed
   - Mock any file system operations if required

## Expected Responses and Status Codes

### Success Responses

1. `GET /admin/stats` - 200 OK with `AdminStatsRead` object
2. `GET /admin/users` - 200 OK with `UserListRead` object
3. `DELETE /admin/users/{user_id}` - 204 No Content
4. `GET /admin/posts` - 200 OK with `PostListRead` object
5. `DELETE /admin/posts/{post_id}` - 204 No Content

### Error Responses

1. **401 Unauthorized**
   - Missing or invalid JWT token
   - Invalid credentials

2. **403 Forbidden**
   - User does not have admin role
   - Access forbidden due to insufficient privileges

3. **404 Not Found**
   - User or post not found when trying to delete
   - Invalid user_id or post_id

4. **400 Bad Request**
   - User trying to delete themselves

## Test Execution

### Unit Tests
- Run with: `pytest backend/app/tests/unit/test_admin.py`
- Focus on testing individual functions in isolation
- Use mocking to simulate database and external dependencies

### Integration Tests
- Run with: `pytest backend/app/tests/integration/test_admin.py`
- Test complete endpoint workflows
- May require a test database depending on implementation

## Implementation Notes

1. **Test File Structure**
   - Follow the existing pattern in `test_media.py` for both unit and integration tests
   - Use `@pytest.mark.asyncio` for async test functions
   - Use `TestClient` from `fastapi.testclient` for integration tests

2. **Mocking Approach**
   - Use `unittest.mock.patch` to mock specific functions
   - Mock at the level of CRUD functions rather than database sessions where possible
   - Use `AsyncMock` for async functions

3. **Test Data Generation**
   - Create helper functions to generate test users, posts, etc.
   - Use `uuid.uuid4()` for generating unique IDs
   - Ensure test data matches the expected schemas

4. **Authentication in Tests**
   - Create helper functions to generate JWT tokens for test users
   - Use the same SECRET_KEY as in the application settings
   - Follow the same token structure as the real application

5. **Database Considerations**
   - For unit tests, fully mock database operations
   - For integration tests, either use a separate test database or fully mock as well
   - Ensure tests don't affect the development or production databases