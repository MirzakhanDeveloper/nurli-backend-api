from fastapi import APIRouter
from pydantic import BaseModel
from database.firebase_db import db

router = APIRouter()

class AttendanceEvent(BaseModel):
    student_id: str
    timestamp: str
    camera_location: str

@router.post("/attendance")
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