import json
import unittest
import app
from models import Song


class GetAllSongsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.app.test_client()
        Song.objects.all().delete()

    def test_it_validates_invalid_parameters(self):
        response = self.app.get('/songs?current_page=asd&page_size=1')
        self.assertEqual(response.status_code, 400)
        self.assertIn('current_page', json.loads(response.data)['message'])
        response = self.app.get('/songs?current_page=0&page_size=1')
        self.assertEqual(response.status_code, 400)
        self.assertIn('current_page', json.loads(response.data)['message'])
        response = self.app.get('/songs?current_page=-1&page_size=1')
        self.assertEqual(response.status_code, 400)
        self.assertIn('current_page', json.loads(response.data)['message'])

        response = self.app.get('/songs?current_page=1&page_size=asd')
        self.assertEqual(response.status_code, 400)
        self.assertIn('page_size', json.loads(response.data)['message'])
        response = self.app.get('/songs?current_page=1&page_size=0')
        self.assertEqual(response.status_code, 400)
        self.assertIn('page_size', json.loads(response.data)['message'])
        response = self.app.get('/songs?current_page=1&page_size=-1')
        self.assertEqual(response.status_code, 400)
        self.assertIn('page_size', json.loads(response.data)['message'])

    def test_it_returns_empty_list(self):
        response = self.app.get('/songs')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), [])

    def test_it_paginates_data(self):
        self._populate_database()
        self._assert_response_size('/songs?current_page=1&page_size=3', 3)
        self._assert_response_size('/songs?current_page=2&page_size=3', 1)

    def _assert_response_size(self, url, size):
        response = self.app.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json.loads(response.data)), size)

    def test_it_returns_page_not_found(self):
        self._populate_database()
        response = self.app.get('/songs?current_page=2&page_size=5')
        self.assertEqual(response.status_code, 404)

    def _populate_database(self):
        Song(artist='myself', title='first song', level=11, difficulty=1, released='2017-01-11').save()
        Song(artist='myself', title='second song', level=12, difficulty=2, released='2017-01-12').save()
        Song(artist='myself', title='third song', level=13, difficulty=3, released='2017-01-13').save()
        Song(artist='myself', title='fourth song', level=14, difficulty=4, released='2017-01-14').save()

if __name__ == '__main__':
    unittest.main()
