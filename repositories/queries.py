AUTH_USER_PASS_CHECK = '''
    SELECT
        id, username, display_name, email, gender
    FROM users
    WHERE username = $1 AND password = $2
'''
AUTH_USER_RETRIEVE_KEY = '''
    SELECT key FROM auths WHERE user_id = $1
'''
AUTH_USER_RETRIEVE_USER_BY_KEY = '''
    SELECT user_id FROM auths WHERE key = $1
'''
AUTH_USER_INSERT_KEY = '''
    INSERT INTO auths VALUES ($1, $2) RETURNING *
'''
AUTH_USER_RETRIEVE_USERDATA_BY_KEY = '''
    SELECT
        u.id, u.username, u.display_name, u.email, u.gender
    FROM auths a
    LEFT JOIN 
        users u ON a.user_id = u.id
    WHERE a.key = $1
'''
DOCS_GET_USER_DOCS = '''
    SELECT
        id,
        filename,
        filetype,
        PG_SIZE_PRETTY(COALESCE(LENGTH(data), 0)::numeric) AS filesize
    FROM documents
    WHERE user_id = $1
'''
DOCS_GET_BY_ID = '''
    SELECT
        id,
        user_id,
        filename,
        filetype,
        PG_SIZE_PRETTY(COALESCE(LENGTH(data), 0)::numeric) AS filesize,
        data
    FROM documents
    WHERE id = $1
'''
DOCS_DELETE_DOC = '''
    DELETE FROM documents WHERE id = $1 AND user_id = $2 RETURNING id
'''
DOCS_INSERT_DOC = '''
    INSERT INTO documents
        (user_id, filename, filetype, data)
    VALUES
        ($1, $2, 'pdf', $3)
    RETURNING id, user_id, filename, filetype
'''