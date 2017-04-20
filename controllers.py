import exceptions
from models import Song


class SongsController(object):
    def __init__(self, db):
        """
        :type db: flask_mongoengine.MongoEngine 
        """
        self.db = db

    def get_all_songs(self, request):
        """
        :type request: flask.request 
        :rtype: list[dict]
        """
        request = self._validate_request_parameters(request, param_list=('current_page', 'page_size'))
        current_page = int(request.args.get('current_page', 1))
        page_size = int(request.args.get('page_size', 10))
        songs = Song.objects.paginate(page=current_page, per_page=page_size)
        return [song.as_json() for song in songs.items]

    @staticmethod
    def _validate_request_parameters(request, param_list):
        """
        :type request: flask.request 
        :rtype: flask.request 
        """
        for param in param_list:
            try:
                if int(request.args.get(param, 1)) <= 0:
                    raise exceptions.InvalidParameterError('{} must be greater than zero.'.format(param))
            except ValueError:
                raise exceptions.InvalidParameterError('{} must be an int value.'.format(param))
        return request

    def get_average_difficulty(self, request):
        """
        :param request: flask.request
        :rtype: dict
        """
        request = self._validate_request_parameters(request, param_list=('level',))
        query = {}
        if request.args.get('level'):
            query = {'level': request.args.get('level')}
        return {'average': round(Song.objects.filter(**query).average('difficulty'), 2)}
