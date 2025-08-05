# Posts Endpoints Test Plan

This document outlines a comprehensive test plan for the posts endpoints in `backend/app/api/v1/endpoints/posts.py`.

## Overview

The posts endpoints provide CRUD functionality for managing blog posts. There are 7 endpoints:

1. `POST /` - Create a new post
2. `PUT /{post_id}` - Update an existing post
3. `DELETE /{post_id}` - Delete a post
4. `GET /drafts` - Retrieve draft posts (for authenticated users)
5. `GET /published` - Retrieve published posts
6. `POST /{post_id}/publish` - Publish a draft post
7. `POST /{post_id}/unpublish` - Unpublish a published post

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

1. `backend/app/tests/unit/test_posts.py` - Unit tests for posts endpoints
2. `backend/app/tests/integration/test_posts.py` - Integration tests for posts endpoints

## Detailed Test Cases

### 1. POST / - Create a new post

#### Unit Tests

**test_create_new_post_success**
- Mock `post_crud.create_post` to return a mock post
- Call the endpoint with valid post data
- Verify:
  - Response status code is 201
  - Response contains expected post data
  - `post_crud.create_post` was called with correct parameters

**test_create_new_post_db_error**
- Mock `post_crud.create_post` to raise an exception
- Call the endpoint with valid post data
- Verify:
  - Appropriate error response is returned
  - Exception is handled properly

**test_create_new_post_invalid_data**
- Call the endpoint with invalid post data (missing required fields)
- Verify:
  - Response status code is 422
  - Error message indicates validation errors

#### Integration Tests

**test_create_new_post_success**
- Create a test user and category
- Call the endpoint with valid post data
- Verify:
  - Response status code is 201
  - Response contains expected post data
  - Post is actually stored in database

**test_create_new_post_invalid_data**
- Call the endpoint with invalid post data (missing required fields)
- Verify:
  - Response status code is 422
  - Error message indicates validation errors

### 2. PUT /{post_id} - Update an existing post

#### Unit Tests

**test_update_existing_post_success**
- Mock `post_crud.get_post_by_id` to return a mock post
- Mock database session operations to simulate successful update
- Call the endpoint with valid post ID and update data
- Verify:
  - Response status code is 200
  - Response contains updated post data
  - `post_crud.get_post_by_id` was called with correct parameters
  - Database session methods were called with correct parameters

**test_update_existing_post_not_found**
- Mock `post_crud.get_post_by_id` to raise HTTPException (404)
- Call the endpoint with invalid post ID and update data
- Verify:
  - Response status code is 404
  - Error message indicates post not found

**test_update_existing_post_invalid_data**
- Mock `post_crud.get_post_by_id` to return a mock post
- Call the endpoint with valid post ID and invalid update data
- Verify:
  - Response status code is 422
  - Error message indicates validation errors

**test_update_existing_post_db_error**
- Mock `post_crud.get_post_by_id` to return a mock post
- Mock database session operations to raise an exception
- Call the endpoint with valid post ID and update data
- Verify:
  - Appropriate error response is returned
  - Exception is handled properly

#### Integration Tests

**test_update_existing_post_success**
- Create a test post
- Call the endpoint with the post ID and update data
- Verify:
  - Response status code is 200
  - Response contains updated post data
  - Post is actually updated in database

**test_update_existing_post_not_found**
- Call the endpoint with a non-existent post ID and update data
- Verify:
  - Response status code is 404
  - Error message indicates post not found

**test_update_existing_post_invalid_data**
- Create a test post
- Call the endpoint with the post ID and invalid update data
- Verify:
  - Response status code is 422
  - Error message indicates validation errors

### 3. DELETE /{post_id} - Delete a post

#### Unit Tests

**test_delete_post_by_id_success**
- Mock `post_crud.get_post_by_id` to return a mock post
- Mock database session operations to simulate successful deletion
- Call the endpoint with a valid post ID
- Verify:
  - Response status code is 204 (No Content)
  - `post_crud.get_post_by_id` was called with correct parameters
  - Database session delete and commit methods were called

**test_delete_post_by_id_not_found**
- Mock `post_crud.get_post_by_id` to raise HTTPException (404)
- Call the endpoint with a non-existent post ID
- Verify:
  - Response status code is 404
  - Error message indicates post not found

