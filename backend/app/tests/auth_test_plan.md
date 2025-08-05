# Auth Endpoints Test Plan

This document outlines a comprehensive test plan for the auth endpoints in `backend/app/api/v1/endpoints/auth.py`.

## Overview

The auth endpoints provide authentication functionality for users. There are 5 endpoints:

1. `POST /auth/login` - Authenticate user and return JWT token
2. `POST /auth/logout` - Logout user by invalidating the token
3. `POST /auth/refresh` - Refresh JWT token
4. `POST /auth/forgot-password` - Request password reset
5. `POST /auth/reset-password` - Reset password with token

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

1. `backend/app/tests/unit/test_auth.py` - Unit tests for auth endpoints
2. `backend/app/tests/integration/test_auth.py` - Integration tests for auth endpoints

## Detailed Test Cases

### 1. POST /auth/login - Authenticate user and return JWT token

#### Unit Tests

**test_login_success**
- Mock `authenticate_user` to return a mock user
- Call the endpoint with valid credentials
- Verify:
  - Response status code is 200
  - Response contains access_token and token_type
  - `authenticate_user` was called with correct parameters
  - `create_access_token` was called with correct parameters

**test_login_invalid_credentials**
- Mock `authenticate_user` to return None
- Call the endpoint with invalid credentials
- Verify:
  - Response status code is 401
  - Error message indicates incorrect email or password
  - Response includes WWW-Authenticate header

**test_login_missing_fields**
- Call the endpoint with missing required fields
- Verify:
  - Response status code is 422
  - Error message indicates validation errors

#### Integration Tests

**test_login_success**
- Create a test user with hashed password
- Call the endpoint with valid credentials
- Verify:
  - Response status code is 200
  - Response contains access_token and token_type
  - Token can be decoded and contains correct user ID

**test_login_invalid_credentials**
- Call the endpoint with invalid credentials
- Verify:
  - Response status code is 401
  - Error message indicates incorrect email or password
  - Response includes WWW-Authenticate header

**test_login_missing_fields**
- Call the endpoint with missing required fields
- Verify:
  - Response status code is 422
  - Error message indicates validation errors

### 2. POST /auth/logout - Logout user by invalidating the token

#### Unit Tests

**test_logout_success**
- Call the endpoint with a valid token
- Verify:
  - Response status code is 200
  - Response contains success message
  - In a real implementation, would check that token is added to blacklist

**test_logout_missing_token**
- Call the endpoint without required token field
- Verify:
  - Response status code is 422
  - Error message indicates validation errors

#### Integration Tests

**test_logout_success**
- Call the endpoint with a valid token
- Verify:
  - Response status code is 200
  - Response contains success message

**test_logout_missing_token**
- Call the endpoint without required token field
- Verify:
  - Response status code is 422
  - Error message indicates validation errors

### 3. POST /auth/refresh - Refresh JWT token

#### Unit Tests

**test_refresh_token_success**
- Call the endpoint with a valid refresh token
- Verify:
  - Response status code is 200
  - Response contains new access_token and token_type
  - New token is different from any previous token
  - In a real implementation, would validate the refresh token

**test_refresh_token_missing_fields**
- Call the endpoint with missing required fields
- Verify:
  - Response status code is 422
  - Error message indicates validation errors

#### Integration Tests

**test_refresh_token_success**
- Call the endpoint with a valid refresh token
- Verify:
  - Response status code is 200
  - Response contains new access_token and token_type
  - New token can be decoded and contains correct subject

**test_refresh_token_missing_fields**
- Call the endpoint with missing required fields
- Verify:
  - Response status code is 422
  - Error message indicates validation errors

### 4. POST /auth/forgot-password - Request password reset

#### Unit Tests

**test_forgot_password_success**
- Mock database operations to simulate user exists
- Call the endpoint with a valid email
- Verify:
  - Response status code is 200
  - Response contains success message
  - In a real implementation, would check that email would be sent

**test_forgot_password_user_not_found**
- Mock database operations to simulate user does not exist
- Call the endpoint with an email that doesn't exist
- Verify:
  - Response status code is 200
  - Response contains success message (for security reasons)
  - No email would be sent in real implementation

**test_forgot_password_invalid_email**
- Call the endpoint with an invalid email format
- Verify:
  - Response status code is 422
  - Error message indicates validation errors

#### Integration Tests

**test_forgot_password_success**
- Create a test user
- Call the endpoint with the user's email
- Verify:
  - Response status code is 200
  - Response contains success message

