import os
import vertexai
from vertexai.generative_models import GenerativeModel
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from routers import attendance
from database.firebase_db import db  
from core.websocket_manager import manager 

# 1. JSON pasportni tizimga ko'rsatamiz (Fayl nomi to'g'ri bo'lishi shart)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "vertex_key.json"

# 2. Vertex AI ni ishga tushiramiz (Sizning JSON faylingizdagi loyiha ID raqami)
# YANGI QATOR (O'zbekistonga yaqinlashtirilgan va barqaror):
vertexai.init(project="nurli-ai-core", location="us-central1")

app = FastAPI(
    title="Nurli Venture Studio API", 
    description="Barcha AI loyihalar va qurilmalarni boshqarish markazi",
    version="1.0.0"
)

templates = Jinja2Templates(directory="templates")
app.include_router(attendance.router, tags=["Davomat Tizimi"])

@app.websocket("/ws/dashboard")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.get("/")
def home():
    return {"message": "Nurli API Markaziga Xush Kelibsiz. Boshqaruv paneli uchun /panel manziliga kiring."}

@app.get("/panel", response_class=HTMLResponse, tags=["Web Panel"])
def admin_panel(request: Request):
    try:
        docs = db.collection("attendance_logs").order_by("last_seen", direction="DESCENDING").limit(10).stream()
        logs_list = [doc.to_dict() for doc in docs]
    except Exception as e:
        logs_list = []
        print(f"Bazadan o'qishda xatolik: {e}")

    return templates.TemplateResponse("dashboard.html", {"request": request, "logs": logs_list})

# --- YANGI: Haqiqiy Vertex AI Bashorat Xonasi ---
@app.get("/api/ai-analysis", tags=["Sun'iy Intellekt"])
def get_vertex_prediction():
    try:
        # 1. Firebase'dan oxirgi 20 ta davomatni o'qiymiz
        docs = db.collection("attendance_logs").order_by("last_seen", direction="DESCENDING").limit(20).stream()
        logs_text = "Maktab davomat jadvali:\n"
        
        for doc in docs:
            data = doc.to_dict()
            # Kamera nomini xavfsiz ajratib olamiz
            kamera_holati = data.get('camera', "Noma'lum")
            logs_text += f"O'quvchi ID: {data['student_id']}, Vaqt: {data['last_seen']}, Kamera: {kamera_holati}\n"

        # 2. AI ga direktor nomidan buyruq beramiz
        prompt = f"""
        Siz maktab direktorining aqlli yordamchisisiz. Quyidagi jonli davomat ma'lumotlarini tahlil qiling:
        {logs_text}
        
        Iltimos, o'zbek tilida qisqa va aniq qilib quyidagilarni yozib bering:
        1. Umumiy davomat holati qanday?
        2. Tizim to'g'ri va xavfsiz ishlayotgani haqida xulosa.
        3. Kechikish xavfi bor o'quvchilar va ularni nazorat qilish bo'yicha maslahat.
        """
        
        # 3. Mintaqa tanlamaydigan va 100% barqaror ishlaydigan model
       # Eski qator: model = GenerativeModel('gemini-1.5-flash-001')

        # YANGI QATOR:
        model = GenerativeModel('gemini-1.5-flash-001')
        response = model.generate_content(prompt)
        
        return {"status": "success", "ai_analysis": response.text}
        
    except Exception as e:
        return {"status": "error", "message": str(e)}