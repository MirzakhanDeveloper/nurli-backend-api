import cv2
from deepface import DeepFace
import time
import requests

# O'quvchilar rasmlari turgan papka
db_path = "students_db"

# Noutbuk kamerasini yoqish (0 - asosiy kamera)
cap = cv2.VideoCapture(0)

print("Kamera ishga tushdi. Yuzlar qidirilmoqda...")

# Har soniyada kadrni tahlil qilmaslik uchun (kompyuterni qotirmaslik uchun)
# faqat har 30-kadrni tahlil qilamiz.
frame_count = 0
recognized_student = None

while True:
    ret, frame = cap.read()
    if not ret:
        print("Kameradan tasvir olinmadi!")
        break

    frame_count += 1

    # Faqat har 30-kadrda (taxminan har 1 soniyada) DeepFace tahlilini ishga tushiramiz
    if frame_count % 30 == 0:
        try:
            # Vaqtincha rasmni saqlab, DeepFace'ga beramiz
            cv2.imwrite("temp_frame.jpg", frame)
            
            # Yuzni bazadagi rasmlar bilan solishtirish
            result = DeepFace.find(img_path="temp_frame.jpg", db_path=db_path, enforce_detection=False, silent=True)
            
            if len(result) > 0 and len(result[0]) > 0:
                # Agar yuz topilsa, fayl nomini (ID ni) ajratib olamiz
                matched_image = result[0]['identity'][0]
                student_id = matched_image.split('/')[-1].split('\\')[-1].split('.')[0]
                
                recognized_student = student_id
                current_time = time.strftime('%Y-%m-%d %H:%M:%S')
                print(f"✅ O'quvchi aniqlandi! ID: {student_id} | Vaqt: {current_time}")
                
                # --- API ga ma'lumot yuborish qismi ---
                api_url = "http://127.0.0.1:8000/attendance"
                data = {
                    "student_id": str(student_id),
                    "timestamp": current_time,
                    "camera_location": "Maktab_Asosiy_Kirish"
                }
                try:
                    # Lokal FastAPI serverga POST so'rov yuboramiz
                    response = requests.post(api_url, json=data)
                    print("🌐 Server javobi:", response.json())
                except Exception as e:
                    print("⚠️ Serverga ulanib bo'lmadi! API (api.py) ishlayotganini tekshiring.")
                # --------------------------------------
                
            else:
                recognized_student = None
                
        except Exception as e:
            pass # Yuz topilmasa yoki xato bo'lsa, dastur to'xtab qolmasligi uchun

    # Ekranga natijani yozish
    if recognized_student:
        cv2.putText(frame, f"O'quvchi: {recognized_student}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    else:
        cv2.putText(frame, "Yuz izlanmoqda...", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Videoni ekranda ko'rsatish
    cv2.imshow('Nurli MVP - Kamera', frame)

    # 'q' tugmasi bosilsa dasturdan chiqadi
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()