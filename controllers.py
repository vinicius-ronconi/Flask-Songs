import exceptions
from beans import RequestParameterValidator
from models import Song
from mongoengine.queryset.visitor import Q


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
        request = self._validate_request_parameters(
            request,
            validators={
                'current_page': RequestParameterValidator(
                    cast_func=int,
                    required=False,
                    min_value=1,
                    max_value=None,
                    default=1,
                ),
                'page_size': RequestParameterValidator(
                    cast_func=int,
                    required=False,
                    min_value=1,
                    max_value=None,
                    default=5,
                ),
            },
        )
        current_page = int(request.args.get('current_page', 1))
        page_size = int(request.args.get('page_size', 10))
        songs = Song.objects.paginate(page=current_page, per_page=page_size)
        return [song.as_json() for song in songs.items]

    def get_average_difficulty(self, request):
        """
        :param request: flask.request
        :rtype: dict
        """
        request = self._validate_request_parameters(
            request,
            validators={
                'level': RequestParameterValidator(
                    cast_func=int,
                    required=False,
                    min_value=1,
                    max_value=None,
                    default=1,
                ),
            },
        )
        query = {}
        if request.args.get('level'):
            query = {'level': request.args.get('level')}
        return {'average': round(Song.objects.filter(**query).average('difficulty'), 2)}

    def get_songs_by_keyword(self, request):
        """
        :type request: flask.request
        :rtype: list[dict]
        """
        request = self._validate_request_parameters(
            request,
            validators={
                'query': RequestParameterValidator(
                    cast_func=str,
                    required=True,
                    min_value=None,
                    max_value=None,
                    default=None,
                ),
            },
        )
        keyword = request.args.get('query')
        songs = Song.objects(Q(artist__icontains=keyword) | Q(title__icontains=keyword))
        return [song.as_json() for song in songs]

    def rate_song(self, request, song_id):
        """
        :type request: flask.request
        :type song_id: str
        :rtype: dict
        """
        request = self._validate_request_parameters(
            request,
            validators={
                'rating': RequestParameterValidator(cast_func=int, required=True, min_value=1, max_value=5, default=1),
            },
        )
        song = Song.objects.get_or_404(pk=song_id)
        song.rating = int(request.args.get('rating'))
        song.save()
        return song.as_json()

    @staticmethod
    def _validate_request_parameters(request, validators):
        """
        :type request: flask.request
        :type validators: dict[str: beans.RequestParameterValidator]
        :rtype: flask.request
        """
        for param_name, validator in validators.items():
            if validator.required and param_name not in request.args:
                raise exceptions.InvalidParameterError('Missing required parameter: {}'.format(param_name))

            param_value = request.args.get(param_name, validator.default)
            if validator.cast_func is not None:
                try:
                    param_value = validator.cast_func(param_value)
                except ValueError:
                    raise exceptions.InvalidParameterError(
                        '{} must be {} type'.format(param_name, validator.cast_func.__name__)
                    )
            if validator.min_value is not None:
                if param_value < validator.min_value:
                    raise exceptions.InvalidParameterError(
                        '{} must be greater than or equal to {}.'.format(param_name, validator.min_value)
                    )
            if validator.max_value is not None:
                if param_value > validator.max_value:
                    raise exceptions.InvalidParameterError(
                        '{} must be lower than or equal to {}.'.format(param_name, validator.max_value)
                    )
        return request
