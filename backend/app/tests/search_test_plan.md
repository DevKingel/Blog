# Search Endpoints Test Plan

This document outlines a comprehensive test plan for the search endpoints in `backend/app/api/v1/endpoints/search.py`.

## Overview

The search endpoints provide functionality for searching various entities in the system. There are 4 endpoints:

1. `GET /search/posts` - Search posts by query string in title or content
2. `GET /search/users` - Search users by query string in username or email
3. `GET /search/categories` - Search categories by query string in name
4. `GET /search/tags` - Search tags by query string in name

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

1. `backend/app/tests/unit/test_search.py` - Unit tests for search endpoints
2. `backend/app/tests/integration/test_search.py` - Integration tests for search endpoints

## Detailed Test Cases

### 1. GET /search/posts - Search posts by query string

#### Unit Tests

**test_search_posts_success**
- Mock `post_crud.search_posts` to return mock posts and total count
- Call the endpoint with a valid query string
- Verify:
  - Response status code is 200
  - Response contains posts and total count matching the mock data
  - `post_crud.search_posts` was called with correct parameters

**test_search_posts_empty_results**
- Mock `post_crud.search_posts` to return empty list and zero count
- Call the endpoint with a query string that returns no results
- Verify:
  - Response status code is 200
  - Response contains empty posts list and zero total count

**test_search_posts_missing_query**
- Call the endpoint without required query parameter
- Verify:
  - Response status code is 422
  - Error message indicates validation errors for missing query

**test_search_posts_short_query**
- Call the endpoint with a query string shorter than minimum length (1 character)
- Verify:
  - Response status code is 422
  - Error message indicates validation errors for query length

#### Integration Tests

**test_search_posts_success**
- Create test posts in the database with various titles and content
- Call the endpoint with a query that matches some posts
- Verify:
  - Response status code is 200
  - Response contains matching posts and correct total count
  - Only posts matching the query are returned

**test_search_posts_empty_results**
- Call the endpoint with a query that matches no posts
- Verify:
  - Response status code is 200
  - Response contains empty posts list and zero total count

**test_search_posts_pagination**
- Create multiple test posts in the database
- Call the endpoint with skip and limit parameters
- Verify:
  - Response status code is 200
  - Response contains correct number of posts based on pagination
  - Total count reflects the actual number of matching posts

### 2. GET /search/users - Search users by query string

#### Unit Tests

**test_search_users_success**
- Mock `user_crud.search_users` to return mock users and total count
- Call the endpoint with a valid query string
- Verify:
  - Response status code is 200
  - Response contains users and total count matching the mock data
  - `user_crud.search_users` was called with correct parameters

**test_search_users_empty_results**
- Mock `user_crud.search_users` to return empty list and zero count
- Call the endpoint with a query string that returns no results
- Verify:
  - Response status code is 200
  - Response contains empty users list and zero total count

**test_search_users_missing_query**
- Call the endpoint without required query parameter
- Verify:
  - Response status code is 422
  - Error message indicates validation errors for missing query

**test_search_users_short_query**
- Call the endpoint with a query string shorter than minimum length (1 character)
- Verify:
  - Response status code is 422
  - Error message indicates validation errors for query length

#### Integration Tests

**test_search_users_success**
- Create test users in the database with various usernames and emails
- Call the endpoint with a query that matches some users
- Verify:
  - Response status code is 200
  - Response contains matching users and correct total count
  - Only users matching the query are returned

**test_search_users_empty_results**
- Call the endpoint with a query that matches no users
- Verify:
  - Response status code is 200
  - Response contains empty users list and zero total count

**test_search_users_pagination**
- Create multiple test users in the database
- Call the endpoint with skip and limit parameters
- Verify:
  - Response status code is 200
  - Response contains correct number of users based on pagination
  - Total count reflects the actual number of matching users

### 3. GET /search/categories - Search categories by query string

#### Unit Tests

**test_search_categories_success**
- Mock `category_crud.search_categories` to return mock categories and total count
- Call the endpoint with a valid query string
- Verify:
  - Response status code is 200
  - Response contains categories and total count matching the mock data
  - `category_crud.search_categories` was called with correct parameters

**test_search_categories_empty_results**
- Mock `category_crud.search_categories` to return empty list and zero count
- Call the endpoint with a query string that returns no results
- Verify:
  - Response status code is 200
  - Response contains empty categories list and zero total count

