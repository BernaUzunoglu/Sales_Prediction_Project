from fastapi import APIRouter
# API Sağlık Kontrolü - API’nin çalışıp çalışmadığını kontrol eden basit bir endpoint.
router = APIRouter()

@router.get("/")
def health_check():
    breakpoint()
    return {"status": "API is running smoothly!"}
