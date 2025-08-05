# Tags Endpoints Test Plan

This document outlines a comprehensive test plan for the tags endpoints in `backend/app/api/v1/endpoints/tags.py`.

## Overview

The tags endpoints provide CRUD functionality for managing tags and retrieving posts associated with specific tags. There are 6 endpoints:

1. `POST /tags/` - Create a new tag
2. `GET /tags/` - Retrieve tags with pagination
3. `GET /tags/{tag_id}` - Get a specific tag by id
4. `PUT /tags/{tag_id}` - Update a tag
5. `DELETE /tags/{tag_id}` - Delete a tag
6. `GET /tags/{tag_id}/posts` - Get all posts with a specific tag

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

1. `backend/app/tests/unit/test_tags.py` - Unit tests for tags endpoints
2. `backend/app/tests/integration/test_tags.py` - Integration tests for tags endpoints

## Detailed Test Cases

### 1. POST /tags/ - Create a new tag

#### Unit Tests

**test_create_tag_success**
- Mock `tag_crud.get_tag_by_name_or_slug` to return None (no existing tag)
- Mock `tag_crud.create_tag` to return a mock tag
- Call the endpoint with valid tag data
- Verify:
  - Response status code is 201
  - Response contains tag data matching the mock tag
  - `tag_crud.get_tag_by_name_or_slug` was called with correct parameters
  - `tag_crud.create_tag` was called with correct parameters

**test_create_tag_duplicate_name**
- Mock `tag_crud.get_tag_by_name_or_slug` to return an existing tag
- Call the endpoint with tag data that conflicts with existing tag
- Verify:
  - Response status code is 400
  - Error message indicates tag with this name or slug already exists
  - `tag_crud.create_tag` was not called

**test_create_tag_invalid_data**
- Call the endpoint with invalid tag data
- Verify:
  - Response status code is 422
  - Error message indicates validation errors
  - `tag_crud.get_tag_by_name_or_slug` and `tag_crud.create_tag` were not called

#### Integration Tests

**test_create_tag_success**
- Call the endpoint with valid tag data
- Verify:
  - Response status code is 201
  - Response contains tag data matching the input
  - Tag is actually stored in the database

**test_create_tag_duplicate_name**
- Create a tag in the database
- Call the endpoint with tag data that conflicts with the existing tag
- Verify:
  - Response status code is 400
  - Error message indicates tag with this name or slug already exists

**test_create_tag_duplicate_slug**
- Create a tag in the database
- Call the endpoint with tag data that has a different name but same slug as existing tag
- Verify:
  - Response status code is 400
  - Error message indicates tag with this name or slug already exists

### 2. GET /tags/ - Retrieve tags with pagination

#### Unit Tests

**test_read_tags_success**
- Mock `tag_crud.get_all_tags` to return a list of mock tags
- Call the endpoint with skip and limit parameters
- Verify:
  - Response status code is 200
  - Response contains correct number of tags based on pagination
  - `tag_crud.get_all_tags` was called

**test_read_tags_empty**
- Mock `tag_crud.get_all_tags` to return an empty list
- Call the endpoint
- Verify:
  - Response status code is 200
  - Response contains an empty list

#### Integration Tests

**test_read_tags_success**
- Create multiple tags in the database
- Call the endpoint with skip and limit parameters
- Verify:
  - Response status code is 200
  - Response contains correct number of tags based on pagination
  - Tags match those stored in the database

**test_read_tags_empty**
- Call the endpoint when no tags exist in the database
- Verify:
  - Response status code is 200
  - Response contains an empty list

### 3. GET /tags/{tag_id} - Get a specific tag by id

#### Unit Tests

**test_read_tag_by_id_success**
- Mock `tag_crud.get_tag_by_id` to return a mock tag
- Call the endpoint with a valid tag_id
- Verify:
  - Response status code is 200
  - Response contains tag data matching the mock tag
  - `tag_crud.get_tag_by_id` was called with correct parameters