**test_delete_post_by_id_db_error**
- Mock `post_crud.get_post_by_id` to return a mock post
- Mock database session operations to raise an exception
- Call the endpoint with a valid post ID
- Verify:
  - Appropriate error response is returned
  - Exception is handled properly

#### Integration Tests

**test_delete_post_by_id_success**
- Create a test post
- Call the endpoint with the post ID
- Verify:
  - Response status code is 204 (No Content)
  - Post is actually deleted from database

**test_delete_post_by_id_not_found**
- Call the endpoint with a non-existent post ID
- Verify:
  - Response status code is 404
  - Error message indicates post not found

### 4. GET /drafts - Retrieve draft posts

#### Unit Tests

**test_read_draft_posts_success**
- Mock database execute to return sample draft posts with relationships
- Call the endpoint
- Verify:
  - Response status code is 200
  - Response contains expected list of draft posts
  - Database execute was called with correct query for drafts

**test_read_draft_posts_empty_result**
- Mock database execute to return empty result
- Call the endpoint
- Verify:
  - Response status code is 200
  - Response contains empty list

**test_read_draft_posts_db_error**
- Mock database execute to raise an exception
- Call the endpoint
- Verify:
  - Appropriate error response is returned
  - Exception is handled properly

#### Integration Tests

**test_read_draft_posts_success**
- Create several test draft posts
- Call the endpoint
- Verify:
  - Response status code is 200
  - Response contains expected list of draft posts
  - All created draft posts are in the response

**test_read_draft_posts_empty_result**
- Call the endpoint when no draft posts exist
- Verify:
  - Response status code is 200
  - Response contains empty list

### 5. GET /published - Retrieve published posts

#### Unit Tests

**test_read_published_posts_success**
- Mock database execute to return sample published posts with relationships
- Call the endpoint
- Verify:
  - Response status code is 200
  - Response contains expected list of published posts
  - Database execute was called with correct query for published posts

**test_read_published_posts_empty_result**
- Mock database execute to return empty result
- Call the endpoint
- Verify:
  - Response status code is 200
  - Response contains empty list

**test_read_published_posts_db_error**
- Mock database execute to raise an exception
- Call the endpoint
- Verify:
  - Appropriate error response is returned
  - Exception is handled properly

#### Integration Tests

**test_read_published_posts_success**
- Create several test published posts
- Call the endpoint
- Verify:
  - Response status code is 200
  - Response contains expected list of published posts
  - All created published posts are in the response

**test_read_published_posts_empty_result**
- Call the endpoint when no published posts exist
- Verify:
  - Response status code is 200
  - Response contains empty list

### 6. POST /{post_id}/publish - Publish a draft post

#### Unit Tests

**test_publish_post_success**
- Mock `post_crud.get_post_by_id` to return a mock draft post (is_published=False)
- Mock database session operations to simulate successful publish
- Call the endpoint with a valid post ID
- Verify:
  - Response status code is 200
  - Response contains updated post data with is_published=True
  - `post_crud.get_post_by_id` was called with correct parameters
  - Database session methods were called with correct parameters

**test_publish_post_not_found**
- Mock `post_crud.get_post_by_id` to raise HTTPException (404)
- Call the endpoint with a non-existent post ID
- Verify:
  - Response status code is 404
  - Error message indicates post not found

**test_publish_post_already_published**
- Mock `post_crud.get_post_by_id` to return a mock published post (is_published=True)
- Call the endpoint with a valid post ID
- Verify:
  - Response status code is 400
  - Error message indicates post is already published

**test_publish_post_db_error**
- Mock `post_crud.get_post_by_id` to return a mock draft post
- Mock database session operations to raise an exception
- Call the endpoint with a valid post ID
- Verify:
  - Appropriate error response is returned
  - Exception is handled properly

#### Integration Tests

**test_publish_post_success**
- Create a test draft post
- Call the endpoint with the post ID
- Verify:
  - Response status code is 200
  - Response contains updated post data with is_published=True
  - Post is actually updated in database with published status

**test_publish_post_not_found**
- Call the endpoint with a non-existent post ID
- Verify:
  - Response status code is 404
  - Error message indicates post not found

**test_publish_post_already_published**
- Create a test published post
- Call the endpoint with the post ID
- Verify:
  - Response status code is 400
  - Error message indicates post is already published

