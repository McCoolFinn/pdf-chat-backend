from hashlib import sha256
from os import urandom

from .database_repository import DatabaseRepository
from .queries import *
from .exceptions import AuthDeniedException

class UserRepository(DatabaseRepository):
    '''
    Repository object for managing user/auth data
    '''
    async def get_data_with_key(self, key):
        '''
        Simple function to handle user data retrieval for middleware
        '''
        async with self._pool.acquire() as conn:
            res = await conn.fetchrow(
                AUTH_USER_RETRIEVE_USERDATA_BY_KEY,
                key
            )
        
        return dict(res) if res else None

    async def authenticate(self, auth_data):
        '''
        Takes user authorization data, authenticates it and returns a user
        object with an API key
        '''
        auth_key = None

        async with self._pool.acquire() as conn:
            # make sure user credentials match
            res = await conn.fetchrow(
                AUTH_USER_PASS_CHECK,
                auth_data.username,
                sha256(
                    bytes(auth_data.password, encoding='utf-8')
                ).hexdigest()
            )
            if not res:
                raise AuthDeniedException('Credentials invalid')
            user_data = dict(res)

            # check if the user already has an auth key and set it
            res = await conn.fetchrow(
                AUTH_USER_RETRIEVE_KEY,
                user_data['id']
            )
            if res:
                auth_key = res['key']

            # keep rotating until with have an unused auth key to provide
            attempts = 0
            while auth_key is None and attempts < 5:
                attempts += 1
                current_key = sha256(urandom(32)).hexdigest()
                res = await conn.fetchrow(
                    AUTH_USER_RETRIEVE_USER_BY_KEY,
                    current_key
                )
                if not res:
                    res = await conn.fetchval(
                        AUTH_USER_INSERT_KEY,
                        current_key,
                        user_data['id']
                    )
                    auth_key = res

            user_data['key'] = auth_key
            if not auth_key:
                raise AuthDeniedException('Error granting authorization')
            
            return user_data