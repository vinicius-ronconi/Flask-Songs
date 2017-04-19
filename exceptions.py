class InvalidParameterError(Exception):
    status_code = 400

    def __init__(self, message):
        super(InvalidParameterError, self).__init__(self)
        self.message = message

    def to_dict(self):
        return {'message': self.message}
