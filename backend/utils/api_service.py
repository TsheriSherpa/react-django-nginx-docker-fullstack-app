""" Api Service Class """


class ApiService:

    error_code = 422
    error_message = "Something went wrong"

    @classmethod
    def setError(cls, error_message="Something went wrong", error_code=422):
        cls.error_code = error_code
        cls.error_message = error_message

    @classmethod
    def getErrorMessage(cls):
        return cls.error_message

    @classmethod
    def getErrorCode(cls):
        return cls.error_code
