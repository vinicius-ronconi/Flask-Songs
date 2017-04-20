import json
import unittest
import app
from models import Song


class SearchSongsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.app.test_client()
        Song.objects.all().delete()
        self._populate_database()

    def tearDown(self):
        Song.objects.all().delete()

    def test_it_searches_on_artist_and_title(self):
        self._assert_search_results('/songs/search?query=myself', 4)
        self._assert_search_results('/songs/search?query=beatles', 1)
        self._assert_search_results('/songs/search?query=FIRST', 1)

    def _assert_search_results(self, url, record_count):
        response = self.app.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json.loads(response.data)), record_count)

    def test_it_validates_missing_parameter(self):
        response = self.app.get('/songs/search')
        self.assertEqual(response.status_code, 400)
        self.assertIn('query', json.loads(response.data)['message'])

    @staticmethod
    def _populate_database():
        Song(artist='myself', title='first song', level=1, difficulty=1, released='2017-01-11').save()
        Song(artist='myself', title='second song', level=1, difficulty=2, released='2017-01-12').save()
        Song(artist='Beatles', title='third song by myself', level=1, difficulty=3, released='2017-01-13').save()
        Song(artist='myself', title='fourth song', level=2, difficulty=6, released='2017-01-14').save()


if __name__ == '__main__':
    unittest.main()
