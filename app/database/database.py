from database.queries import GET_USER_ID_BY_SESSION, STORE_USER_SESSION, INSERT_USER, SELECT_USER, GET_USER_ROLE_BY_SESSION
from psycopg_pool import ConnectionPool

class DatabasePool:
    def __init__(self):
        self.pool = ConnectionPool(
            "postgresql://postgres:admin@localhost:5432/postgres", 
            max_size=10
        ) 

    def get_user_id_by_session(self, session_id: str):
        with self.pool.connection() as conn:
            with conn.cursor() as cur: 
                cur.execute(GET_USER_ID_BY_SESSION, (session_id,))
                
                if cur.rowcount == 0:
                    return {"status": 400, "error_message": "Invalid session"}
                
                else:
                    return {"status": 200, "user_id": cur.fetchone()[0]}

    def store_user_session(self, email: str, password: str, username: str, session_id: str):
        with self.pool.connection() as conn:
            with conn.cursor() as cur: 
                cur.execute(STORE_USER_SESSION, (email, password, session_id, username))

                if cur.fetchone() is None:
                    return {"status": 400, "error_message": "Failed to store user session"}
                
                else:                    
                    return {"status": 200}

    def insert_user(self, user_id: str, email: str, password: str, username: str):
        with self.pool.connection() as conn:
            with conn.cursor() as cur: 
                print(f"Inserting user with email: {email} and password: {password}")

                cur.execute(INSERT_USER, (user_id, email, password, username))

                if cur.fetchone() is None:  
                    return {"status": 400, "error_message": "User has already created "}
                
                else:
                    return {"status": 200}
    
    def select_user(self, email: str, password: str):
         with self.pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(SELECT_USER, (email, password))

                if cur.rowcount == 0:
                    return {"status" : 400, "error_message": "User not found"}

                else:
                    database_email, database_password, username = cur.fetchone()
                    if database_email == email and database_password == password:
                        return {"status" : 200, "username": username}

    def get_user_role_by_user_session(self, user_id: str):
         with self.pool.connection() as conn:
            with conn.cursor() as cur: 
                cur.execute(GET_USER_ROLE_BY_SESSION, (user_id,))
                
                if cur.rowcount == 0:
                    return {"status": 400, "error_message": "Invalid session"}
                
                else:
                    data = cur.fetchone()
                    return {"status": 200, "user_name": data[0], "user_role": data[1]}
