# Media Endpoints Test Plan

This document outlines a comprehensive test plan for the media endpoints in `backend/app/api/v1/endpoints/media.py`.

## Overview

The media endpoints provide functionality for uploading, listing, and deleting media files. There are 3 endpoints:

1. `POST /` - Upload a new media file
2. `GET /` - List all uploaded media with pagination
3. `DELETE /{media_id}` - Delete a media entry and its associated file

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

1. `backend/app/tests/unit/test_media.py` - Unit tests for media endpoints (already exists but may need expansion)
2. `backend/app/tests/integration/test_media.py` - Integration tests for media endpoints (exists but needs completion)

## Detailed Test Cases

### 1. POST / - Upload a new media file

#### Unit Tests

**test_upload_media_success**
- Mock file validation to pass (valid content type and size)
- Mock file reading to return sample data
- Mock file writing to simulate successful file save
- Mock `media_crud.create_media` to return a mock media object
- Mock `get_session` dependency to return a mock database session
- Call the endpoint with a valid file
- Verify:
  - Response status code is 201 (Created)
  - Response contains expected media fields
  - File was "written" to the correct location
  - `media_crud.create_media` was called with correct parameters
  - File validation was performed

**test_upload_media_invalid_content_type**
- Mock file with invalid content type (e.g., "application/exe")
- Mock `get_session` dependency to return a mock database session
- Call the endpoint with the invalid file
- Verify:
  - Response status code is 400 (Bad Request)
  - Error message indicates file type not allowed
  - File was not saved
  - Database entry was not created

**test_upload_media_file_too_large**
- Mock file with valid content type but size exceeding MAX_FILE_SIZE
- Mock `get_session` dependency to return a mock database session
- Call the endpoint with the large file
- Verify:
  - Response status code is 413 (Request Entity Too Large)
  - Error message indicates file size exceeds limit
  - File was not saved
  - Database entry was not created

**test_upload_media_db_error**
- Mock file validation to pass
- Mock file reading and writing to succeed
- Mock `media_crud.create_media` to raise an exception
- Mock `get_session` dependency to return a mock database session
- Call the endpoint with a valid file
- Verify:
  - Appropriate error response is returned
  - File cleanup occurs (uploaded file is removed)
  - Exception is handled properly

**test_upload_media_file_write_error**
- Mock file validation to pass
- Mock file reading to succeed
- Mock file writing to raise an exception
- Mock `get_session` dependency to return a mock database session
- Call the endpoint with a valid file
- Verify:
  - Appropriate error response is returned
  - No database entry was created
  - Exception is handled properly

#### Integration Tests

**test_upload_media_success**
- Create a temporary file with valid content
- Call the endpoint with the file
- Verify:
  - Response status code is 201 (Created)
  - Response contains expected media fields
  - File exists in the media directory
  - Database entry was created with correct information
  - File path in database matches actual file location

**test_upload_media_invalid_content_type**
- Create a temporary file with invalid content type
- Call the endpoint with the file
- Verify:
  - Response status code is 400 (Bad Request)
  - Error message indicates file type not allowed
  - File was not saved to media directory
  - No database entry was created

**test_upload_media_file_too_large**
- Create a temporary file larger than MAX_FILE_SIZE
- Call the endpoint with the file
- Verify:
  - Response status code is 413 (Request Entity Too Large)
  - Error message indicates file size exceeds limit
  - File was not saved to media directory
  - No database entry was created

**test_upload_media_no_file**
- Call the endpoint without providing a file
- Verify:
  - Response status code is 422 (Unprocessable Entity)
  - Error message indicates file is required

### 2. GET / - List all uploaded media with pagination

#### Unit Tests

**test_list_media_success**
- Mock `media_crud.get_all_media` to return sample media entries
- Mock `get_session` dependency to return a mock database session
- Call the endpoint with default pagination parameters
- Verify:
  - Response status code is 200 (OK)
  - Response contains expected media list with pagination info
  - `media_crud.get_all_media` was called with correct parameters

