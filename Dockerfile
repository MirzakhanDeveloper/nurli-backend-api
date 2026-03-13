# 1. Dastur ishlashi uchun poydevor: Python'ning rasmiy va yengil versiyasini yuklaymiz
FROM python:3.11-slim

# 2. Konteyner ichida kodlarimiz turadigan "app" nomli ishchi papka yaratamiz
WORKDIR /app

# 3. Kutubxonalar ro'yxatini (requirements.txt) konteynerga ko'chiramiz
COPY requirements.txt .

# 4. Ro'yxatdagi barcha kutubxonalarni (fastapi, uvicorn, firebase-admin) o'rnatamiz
RUN pip install --no-cache-dir -r requirements.txt

# 5. O'zimiz yozgan barcha kodlarni (main_api.py, routers, database) konteynerga ko'chiramiz
COPY . .

# 6. Render.com bizning dasturimizni ko'rishi uchun 10000-portni ochiq qoldiramiz
EXPOSE 10000

# 7. Konteyner ishga tushganda bajarilishi kerak bo'lgan asosiy start buyrug'i
CMD ["uvicorn", "main_api:app", "--host", "0.0.0.0", "--port", "10000"]