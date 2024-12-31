from fastapi import APIRouter

router = APIRouter()

@router.get("/data")
async def get_data():
    return {"message": "Hello from FastAPI!", "count": 42}

@router.post("/data")
async def post_data(data: dict):
    print(f"Received data: {data}")
    return {"status": "success", "received": data}