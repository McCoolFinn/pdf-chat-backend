async def check_authorization_headers(request, sha_pass = False):
    '''
    A utility function for verifying the format of user provided auth headers
    '''
    if(request.headers.get('Authorization')):
        valid_auth_type = (
            (not sha_pass and
            len(request.authorization.username) > 0 and
            len(request.authorization.password) > 0)
            or
            (request.authorization.username == 'X-Api-Key' and
            len(request.authorization.password) == 64)
        )
        return True if valid_auth_type else False
    return False