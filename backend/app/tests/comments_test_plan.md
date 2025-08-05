# Comments Endpoints Test Plan

This document outlines a comprehensive test plan for the comments endpoints in `backend/app/api/v1/endpoints/comments.py`.

## Overview

The comments endpoints provide functionality for managing comments on posts and replies to comments. There are 7 endpoints:

1. `GET /posts/{post_id}/comments` - Get all comments for a specific post
2. `POST /posts/{post_id}/comments` - Add a comment to a post
3. `GET /{comment_id}` - Get a specific comment by id
4. `PUT /{comment_id}` - Update a comment
5. `DELETE /{comment_id}` - Delete a comment
6. `POST /{comment_id}/reply` - Reply to a comment
7. `GET /{comment_id}/replies` - Get replies to a comment

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

1. `backend/app/tests/unit/test_comments.py` - Unit tests for comments endpoints
2. `backend/app/tests/integration/test_comments.py` - Integration tests for comments endpoints

## Detailed Test Cases

### 1. GET /posts/{post_id}/comments - Get all comments for a specific post

#### Unit Tests

**test_read_comments_by_post_success**
- Mock `comment_crud.get_comments_by_post` to return sample comments
- Call the endpoint with a valid post ID
- Verify:
  - Response status code is 200
  - Response contains expected list of comments
  - `comment_crud.get_comments_by_post` was called with correct parameters

**test_read_comments_by_post_empty_result**
- Mock `comment_crud.get_comments_by_post` to return empty list
- Call the endpoint with a valid post ID
- Verify:
  - Response status code is 200
  - Response contains empty list

**test_read_comments_by_post_db_error**
- Mock `comment_crud.get_comments_by_post` to raise an exception
- Call the endpoint with a valid post ID
- Verify:
  - Appropriate error response is returned
  - Exception is handled properly

#### Integration Tests

**test_read_comments_by_post_success**
- Create a test post
- Create several test comments for the post
- Call the endpoint with the post ID
- Verify:
  - Response status code is 200
  - Response contains expected list of comments
  - All created comments for the post are in the response

**test_read_comments_by_post_empty_result**
- Create a test post without any comments
- Call the endpoint with the post ID
- Verify:
  - Response status code is 200
  - Response contains empty list

**test_read_comments_by_post_nonexistent_post**
- Call the endpoint with a non-existent post ID
- Verify:
  - Response status code is 404 (Not Found)
  - Error message indicates post not found

### 2. POST /posts/{post_id}/comments - Add a comment to a post

#### Unit Tests

**test_create_comment_for_post_success**
- Mock `post_crud.get_post_by_id` to return a mock post
- Mock `comment_crud.create_comment` to return a mock comment
- Call the endpoint with valid post ID and comment data
- Verify:
  - Response status code is 201
  - Response contains expected comment data
  - `post_crud.get_post_by_id` was called with correct parameters
  - `comment_crud.create_comment` was called with correct parameters

**test_create_comment_for_post_invalid_post**
- Mock `post_crud.get_post_by_id` to raise HTTPException (404)
- Call the endpoint with invalid post ID and comment data
- Verify:
  - Response status code is 404
  - Error message indicates post not found

**test_create_comment_for_post_missing_fields**
- Call the endpoint with missing required fields in comment data
- Verify:
  - Response status code is 422
  - Error message indicates validation errors

**test_create_comment_for_post_db_error**
- Mock `post_crud.get_post_by_id` to return a mock post
- Mock `comment_crud.create_comment` to raise an exception
- Call the endpoint with valid post ID and comment data
- Verify:
  - Appropriate error response is returned
  - Exception is handled properly

#### Integration Tests

**test_create_comment_for_post_success**
- Create a test post
- Create a test user
- Call the endpoint with valid post ID and comment data
- Verify:
  - Response status code is 201
  - Response contains expected comment data
  - Comment is actually stored in database

**test_create_comment_for_post_invalid_post**
- Call the endpoint with invalid post ID and comment data
- Verify:
  - Response status code is 404
  - Error message indicates post not found

