from unittest.mock import MagicMock, patch
import zmq
from eg1.api.runners import your_listener_function  # Replace with your actual function

def test_zeromq_listener():
    with patch('zmq.Context') as MockContext:
        mock_socket = MagicMock()
        MockContext.return_value.socket.return_value = mock_socket
        mock_socket.recv.return_value = b"test message"

        # Call your listener function
        your_listener_function()

        # Assert that the message was processed as expected
        # Example: assert some_function_was_called_with("test message")
