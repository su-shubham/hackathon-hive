from pydantic import BaseModel

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    username:str = None

class CreateUser(BaseModel):
    username:str
    email:str
    password:str
    full_name:str

class ResponseUser(BaseModel):
    username:str
    email:str
    full_name:str

class CreateHackathon(BaseModel):
    title:str
    description:str
    background_image:str
    hackathon_image:str
    type_of_submission:str
    start_datetime:str
    end_datetime:str
    reward_prize:float

class UpdateHackathon(BaseModel):
    title:str
    description:str
    background_image:str
    hackathon_image:str
    type_of_submission:str
    start_datetime:str
    end_datetime:str
    reward_prize:float

class User(BaseModel):
    email:str | None = None
    password:str | None = None

class UserInDB(User):
    hashed_password: str

class RegisterHackathon(BaseModel):
    user_id:str
    hackathon_id:str

    