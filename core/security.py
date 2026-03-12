from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader

# Xavfsizlik kaliti nomi (So'rovning Header qismida shunday nom bilan keladi)
API_KEY_NAME = "X-API-Key"

# O'zimizning maxfiy kalitimiz (Buni hakerlar bilmasligi kerak!)
SECRET_API_KEY = "Nurli_Super_Secret_Key_2026_!@#"

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != SECRET_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Ruxsat etilmagan! Xavfsizlik kaliti xato yoki yo'q.",
        )
    return api_key