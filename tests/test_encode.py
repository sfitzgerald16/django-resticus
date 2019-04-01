import json

from django.test import TestCase
from resticus import encoders
from resticus.iterators import iterlist, iterdict


class TestEncode(TestCase):
    def setUp(self):
        self.encoder = encoders.JSONEncoder()

    def test_generator_default(self):
        encoded = self.encoder.default((x for x in range(10)))
        assert isinstance(encoded, iterlist)

    def test_encode_iterlist(self):
        generator = (x for x in range(10))
        encoded = self.encoder.encode(generator)
        assert encoded == json.dumps([x for x in range(10)])

    def test_iterencode_iterlist(self):
        generator = (x for x in range(10))
        encoded = ''.join(self.encoder.iterencode(generator))
        assert encoded == json.dumps([x for x in range(10)])

    def test_encode_iterdict(self):
        generator = iterdict((str(x), x) for x in range(10))
        encoded = self.encoder.encode(generator)
        assert encoded == json.dumps({str(x): x for x in range(10)})

    def test_iterencode_iterdict(self):
        generator = iterdict((str(x), x) for x in range(10))
        encoded = ''.join(self.encoder.iterencode(generator))
        assert encoded == json.dumps({str(x): x for x in range(10)})
