from rest_framework.response import Response


class ApiResponse:
    @classmethod
    def send_success(cls, message, status_code=200):
        return Response({
            "status": True,
            "data": message
        }, status_code)

    @classmethod
    def send_error(cls, message, status_code=422):
        return Response({
            "status": False,
            "error": message
        }, status_code)
