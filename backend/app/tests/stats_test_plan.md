# Stats Endpoints Test Plan

This document outlines a comprehensive test plan for the stats endpoints in `backend/app/api/v1/endpoints/stats.py`.

## Overview

The stats endpoints provide functionality for retrieving and recording statistics for posts, users, and the site. There are 6 endpoints:

1. `GET /stats/posts/{post_id}` - Get statistics for a specific post
2. `GET /stats/users/{user_id}` - Get statistics for a specific user
3. `GET /stats/site` - Get overall site statistics
4. `POST /stats/posts/{post_id}/view` - Record a post view
5. `POST /stats/posts/{post_id}/like` - Record a post like
6. `DELETE /stats/posts/{post_id}/like` - Remove a post like

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

1. `backend/app/tests/unit/test_stats.py` - Unit tests for stats endpoints
2. `backend/app/tests/integration/test_stats.py` - Integration tests for stats endpoints

## Detailed Test Cases

### 1. GET /stats/posts/{post_id} - Get statistics for a specific post

#### Unit Tests

**test_get_post_statistics_success**
- Mock `stat_crud.get_stat_by_post_id` to return a mock stat object
- Call the endpoint with a valid post_id
- Verify:
  - Response status code is 200
  - Response contains post_id, views, and likes matching the mock data
  - `stat_crud.get_stat_by_post_id` was called with correct parameters

**test_get_post_statistics_not_found**
- Mock `stat_crud.get_stat_by_post_id` to raise HTTPException with 404 status
- Call the endpoint with a non-existent post_id
- Verify:
  - Response status code is 404
  - Error message indicates post not found

#### Integration Tests

**test_get_post_statistics_success**
- Create a test post and its associated statistics in the database
- Call the endpoint with the post's ID
- Verify:
  - Response status code is 200
  - Response contains correct post_id, views, and likes
  - Values match what was stored in the database

**test_get_post_statistics_not_found**
- Call the endpoint with a non-existent post ID
- Verify:
  - Response status code is 404
  - Error message indicates post not found

### 2. GET /stats/users/{user_id} - Get statistics for a specific user

#### Unit Tests

**test_get_user_statistics_success**
- Mock `stat_crud.get_user_stats` to return mock user statistics
- Call the endpoint with a valid user_id
- Verify:
  - Response status code is 200
  - Response contains user statistics matching the mock data
  - `stat_crud.get_user_stats` was called with correct parameters

**test_get_user_statistics_not_found**
- Mock `stat_crud.get_user_stats` to raise HTTPException with 404 status
- Call the endpoint with a non-existent user_id
- Verify:
  - Response status code is 404
  - Error message indicates user not found

#### Integration Tests

**test_get_user_statistics_success**
- Create a test user and associated statistics in the database
- Call the endpoint with the user's ID
- Verify:
  - Response status code is 200
  - Response contains correct user statistics
  - Values match what was stored in the database

**test_get_user_statistics_not_found**
- Call the endpoint with a non-existent user ID
- Verify:
  - Response status code is 404
  - Error message indicates user not found

### 3. GET /stats/site - Get overall site statistics

#### Unit Tests

**test_get_site_statistics_success**
- Mock `stat_crud.get_site_stats` to return mock site statistics
- Call the endpoint
- Verify:
  - Response status code is 200
  - Response contains site statistics matching the mock data
  - `stat_crud.get_site_stats` was called

#### Integration Tests

**test_get_site_statistics_success**
- Create test data in the database (posts, users, etc.)
- Call the endpoint
- Verify:
  - Response status code is 200
  - Response contains correct site statistics
  - Values match what was calculated from the database

### 4. POST /stats/posts/{post_id}/view - Record a post view

#### Unit Tests

**test_record_post_view_success**
- Mock `stat_crud.increment_post_views` to return a mock stat object with incremented views
- Call the endpoint with a valid post_id
- Verify:
  - Response status code is 201
  - Response contains success message and updated views count
  - `stat_crud.increment_post_views` was called with correct parameters

**test_record_post_view_not_found**
- Mock `stat_crud.increment_post_views` to raise HTTPException with 404 status
- Call the endpoint with a non-existent post_id
- Verify:
  - Response status code is 404
  - Error message indicates post not found

#### Integration Tests

**test_record_post_view_success**
- Create a test post with initial statistics in the database
- Call the endpoint with the post's ID
- Verify:
  - Response status code is 201
  - Response contains success message and updated views count
  - Views count in database has been incremented by 1

