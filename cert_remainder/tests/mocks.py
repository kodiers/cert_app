from unittest.mock import Mock


def create_mock_request(user: 'User') -> Mock:
    """
    Create mock request with user variable
    """
    mock_request = Mock()
    mock_request.user = user
    return mock_request
