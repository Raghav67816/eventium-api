from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from auth_router import auth_router
from events_router import events_router
from client import s_client

app = FastAPI()
app.include_router(auth_router)
app.include_router(events_router)

# @app.middleware('http')
# async def verify_jwt(request: Request, call_next):
#     try:
#         public_paths = [
#             '/auth/get-magic-link',
#             '/auth/verify-otp',
#             '/docs',
#             '/openapi.json',
#             '/'
#         ]

#         if any(request.url.path.startswith(p) for p in public_paths):
#             return await call_next(request)

#         auth_header = request.headers.get("Authorization")
#         if not auth_header:
#             raise HTTPException(status_code=401, detail="missing key")
        
#         user = s_client.auth.get_claims(auth_header.split(" ")[1])
#         if not user:
#             raise HTTPException(status_code=401, detail="invalid key")
        
#         response = await call_next(request)
#         return response
    
#     except HTTPException:
#         pass

#     except Exception as error:
#         print(error)
#         raise HTTPException(status_code=500, detail="system error")