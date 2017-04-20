from flask_mongoengine import MongoEngine
from mongoengine import *

db = MongoEngine()
connect('songsdb')


class Song(db.Document):
    artist = StringField(required=True)
    title = StringField(required=True)
    difficulty = DecimalField(required=True)
    level = IntField(required=True)
    released = StringField(required=True)
    rating = IntField(min_value=1, max_value=5)

    def as_json(self):
        return {
            'id': str(self.id),
            'artist': self.artist,
            'title': self.title,
            'difficulty': float(str(self.difficulty)),
            'level': self.level,
            'released': self.released,
            'rating': self.rating,
        }


def populate_songs_db():
    Song(artist='Mr Fastfinger', title='Awaki-Waki', difficulty=15, level=13, released='2012-05-11').save()
    Song(artist='The Yousicians', title='A New Kennel', difficulty=9.1, level=9, released='2010-02-03').save()
    Song(artist='The Yousicians', title='Alabama Sunrise', difficulty=5, level=6, released='2016-04-01').save()
    Song(artist='The Yousicians', title="Can't Buy Me Skills", difficulty=9, level=9, released='2016-05-01').save()
    Song(artist='The Yousicians', title='Babysitting', difficulty=7, level=6, released='2016-07-01').save()
    Song(artist='The Yousicians', title='Wishing In The Night', difficulty=10.98, level=9, released='2016-01-01').save()
    Song(artist='The Yousicians', title='Vivaldi Allegro Mashup', difficulty=13, level=13, released='2016-06-01').save()
    Song(
        artist='The Yousicians', title='Lycanthropic Metamorphosis', difficulty=14.6, level=13, released='2016-10-26'
    ).save()
    Song(
        artist='The Yousicians', title="You've Got The Power", difficulty=13.22, level=13, released='2014-12-20'
    ).save()
    Song(
        artist='The Yousicians', title='Opa Opa Ta Bouzoukia', difficulty=14.66, level=13, released='2013-04-27'
    ).save()
    Song(
        artist='The Yousicians', title='Greasy Fingers - boss level', difficulty=2, level=3, released='2016-03-01'
    ).save()


if not Song.objects.all():
    populate_songs_db()
