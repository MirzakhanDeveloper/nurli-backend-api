import cv2
from deepface import DeepFace
import time
import requests

# O'quvchilar rasmlari turgan papka
db_path = "students_db"

# Noutbuk kamerasini yoqish (0 - asosiy kamera)
cap = cv2.VideoCapture(0)

print("Kamera ishga tushdi. Yuzlar qidirilmoqda...")

frame_count = 0
recognized_student = None

# YANGI: Spamni oldini olish uchun xotira
last_sent_times = {}
COOLDOWN_SECONDS = 30 # Bitta o'quvchini qayta jo'natishdan oldin necha soniya kutish kerak?

while True:
    ret, frame = cap.read()
    if not ret:
        print("Kameradan tasvir olinmadi!")
        break

    frame_count += 1

    if frame_count % 30 == 0:
        try:
            cv2.imwrite("temp_frame.jpg", frame)
            
            result = DeepFace.find(img_path="temp_frame.jpg", db_path=db_path, enforce_detection=False, silent=True)
            
            if len(result) > 0 and len(result[0]) > 0:
                matched_image = result[0]['identity'][0]
                student_id = matched_image.split('/')[-1].split('\\')[-1].split('.')[0]
                
                current_time_sec = time.time()
                current_time = time.strftime('%Y-%m-%d %H:%M:%S')
                
                # YANGI MANTIQ: Agar bu o'quvchi oxirgi 30 soniya ichida jo'natilgan bo'lsa, API ga yozmaymiz
                if student_id in last_sent_times and (current_time_sec - last_sent_times[student_id]) < COOLDOWN_SECONDS:
                    # Shunchaki ekranda ismini ko'rsatish uchun saqlaymiz, lekin serverga jo'natmaymiz
                    recognized_student = student_id
                else:
                    # Yangi odam yoki 30 soniyadan keyin yana kelgan bo'lsa -> Serverga jo'natamiz
                    recognized_student = student_id
                    last_sent_times[student_id] = current_time_sec # Xotirani yangilaymiz
                    
                    print(f"✅ O'quvchi aniqlandi! ID: {student_id} | Vaqt: {current_time}")
                    
                    # --- API ga ma'lumot yuborish qismi ---
                    api_url = "http://127.0.0.1:8000/attendance"
                    
                    headers = {
                        "X-API-Key": "Nurli_Super_Secret_Key_2026_!@#"
                    }
                    
                    data = {
                        "student_id": str(student_id),
                        "timestamp": current_time,
                        "camera_location": "Maktab_Asosiy_Kirish"
                    }
                    try:
                        response = requests.post(api_url, json=data, headers=headers)
                        print("🌐 Server javobi:", response.json())
                    except Exception as e:
                        print("⚠️ Serverga ulanib bo'lmadi! API ishlayotganini tekshiring.")
                
            else:
                recognized_student = None
                
        except Exception as e:
            pass # Yuz topilmasa yoki xato bo'lsa, dastur to'xtab qolmasligi uchun

    # Ekranga natijani yozish
    if recognized_student:
        cv2.putText(frame, f"O'quvchi: {recognized_student}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    else:
        cv2.putText(frame, "Yuz izlanmoqda...", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow('Nurli MVP - Kamera', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()