import logging
import os
import tempfile
import unittest
from unittest.mock import patch, MagicMock
from utils.logging import setup_logging

class TestLoggingSetup(unittest.TestCase):
    def setUp(self):
        # Create temporary log file
        self.temp_log = tempfile.NamedTemporaryFile(delete=False)
        self.log_path = self.temp_log.name
        self.temp_log.close()

    def tearDown(self):
        # Clean up temporary log file
        if os.path.exists(self.log_path):
            os.unlink(self.log_path)

    @patch('utils.logging.Config')
    @patch('utils.logging.logging.FileHandler')
    @patch('utils.logging.logging.StreamHandler')
    def test_logging_setup(self, mock_stream, mock_file, mock_config):
        """Test logging configuration with handlers and formatters"""
        # Mock config settings
        mock_config.LOG_LEVEL = logging.INFO
        
        # Mock file handler to use temp file
        mock_file.return_value = logging.FileHandler(self.log_path)
        
        # Call setup
        logger = setup_logging()
        
        # Verify logger config
        self.assertEqual(logger.level, logging.INFO)
        self.assertEqual(len(logger.handlers), 2)
        
        # Verify formatters
        for handler in logger.handlers:
            self.assertIsNotNone(handler.formatter)
            format_str = handler.formatter._fmt
            self.assertIn('%(asctime)s', format_str)
            self.assertIn('%(name)s', format_str)
            self.assertIn('%(levelname)s', format_str)
            self.assertIn('%(message)s', format_str)

    @patch('utils.logging.Config')
    def test_log_file_creation(self, mock_config):
        """Test that logs are written to file"""
        mock_config.LOG_LEVEL = logging.DEBUG
        
        # Setup logging
        logger = setup_logging()
        
        # Write test log
        test_message = "TEST_LOG_MESSAGE_123"
        logger.debug(test_message)
        
        # Force log flush
        for handler in logger.handlers:
            handler.flush()
        
        # Verify log content
        with open(self.log_path, 'r') as log_file:
            content = log_file.read()
            self.assertIn(test_message, content)

    @patch('utils.logging.Config')
    def test_log_level_config(self, mock_config):
        """Test different log level configurations"""
        test_cases = [
            ('DEBUG', logging.DEBUG),
            ('INFO', logging.INFO),
            ('WARNING', logging.WARNING),
            ('ERROR', logging.ERROR),
            ('CRITICAL', logging.CRITICAL)
        ]
        
        for level_name, level_value in test_cases:
            mock_config.LOG_LEVEL = level_value
            logger = setup_logging()
            self.assertEqual(logger.level, level_value)

if __name__ == '__main__':
    unittest.main()