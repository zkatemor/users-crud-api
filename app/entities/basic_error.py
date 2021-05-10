class BasicError(Exception):
    def __init__(self, message='Internal Server Error', status=500):
        self.message = message
        self.status = status

    def __str__(self):
        return self.message
