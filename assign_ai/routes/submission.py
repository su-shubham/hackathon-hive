from uuid import UUID

from db import get_session
from fastapi import APIRouter, Depends, HTTPException
from models import Hackathon, HackathonUser, Submission, User
from schemas import CreateSubmission, ResponseSubmission
from sqlalchemy.orm import Session

from .users import current_user

router = APIRouter(prefix="/submissions", tags=["Submissions"])


@router.post(
    "/hackathons/{hackathon_id}/submissions", response_model=ResponseSubmission
)
def create_submission(
    hackathon_id: UUID,
    submission: CreateSubmission,
    db: Session = Depends(get_session),
    current_user: User = Depends(current_user),
):
    hackathon = db.query(Hackathon).filter(Hackathon.id == hackathon_id).first()
    if not hackathon:
        raise HTTPException(status_code=404, detail="Hackathon not found")
    user_hackathon = (
        db.query(HackathonUser)
        .filter(
            HackathonUser.hackathon_id == hackathon_id,
            HackathonUser.user_id == current_user.id,
        )
        .first()
    )
    if not user_hackathon:
        raise HTTPException(
            status_code=400, detail="User not enrolled in the hackathon"
        )
    if hackathon.type_of_submission == "type1":
        pass
    elif hackathon.type_of_submission == "type2":
        pass
    else:
        raise HTTPException(status_code=500, detail="Invalid type_of_submission")

    db_submission = Submission(
        name=submission.name,
        summary=submission.summary,
        submission=submission.submission,
        hackathon_id=hackathon_id,
        user_id=current_user.id,
    )
    db.add(db_submission)
    db.commit()
    db.refresh(db_submission)
    return ResponseSubmission(**db_submission.dict())
