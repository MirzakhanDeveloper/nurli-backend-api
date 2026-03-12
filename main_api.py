from fastapi import FastAPI
from routers import attendance

app = FastAPI(
    title="Nurli Venture Studio API", 
    description="Barcha AI loyihalar va qurilmalarni boshqarish markazi",
    version="1.0.0"
)

# Davomat modulini asosiy dasturga ulaymiz
app.include_router(attendance.router, tags=["Davomat Tizimi"])

@app.get("/")
def home():
    return {"message": "Nurli API Markaziga Xush Kelibsiz. Boshqaruv paneli uchun /docs manziliga kiring."}