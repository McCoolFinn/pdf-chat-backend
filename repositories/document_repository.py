from base64 import b64decode, b64encode

from .database_repository import DatabaseRepository
from .queries import *
from .exceptions import *

class DocumentRepository(DatabaseRepository):
    async def get_user_documents(self, user_id):
        async with self._pool.acquire() as conn:
            res = await conn.fetch(
                DOCS_GET_USER_DOCS,
                user_id
            )
        
        return [dict(item) for item in res]
    
    async def upload_user_document(self, user_id, request_data):
        binary_data = b64decode(request_data['filedata'].encode('ascii'))
        async with self._pool.acquire() as conn:
            res = await conn.fetchrow(
                DOCS_INSERT_DOC,
                user_id,
                request_data['filename'],
                binary_data
            )

        return dict(res)
    
    async def get_document(self, user_id, id):
        async with self._pool.acquire() as conn:
            res = await conn.fetchrow(
                DOCS_GET_BY_ID,
                id
            )

            if not res:
                raise ResourceNotFoundException(
                    'Document doesn\'t exist'
                )
            if res['user_id'] != user_id:
                raise AccessDeniedException(
                    'You don\'t have access to this resource'
                )
            
            res = dict(res)
            res['data'] = b64encode(res['data']).decode('ascii')

        return res

    async def delete_document(self, user_id, id):
        async with self._pool.acquire() as conn:
            res = await conn.fetchrow(
                DOCS_DELETE_DOC,
                id, user_id
            )

            if not res:
                raise ResourceNotFoundException(
                    'Document doesn\'t exist'
                )

        return {}