GET_USER_ID_BY_SESSION = """ 
    SELECT user_id FROM users_session WHERE user_session_id = %s
"""
STORE_USER_SESSION = """
    INSERT INTO users_session (user_id, user_session_id, user_name, user_role)
    VALUES ((SELECT user_id FROM users_credentials WHERE user_email = TRIM(%s) AND user_password = TRIM(%s)), TRIM(%s), TRIM(%s), 'client')
    RETURNING 200
"""
INSERT_USER = """ 
    INSERT INTO users_credentials (user_id, user_email, user_password, user_name, user_role) 
    VALUES (TRIM(%s), TRIM(%s), TRIM(%s), TRIM(%s), 'client')
    ON CONFLICT (user_email) DO NOTHING
    RETURNING user_email
"""
SELECT_USER = """
    SELECT user_email, user_password, user_name FROM users_credentials WHERE user_email = %s AND user_password = %s
"""

GET_USER_ROLE_BY_SESSION = """
    SELECT user_name, user_role FROM users_session WHERE user_session_id = %s
"""