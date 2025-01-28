from quart import request, jsonify
import asyncpg

from ..utils import check_authorization_headers
from ..repositories import UserRepository

def skip_auth_check(func):
    func._skip_auth_check = True
    return func

def install_middleware(app):
    @app.before_serving
    async def create_db_pool():
        app.db_pool = await asyncpg.create_pool('postgresql://postgres:PASSWORD@localhost:5432/pdf_chat')
    
    @app.after_serving
    async def destroy_db_pool():
        await app.db_pool.close()
    
    @app.before_request
    async def check_auth():
        allowed = False

        endpoint = request.endpoint
        if (
            # endpoints set to skip the check are allowed
            (endpoint and hasattr(app.view_functions[endpoint], '_skip_auth_check'))
            # same goes for OPTIONS preflight requests
            or request.method == 'OPTIONS'
        ):
            allowed = True
        else:
            if await check_authorization_headers(request, sha_pass=True):
                repo = UserRepository(app.db_pool)
                user_data = await repo.get_data_with_key(
                    request.authorization.password
                )
                if user_data:
                    app.user = user_data
                    allowed = True
        
        if not allowed:
            return jsonify({
                'message': 'Not Authenticated'
            }), 401
        
    return app