**test_read_tag_by_id_not_found**
- Mock `tag_crud.get_tag_by_id` to return None
- Call the endpoint with a non-existent tag_id
- Verify:
  - Response status code is 404
  - Error message indicates "Tag not found"
  - `tag_crud.get_tag_by_id` was called with correct parameters

#### Integration Tests

**test_read_tag_by_id_success**
- Create a tag in the database
- Call the endpoint with the tag's ID
- Verify:
  - Response status code is 200
  - Response contains tag data matching what was stored
  - All required fields are present in the response

**test_read_tag_by_id_not_found**
- Call the endpoint with a non-existent tag ID
- Verify:
  - Response status code is 404
  - Error message indicates "Tag not found"

### 4. PUT /tags/{tag_id} - Update a tag

#### Unit Tests

**test_update_tag_success**
- Mock `tag_crud.get_tag_by_id` to return an existing mock tag
- Mock `tag_crud.get_tag_by_name_or_slug` to return None (no conflicts)
- Mock `tag_crud.update_tag` to return an updated mock tag
- Call the endpoint with valid tag update data
- Verify:
  - Response status code is 200
  - Response contains updated tag data
  - `tag_crud.get_tag_by_id` was called with correct parameters
  - `tag_crud.get_tag_by_name_or_slug` was called with correct parameters
  - `tag_crud.update_tag` was called with correct parameters

**test_update_tag_not_found**
- Mock `tag_crud.get_tag_by_id` to return None
- Call the endpoint with tag update data
- Verify:
  - Response status code is 404
  - Error message indicates tag not found
  - `tag_crud.get_tag_by_name_or_slug` and `tag_crud.update_tag` were not called

**test_update_tag_duplicate_name**
- Mock `tag_crud.get_tag_by_id` to return an existing mock tag
- Mock `tag_crud.get_tag_by_name_or_slug` to return a different existing tag
- Call the endpoint with update data that conflicts with another tag
- Verify:
  - Response status code is 400
  - Error message indicates tag with this name or slug already exists
  - `tag_crud.update_tag` was not called

**test_update_tag_invalid_data**
- Mock `tag_crud.get_tag_by_id` to return an existing mock tag
- Call the endpoint with invalid update data
- Verify:
  - Response status code is 422
  - Error message indicates validation errors
  - `tag_crud.get_tag_by_name_or_slug` and `tag_crud.update_tag` were not called

#### Integration Tests

**test_update_tag_success**
- Create a tag in the database
- Call the endpoint with valid update data
- Verify:
  - Response status code is 200
  - Response contains updated tag data
  - Tag data in database has been updated correctly

**test_update_tag_not_found**
- Call the endpoint with update data and a non-existent tag ID
- Verify:
  - Response status code is 404
  - Error message indicates tag not found

**test_update_tag_partial**
- Create a tag in the database
- Call the endpoint with partial update data (only name, not slug)
- Verify:
  - Response status code is 200
  - Response contains updated name but unchanged slug
  - Only the specified field was updated in the database

### 5. DELETE /tags/{tag_id} - Delete a tag

#### Unit Tests

**test_delete_tag_success**
- Mock `tag_crud.delete_tag` to return True
- Call the endpoint with a valid tag_id
- Verify:
  - Response status code is 204
  - Response body is empty
  - `tag_crud.delete_tag` was called with correct parameters

**test_delete_tag_not_found**
- Mock `tag_crud.delete_tag` to return False
- Call the endpoint with a non-existent tag_id
- Verify:
  - Response status code is 404
  - Error message indicates "Tag not found"

#### Integration Tests

**test_delete_tag_success**
- Create a tag in the database
- Call the endpoint with the tag's ID
- Verify:
  - Response status code is 204
  - Response body is empty
  - Tag no longer exists in the database

