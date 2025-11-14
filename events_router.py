from client import s_client
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse

events_router = APIRouter(prefix="/event")
valid_fields = [
    'organisers',
    'participants',
    'current_participants',
    'venue',
    'country_city',
    'max_participants'
]

@events_router.post("/my-events")
async def get_my_events(request: Request):
    data = await request.json()
    events = s_client.table("events").select("*").execute()

    if events:
        events_ = [
            event for event in events.data
            if any(org.get("email") == data["email"] for org in event.get("organisers", []))
        ]

        return JSONResponse(
            status_code=200, content={
                "msg": "success",
                "events": events_
            }
        )
   
@events_router.post("/query/general")
async def general_query(request: Request):
    data = await request.json()
    if data['field'] in valid_fields:
        query = s_client.table("events").select(data['field']).eq("id", data['id']).maybe_single().execute()
        if query:
            return JSONResponse(
                status_code=200,
                content={
                    "msg": "success",
                    "data": query.data                    
                }
            )
        
    else:
        raise HTTPException(400, detail="not a valid field")
    

# @events_router.post("/add-org")
# # async def add_org(request: Request):
# def add_org(event_id: str, org_id: str):
#     # data = await request.json()
#     # if not data['event-name'] and not data['org-id']:
#     if not event_id and not org_id:
#         raise HTTPException(status_code=403, detail="provide all details")
    
#     else:
#         # org = s_client.table("users").select("email").eq("id", data['org-id']).execute()
#         org = s_client.table("users").select("id").eq("email", org_id).execute()
#         if org:
#             event = s_client.table("events").select("organisers").eq("id", event_id).execute()
#             if event:
#                 orgs = event.data
#                 orgs.append(org_id)
#                 s_client.table("events").update({"organisers": orgs}).eq("id", event_id).execute()
#                 return JSONResponse(
#                     status_code=200,
#                     content={
#                         "msg": "success"
#                     }
#                 )

@events_router.post("/invite-org")
async def invite_org(request: Request):
    data = await request.json()
    if data:
        s_client.auth.admin.invite_user_by_email(data['email'], options={
            "redirect_to": "https://google.com"
        })
    else:
        raise HTTPException(status_code=403, detail="provide email")

