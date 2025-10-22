from fastapi import FastAPI, UploadFile, File, HTTPException, Response
from PIL import Image
from io import BytesIO

app = FastAPI()
MOODLE_LOGIN = "vulkan21"

@app.get("/login")
def login():
    return Response(content=MOODLE_LOGIN, media_type="text/plain; charset=utf-8")

@app.post("/size2json")
async def size2json(image: UploadFile = File(...)):
    if image.content_type not in ("image/png",):
        raise HTTPException(status_code=415, detail="Only PNG is supported")
    data = await image.read()
    try:
        with Image.open(BytesIO(data)) as im:
            w, h = im.size
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid PNG")
    return Response(content=f'{{"width":{w},"height":{h}}}', media_type="application/json")

