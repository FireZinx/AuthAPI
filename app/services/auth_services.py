import secrets

class AuthenticationServices:
    def __init__(self, database):
        self.database = database

    def auth_session(self, request: Request):
        session_id = request.cookies.get("session_id")

        if session_id:
            result = self.database.get_user_id_by_session(session_id)

            print(result["status"])

            if result["status"] == 200:
                user_id = result["user_id"]
                return self.database.get_user_role_by_user_session(session_id)
                
            else:
                return {"status": 400, "error_message": "Invalid session"}
        else:
            return {"status": 400, "error_message": "No session found"}

    def signup_fetch(self, signup_request: SignupRequest):
        if not (signup_request.email and signup_request.password):
            return {"status": 400, "error_message": "Email and password are required"}

        elif len(signup_request.password) < 8:
            return {"status": 400, "error_message": "Password must be at least 8 characters long"} 

        else:
            user_id = secrets.token_urlsafe(48)[:64]
            result = self.database.insert_user(user_id=user_id, email=signup_request.email, password=signup_request.password, username=signup_request.username)

        return result

    def login_fetch(self, login_request: LoginRequest, response: Response, request: Request):
        request_session = request.cookies.get("session_id")

        if not request_session:
            pending_user = self.database.select_user(login_request.email, login_request.password)

            print("Peding user passed to login_fetch: ", pending_user)

            if pending_user["status"] == 200: 
                session_id = secrets.token_urlsafe(38)[:48]

                session_pending = self.database.store_user_session(login_request.email, login_request.password, login_request.username, session_id)

                print("Session pending passed to login_fetch: ", session_pending)

                if session_pending["status"] == 200:
                    response.set_cookie(key="session_id", value=session_id, httponly=True, secure=False, samesite="lax")

                return {"status": 200, "username": pending_user["username"]}
            else:
                return pending_user
        else:
            return {"status": 400, "error_message": "User is already logged in"}