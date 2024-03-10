import unittest
from unittest.mock import MagicMock, patch
from main import generate_response, send_audio, send_text_message, bot, client

class TestTelegramBot(unittest.TestCase):
    @patch('main.generate_response')
    def test_generate_response(self, mock_generate_response):
        mock_generate_response.return_value = ("Response text", "Audio content")
        question = "Como falar oi em italiano?"
        response_text, audio_content = generate_response(question)
        self.assertEqual(response_text, "Response text")
        self.assertEqual(audio_content, "Audio content")

    @patch('main.send_audio')
    def test_send_audio(self, mock_send_audio):
        # Mock the message object
        message = MagicMock()
        message.chat.id = "test_chat_id"

        audio_content = "This is a test audio content."
        send_audio(message, audio_content)

        # Assert that send_audio function was called with correct parameters
        mock_send_audio.assert_called_with(message, audio_content)

    @patch('main.bot.reply_to')
    @patch('main.generate_response')
    def test_send_text_message(self, mock_generate_response, mock_reply_to):
        # Mock the message object
        message = MagicMock()
        message.text = "This is a test message."

        mock_generate_response.return_value = ("Expected response text", "Audio content")

        send_text_message(message)

        # Assert that reply_to function was called with non-empty response
        mock_reply_to.assert_called_with(message, "Expected response text")

if __name__ == '__main__':
    unittest.main()
