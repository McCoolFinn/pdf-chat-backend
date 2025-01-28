class APIException(Exception):
  status = 500

class AuthException(APIException):
  status = 401
class AuthDeniedException(AuthException):
  pass

class DataException(APIException):
  pass
class AccessDeniedException(DataException):
  status = 403
class ResourceNotFoundException(DataException):
  status = 404