**test_create_comment_for_post_missing_fields**
- Call the endpoint with missing required fields in comment data
- Verify:
  - Response status code is 422
  - Error message indicates validation errors

### 3. GET /{comment_id} - Get a specific comment by id

#### Unit Tests

**test_read_comment_by_id_success**
- Mock `comment_crud.get_comment_by_id` to return a mock comment
- Call the endpoint with a valid comment ID
- Verify:
  - Response status code is 200
  - Response contains expected comment data
  - `comment_crud.get_comment_by_id` was called with correct parameters

**test_read_comment_by_id_not_found**
- Mock `comment_crud.get_comment_by_id` to return None
- Call the endpoint with a non-existent comment ID
- Verify:
  - Response status code is 404
  - Error message indicates comment not found

**test_read_comment_by_id_invalid_uuid**
- Call the endpoint with an invalid comment ID format
- Verify:
  - Response status code is 422
  - Error message indicates validation errors

#### Integration Tests

**test_read_comment_by_id_success**
- Create a test comment
- Call the endpoint with the comment ID
- Verify:
  - Response status code is 200
  - Response contains expected comment data
  - Comment data matches what was created

**test_read_comment_by_id_not_found**
- Call the endpoint with a non-existent comment ID
- Verify:
  - Response status code is 404
  - Error message indicates comment not found

**test_read_comment_by_id_invalid_uuid**
- Call the endpoint with an invalid comment ID format
- Verify:
  - Response status code is 422
  - Error message indicates validation errors

### 4. PUT /{comment_id} - Update a comment

#### Unit Tests

**test_update_comment_by_id_success**
- Mock `comment_crud.get_comment_by_id` to return a mock comment
- Mock `comment_crud.update_comment` to return an updated mock comment
- Call the endpoint with a valid comment ID and update data
- Verify:
  - Response status code is 200
  - Response contains expected updated comment data
  - `comment_crud.get_comment_by_id` was called with correct parameters
  - `comment_crud.update_comment` was called with correct parameters

**test_update_comment_by_id_not_found**
- Mock `comment_crud.get_comment_by_id` to return None
- Call the endpoint with a non-existent comment ID and update data
- Verify:
  - Response status code is 404
  - Error message indicates comment not found

**test_update_comment_by_id_invalid_data**
- Mock `comment_crud.get_comment_by_id` to return a mock comment
- Call the endpoint with a valid comment ID and invalid update data
- Verify:
  - Response status code is 422
  - Error message indicates validation errors

**test_update_comment_by_id_db_error**
- Mock `comment_crud.get_comment_by_id` to return a mock comment
- Mock `comment_crud.update_comment` to return None
- Call the endpoint with a valid comment ID and update data
- Verify:
  - Response status code is 404
  - Error message indicates comment not found

#### Integration Tests

**test_update_comment_by_id_success**
- Create a test comment
- Call the endpoint with the comment ID and update data
- Verify:
  - Response status code is 200
  - Response contains expected updated comment data
  - Comment is actually updated in database

**test_update_comment_by_id_not_found**
- Call the endpoint with a non-existent comment ID and update data
- Verify:
  - Response status code is 404
  - Error message indicates comment not found

**test_update_comment_by_id_invalid_data**
- Create a test comment
- Call the endpoint with the comment ID and invalid update data
- Verify:
  - Response status code is 422
  - Error message indicates validation errors

### 5. DELETE /{comment_id} - Delete a comment

#### Unit Tests

**test_delete_comment_by_id_success**
- Mock `comment_crud.get_comment_by_id` to return a mock comment
- Mock `comment_crud.delete_comment` to return True
- Call the endpoint with a valid comment ID
- Verify:
  - Response status code is 204 (No Content)
  - `comment_crud.get_comment_by_id` was called with correct parameters
  - `comment_crud.delete_comment` was called with correct parameters

