from fastapi import APIRouter, Depends # Depends qo'shildi
from pydantic import BaseModel
from database.firebase_db import db
from core.security import verify_api_key # Qorovulni chaqirib oldik

router = APIRouter()

class AttendanceEvent(BaseModel):
    student_id: str
    timestamp: str
    camera_location: str

# DIQQAT: Endpointga "dependencies" orqali qulf osdik!
@router.post("/attendance", dependencies=[Depends(verify_api_key)])
def record_attendance(event: AttendanceEvent):
    print(f"☁️ SERVERGA KELDI -> O'quvchi ID: {event.student_id} | Vaqt: {event.timestamp}")
    try:
        doc_ref = db.collection("attendance_logs").document(event.student_id)
        doc_ref.set({
            "student_id": event.student_id,
            "last_seen": event.timestamp,
            "camera": event.camera_location,
            "status": "present"
        })
        return {"status": "success", "message": "Davomat Firestore-ga yozildi!"}
    except Exception as e:
        return {"status": "error", "message": str(e)}