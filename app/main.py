from fastapi import APIRouter, FastAPI, Request
from mangum import Mangum
from starlette.middleware.cors import CORSMiddleware

import app.calculation.api.v1.routes.api as calculation_route
from app.core_services.v1.services import resource

lambdaPaths = resource.resources()

if lambdaPaths["staging"] is None:
    fastapi_doc = None
else:
    fastapi_doc = f'{lambdaPaths["staging"]}/{lambdaPaths["resource"]}'

app = FastAPI(root_path=fastapi_doc)
router = APIRouter()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_cors_header(request: Request, call_next):
    """
    Add Cors Header
    ---------------

    This function will add CORS headers to HTTP responses

    Args:
        request (Request): The incoming HTTP request object
        call_next: A callable representing the next middleware or route handler in the chain.

    Returns:
        Response: The HTTP response object with added CORS headers
    """
    response = await call_next(request)
    response.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "*"
    return response


@app.get("/")
async def default():
    return {"message": "visit /docs for swagger"}


app.include_router(router)
app.include_router(calculation_route.router)

handler = Mangum(app, api_gateway_base_path=lambdaPaths["resource"])
