import json
import unittest
import app
from models import Song


class AverageDifficultyTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.app.test_client()
        Song.objects.all().delete()
        self._populate_database()

    def tearDown(self):
        Song.objects.all().delete()

    def test_it_returns_zero_when_no_music_was_found_in_level(self):
        self._assert_average_difficulty('/songs/avg/difficulty?level=5', 0)

    def test_it_returns_global_average_if_no_level_filter(self):
        self._assert_average_difficulty('/songs/avg/difficulty', 3)

    def test_it_returns_level_average_difficulty(self):
        self._assert_average_difficulty('/songs/avg/difficulty?level=1', 2)
        self._assert_average_difficulty('/songs/avg/difficulty?level=2', 6)

    def _assert_average_difficulty(self, url, average_value):
        response = self.app.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)['average'], average_value)

    def test_it_validates_invalid_parameters(self):
        response = self.app.get('/songs/avg/difficulty?level=0')
        self.assertEqual(response.status_code, 400)
        self.assertIn('level', json.loads(response.data)['message'])
        response = self.app.get('/songs/avg/difficulty?level=-1')
        self.assertEqual(response.status_code, 400)
        self.assertIn('level', json.loads(response.data)['message'])
        response = self.app.get('/songs/avg/difficulty?level=asdasda')
        self.assertEqual(response.status_code, 400)
        self.assertIn('level', json.loads(response.data)['message'])

    @staticmethod
    def _populate_database():
        Song(artist='myself', title='first song', level=1, difficulty=1, released='2017-01-11').save()
        Song(artist='myself', title='second song', level=1, difficulty=2, released='2017-01-12').save()
        Song(artist='myself', title='third song', level=1, difficulty=3, released='2017-01-13').save()
        Song(artist='myself', title='fourth song', level=2, difficulty=6, released='2017-01-14').save()


if __name__ == '__main__':
    unittest.main()