**test_search_categories_missing_query**
- Call the endpoint without required query parameter
- Verify:
  - Response status code is 422
  - Error message indicates validation errors for missing query

**test_search_categories_short_query**
- Call the endpoint with a query string shorter than minimum length (1 character)
- Verify:
  - Response status code is 422
  - Error message indicates validation errors for query length

#### Integration Tests

**test_search_categories_success**
- Create test categories in the database with various names
- Call the endpoint with a query that matches some categories
- Verify:
  - Response status code is 200
  - Response contains matching categories and correct total count
  - Only categories matching the query are returned

**test_search_categories_empty_results**
- Call the endpoint with a query that matches no categories
- Verify:
  - Response status code is 200
  - Response contains empty categories list and zero total count

**test_search_categories_pagination**
- Create multiple test categories in the database
- Call the endpoint with skip and limit parameters
- Verify:
  - Response status code is 200
  - Response contains correct number of categories based on pagination
  - Total count reflects the actual number of matching categories

### 4. GET /search/tags - Search tags by query string

#### Unit Tests

**test_search_tags_success**
- Mock `tag_crud.search_tags` to return mock tags and total count
- Call the endpoint with a valid query string
- Verify:
  - Response status code is 200
  - Response contains tags and total count matching the mock data
  - `tag_crud.search_tags` was called with correct parameters

**test_search_tags_empty_results**
- Mock `tag_crud.search_tags` to return empty list and zero count
- Call the endpoint with a query string that returns no results
- Verify:
  - Response status code is 200
  - Response contains empty tags list and zero total count

**test_search_tags_missing_query**
- Call the endpoint without required query parameter
- Verify:
  - Response status code is 422
  - Error message indicates validation errors for missing query

**test_search_tags_short_query**
- Call the endpoint with a query string shorter than minimum length (1 character)
- Verify:
  - Response status code is 422
  - Error message indicates validation errors for query length

#### Integration Tests

**test_search_tags_success**
- Create test tags in the database with various names
- Call the endpoint with a query that matches some tags
- Verify:
  - Response status code is 200
  - Response contains matching tags and correct total count
  - Only tags matching the query are returned

**test_search_tags_empty_results**
- Call the endpoint with a query that matches no tags
- Verify:
  - Response status code is 200
  - Response contains empty tags list and zero total count

**test_search_tags_pagination**
- Create multiple test tags in the database
- Call the endpoint with skip and limit parameters
- Verify:
  - Response status code is 200
  - Response contains correct number of tags based on pagination
  - Total count reflects the actual number of matching tags

## Test Data and Fixtures

### Required Test Data

1. **Test Posts Fixture**
   - Posts with various titles and content for testing post search
   - Posts with specific keywords for targeted search tests

2. **Test Users Fixture**
   - Users with various usernames and emails for testing user search
   - Users with specific keywords for targeted search tests

3. **Test Categories Fixture**
   - Categories with various names for testing category search
   - Categories with specific keywords for targeted search tests

4. **Test Tags Fixture**
   - Tags with various names for testing tag search
   - Tags with specific keywords for targeted search tests

5. **Test Database Session**
   - Mock database session for unit tests
   - Real database session for integration tests (if needed)

### Mocking Strategies

1. **Database Operations**
   - Mock `post_crud.search_posts` function for post search tests
   - Mock `user_crud.search_users` function for user search tests
   - Mock `category_crud.search_categories` function for category search tests
   - Mock `tag_crud.search_tags` function for tag search tests
   - Use `unittest.mock.patch` to mock specific CRUD functions

2. **Dependencies**
   - Mock `get_session` dependency to return mock database sessions

## Expected Responses and Status Codes

### Success Responses

1. `GET /search/posts` - 200 OK with `PostSearchResult` object
2. `GET /search/users` - 200 OK with `UserSearchResult` object
3. `GET /search/categories` - 200 OK with `CategorySearchResult` object
4. `GET /search/tags` - 200 OK with `TagSearchResult` object

### Error Responses

1. **422 Unprocessable Entity**
   - Missing required query parameter
   - Query parameter shorter than minimum length

## Test Execution

### Unit Tests
- Run with: `pytest backend/app/tests/unit/test_search.py`
- Focus on testing individual functions in isolation
- Use mocking to simulate database and external dependencies

### Integration Tests
- Run with: `pytest backend/app/tests/integration/test_search.py`
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
   - Create helper functions to generate test entities
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