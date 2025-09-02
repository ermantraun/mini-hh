from fastapi import APIRouter, Depends, HTTPException
from dishka.integrations.fastapi import FromDishka, DishkaRoute
from api.schemas.resume import ResumeCreate, ResumeUpdate, ResumeOut, ResumeList
from application.resume.interactors import ResumeInteractor
from application.resume.exceptions import ResumeNotFound
from api.handlers.deps import get_current_user_id

router = APIRouter(prefix="/resumes", tags=["resumes"], route_class=DishkaRoute)

@router.post("", response_model=ResumeOut, status_code=201)
async def create_resume(
    payload: ResumeCreate,
    interactor: FromDishka[ResumeInteractor],
    user_id: int = Depends(get_current_user_id),
    
):
    r = await interactor.create(user_id, payload.title, payload.content)
    return ResumeOut(**r.__dict__)

@router.get("", response_model=ResumeList)
async def list_resumes(
    interactor: FromDishka[ResumeInteractor],
    user_id: int = Depends(get_current_user_id),
    
):
    items = await interactor.list_user(user_id)
    return ResumeList(items=[ResumeOut(**x.__dict__) for x in items])

@router.get("/{resume_id}", response_model=ResumeOut)
async def get_resume(
    resume_id: int,
    interactor: FromDishka[ResumeInteractor],
    user_id: int = Depends(get_current_user_id),
    
):
    try:
        r = await interactor.get(user_id, resume_id)
        return ResumeOut(**r.__dict__)
    except ResumeNotFound:
        raise HTTPException(status_code=404, detail="Not found")

@router.put("/{resume_id}", response_model=ResumeOut)
async def update_resume(
    resume_id: int,
    payload: ResumeUpdate,
    interactor: FromDishka[ResumeInteractor],
    user_id: int = Depends(get_current_user_id),
    
):
    try:
        r = await interactor.update(user_id, resume_id, payload.title, payload.content)
        return ResumeOut(**r.__dict__)
    except ResumeNotFound:
        raise HTTPException(status_code=404, detail="Not found")

@router.delete("/{resume_id}", status_code=204)
async def delete_resume(
    resume_id: int,
    interactor: FromDishka[ResumeInteractor],
    user_id: int = Depends(get_current_user_id),
    
):
    try:
        await interactor.delete(user_id, resume_id)
    except ResumeNotFound:
        raise HTTPException(status_code=404, detail="Not found")