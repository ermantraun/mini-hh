from fastapi import APIRouter, Depends, HTTPException
from dishka.integrations.fastapi import FromDishka, DishkaRoute
from api.schemas.improvement import ImprovementOut, ImprovementList
from application.improvement.interactors import ImprovementInteractor
from application.resume.exceptions import ResumeNotFound
from api.handlers.deps import get_current_user_id

router = APIRouter(prefix="/resumes/{resume_id}/improvements", tags=["improvements"], route_class=DishkaRoute)

@router.post("/improve", response_model=ImprovementOut)
async def improve_resume(
    resume_id: int,
    interactor: FromDishka[ImprovementInteractor],
    user_id: int = Depends(get_current_user_id),
    
):
    try:
        rec = await interactor.improve(user_id, resume_id)
        return ImprovementOut(**rec.__dict__)
    except ResumeNotFound:
        raise HTTPException(status_code=404, detail="Resume not found")

@router.get("", response_model=ImprovementList)
async def list_improvements(
    resume_id: int,
    interactor: FromDishka[ImprovementInteractor],
    user_id: int = Depends(get_current_user_id),
    
):
    try:
        rows = await interactor.list_improvements(user_id, resume_id)
        return ImprovementList(items=[ImprovementOut(**r.__dict__) for r in rows])
    except ResumeNotFound:
        raise HTTPException(status_code=404, detail="Resume not found")