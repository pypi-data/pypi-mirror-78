import os
import sys
import unittest
import json
from unittest.mock import Mock, MagicMock, patch, PropertyMock
from ..test_utils import mockSessionResponse, Fake_Session_Mock
from ..test_utils import run_mix
from ...mixtapes import Mixtapes, Session
from ...utils import request

Session = request.Session
Session.TIMEOUT = 180

mix = run_mix("hot")
# search_mix = run_mix(search="jay-z")


class TestMixtapes(unittest.TestCase):
    Mixtapes._session = PropertyMock(return_value=mockSessionResponse)

    def test_category_set_correct(self):
        # testing category
        results = mix.artists
        self.assertIsNotNone(results)

    @patch.object(Mixtapes, "_getMixtapeResponse")
    def test_start_function(self, start):
        start(start="lil wayne")
        # mix = self.mix
        start.assert_called_once()
        start.assert_called_once_with(start="lil wayne")

    def test_if_mixtapes_has_attributes(self):
        assert hasattr(mix, "artist") == False
        self.assertEqual(len(mix.artists), 12)
        self.assertEqual(len(mix.links), 12)
        self.assertEqual(len(mix.views), 12)

    @patch.object(Mixtapes, "artists", autospec=True)
    def test_artist_found_length(self, MT):
        MT.return_value = ["Jay-z", "Lil wayne", "1", "2", "3", "4"]
        self.assertEqual(len(mix.artists.return_value), 6)

    def test_search_has_results(self):
        session = mix._session
        session.method = Mock(return_value="Jay-Z")
        results = mix.search("anything")
        self.assertEqual(results, "Jay-Z")

    def test_search_parameters(self):
        # testing for serch to return None value
        results = mix.search("")
        self.assertEqual(results, None)

    @patch.object(Mixtapes, "artists", autospec=True)
    def test_artist_found_length(self, MT):
        MT.return_value = ["Jay-z", "Lil wayne", "1", "2", "3", "4"]
        self.assertEqual(len(mix.artists.return_value), 6)

    @patch.object(Mixtapes, "search", autospec=True)
    def test_search_function_called_once(self, MT):
        session = mix._session
        session.method = Mock(return_value="Jay-Z")
        MT.return_value = None
        mix._getMixtapeResponse(search="Jay-Z")
        count = MT.call_count
        self.assertEqual(count, 1)
