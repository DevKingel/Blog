# Categories Endpoints Test Plan

This document outlines a comprehensive test plan for the categories endpoints in `backend/app/api/v1/endpoints/categories.py`.

## Overview

The categories endpoints provide CRUD functionality for managing blog post categories. There are 6 endpoints:

1. `POST /categories/` - Create a new category
2. `GET /categories/` - Retrieve categories with pagination
3. `GET /categories/{category_id}` - Get a specific category by ID
4. `PATCH /categories/{category_id}` - Update a category
5. `DELETE /categories/{category_id}` - Delete a category
6. `GET /categories/{category_id}/posts` - Get all posts in a specific category

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

1. `backend/app/tests/unit/test_categories.py` - Unit tests for categories endpoints
2. `backend/app/tests/integration/test_categories.py` - Integration tests for categories endpoints

## Detailed Test Cases

### 1. POST /categories/ - Create a new category

#### Unit Tests

**test_create_category_success**
- Mock `category_crud.get_all_categories` to return empty list (no existing categories)
- Mock `category_crud.create_category` to return a mock category
- Call the endpoint with valid category data
- Verify:
  - Response status code is 201
  - Response contains expected category fields
  - `category_crud.get_all_categories` was called to check for duplicates
  - `category_crud.create_category` was called with correct parameters

**test_create_category_duplicate_name**
- Mock `category_crud.get_all_categories` to return a list with an existing category with same name
- Call the endpoint with category data that has the same name
- Verify:
  - Response status code is 400
  - Error message indicates category with this name already exists
  - `category_crud.create_category` was not called

**test_create_category_duplicate_slug**
- Mock `category_crud.get_all_categories` to return a list with an existing category with same slug
- Call the endpoint with category data that has the same slug
- Verify:
  - Response status code is 400
  - Error message indicates category with this slug already exists
  - `category_crud.create_category` was not called

**test_create_category_invalid_data**
- Call the endpoint with invalid category data (missing required fields)
- Verify:
  - Response status code is 422
  - Error message indicates validation errors

#### Integration Tests

**test_create_category_success**
- Call the endpoint with valid category data
- Verify:
  - Response status code is 201
  - Response contains expected category fields
  - Category is actually created in database

**test_create_category_duplicate_name**
- Create a category in the database
- Call the endpoint with category data that has the same name
- Verify:
  - Response status code is 400
  - Error message indicates category with this name already exists

**test_create_category_duplicate_slug**
- Create a category in the database
- Call the endpoint with category data that has the same slug
- Verify:
  - Response status code is 400
  - Error message indicates category with this slug already exists

**test_create_category_invalid_data**
- Call the endpoint with invalid category data (missing required fields)
- Verify:
  - Response status code is 422
  - Error message indicates validation errors

### 2. GET /categories/ - Retrieve categories with pagination

#### Unit Tests

**test_get_categories_success**
- Mock `category_crud.get_all_categories` to return sample categories
- Call the endpoint with default pagination parameters
- Verify:
  - Response status code is 200
  - Response contains expected category list
  - `category_crud.get_all_categories` was called with correct parameters

**test_get_categories_with_pagination**
- Mock `category_crud.get_all_categories` to return sample categories
- Call the endpoint with custom skip and limit parameters
- Verify:
  - Response status code is 200
  - Response contains expected category list with correct pagination
  - `category_crud.get_all_categories` was called with correct skip/limit parameters

**test_get_categories_empty_result**
- Mock `category_crud.get_all_categories` to return empty list
- Call the endpoint
- Verify:
  - Response status code is 200
  - Response contains empty category list

#### Integration Tests

**test_get_categories_success**
- Create several test categories
- Call the endpoint with default parameters
- Verify:
  - Response status code is 200
  - Response contains expected category list
  - All created categories are in the response

**test_get_categories_with_pagination**
- Create several test categories (more than default limit)
- Call the endpoint with custom skip and limit parameters
- Verify:
  - Response status code is 200
  - Response contains expected category list with correct pagination
  - Pagination works correctly

**test_get_categories_empty_result**
- Call the endpoint when no categories exist
- Verify:
  - Response status code is 200
  - Response contains empty category list

### 3. GET /categories/{category_id} - Get a specific category by ID

#### Unit Tests

**test_get_category_by_id_success**
- Mock `category_crud.get_category_by_id` to return a mock category
- Call the endpoint with a valid category ID
- Verify:
  - Response status code is 200
  - Response contains expected category fields
  - `category_crud.get_category_by_id` was called with correct parameters

