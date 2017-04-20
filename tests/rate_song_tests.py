import json
import unittest
import app
from models import Song


class RateSongTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.app.test_client()
        Song.objects.all().delete()
        self.song = Song(artist='myself', title='first song', level=1, difficulty=1, released='2017-01-11').save()
        self.base_url = '/songs/rating/{song_id}'.format(song_id=self.song.id)

    def tearDown(self):
        Song.objects.all().delete()

    def test_it_updates_song_rating(self):
        response = self.app.post('{base_url}?rating=5'.format(base_url=self.base_url))
        self.assertEqual(response.status_code, 200)
        self.assertIn(str(self.song.id), json.loads(response.data)['id'])
        self.assertEqual(json.loads(response.data)['rating'], 5)
        updated_song = Song.objects.get(pk=self.song.id)
        self.assertEqual(updated_song.rating, 5)

    def test_it_returns_404_on_invalid_song_id(self):
        response = self.app.post('/songs/rating/some_invalid_song_id?rating=5')
        self.assertEqual(response.status_code, 404)

    def test_it_validates_invalid_parameters(self):
        response = self.app.post(self.base_url)
        self.assertEqual(response.status_code, 400)
        self.assertIn('rating', json.loads(response.data)['message'])
        response = self.app.post('{base_url}?rating=0'.format(base_url=self.base_url))
        self.assertEqual(response.status_code, 400)
        self.assertIn('rating', json.loads(response.data)['message'])
        response = self.app.post('{base_url}?rating=6'.format(base_url=self.base_url))
        self.assertEqual(response.status_code, 400)
        self.assertIn('rating', json.loads(response.data)['message'])
        response = self.app.post('{base_url}?rating=asdfg'.format(base_url=self.base_url))
        self.assertEqual(response.status_code, 400)
        self.assertIn('rating', json.loads(response.data)['message'])

        response = self.app.get('{base_url}?rating=4'.format(base_url=self.base_url))
        self.assertEqual(response.status_code, 405)


if __name__ == '__main__':
    unittest.main()
