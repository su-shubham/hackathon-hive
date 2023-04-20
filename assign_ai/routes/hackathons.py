from fastapi import APIRouter, status, Depends, HTTPException
from sqlmodel import Session, select
from schemas import CreateHackathon, UpdateHackathon
from models import Hackathon, HackathonUser
from db import get_session
from .users import current_user
from schemas import User
import uuid


router = APIRouter(prefix="/hackathons", tags=["Hackathons"])


@router.get("/")
def list_hackathons(session: Session = Depends(get_session)):
    hackathon = select(Hackathon)
    result = session.exec(hackathon).all()
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Hackathon not found"
        )  # noqa: E501
    return result


@router.get("/{hackathon_id}")
def get_hackathon_id(hackathon_id: str, session: Session = Depends(get_session)):
    hackathon = select(Hackathon).where(Hackathon.id == hackathon_id)
    result = session.exec(hackathon).first()
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"{hackathon_id}is not found"
        )  # noqa: E501
    return result


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_hackathon(
    hackathons: CreateHackathon,
    session: Session = Depends(get_session),
    current_user: User = Depends(current_user),
):  # noqa: E501
    if not current_user:
        raise HTTPException(
            status_code=404, detail="User is not currently logged in"
        )  # noqa: E501
    hackathon = Hackathon(**hackathons.dict())
    session.add(hackathon)
    session.commit()
    session.refresh(hackathon)
    return hackathon


@router.put("/{hackathon_id}", response_model=Hackathon)
def update_hackathon(
    hackathon_id: str,
    hackathons: UpdateHackathon,
    session: Session = Depends(get_session),
):  # noqa: E501
    update_hackathon = session.get(Hackathon, hackathon_id)
    if not update_hackathon:
        raise HTTPException(status_code=404, detail="Hackathon not found")
    for field, value in hackathons.dict(exclude_unset=True).items():
        setattr(update_hackathon, field, value)
    session.add(update_hackathon)
    session.commit()
    session.refresh(update_hackathon)
    return update_hackathon


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_to_hackathon(
    hackathon_id: uuid.UUID,
    current_user: User = Depends(current_user),
    session: Session = Depends(get_session),
):  # noqa: E501
    if not current_user:
        raise HTTPException(
            status_code=404, detail="To register first needs to be logged In....."
        )  # noqa: E501
    hackathon = session.get(Hackathon, hackathon_id)
    if not hackathon:
        raise HTTPException(status_code=404, detail="Hackathon not found")
    existing_registration = (
        session.query(HackathonUser)
        .filter_by(hackathon_id=hackathon_id, user_id=current_user.id)
        .first()
    )  # noqa: E501
    if existing_registration:
        raise HTTPException(
            status_code=400, detail="User has already registered for this hackathon"
        )  # noqa: E501
    register = HackathonUser(hackathon_id=hackathon_id, user_id=current_user.id)
    session.add(register)
    session.commit()
    session.refresh(register)
    return register

@router.get("/hackathons")
async def read_hackathons_for_current_user(
    current_user: User = Depends(current_user)
):
    hackathons = await current_user.hackathons
    return hackathons