**test_get_category_by_id_not_found**
- Mock `category_crud.get_category_by_id` to return None
- Call the endpoint with a non-existent category ID
- Verify:
  - Response status code is 404
  - Error message indicates category not found

**test_get_category_by_id_invalid_uuid**
- Call the endpoint with an invalid UUID format
- Verify:
  - Response status code is 422
  - Error message indicates validation errors

#### Integration Tests

**test_get_category_by_id_success**
- Create a test category
- Call the endpoint with the category's ID
- Verify:
  - Response status code is 200
  - Response contains expected category fields
  - Category data matches what was created

**test_get_category_by_id_not_found**
- Call the endpoint with a non-existent category ID
- Verify:
  - Response status code is 404
  - Error message indicates category not found

**test_get_category_by_id_invalid_uuid**
- Call the endpoint with an invalid UUID format
- Verify:
  - Response status code is 422
  - Error message indicates validation errors

### 4. PATCH /categories/{category_id} - Update a category

#### Unit Tests

**test_update_category_success**
- Mock `category_crud.get_category_by_id` to return an existing category
- Mock `category_crud.get_all_categories` to return only the category being updated
- Mock `category_crud.update_category` to return the updated category
- Call the endpoint with valid update data
- Verify:
  - Response status code is 200
  - Response contains updated category fields
  - `category_crud.get_category_by_id` was called to check existence
  - `category_crud.get_all_categories` was called to check for duplicates
  - `category_crud.update_category` was called with correct parameters

**test_update_category_not_found**
- Mock `category_crud.get_category_by_id` to return None
- Call the endpoint with update data for a non-existent category
- Verify:
  - Response status code is 404
  - Error message indicates category not found
  - `category_crud.update_category` was not called

**test_update_category_duplicate_name**
- Mock `category_crud.get_category_by_id` to return the category being updated
- Mock `category_crud.get_all_categories` to return another category with the same name
- Call the endpoint with update data that conflicts with existing category name
- Verify:
  - Response status code is 400
  - Error message indicates category with this name already exists
  - `category_crud.update_category` was not called

**test_update_category_duplicate_slug**
- Mock `category_crud.get_category_by_id` to return the category being updated
- Mock `category_crud.get_all_categories` to return another category with the same slug
- Call the endpoint with update data that conflicts with existing category slug
- Verify:
  - Response status code is 400
  - Error message indicates category with this slug already exists
  - `category_crud.update_category` was not called

**test_update_category_no_data**
- Call the endpoint with empty update data
- Verify:
  - Response status code is 400
  - Error message indicates no data provided for update

**test_update_category_invalid_data**
- Call the endpoint with invalid update data
- Verify:
  - Response status code is 422
  - Error message indicates validation errors

#### Integration Tests

**test_update_category_success**
- Create a test category
- Call the endpoint with valid update data
- Verify:
  - Response status code is 200
  - Response contains updated category fields
  - Category is actually updated in database

**test_update_category_not_found**
- Call the endpoint with update data for a non-existent category ID
- Verify:
  - Response status code is 404
  - Error message indicates category not found

**test_update_category_duplicate_name**
- Create two test categories
- Call the endpoint to update one category with the name of the other
- Verify:
  - Response status code is 400
  - Error message indicates category with this name already exists

**test_update_category_duplicate_slug**
- Create two test categories
- Call the endpoint to update one category with the slug of the other
- Verify:
  - Response status code is 400
  - Error message indicates category with this slug already exists

**test_update_category_no_data**
- Call the endpoint with empty update data
- Verify:
  - Response status code is 400
  - Error message indicates no data provided for update

**test_update_category_invalid_data**
- Call the endpoint with invalid update data
- Verify:
  - Response status code is 422
  - Error message indicates validation errors

### 5. DELETE /categories/{category_id} - Delete a category

#### Unit Tests

**test_delete_category_success**
- Mock `category_crud.get_category_by_id` to return a mock category
- Mock `category_crud.delete_category` to return True
- Call the endpoint with a valid category ID
- Verify:
  - Response status code is 204
  - `category_crud.get_category_by_id` was called with correct parameters
  - `category_crud.delete_category` was called with correct parameters

**test_delete_category_not_found**
- Mock `category_crud.get_category_by_id` to return None
- Call the endpoint with a non-existent category ID
- Verify:
  - Response status code is 404
  - Error message indicates category not found
  - `category_crud.delete_category` was not called

