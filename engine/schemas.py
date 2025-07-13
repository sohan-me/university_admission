from pydantic import BaseModel, EmailStr
from typing import Optional
from fastapi import UploadFile



class CountryBase(BaseModel):
	name : str


class CountryResponse(CountryBase):
	id : int

	class Config:
		orm_mode = True



class UniversityBase(BaseModel):
	varsity_type : str
	name : str
	location : str


class UniversityCreate(UniversityBase):
	country_id: int

	class Config:
		orm_mode = True


class UniversityUpdate(BaseModel):
	varsity_type: Optional[str] = None
	name: Optional[str] = None
	location: Optional[str] = None
	country_id: Optional[int] = None


class UniversityResponse(UniversityBase):
	id : int
	country : CountryResponse
	image: Optional[str] = None

	class Config:
		orm_mode = True




class CourseBase(BaseModel):
	course_type : str
	fee : int


class CourseCreate(CourseBase):
	university_id: int


class CourseUpdate(BaseModel):
	course_type: Optional[str] = None
	fee: Optional[int] = None
	university_id: Optional[int] = None
	

class CourseResponse(CourseBase):
	id: int
	university : UniversityResponse
	image: Optional[str] = None

	class Config:
		orm_mode = True


''' Agent Application Documents Schemas Start'''


class AgentApplicationDocumentsCreate(BaseModel):
    admission_application_id: int


class AgentApplicationDocumentsResponse(BaseModel):
    id: int
    admission_application_id: int
    passport: Optional[str] = None
    masters_certificate: Optional[str] = None
    masters_transcript: Optional[str] = None
    honers_certificate: Optional[str] = None
    honers_transcript: Optional[str] = None
    hsc_certificate: Optional[str] = None
    hsc_transcript: Optional[str] = None
    ssc_certificate: Optional[str] = None
    ssc_transcript: Optional[str] = None
    ielts_certificate: Optional[str] = None
    cv: Optional[str] = None
    resume: Optional[str] = None
    lor: Optional[str] = None
    job_letter: Optional[str] = None
    others: Optional[str] = None

    class Config:
        orm_mode = True



''' Agent Application Documents Schemas End'''


''' Student Admission Application Schemas Start '''

class StudentAdmissionApplicationBase(BaseModel):
    name: str
    phone: str
    email: Optional[str] = None
    residence_country: str
    interest_country: str
    intake_interest: str
    last_graduation: str
    interested_course: str
    current_stage: Optional[str] = None


class StudentAdmissionApplicationCreate(StudentAdmissionApplicationBase):
    pass


class StudentAdmissionApplicationUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    residence_country: Optional[str] = None
    interest_country: Optional[str] = None
    intake_interest: Optional[str] = None
    last_graduation: Optional[str] = None
    interested_course: Optional[str] = None
    current_stage: Optional[str] = None


class StudentApplicationDocumentsResponse(BaseModel):
    id: int
    admission_application_id: int
    passport: Optional[str] = None
    last_graduation_certificate: Optional[str] = None

    class Config:
        orm_mode = True


class StudentAdmissionApplicationResponse(StudentAdmissionApplicationBase):
    id: int
    documents: Optional[StudentApplicationDocumentsResponse] = None

    class Config:
        orm_mode = True


''' Student Admission Application Schemas End '''


''' Agent Admission Application Schemas Start'''



class AgentAdmissionApplicationBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str
    passport_no: str
    last_graduation: Optional[str] = None


class AgentAdmissionApplicationCreate(AgentAdmissionApplicationBase):
    course_id: Optional[int] = None
    university_one_id: Optional[int] = None
    university_two_id: Optional[int] = None
    university_three_id: Optional[int] = None


class AgentAdmissionApplicationUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    passport_no: Optional[str] = None
    course_id: Optional[int] = None
    university_one_id: Optional[int] = None
    university_two_id: Optional[int] = None
    university_three_id: Optional[int] = None
    last_graduation: Optional[str] = None


class AgentAdmissionApplicationResponse(AgentAdmissionApplicationBase):
    id: int
    agent_id: int
    course: Optional[CourseResponse] = None
    university_one: Optional[UniversityResponse] = None
    university_two: Optional[UniversityResponse] = None
    university_three: Optional[UniversityResponse] = None
    documents: Optional[AgentApplicationDocumentsResponse] = None

    class Config:
        orm_mode = True


''' Agent Admission Application Schemas End'''