**test_list_media_with_pagination**
- Mock `media_crud.get_all_media` to return sample media entries
- Mock `get_session` dependency to return a mock database session
- Call the endpoint with custom skip and limit parameters
- Verify:
  - Response status code is 200 (OK)
  - Response contains expected media list with correct pagination info
  - `media_crud.get_all_media` was called with correct skip/limit parameters

**test_list_media_empty_result**
- Mock `media_crud.get_all_media` to return empty list
- Mock `get_session` dependency to return a mock database session
- Call the endpoint
- Verify:
  - Response status code is 200 (OK)
  - Response contains empty media list with correct pagination info

**test_list_media_db_error**
- Mock `media_crud.get_all_media` to raise an exception
- Mock `get_session` dependency to return a mock database session
- Call the endpoint
- Verify:
  - Appropriate error response is returned
  - Exception is handled properly

#### Integration Tests

**test_list_media_success**
- Create several test media entries in database
- Call the endpoint
- Verify:
  - Response status code is 200 (OK)
  - Response contains expected media list with pagination info
  - All created media entries are in the response
  - Media entries contain correct information

**test_list_media_with_pagination**
- Create several test media entries in database (more than default limit)
- Call the endpoint with custom skip and limit parameters
- Verify:
  - Response status code is 200 (OK)
  - Response contains expected media list with correct pagination info
  - Pagination works correctly (correct page, size, total)

**test_list_media_empty_result**
- Ensure no media entries exist in database
- Call the endpoint
- Verify:
  - Response status code is 200 (OK)
  - Response contains empty media list with correct pagination info

### 3. DELETE /{media_id} - Delete a media entry and its associated file

#### Unit Tests

**test_delete_media_success**
- Mock `media_crud.get_media_by_id` to return a mock media object
- Mock file system operations to simulate file exists and successful deletion
- Mock `media_crud.delete_media` to return True
- Mock `get_session` dependency to return a mock database session
- Call the endpoint with a valid media ID
- Verify:
  - Response status code is 204 (No Content)
  - File was deleted from file system
  - `media_crud.delete_media` was called with correct parameters
  - `media_crud.get_media_by_id` was called with correct parameters

**test_delete_media_not_found**
- Mock `media_crud.get_media_by_id` to raise HTTPException (404)
- Mock `get_session` dependency to return a mock database session
- Call the endpoint with a non-existent media ID
- Verify:
  - Response status code is 404 (Not Found)
  - Error message indicates media not found
  - No file operations were performed

**test_delete_media_file_not_found**
- Mock `media_crud.get_media_by_id` to return a mock media object
- Mock file system operations to simulate file does not exist
- Mock `media_crud.delete_media` to return True
- Mock `get_session` dependency to return a mock database session
- Call the endpoint with a valid media ID
- Verify:
  - Response status code is 204 (No Content)
  - Database entry was deleted
  - No error occurred due to missing file

**test_delete_media_file_deletion_error**
- Mock `media_crud.get_media_by_id` to return a mock media object
- Mock file system operations to simulate file exists but deletion fails
- Mock `media_crud.delete_media` to return True
- Mock `get_session` dependency to return a mock database session
- Call the endpoint with a valid media ID
- Verify:
  - Response status code is 204 (No Content)
  - Database entry was deleted
  - Error in file deletion was logged but did not affect response

**test_delete_media_db_error**
- Mock `media_crud.get_media_by_id` to return a mock media object
- Mock file system operations to simulate successful file deletion
- Mock `media_crud.delete_media` to raise an exception
- Mock `get_session` dependency to return a mock database session
- Call the endpoint with a valid media ID
- Verify:
  - Appropriate error response is returned
  - File was deleted but database entry remains
  - Exception is handled properly

#### Integration Tests

**test_delete_media_success**
- Create a test media entry with actual file
- Call the endpoint with the media ID
- Verify:
  - Response status code is 204 (No Content)
  - File is deleted from file system
  - Database entry is deleted
  - Media entry no longer appears in list

