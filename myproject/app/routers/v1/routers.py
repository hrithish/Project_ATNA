from fastapi import APIRouter
from .sample_router import session_router
router = APIRouter(prefix='/v1', tags=['v1'])

router.include_router(session_router) #changed sample router to session router