**test_delete_comment_by_id_not_found**
- Mock `comment_crud.get_comment_by_id` to return None
- Call the endpoint with a non-existent comment ID
- Verify:
  - Response status code is 404
  - Error message indicates comment not found

**test_delete_comment_by_id_db_error**
- Mock `comment_crud.get_comment_by_id` to return a mock comment
- Mock `comment_crud.delete_comment` to return False
- Call the endpoint with a valid comment ID
- Verify:
  - Response status code is 404
  - Error message indicates comment not found

#### Integration Tests

**test_delete_comment_by_id_success**
- Create a test comment
- Call the endpoint with the comment ID
- Verify:
  - Response status code is 204 (No Content)
  - Comment is actually deleted from database

**test_delete_comment_by_id_not_found**
- Call the endpoint with a non-existent comment ID
- Verify:
  - Response status code is 404
  - Error message indicates comment not found

### 6. POST /{comment_id}/reply - Reply to a comment

#### Unit Tests

**test_reply_to_comment_success**
- Mock `comment_crud.get_comment_by_id` to return a mock parent comment
- Mock `comment_crud.create_comment` to return a mock reply comment
- Call the endpoint with a valid parent comment ID and reply data
- Verify:
  - Response status code is 201
  - Response contains expected reply comment data
  - `comment_crud.get_comment_by_id` was called with correct parameters
  - `comment_crud.create_comment` was called with correct parameters
  - Created comment has correct post_id from parent comment
  - Created comment has correct parent_comment_id

**test_reply_to_comment_parent_not_found**
- Mock `comment_crud.get_comment_by_id` to return None
- Call the endpoint with a non-existent parent comment ID and reply data
- Verify:
  - Response status code is 404
  - Error message indicates parent comment not found

**test_reply_to_comment_missing_fields**
- Mock `comment_crud.get_comment_by_id` to return a mock parent comment
- Call the endpoint with missing required fields in reply data
- Verify:
  - Response status code is 422
  - Error message indicates validation errors

**test_reply_to_comment_db_error**
- Mock `comment_crud.get_comment_by_id` to return a mock parent comment
- Mock `comment_crud.create_comment` to raise an exception
- Call the endpoint with a valid parent comment ID and reply data
- Verify:
  - Appropriate error response is returned
  - Exception is handled properly

#### Integration Tests

**test_reply_to_comment_success**
- Create a test post
- Create a test parent comment
- Call the endpoint with the parent comment ID and reply data
- Verify:
  - Response status code is 201
  - Response contains expected reply comment data
  - Reply comment is actually stored in database
  - Reply comment has correct post_id from parent comment
  - Reply comment has correct parent_comment_id

**test_reply_to_comment_parent_not_found**
- Call the endpoint with a non-existent parent comment ID and reply data
- Verify:
  - Response status code is 404
  - Error message indicates parent comment not found

**test_reply_to_comment_missing_fields**
- Create a test parent comment
- Call the endpoint with the parent comment ID and missing required fields in reply data
- Verify:
  - Response status code is 422
  - Error message indicates validation errors

### 7. GET /{comment_id}/replies - Get replies to a comment

#### Unit Tests

**test_read_replies_to_comment_success**
- Mock `comment_crud.get_comment_by_id` to return a mock parent comment
- Mock `comment_crud.get_replies_by_comment` to return sample replies
- Call the endpoint with a valid parent comment ID
- Verify:
  - Response status code is 200
  - Response contains expected list of replies
  - `comment_crud.get_comment_by_id` was called with correct parameters
  - `comment_crud.get_replies_by_comment` was called with correct parameters

**test_read_replies_to_comment_parent_not_found**
- Mock `comment_crud.get_comment_by_id` to return None
- Call the endpoint with a non-existent parent comment ID
- Verify:
  - Response status code is 404
  - Error message indicates parent comment not found

**test_read_replies_to_comment_empty_result**
- Mock `comment_crud.get_comment_by_id` to return a mock parent comment
- Mock `comment_crud.get_replies_by_comment` to return empty list
- Call the endpoint with a valid parent comment ID
- Verify:
  - Response status code is 200
  - Response contains empty list

