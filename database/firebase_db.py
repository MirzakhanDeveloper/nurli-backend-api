import firebase_admin
from firebase_admin import credentials, firestore

try:
    # Firebase kalitini ulash
    cred = credentials.Certificate("firebase_key.json")
    # Agar app allaqachon initialize bo'lgan bo'lsa, xato bermasligi uchun tekshiramiz
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)
    db = firestore.client()
    print("Firebase muvaffaqiyatli ulandi!")
except Exception as e:
    print(f"Firebase ulanishida xatolik: {e}")