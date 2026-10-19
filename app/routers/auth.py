from schemas.auth import SignupRequest, LoginRequest
from services.auth_services import AuthenticationServices
from fastapi import APIRouter, Request, Response

class Authentication():
    def __init__(self, database):
        self.router = APIRouter(prefix="/api", tags=["auth"])

        self.router.add_api_route("/authsession", self.auth_session, methods=["POST"])
        self.router.add_api_route("/signupsubmit", self.signup_fetch, methods=["POST"])
        self.router.add_api_route("/requestlogin", self.login_fetch, methods=["POST"])

        self.auth_services = AuthenticationServices(database)

    async def auth_session(self, request: Request):
        return self.auth_services.auth_session(request)

    async def signup_fetch(self, signup_request: SignupRequest):
        return self.auth_services.signup_fetch(signup_request)

    async def login_fetch(self, login_request: LoginRequest, response: Response, request: Request):
        return self.auth_services.login_fetch(login_request, response, request)