import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
from datetime import datetime, timedelta
from mangum import Mangum
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()
handler = Mangum(app)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

URL= os.env.get("SUPABASE_URL", "")
KEY= os.env.get("SUPABASE_KEY", "")

supabase: Client = create_client(URL, KEY)

@app.post("/log-connection")
async def log_connection():
    # Insert data into Supabase
    supabase.table("connections").insert({"platform": "linkedin"}).execute()
    return {"status": "success"}

@app.get("/weekly-stats")
async def get_stats():
    # Get timestamp for 7 days ago
    one_week_ago = (datetime.now() - timedelta(days=7)).isoformat()
    
    # Query Supabase for records newer than one week ago
    response = supabase.table("connections").select("*", count="exact").gt("created_at", one_week_ago).execute()
    
    return {"weekly_total": response.count}