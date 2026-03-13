from fastapi import APIRouter, Depends
from pydantic import BaseModel
from database.firebase_db import db
from core.security import verify_api_key
from core.websocket_manager import manager # YANGI: Menejerni chaqiramiz

router = APIRouter()

class AttendanceEvent(BaseModel):
    student_id: str
    timestamp: str
    camera_location: str

# DIQQAT: async def qildik
@router.post("/attendance", dependencies=[Depends(verify_api_key)])
async def record_attendance(event: AttendanceEvent): 
    print(f"☁️ SERVERGA KELDI -> O'quvchi ID: {event.student_id} | Vaqt: {event.timestamp}")
    try:
        # 1. Firebase-ga yozamiz
        doc_ref = db.collection("attendance_logs").document(event.student_id)
        doc_ref.set({
            "student_id": event.student_id,
            "last_seen": event.timestamp,
            "camera": event.camera_location,
            "status": "present"
        })
        
        # 2. YANGI: Barcha tinglab turganlarga (Web panelga) shu zahoti xabar tarqatamiz!
        await manager.broadcast_json({
            "student_id": event.student_id,
            "last_seen": event.timestamp,
            "camera": event.camera_location,
            "status": "Keldi"
        })
        
        return {"status": "success", "message": "Davomat saqlandi va Web-ga tarqatildi!"}
    except Exception as e:
        return {"status": "error", "message": str(e)}