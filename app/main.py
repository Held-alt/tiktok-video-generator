from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from app.services.generate_video import generate_video

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate")
async def generate_endpoint(question: str = Form(...)):
    return generate_video(question)

@app.get("/")
def read_root():
    return {"message": "TikTok Video Generator API"}
