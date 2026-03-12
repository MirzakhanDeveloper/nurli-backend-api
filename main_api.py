from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from routers import attendance
from database.firebase_db import db  # Bazadan o'qish uchun kerak

app = FastAPI(
    title="Nurli Venture Studio API", 
    description="Barcha AI loyihalar va qurilmalarni boshqarish markazi",
    version="1.0.0"
)

# HTML shablonlar papkasini ulaymiz
templates = Jinja2Templates(directory="templates")

# Davomat modulini asosiy dasturga ulaymiz
app.include_router(attendance.router, tags=["Davomat Tizimi"])

@app.get("/")
def home():
    return {"message": "Nurli API Markaziga Xush Kelibsiz. Boshqaruv paneli uchun /panel manziliga kiring."}

# YANGI: Super Admin Paneli
@app.get("/panel", response_class=HTMLResponse, tags=["Web Panel"])
def admin_panel(request: Request):
    # Firebase-dan eng so'nggi 10 ta davomatni tortib olamiz
    try:
        docs = db.collection("attendance_logs").order_by("last_seen", direction="DESCENDING").limit(10).stream()
        logs_list = [doc.to_dict() for doc in docs]
    except Exception as e:
        logs_list = []
        print(f"Bazadan o'qishda xatolik: {e}")

    # Ularni HTML shablonga berib yuboramiz
    return templates.TemplateResponse("dashboard.html", {"request": request, "logs": logs_list})