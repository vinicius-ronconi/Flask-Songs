from flask import Flask
from flask import jsonify
from flask import request
from flask.views import MethodView
from flask_mongoengine import MongoEngine
from controllers import SongsController
import exceptions


app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb://localhost/songsdb',
}
db = MongoEngine(app)

songs_controller = SongsController(db)


class AllSongsView(MethodView):
    def get(self):
        return jsonify(songs_controller.get_all_songs(request))


class AverageDifficultyView(MethodView):
    def get(self):
        return jsonify(songs_controller.get_average_difficulty(request))


class SongsSearchView(MethodView):
    def get(self):
        return jsonify(songs_controller.get_songs_by_keyword(request))


@app.errorhandler(exceptions.InvalidParameterError)
def handle_invalid_parameters(error):
    """
    :type error: exceptions.InvalidParameterError 
    :return: 
    """
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


app.add_url_rule('/songs', view_func=AllSongsView.as_view('all_songs'))
app.add_url_rule('/songs/avg/difficulty', view_func=AverageDifficultyView.as_view('average_difficulty'))
app.add_url_rule('/songs/search', view_func=SongsSearchView.as_view('songs_search'))


if __name__ == '__main__':
    app.run()
