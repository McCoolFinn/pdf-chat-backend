from quart import Quart, request, jsonify
from quart_cors import cors
from hashlib import sha256
from os import urandom
import json

from .middleware import skip_auth_check, install_middleware
from .utils import check_authorization_headers
from .repositories import UserRepository, DocumentRepository
from .repositories.exceptions import *

app = install_middleware(Quart(__name__))
app = cors(app, allow_origin="*")

@app.get('/')
async def index():
    return "Logged in!"

@app.post('/auth')
@skip_auth_check
async def login():
    try:
        # why bother, if they haven't given us a proper request?
        if not await check_authorization_headers(request):
            raise AuthDeniedException('Credentials malformed')
        
        repo = UserRepository(app.db_pool)
        authentication = await repo.authenticate(request.authorization)

        return jsonify(
            authentication
        )
    except AuthException as e:
        return jsonify({
            'message': str(e)
        }), e.status
    except Exception as e:
        return jsonify({
            'message': 'Unhandled Error'
        }), 500

@app.route('/user', methods=['GET', 'POST', 'PATCH', 'DELETE'])
@skip_auth_check
async def signup():
    repo = UserRepository(app.db_pool)
    authentication = await repo.authenticate(request.authorization)

@app.get('/arrivals')
@skip_auth_check
async def arrivals():
    data = {}
    with open('/Users/jeff/Development/pdf-chat/backend-server/request.json', 'r', encoding='utf-8') as file:
        data = json.loads(file.read())
    return jsonify(data)

@app.get('/documents')
async def documents():
    repo = DocumentRepository(app.db_pool)
    docs = await repo.get_user_documents(app.user['id'])

    return jsonify(docs)

@app.route('/document', methods=['POST'])
async def uploadDocument():
    repo = DocumentRepository(app.db_pool)
    doc = await repo.upload_user_document(app.user['id'], await request.json)
    
    return jsonify(doc)

@app.route('/document/<int:id>', methods=['GET', 'DELETE'])
async def document(id):
    repo = DocumentRepository(app.db_pool)
    try:
        results = (repo.delete_document(app.user['id'], id)
            if request.method == 'DELETE'
            else repo.get_document(app.user['id'], id)
        )

        return jsonify(await results)
    except DataException as e:
        return jsonify({
            'message': str(e)
        }), e.status
    except Exception as e:
        print(e)
        return jsonify({
            'message': 'Unhandled Error'
        }), 500