**test_delete_tag_not_found**
- Call the endpoint with a non-existent tag ID
- Verify:
  - Response status code is 404
  - Error message indicates "Tag not found"

### 6. GET /tags/{tag_id}/posts - Get all posts with a specific tag

#### Unit Tests

**test_get_posts_with_tag_success**
- Mock `tag_crud.get_tag_by_id` to return an existing mock tag
- Mock `get_posts_by_tag` to return a list of mock posts
- Call the endpoint with a valid tag_id
- Verify:
  - Response status code is 200
  - Response contains list of posts with the tag
  - `tag_crud.get_tag_by_id` was called with correct parameters
  - `get_posts_by_tag` was called with correct parameters

**test_get_posts_with_tag_not_found**
- Mock `tag_crud.get_tag_by_id` to return None
- Call the endpoint with a non-existent tag_id
- Verify:
  - Response status code is 404
  - Error message indicates "Tag not found"
  - `get_posts_by_tag` was not called

#### Integration Tests

**test_get_posts_with_tag_success**
- Create a tag and posts with that tag in the database
- Call the endpoint with the tag's ID
- Verify:
  - Response status code is 200
  - Response contains list of posts with the tag
  - All posts in response actually have the specified tag

**test_get_posts_with_tag_empty**
- Create a tag but no posts with that tag in the database
- Call the endpoint with the tag's ID
- Verify:
  - Response status code is 200
  - Response contains an empty list

**test_get_posts_with_tag_not_found**
- Call the endpoint with a non-existent tag ID
- Verify:
  - Response status code is 404
  - Error message indicates "Tag not found"

## Test Data and Fixtures

### Required Test Data

1. **Test Tags Fixture**
   - Tags with name and slug for testing tag operations
   - Valid tag data that matches the Tag model schema

2. **Test Posts Fixture**
   - Posts associated with tags for testing the get posts by tag endpoint
   - Posts with various tags for comprehensive testing

3. **Test Database Session**
   - Mock database session for unit tests
   - Real database session for integration tests (if needed)

### Mocking Strategies

1. **Database Operations**
   - Mock `tag_crud.get_tag_by_name_or_slug` function for tag creation and update
   - Mock `tag_crud.get_tag_by_id` function for tag retrieval, update, and deletion
   - Mock `tag_crud.create_tag` function for tag creation
   - Mock `tag_crud.get_all_tags` function for tag listing
   - Mock `tag_crud.update_tag` function for tag update
   - Mock `tag_crud.delete_tag` function for tag deletion
   - Mock `get_posts_by_tag` function for getting posts with a specific tag
   - Use `unittest.mock.patch` to mock specific CRUD functions

2. **Dependencies**
   - Mock `get_session` dependency to return mock database sessions

## Expected Responses and Status Codes

### Success Responses

1. `POST /tags/` - 201 Created with `TagRead` object
2. `GET /tags/` - 200 OK with list of `TagRead` objects
3. `GET /tags/{tag_id}` - 200 OK with `TagRead` object
4. `PUT /tags/{tag_id}` - 200 OK with `TagRead` object
5. `DELETE /tags/{tag_id}` - 204 No Content with empty response body
6. `GET /tags/{tag_id}/posts` - 200 OK with list of `PostRead` objects

### Error Responses

1. **400 Bad Request**
   - Tag with this name or slug already exists during creation or update

2. **404 Not Found**
   - Tag not found when retrieving, updating, or deleting by ID
   - Tag not found when getting posts with tag

3. **422 Unprocessable Entity**
   - Validation errors in tag data
   - Missing required fields in request body

## Test Execution

### Unit Tests
- Run with: `pytest backend/app/tests/unit/test_tags.py`
- Focus on testing individual functions in isolation
- Use mocking to simulate database and external dependencies

### Integration Tests
- Run with: `pytest backend/app/tests/integration/test_tags.py`
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
   - Create helper functions to generate test tags and posts
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