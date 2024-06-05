from fastapi import HTTPException, status


class SessionException(HTTPException):
    def __init__(self, message):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=message,
        )


class UnprocessableEntityException(HTTPException):
    def __init__(self, message):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=message,
        )


class UnauthorizedException(HTTPException):
    def __init__(self, message):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=message)


class InternalServerError(HTTPException):
    def __init__(self, message):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message
        )


class NotFoundException(HTTPException):
    def __init__(self, message):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=message)


# class UnsupportedMediaException(HTTPException):
#     def __init__(self, message):
#         super().__init__(
#             status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
#             detail=message,
#         )


# class FileEntityTooLargeException(HTTPException):
#     def __init__(self, message):
#         super().__init__(
#             status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
#             detail=message,
#         )
