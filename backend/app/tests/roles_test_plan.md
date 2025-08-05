# Roles Endpoints Test Plan

This document outlines a comprehensive test plan for the roles endpoints in `backend/app/api/v1/endpoints/roles.py`.

## Overview

The roles endpoints provide CRUD functionality for managing roles. Based on the existing CRUD operations and schema, there should be 5 endpoints:

1. `POST /roles/` - Create a new role
2. `GET /roles/` - Retrieve all roles
3. `GET /roles/{role_id}` - Get a specific role by id
4. `PUT /roles/{role_id}` - Update a role
5. `DELETE /roles/{role_id}` - Delete a role

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

1. `backend/app/tests/unit/test_roles.py` - Unit tests for roles endpoints
2. `backend/app/tests/integration/test_roles.py` - Integration tests for roles endpoints

## Detailed Test Cases

### 1. POST /roles/ - Create a new role

#### Unit Tests

**test_create_role_success**
- Mock `create_role` function to return a mock role
- Call the endpoint with valid role data
- Verify:
  - Response status code is 201
  - Response contains role data matching the mock role
  - `create_role` was called with correct parameters

**test_create_role_invalid_data**
- Call the endpoint with invalid role data
- Verify:
  - Response status code is 422
  - Error message indicates validation errors
  - `create_role` was not called

#### Integration Tests

**test_create_role_success**
- Call the endpoint with valid role data
- Verify:
  - Response status code is 201
  - Response contains role data matching the input
  - Role is actually stored in the database

### 2. GET /roles/ - Retrieve all roles

#### Unit Tests

**test_read_roles_success**
- Mock `get_all_roles` function to return a list of mock roles
- Call the endpoint
- Verify:
  - Response status code is 200
  - Response contains list of roles matching the mock data
  - `get_all_roles` was called

**test_read_roles_empty**
- Mock `get_all_roles` function to return an empty list
- Call the endpoint
- Verify:
  - Response status code is 200
  - Response contains an empty list

#### Integration Tests

**test_read_roles_success**
- Create multiple roles in the database
- Call the endpoint
- Verify:
  - Response status code is 200
  - Response contains list of roles matching those in the database

**test_read_roles_empty**
- Call the endpoint when no roles exist in the database
- Verify:
  - Response status code is 200
  - Response contains an empty list

### 3. GET /roles/{role_id} - Get a specific role by id

#### Unit Tests

**test_read_role_by_id_success**
- Mock `get_role_by_id` function to return a mock role
- Call the endpoint with a valid role_id
- Verify:
  - Response status code is 200
  - Response contains role data matching the mock role
  - `get_role_by_id` was called with correct parameters

**test_read_role_by_id_not_found**
- Mock `get_role_by_id` function to raise HTTPException with 404 status
- Call the endpoint with a non-existent role_id
- Verify:
  - Response status code is 404
  - Error message indicates "Role not found"
  - `get_role_by_id` was called with correct parameters

#### Integration Tests

**test_read_role_by_id_success**
- Create a role in the database
- Call the endpoint with the role's ID
- Verify:
  - Response status code is 200
  - Response contains role data matching what was stored
  - All required fields are present in the response

**test_read_role_by_id_not_found**
- Call the endpoint with a non-existent role ID
- Verify:
  - Response status code is 404
  - Error message indicates "Role not found"

### 4. PUT /roles/{role_id} - Update a role

#### Unit Tests

**test_update_role_success**
- Mock `get_role_by_id` function to return an existing mock role
- Mock `update_role` function to return an updated mock role
- Call the endpoint with valid role update data
- Verify:
  - Response status code is 200
  - Response contains updated role data
  - `get_role_by_id` was called with correct parameters
  - `update_role` was called with correct parameters

**test_update_role_not_found**
- Mock `get_role_by_id` function to raise HTTPException with 404 status
- Call the endpoint with role update data
- Verify:
  - Response status code is 404
  - Error message indicates role not found
  - `update_role` was not called

**test_update_role_invalid_data**
- Mock `get_role_by_id` function to return an existing mock role
- Call the endpoint with invalid update data
- Verify:
  - Response status code is 422
  - Error message indicates validation errors
  - `update_role` was not called

#### Integration Tests

**test_update_role_success**
- Create a role in the database
- Call the endpoint with valid update data
- Verify:
  - Response status code is 200
  - Response contains updated role data
  - Role data in database has been updated correctly

**test_update_role_not_found**
- Call the endpoint with update data and a non-existent role ID
- Verify:
  - Response status code is 404
  - Error message indicates role not found

**test_update_role_partial**
- Create a role in the database
- Call the endpoint with partial update data (only name)
- Verify:
  - Response status code is 200
  - Response contains updated name
  - Only the specified field was updated in the database

### 5. DELETE /roles/{role_id} - Delete a role

#### Unit Tests

**test_delete_role_success**
- Mock `get_role_by_id` function to return an existing mock role
- Mock `delete_role` function to return None (successful deletion)
- Call the endpoint with a valid role_id
- Verify:
  - Response status code is 204
  - Response body is empty
  - `get_role_by_id` was called with correct parameters
  - `delete_role` was called with correct parameters

**test_delete_role_not_found**
- Mock `get_role_by_id` function to raise HTTPException with 404 status
- Call the endpoint with a non-existent role_id
- Verify:
  - Response status code is 404
  - Error message indicates "Role not found"
  - `delete_role` was not called

#### Integration Tests

**test_delete_role_success**
- Create a role in the database
- Call the endpoint with the role's ID
- Verify:
  - Response status code is 204
  - Response body is empty
  - Role no longer exists in the database

**test_delete_role_not_found**
- Call the endpoint with a non-existent role ID
- Verify:
  - Response status code is 404
  - Error message indicates "Role not found"

## Test Data and Fixtures

### Required Test Data

1. **Test Roles Fixture**
   - Roles with name and description for testing role operations
   - Valid role data that matches the Role model schema

2. **Test Database Session**
   - Mock database session for unit tests
   - Real database session for integration tests (if needed)

### Mocking Strategies

1. **Database Operations**
   - Mock `create_role` function for role creation
   - Mock `get_all_roles` function for role listing
   - Mock `get_role_by_id` function for role retrieval
   - Mock `update_role` function for role update
   - Mock `delete_role` function for role deletion
   - Use `unittest.mock.patch` to mock specific CRUD functions

2. **Dependencies**
   - Mock `get_session` dependency to return mock database sessions

## Expected Responses and Status Codes

### Success Responses

1. `POST /roles/` - 201 Created with `RoleRead` object
2. `GET /roles/` - 200 OK with list of `RoleRead` objects
3. `GET /roles/{role_id}` - 200 OK with `RoleRead` object
4. `PUT /roles/{role_id}` - 200 OK with `RoleRead` object
5. `DELETE /roles/{role_id}` - 204 No Content with empty response body

### Error Responses

1. **404 Not Found**
   - Role not found when retrieving, updating, or deleting by ID

2. **422 Unprocessable Entity**
   - Validation errors in role data
   - Missing required fields in request body

## Test Execution

### Unit Tests
- Run with: `pytest backend/app/tests/unit/test_roles.py`
- Focus on testing individual functions in isolation
- Use mocking to simulate database and external dependencies

### Integration Tests
- Run with: `pytest backend/app/tests/integration/test_roles.py`
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
   - Create helper functions to generate test roles
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