from django.test import TestCase
from resticus.settings import APISettings


class TestSettings(TestCase):
    def test_import_error_message_maintained(self):
        """
        Make sure import errors are captured and raised sensibly.
        """
        settings = APISettings({
            'DEFAULT_AUTHENTICATION_CLASSES': [
                'tests.invalid_module.InvalidClassName'
            ]
        })
        with self.assertRaises(ImportError):
            settings.DEFAULT_AUTHENTICATION_CLASSES

    def test_class_imports(self):
        assert api_settings.JSON_DECODER == encoders.JSONDecoder
        assert api_settings.JSON_ENCODER == encoders.JSONEncoder