### 7. POST /{post_id}/unpublish - Unpublish a published post

#### Unit Tests

**test_unpublish_post_success**
- Mock `post_crud.get_post_by_id` to return a mock published post (is_published=True)
- Mock database session operations to simulate successful unpublish
- Call the endpoint with a valid post ID
- Verify:
  - Response status code is 200
  - Response contains updated post data with is_published=False
  - `post_crud.get_post_by_id` was called with correct parameters
  - Database session methods were called with correct parameters

**test_unpublish_post_not_found**
- Mock `post_crud.get_post_by_id` to raise HTTPException (404)
- Call the endpoint with a non-existent post ID
- Verify:
  - Response status code is 404
  - Error message indicates post not found

**test_unpublish_post_not_published**
- Mock `post_crud.get_post_by_id` to return a mock draft post (is_published=False)
- Call the endpoint with a valid post ID
- Verify:
  - Response status code is 400
  - Error message indicates post is not published

**test_unpublish_post_db_error**
- Mock `post_crud.get_post_by_id` to return a mock published post
- Mock database session operations to raise an exception
- Call the endpoint with a valid post ID
- Verify:
  - Appropriate error response is returned
  - Exception is handled properly

#### Integration Tests

**test_unpublish_post_success**
- Create a test published post
- Call the endpoint with the post ID
- Verify:
  - Response status code is 200
  - Response contains updated post data with is_published=False
  - Post is actually updated in database with unpublished status

**test_unpublish_post_not_found**
- Call the endpoint with a non-existent post ID
- Verify:
  - Response status code is 404
  - Error message indicates post not found

**test_unpublish_post_not_published**
- Create a test draft post
- Call the endpoint with the post ID
- Verify:
  - Response status code is 400
  - Error message indicates post is not published

## Test Data and Fixtures

### Required Test Data

1. **User Fixtures**
   - Users for testing post creation, updates, and ownership
   - Valid JWT tokens for authenticated requests

2. **Category Fixtures**
   - Categories for associating with posts
   - Multiple categories for testing different post categories

3. **Sample Posts**
   - Draft posts for testing draft functionality
   - Published posts for testing published functionality
   - Posts with various relationships (author, category, tags, comments, stats)

4. **Test Database Session**
   - Mock database session for unit tests
   - Real database session for integration tests (if needed)

### Mocking Strategies

1. **Database Operations**
   - Mock `post_crud` functions for unit tests
   - Use `unittest.mock.patch` to mock specific functions
   - For SQLAlchemy operations, mock the `execute`, `add`, `delete`, `commit`, and `refresh` methods on database sessions

2. **Dependencies**
   - Mock `get_session` dependency to return mock database sessions
   - Mock authentication dependencies if needed

3. **External Services**
   - Mock any file system operations if required
   - Mock any external API calls if required

## Expected Responses and Status Codes

### Success Responses

1. `POST /` - 201 Created with `PostRead` object
2. `PUT /{post_id}` - 200 OK with `PostRead` object
3. `DELETE /{post_id}` - 204 No Content
4. `GET /drafts` - 200 OK with list of `PostRead` objects
5. `GET /published` - 200 OK with list of `PostRead` objects
6. `POST /{post_id}/publish` - 200 OK with `PostRead` object
7. `POST /{post_id}/unpublish` - 200 OK with `PostRead` object

### Error Responses

1. **400 Bad Request**
   - Attempting to publish an already published post
   - Attempting to unpublish a draft post
   - Missing or invalid request data

2. **401 Unauthorized**
   - Missing or invalid JWT token
   - Invalid credentials

3. **404 Not Found**
   - Post not found when trying to update, delete, publish, or unpublish
   - Invalid post_id

4. **422 Unprocessable Entity**
   - Validation errors in request body
   - Missing required fields

## Test Execution

### Unit Tests
- Run with: `pytest backend/app/tests/unit/test_posts.py`
- Focus on testing individual functions in isolation
- Use mocking to simulate database and external dependencies

### Integration Tests
- Run with: `pytest backend/app/tests/integration/test_posts.py`
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
   - Create helper functions to generate test users, categories, posts, etc.
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

6. **Draft vs Published Posts**
   - Test both draft and published post scenarios thoroughly
   - Ensure proper filtering in draft and published endpoints
   - Test publish/unpublish workflows completely