**test_delete_media_not_found**
- Call the endpoint with a non-existent media ID
- Verify:
  - Response status code is 404 (Not Found)
  - Error message indicates media not found

**test_delete_media_file_not_found**
- Create a test media entry in database but ensure file does not exist
- Call the endpoint with the media ID
- Verify:
  - Response status code is 204 (No Content)
  - Database entry is deleted
  - No error occurs due to missing file

## Test Data and Fixtures

### Required Test Data

1. **Test Files**
   - Valid image files (JPEG, PNG, GIF, WEBP)
   - Valid document files (PDF, TXT)
   - Invalid files (EXE, other disallowed types)
   - Large files exceeding MAX_FILE_SIZE
   - Small files within size limits

2. **Media Objects**
   - Sample media entries for testing listing and deletion
   - Media entries with various content types
   - Media entries with various file sizes

3. **Test Database Session**
   - Mock database session for unit tests
   - Real database session for integration tests

### Mocking Strategies

1. **Database Operations**
   - Mock CRUD functions for unit tests:
     - `media_crud.create_media`
     - `media_crud.get_all_media`
     - `media_crud.get_media_by_id`
     - `media_crud.delete_media`
   - Use `unittest.mock.patch` to mock specific functions
   - For SQLAlchemy operations, mock the `execute` method on database sessions

2. **File Operations**
   - Mock file system operations:
     - `os.path.exists` to simulate file existence
     - `os.remove` to simulate file deletion
     - `open` to simulate file creation
   - Mock file reading/writing operations on `UploadFile` objects

3. **Dependencies**
   - Mock `get_session` dependency to return mock database sessions
   - Mock file validation methods if needed

4. **External Services**
   - Mock UUID generation if specific IDs are needed for testing
   - Mock file system path operations if needed

## Expected Responses and Status Codes

### Success Responses

1. `POST /` - 201 Created with `MediaRead` object
2. `GET /` - 200 OK with list of `MediaRead` objects
3. `DELETE /{media_id}` - 204 No Content

### Error Responses

1. **400 Bad Request**
   - Invalid file type provided
   - Missing required fields

2. **413 Request Entity Too Large**
   - File size exceeds MAX_FILE_SIZE limit

3. **404 Not Found**
   - Media entry not found when trying to delete
   - Invalid media_id

4. **422 Unprocessable Entity**
   - Missing file in upload request
   - Invalid request parameters

5. **500 Internal Server Error**
   - Database errors
   - File system errors

## Test Execution

### Unit Tests
- Run with: `pytest backend/app/tests/unit/test_media.py`
- Focus on testing individual functions in isolation
- Use mocking to simulate database and file system dependencies

### Integration Tests
- Run with: `pytest backend/app/tests/integration/test_media.py`
- Test complete endpoint workflows
- Use real file operations and database interactions
- Ensure proper cleanup of test files and database entries

## Implementation Notes

1. **Test File Structure**
   - Follow the existing pattern in `test_media.py` for both unit and integration tests
   - Use `@pytest.mark.asyncio` for async test functions
   - Use `TestClient` from `fastapi.testclient` for integration tests

2. **Mocking Approach**
   - Use `unittest.mock.patch` to mock specific functions
   - Mock at the level of CRUD functions rather than database sessions where possible
   - Use `AsyncMock` for async functions
   - Use `Mock` for file objects and file system operations

3. **Test Data Generation**
   - Create helper functions to generate test files
   - Use `uuid.uuid4()` for generating unique IDs
   - Ensure test data matches the expected schemas

4. **File Handling in Tests**
   - Use temporary directories for file operations in integration tests
   - Ensure proper cleanup of test files after each test
   - Test both successful and failed file operations

5. **Database Considerations**
   - For unit tests, fully mock database operations
   - For integration tests, use a test database or ensure proper cleanup
   - Ensure tests don't affect the development or production databases

6. **Error Handling Coverage**
   - Test all error scenarios identified in the implementation
   - Verify proper error messages and status codes
   - Ensure graceful handling of file system errors
   - Test edge cases like file not found during deletion