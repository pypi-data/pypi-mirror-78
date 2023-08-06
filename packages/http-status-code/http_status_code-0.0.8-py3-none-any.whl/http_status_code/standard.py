from . import StatusCode

# General
successful_request = StatusCode(200, 'Successful request')
bad_request = StatusCode(400, 'Bad request')
unauthorized_request = StatusCode(403, 'You are not authorized')
resource_not_found = StatusCode(404, 'The required resource is not found')
request_args_validation_error = StatusCode(410, 'Request arguments (query string or body) validation error')

# Authentication (Codes start from 430)
invalid_credentials = StatusCode(430, 'Invalid credentials')
inactive_account = StatusCode(431, 'Your account is inactive')
missing_token = StatusCode(432, 'Missing token')
invalid_token = StatusCode(433, 'The token is invalid')
expired_token = StatusCode(434, 'The token is expired')
wrong_token = StatusCode(435, 'Wrong token error (related to refresh and access tokens)')
logged_out = StatusCode(436, 'You have logged out. Please log in again')
account_deleted = StatusCode(437, 'Your account has been deleted')

# Database
duplicate_entry = StatusCode(630, 'This record already exists')
related_existing_record = StatusCode(631, 'This record is related to other records. Therefore, it cannot be deleted')
no_result_match = StatusCode(632, 'No result match your search parameters')
