from client import s_client
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Request
from fastapi.exceptions import HTTPException
from supabase_auth.errors import AuthApiError

auth_router = APIRouter(prefix="/auth")

@auth_router.post("/signup")
async def signup(request: Request):
    data = await request.json()
    user = s_client.auth.sign_up({
        "email": data['email'],
        "phone": data['phone'],
        "password": data['password'],
        "options": {
            "data": {
                "name": data['name']
            }
        }
    })

    if user == "User already registered":
        return JSONResponse(
            status_code=200,
            content={
                "msg": "failed",
                "detail": "already exists"
            }
        )
    
    else:
        s_client.table("users").insert({
            "name": data['name'],
            "email": data['email']
        }).execute()
        ids = s_client.table("events").select("organisers_id").eq("id", 5).execute()
        
        if ids.data and len(ids.data) > 0:
            print(ids.data)
            row = ids.data[0]
            orgs = row.get("organisers_id") or []
            orgs.append(data['email'])

            print(orgs)

            out = s_client.table("events").update({
                "organisers_id": orgs
            }).eq("id", 5).execute()

            print(out)

        return JSONResponse(
            status_code=200,
            content={
                "msg": "success",
            }
        )

@auth_router.post("/get-magic-link")
async def get_magic_link(request: Request):
    data = await request.json()
    email = data['email']
    if not email:
        return HTTPException(
            status_code=401, detail="email required"
        )
    else:
        s_client.auth.sign_in_with_otp({"email": email})
        return JSONResponse(
            status_code=200, content={'msg': 'sent'}
        )
    
@auth_router.post("/verify-otp")
async def verify_otp(request: Request):
    try:
        req = await request.json()
        res = s_client.auth.verify_otp(params={
            "email": req['email'],
            "token": req['token'],
            "type": "email"
        })

        if res:
            user = s_client.table("users").select("id").eq("email", req['email']).execute()
            print(user)
            return JSONResponse(
                status_code=200, content={
                    "msg": "success",
                    "access_token": str(res.session.access_token),
                }
            )

        else:
            return JSONResponse(
                status_code=200, content={
                    "msg": "failed"
                }
            )
        
    except AuthApiError:
        return JSONResponse(
                status_code=200, content={
                    "msg": "failed"
                }
            )
