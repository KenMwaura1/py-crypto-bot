import unittest
from unittest.mock import MagicMock
from datetime import datetime
from bot_2 import on_message


class TestBot(unittest.TestCase):
    def test_on_message(self):
        # Mocking the WebSocket and Redis objects
        ws = MagicMock()
        r = MagicMock()

        # Creating a sample message
        message = {
            "k": {
                "s": "BTCUSDT",
                "x": True,
                "s": "BTCUSDT",
                "c": "50000.00",
                "o": "49000.00",
                "h": "51000.00",
                "l": "48000.00",
                "v": "1000.00",
            }
        }

        # Calling the on_message function
        on_message(ws, message)

        # Asserting that the necessary methods were called
        ws.assert_called_once()
        r.lpush.assert_called_once()


if __name__ == "__main__":
    unittest.main()