**test_forgot_password_user_not_found**
- Call the endpoint with an email that doesn't exist
- Verify:
  - Response status code is 200
  - Response contains success message (for security reasons)

**test_forgot_password_invalid_email**
- Call the endpoint with an invalid email format
- Verify:
  - Response status code is 422
  - Error message indicates validation errors

### 5. POST /auth/reset-password - Reset password with token

#### Unit Tests

**test_reset_password_success**
- Mock `verify_password_reset_token` to return a valid email
- Mock database operations to simulate user exists and update
- Call the endpoint with a valid token and new password
- Verify:
  - Response status code is 200
  - Response contains success message
  - `verify_password_reset_token` was called with correct parameters
  - In a real implementation, would check that user's password was updated

**test_reset_password_invalid_token**
- Mock `verify_password_reset_token` to return None
- Call the endpoint with an invalid token
- Verify:
  - Response status code is 400
  - Error message indicates invalid or expired token

**test_reset_password_missing_fields**
- Call the endpoint with missing required fields
- Verify:
  - Response status code is 422
  - Error message indicates validation errors

#### Integration Tests

**test_reset_password_success**
- Generate a valid password reset token
- Call the endpoint with the token and new password
- Verify:
  - Response status code is 200
  - Response contains success message

**test_reset_password_invalid_token**
- Call the endpoint with an invalid token
- Verify:
  - Response status code is 400
  - Error message indicates invalid or expired token

**test_reset_password_missing_fields**
- Call the endpoint with missing required fields
- Verify:
  - Response status code is 422
  - Error message indicates validation errors

## Test Data and Fixtures

### Required Test Data

1. **Test User Fixture**
   - User with email and hashed password for testing login
   - Valid credentials for authentication tests

2. **Valid JWT Tokens**
   - Access tokens for testing authenticated endpoints
   - Refresh tokens for testing token refresh

3. **Password Reset Tokens**
   - Valid password reset tokens for testing reset functionality
   - Expired/invalid tokens for testing error cases

4. **Test Database Session**
   - Mock database session for unit tests
   - Real database session for integration tests (if needed)

### Mocking Strategies

1. **Database Operations**
   - Mock `authenticate_user` function for login tests
   - Mock `get_user_by_email` function for password reset tests
   - Mock `verify_password_reset_token` function for reset password tests
   - Use `unittest.mock.patch` to mock specific functions

2. **Dependencies**
   - Mock `get_session` dependency to return mock database sessions
   - Mock security functions like `create_access_token` if needed

3. **External Services**
   - Mock email sending functionality (not currently implemented but could be in future)
   - Mock JWT token encoding/decoding if needed for specific tests

## Expected Responses and Status Codes

### Success Responses

1. `POST /auth/login` - 200 OK with `Token` object
2. `POST /auth/logout` - 200 OK with success message
3. `POST /auth/refresh` - 200 OK with `Token` object
4. `POST /auth/forgot-password` - 200 OK with success message
5. `POST /auth/reset-password` - 200 OK with `PasswordResetSuccess` object

### Error Responses

1. **400 Bad Request**
   - Invalid or expired password reset token
   - Missing required fields in request body

2. **401 Unauthorized**
   - Invalid credentials for login
   - Missing or invalid JWT token

3. **422 Unprocessable Entity**
   - Validation errors in request body
   - Missing required fields

## Test Execution

### Unit Tests
- Run with: `pytest backend/app/tests/unit/test_auth.py`
- Focus on testing individual functions in isolation
- Use mocking to simulate database and external dependencies

### Integration Tests
- Run with: `pytest backend/app/tests/integration/test_auth.py`
- Test complete endpoint workflows
- May require a test database depending on implementation

## Implementation Notes

1. **Test File Structure**
   - Follow the existing pattern in `test_media.py` for both unit and integration tests
   - Use `@pytest.mark.asyncio` for async test functions
   - Use `TestClient` from `fastapi.testclient` for integration tests

2. **Mocking Approach**
   - Use `unittest.mock.patch` to mock specific functions
   - Mock at the level of security functions rather than database sessions where possible
   - Use `AsyncMock` for async functions

3. **Test Data Generation**
   - Create helper functions to generate test users, tokens, etc.
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

6. **Security Considerations**
   - Follow security best practices in tests (don't hardcode sensitive data)
   - Test both positive and negative security scenarios
   - Ensure error messages don't leak sensitive information