**test_read_replies_to_comment_db_error**
- Mock `comment_crud.get_comment_by_id` to return a mock parent comment
- Mock `comment_crud.get_replies_by_comment` to raise an exception
- Call the endpoint with a valid parent comment ID
- Verify:
  - Appropriate error response is returned
  - Exception is handled properly

#### Integration Tests

**test_read_replies_to_comment_success**
- Create a test post
- Create a test parent comment
- Create several test replies to the parent comment
- Call the endpoint with the parent comment ID
- Verify:
  - Response status code is 200
  - Response contains expected list of replies
  - All created replies to the parent comment are in the response

**test_read_replies_to_comment_parent_not_found**
- Call the endpoint with a non-existent parent comment ID
- Verify:
  - Response status code is 404
  - Error message indicates parent comment not found

**test_read_replies_to_comment_empty_result**
- Create a test post
- Create a test parent comment without any replies
- Call the endpoint with the parent comment ID
- Verify:
  - Response status code is 200
  - Response contains empty list

## Test Data and Fixtures

### Required Test Data

1. **Test Post Fixture**
   - Post for testing comment creation and retrieval
   - Valid post with all required fields

2. **Test User Fixture**
   - User for associating with comments
   - Valid user with all required fields

3. **Test Comments**
   - Multiple comments for testing listing and pagination
   - Comments with various relationships (post, user, parent comment)
   - Comments with different content and timestamps

4. **Test Database Session**
   - Mock database session for unit tests
   - Real database session for integration tests (if needed)

### Mocking Strategies

1. **Database Operations**
   - Mock CRUD functions for unit tests
   - Use `unittest.mock.patch` to mock specific functions
   - For SQLAlchemy operations, mock the `execute` method on database sessions

2. **Dependencies**
   - Mock `get_session` dependency to return mock database sessions
   - Mock any authentication dependencies if needed

3. **External Services**
   - Mock any external services if required
   - Mock file system operations if required

## Expected Responses and Status Codes

### Success Responses

1. `GET /posts/{post_id}/comments` - 200 OK with list of `CommentRead` objects
2. `POST /posts/{post_id}/comments` - 201 Created with `CommentRead` object
3. `GET /{comment_id}` - 200 OK with `CommentRead` object
4. `PUT /{comment_id}` - 200 OK with `CommentRead` object
5. `DELETE /{comment_id}` - 204 No Content
6. `POST /{comment_id}/reply` - 201 Created with `CommentRead` object
7. `GET /{comment_id}/replies` - 200 OK with list of `CommentRead` objects

### Error Responses

1. **400 Bad Request**
   - Invalid request data
   - Missing required fields

2. **401 Unauthorized**
   - Missing or invalid authentication credentials

3. **404 Not Found**
   - Comment, post, or parent comment not found
   - Invalid comment_id or post_id

4. **422 Unprocessable Entity**
   - Validation errors in request body or path parameters
   - Invalid UUID format

## Test Execution

### Unit Tests
- Run with: `pytest backend/app/tests/unit/test_comments.py`
- Focus on testing individual functions in isolation
- Use mocking to simulate database and external dependencies

### Integration Tests
- Run with: `pytest backend/app/tests/integration/test_comments.py`
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
   - Create helper functions to generate test comments, posts, users, etc.
   - Use `uuid.uuid4()` for generating unique IDs
   - Ensure test data matches the expected schemas

4. **Authentication in Tests**
   - If authentication is required, create helper functions to generate JWT tokens for test users
   - Use the same SECRET_KEY as in the application settings
   - Follow the same token structure as the real application

5. **Database Considerations**
   - For unit tests, fully mock database operations
   - For integration tests, either use a separate test database or fully mock as well
   - Ensure tests don't affect the development or production databases

6. **Authorization Considerations**
   - Test both authorized and unauthorized scenarios
   - Test cases where users can only modify their own comments (if applicable)
   - Mock user authentication and authorization checks as needed