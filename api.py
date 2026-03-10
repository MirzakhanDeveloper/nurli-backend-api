from fastapi import FastAPI
from pydantic import BaseModel
import firebase_admin
from firebase_admin import credentials, firestore

# Firebase kalitini ulash (Boyagi json fayl orqali)
cred = credentials.Certificate("firebase_key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

app = FastAPI(title="Nurli Backend API")

class AttendanceEvent(BaseModel):
    student_id: str
    timestamp: str
    camera_location: str

@app.post("/attendance")
def record_attendance(event: AttendanceEvent):
    print(f"📥 SERVERGA KELDI -> O'quvchi ID: {event.student_id} | Vaqt: {event.timestamp}")
    
    try:
        # Firestore-dagi 'attendance_logs' kolleksiyasiga yozamiz
        doc_ref = db.collection("attendance_logs").document(event.student_id)
        doc_ref.set({
            "student_id": event.student_id,
            "last_seen": event.timestamp,
            "camera": event.camera_location,
            "status": "present"
        })
        print("☁️ Firebase-ga muvaffaqiyatli yozildi!")
        return {"status": "success", "message": "Davomat Firestore-ga yozildi"}
    except Exception as e:
        print(f"⚠️ Firebase-ga yozishda xatolik: {e}")
        return {"status": "error", "message": str(e)}