from typing import Any
from fastapi import Depends, FastAPI, HTTPException, Request, Response, status
from fastapi.responses import JSONResponse, PlainTextResponse
from homework_app.modules import DivisionRequest, KeyValue, validate_DivisionRequest, validate_KeyValue  


app = FastAPI()
data_store: dict[str, str] = {}


def check_content_type(request_type: str | None, type: str):
    if request_type == None or request_type != type:
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)


@app.middleware("http")
async def errors_handling(request: Request, call_next):
    try:
        if request.url.path == '/set' or request.url.path == '/divide':
            check_content_type(request.headers.get('content-type'), "application/json")

        return await call_next(request)
    except HTTPException as exc:
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


@app.get("/hello", response_class=PlainTextResponse)  # Set content-type to text\plain
def hello_endpoint():
    return PlainTextResponse(content="HSE One Love!", status_code=status.HTTP_200_OK)


@app.post("/set", response_class=Response)
def set_endpoint(data: KeyValue = Depends(validate_KeyValue)):
    data_store[data.key] = data.value
    return Response(status_code=status.HTTP_200_OK)


@app.get("/get/{key}", response_class=JSONResponse)  # Set content-type to application\json
def get_endpoint(key: str):
    if key not in data_store:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="")
    
    key_value = KeyValue(key=key, value=data_store[key]).model_dump()
    return JSONResponse(content=key_value, status_code=status.HTTP_200_OK)


@app.post("/divide", response_class=PlainTextResponse)  # Set content-type to text\plain
def divide_endpoint(data: DivisionRequest = Depends(validate_DivisionRequest)):
    try:
        result = data.dividend / data.divider
    except ZeroDivisionError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    return PlainTextResponse(content=str(result), status_code=status.HTTP_200_OK)


@app.api_route("/{path:path}", methods=["GET", "PUT", "DELETE", "POST", "PATCH", "OPTIONS", "HEAD"])
def not_allowed_path(path: str):
    raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED)
