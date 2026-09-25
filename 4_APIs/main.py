from fastapi import FastAPI, Path, Query, Form, UploadFile, File
from enum import Enum

app = FastAPI()

db = {
    1:"car",
    2:"laptop",
    3:"box"
}

@app.get("/health")
async def health():
    return {"health": "okay"}


############ Path #################
# Path parameters are part of url.
# Extracts URL path with type validation
@app.get("/item/{item_number}")
async def get_item(
    item_number:int = Path(
        gt=0,
        lt=4,
        title="Item id",
        
    )):             
    return {"item":db.get(int(item_number))}

# Enum path parameter - restricts to allowed values

class ModelName(str, Enum):
    gpt = "gpt"
    llama = "llama"
    haiku = "haiku"

@app.get("/model/{model_name}")
async def get_model(model_name: ModelName):
    return {"model": model_name.value}


########### Query ####################


# Accept query string parameters with defaults and validation.

@app.get("/itemq/")
async def get_item(item_number:str, message:str):
    return {"item":db.get(int(item_number)), "message":message}

@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}


# List query parameter
@app.get("/items/list_query")
async def read_items(tags: list[str] = Query(default=[])):
    return {"tags": tags}




from pydantic import BaseModel, Field, field_validator

class Item(BaseModel):
    name: str
    price: float = Field(gt=0, description="Must be positive")
    description: str | None = None
    tags: list[str] = []

@app.put("/items/{item_id}")
async def update_item(
    item_id: int,             # Path
    item: Item,               # Body (JSON)
    q: str | None = None,     # Query
):
    return {"item_id": item_id, **item.model_dump(), "q": q}

@app.post("/submit/")
async def submit(
    title: str = Form(),
    description: str = Form(default=""),
    file: UploadFile = File(),
):
    contents = await file.read()
    return {
        "title": title,
        "filename": file.filename,
        "size": len(contents),
    }

@app.post('/login')
async def login(
    user_name : str = Form(),
    password : str = Form()):
    return {"username":user_name, "password" : hash(password)}