#### Integration Tests

**test_delete_category_success**
- Create a test category
- Call the endpoint with the category's ID
- Verify:
  - Response status code is 204
  - Category is actually deleted from database

**test_delete_category_not_found**
- Call the endpoint with a non-existent category ID
- Verify:
  - Response status code is 404
  - Error message indicates category not found

### 6. GET /categories/{category_id}/posts - Get all posts in a specific category

#### Unit Tests

**test_get_category_posts_success**
- Mock `category_crud.get_category_by_id` to return a mock category
- Mock `get_posts_by_category` to return sample posts
- Call the endpoint with a valid category ID
- Verify:
  - Response status code is 200
  - Response contains expected post list
  - `category_crud.get_category_by_id` was called to check existence
  - `get_posts_by_category` was called with correct parameters

**test_get_category_posts_category_not_found**
- Mock `category_crud.get_category_by_id` to return None
- Call the endpoint with a non-existent category ID
- Verify:
  - Response status code is 404
  - Error message indicates category not found
  - `get_posts_by_category` was not called

#### Integration Tests

**test_get_category_posts_success**
- Create a test category
- Create several test posts in that category
- Call the endpoint with the category's ID
- Verify:
  - Response status code is 200
  - Response contains expected post list
  - All posts in the category are in the response

**test_get_category_posts_category_not_found**
- Call the endpoint with a non-existent category ID
- Verify:
  - Response status code is 404
  - Error message indicates category not found

**test_get_category_posts_empty_result**
- Create a test category with no posts
- Call the endpoint with the category's ID
- Verify:
  - Response status code is 200
  - Response contains empty post list

## Test Data and Fixtures

### Required Test Data

1. **Category Fixtures**
   - Valid category data for creation tests
   - Multiple categories for pagination tests
   - Categories with various names and slugs for duplicate checking

2. **Post Fixtures**
   - Posts associated with categories for testing the posts endpoint
   - Posts with various relationships (author, tags, etc.)

3. **Test Database Session**
   - Mock database session for unit tests
   - Real database session for integration tests (if needed)

### Mocking Strategies

1. **Database Operations**
   - Mock CRUD functions for unit tests:
     - `category_crud.get_all_categories`
     - `category_crud.get_category_by_id`
     - `category_crud.create_category`
     - `category_crud.update_category`
     - `category_crud.delete_category`
     - `get_posts_by_category`
   - Use `unittest.mock.patch` to mock specific functions
   - For SQLAlchemy operations, mock the `execute` method on database sessions if needed

2. **Dependencies**
   - Mock `get_session` dependency to return mock database sessions
   - Mock any security or authentication dependencies if required

3. **External Services**
   - Mock file system operations if required for media handling
   - Mock any external API calls if needed

## Expected Responses and Status Codes

### Success Responses

1. `POST /categories/` - 201 Created with `CategoryRead` object
2. `GET /categories/` - 200 OK with list of `CategoryRead` objects
3. `GET /categories/{category_id}` - 200 OK with `CategoryRead` object
4. `PATCH /categories/{category_id}` - 200 OK with `CategoryRead` object
5. `DELETE /categories/{category_id}` - 204 No Content
6. `GET /categories/{category_id}/posts` - 200 OK with list of `PostRead` objects

### Error Responses

1. **400 Bad Request**
   - Duplicate category name or slug
   - No data provided for update
   - Invalid request data

2. **404 Not Found**
   - Category not found when trying to get, update, or delete
   - Invalid category_id

3. **422 Unprocessable Entity**
   - Validation errors in request body
   - Invalid UUID format for category_id

## Test Execution

### Unit Tests
- Run with: `pytest backend/app/tests/unit/test_categories.py`
- Focus on testing individual functions in isolation
- Use mocking to simulate database and external dependencies

### Integration Tests
- Run with: `pytest backend/app/tests/integration/test_categories.py`
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
   - Create helper functions to generate test categories, posts, etc.
   - Use `uuid.uuid4()` for generating unique IDs
   - Ensure test data matches the expected schemas

4. **Database Considerations**
   - For unit tests, fully mock database operations
   - For integration tests, either use a separate test database or fully mock as well
   - Ensure tests don't affect the development or production databases

5. **Validation Testing**
   - Test both valid and invalid input data
   - Ensure proper error messages are returned for validation failures
   - Test edge cases like empty strings, special characters, etc.