**test_record_post_view_not_found**
- Call the endpoint with a non-existent post ID
- Verify:
  - Response status code is 404
  - Error message indicates post not found

### 5. POST /stats/posts/{post_id}/like - Record a post like

#### Unit Tests

**test_record_post_like_success**
- Mock `stat_crud.increment_post_likes` to return a mock stat object with incremented likes
- Call the endpoint with a valid post_id
- Verify:
  - Response status code is 201
  - Response contains success message and updated likes count
  - `stat_crud.increment_post_likes` was called with correct parameters

**test_record_post_like_not_found**
- Mock `stat_crud.increment_post_likes` to raise HTTPException with 404 status
- Call the endpoint with a non-existent post_id
- Verify:
  - Response status code is 404
  - Error message indicates post not found

#### Integration Tests

**test_record_post_like_success**
- Create a test post with initial statistics in the database
- Call the endpoint with the post's ID
- Verify:
  - Response status code is 201
  - Response contains success message and updated likes count
  - Likes count in database has been incremented by 1

**test_record_post_like_not_found**
- Call the endpoint with a non-existent post ID
- Verify:
  - Response status code is 404
  - Error message indicates post not found

### 6. DELETE /stats/posts/{post_id}/like - Remove a post like

#### Unit Tests

**test_remove_post_like_success**
- Mock `stat_crud.decrement_post_likes` to return a mock stat object with decremented likes
- Call the endpoint with a valid post_id
- Verify:
  - Response status code is 204
  - Response body is empty
  - `stat_crud.decrement_post_likes` was called with correct parameters

**test_remove_post_like_not_found**
- Mock `stat_crud.decrement_post_likes` to raise HTTPException with 404 status
- Call the endpoint with a non-existent post_id
- Verify:
  - Response status code is 404
  - Error message indicates post not found

#### Integration Tests

**test_remove_post_like_success**
- Create a test post with initial statistics (with at least one like) in the database
- Call the endpoint with the post's ID
- Verify:
  - Response status code is 204
  - Response body is empty
  - Likes count in database has been decremented by 1

**test_remove_post_like_not_found**
- Call the endpoint with a non-existent post ID
- Verify:
  - Response status code is 404
  - Error message indicates post not found

## Test Data and Fixtures

### Required Test Data

1. **Test Posts Fixture**
   - Posts with associated statistics for testing post stats endpoints
   - Posts with varying view and like counts

2. **Test Users Fixture**
   - Users with associated statistics for testing user stats endpoints

3. **Test Site Statistics Data**
   - Various entities in the database to calculate site statistics

4. **Test Database Session**
   - Mock database session for unit tests
   - Real database session for integration tests (if needed)

### Mocking Strategies

1. **Database Operations**
   - Mock `stat_crud.get_stat_by_post_id` function for post stats retrieval
   - Mock `stat_crud.get_user_stats` function for user stats retrieval
   - Mock `stat_crud.get_site_stats` function for site stats retrieval
   - Mock `stat_crud.increment_post_views` function for recording views
   - Mock `stat_crud.increment_post_likes` function for recording likes
   - Mock `stat_crud.decrement_post_likes` function for removing likes
   - Use `unittest.mock.patch` to mock specific CRUD functions

2. **Dependencies**
   - Mock `get_session` dependency to return mock database sessions

## Expected Responses and Status Codes

### Success Responses

1. `GET /stats/posts/{post_id}` - 200 OK with `PostStatsRead` object
2. `GET /stats/users/{user_id}` - 200 OK with `UserStatsRead` object
3. `GET /stats/site` - 200 OK with `SiteStatsRead` object
4. `POST /stats/posts/{post_id}/view` - 201 Created with success message and views count
5. `POST /stats/posts/{post_id}/like` - 201 Created with success message and likes count
6. `DELETE /stats/posts/{post_id}/like` - 204 No Content with empty response body

### Error Responses

1. **404 Not Found**
   - Post not found when retrieving or updating post statistics
   - User not found when retrieving user statistics

## Test Execution

### Unit Tests
- Run with: `pytest backend/app/tests/unit/test_stats.py`
- Focus on testing individual functions in isolation
- Use mocking to simulate database and external dependencies

### Integration Tests
- Run with: `pytest backend/app/tests/integration/test_stats.py`
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
   - Create helper functions to generate test entities and statistics
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