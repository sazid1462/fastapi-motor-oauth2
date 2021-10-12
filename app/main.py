from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from app.core.config import settings
from app.database.mongodb import mongodb_disconnect
from app.api.v1 import token, users


app = FastAPI(
    title=settings.app_name,
    description=settings.description,
    version=settings.version,
    terms_of_service=settings.terms_of_service,
    contact={
        "name": settings.contact_person,
        "email": settings.contact_email
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    }
)

# app.add_middleware(HTTPSRedirectMiddleware)
# app.add_middleware(
#     TrustedHostMiddleware, allowed_hosts=[
#         "example.com", "*.example.com"]
# )
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=500)

app.include_router(token.router)
app.include_router(users.router)


@app.on_event("startup")
async def startup_db_client():
    # await mongodb_connect()
    pass


@app.on_event("shutdown")
async def shutdown_db_client():
    await mongodb_disconnect()
