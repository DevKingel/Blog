# Profile Endpoints Test Plan

This document outlines a comprehensive test plan for the profile endpoints in `backend/app/api/v1/endpoints/profile.py`.

## Overview

The profile endpoints provide functionality for users to view and update their own profile information. There are 2 endpoints:

1. `GET /profile/` - Get current user's profile
2. `PUT /profile/` - Update current user's profile

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

1. `backend/app/tests/unit/test_profile.py` - Unit tests for profile endpoints
2. `backend/app/tests/integration/test_profile.py` - Integration tests for profile endpoints

## Detailed Test Cases

### 1. GET /profile/ - Get current user's profile

#### Unit Tests

**test_get_current_user_profile_success**
- Mock `get_user_by_id` to return a mock user
- Call the endpoint with a valid user_id
- Verify:
  - Response status code is 200
  - Response contains user profile data matching the mock user
  - `get_user_by_id` was called with correct parameters

**test_get_current_user_profile_user_not_found**
- Mock `get_user_by_id` to return None
- Call the endpoint with a non-existent user_id
- Verify:
  - Response status code is 404
  - Error message indicates "User not found"
  - `get_user_by_id` was called with correct parameters

#### Integration Tests

**test_get_current_user_profile_success**
- Create a test user in the database
- Call the endpoint with the user's ID
- Verify:
  - Response status code is 200
  - Response contains user profile data matching the created user
  - All required fields are present in the response

**test_get_current_user_profile_user_not_found**
- Call the endpoint with a non-existent user ID
- Verify:
  - Response status code is 404
  - Error message indicates "User not found"

### 2. PUT /profile/ - Update current user's profile

#### Unit Tests

**test_update_current_user_profile_success**
- Mock `get_user_by_id` to return a mock user
- Mock `update_user` to return an updated mock user
- Call the endpoint with valid profile update data
- Verify:
  - Response status code is 200
  - Response contains updated user profile data
  - `get_user_by_id` was called with correct parameters
  - `update_user` was called with correct parameters
  - Only non-None values from ProfileUpdate are passed to update_user

**test_update_current_user_profile_user_not_found_get**
- Mock `get_user_by_id` to return None
- Call the endpoint with profile update data
- Verify:
  - Response status code is 404
  - Error message indicates "User not found"
  - `update_user` was not called

**test_update_current_user_profile_user_not_found_update**
- Mock `get_user_by_id` to return a mock user
- Mock `update_user` to return None
- Call the endpoint with profile update data
- Verify:
  - Response status code is 404
  - Error message indicates "User not found"
  - Both `get_user_by_id` and `update_user` were called

**test_update_current_user_profile_invalid_data**
- Mock `get_user_by_id` to return a mock user
- Call the endpoint with invalid profile update data
- Verify:
  - Response status code is 422
  - Error message indicates validation errors
  - `update_user` was not called

#### Integration Tests

**test_update_current_user_profile_success**
- Create a test user in the database
- Call the endpoint with valid profile update data
- Verify:
  - Response status code is 200
  - Response contains updated user profile data
  - User data in database has been updated correctly

**test_update_current_user_profile_user_not_found**
- Call the endpoint with profile update data and a non-existent user ID
- Verify:
  - Response status code is 404
  - Error message indicates "User not found"

**test_update_current_user_profile_partial_update**
- Create a test user in the database
- Call the endpoint with partial profile update data (only username, not email)
- Verify:
  - Response status code is 200
  - Response contains updated username but unchanged email
  - Only the specified field was updated in the database

## Test Data and Fixtures

### Required Test Data

1. **Test User Fixture**
   - User with username, email, and hashed password for testing profile operations
   - Valid user data that matches the User model schema

2. **Profile Update Data**
   - Valid profile update data with username and email
   - Partial profile update data (only username or only email)
   - Invalid profile update data for testing validation errors

3. **Test Database Session**
   - Mock database session for unit tests
   - Real database session for integration tests (if needed)

### Mocking Strategies

1. **Database Operations**
   - Mock `get_user_by_id` function for both GET and PUT endpoints
   - Mock `update_user` function for PUT endpoint
   - Use `unittest.mock.patch` to mock specific CRUD functions

2. **Dependencies**
   - Mock `get_session` dependency to return mock database sessions
   - Mock any security functions if needed for future extensions

3. **User Authentication**
   - In unit tests, pass user_id directly as parameter (as in current implementation)
   - In integration tests, may need to implement authentication helpers if authentication is added to profile endpoints

## Expected Responses and Status Codes

### Success Responses

1. `GET /profile/` - 200 OK with `ProfileRead` object
2. `PUT /profile/` - 200 OK with `ProfileRead` object

### Error Responses

1. **404 Not Found**
   - User not found when retrieving profile
   - User not found when updating profile

2. **422 Unprocessable Entity**
   - Validation errors in profile update data
   - Missing required fields in request body

## Test Execution

### Unit Tests
- Run with: `pytest backend/app/tests/unit/test_profile.py`
- Focus on testing individual functions in isolation
- Use mocking to simulate database and external dependencies

### Integration Tests
- Run with: `pytest backend/app/tests/integration/test_profile.py`
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
   - Create helper functions to generate test users
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

6. **Authorization Testing**
   - Currently, the profile endpoints don't implement authorization checks
   - When authorization is added, tests should verify:
     - Users can only access their own profile
     - Unauthorized users receive appropriate error responses