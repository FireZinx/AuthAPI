from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from database.database import DatabasePool
from routers.auth import Authentication

import uvicorn

class Main():
    def __init__(self):
        self.app = FastAPI()
        self.database = DatabasePool()
        self.auth = Authentication(self.database)

        self.app.include_router(self.auth.router)

        origins = [
            "http://localhost:3000",
        ]

        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        self.start()

    def start(self):
        uvicorn.run(self.app, host="192.168.15.3", port=5000,  proxy_headers=True, forwarded_allow_ips="*")

if __name__ == "__main__":
    Main()