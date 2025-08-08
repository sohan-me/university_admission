from pydantic import BaseModel, EmailStr
from typing import Optional
from fastapi import UploadFile
from .models import VarsityType
from datetime import datetime

class CountryBase(BaseModel):
    name: str
    description: Optional[str] = None

class CountryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class CountryResponse(CountryBase):
	id : int

	class Config:
		orm_mode = True



class UniversityBase(BaseModel):
    varsity_type: VarsityType
    name: str
    description: Optional[str] = None
    location: str
    website_link: Optional[str] = None

    class Config:
        use_enum_values = True


class UniversityCreate(UniversityBase):
	country_id: int

	class Config:
		orm_mode = True


class UniversityUpdate(BaseModel):
    varsity_type: Optional[VarsityType] = None
    name: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    country_id: Optional[int] = None
    website_link: Optional[str] = None
    

class UniversityResponse(UniversityBase):
	id : int
	country : CountryResponse
	image: Optional[str] = None

	class Config:
		orm_mode = True



class CourseBase(BaseModel):
    name: str
    course_type: str
    fee: int
    description: Optional[str] = None


class CourseCreate(CourseBase):
	university_id: int


class CourseUpdate(BaseModel):
    name: Optional[str] = None
    course_type: Optional[str] = None
    fee: Optional[int] = None
    description: Optional[str] = None
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

''' Intake Admission Application Schemas Start '''

class IntakeBase(BaseModel):
    name: str


class IntakeCreate(IntakeBase):
    pass


class IntakeUpdate(IntakeBase):
    pass


class IntakeResponse(IntakeBase):
    id: int

    class Config:
        orm_mode = True

''' Intake Admission Application Schemas End '''



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
    preferred_university_id: Optional[int] = None


class StudentAdmissionApplicationUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    preferred_university_id: Optional[int] = None
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
    preferred_university: UniversityResponse
    documents: Optional[StudentApplicationDocumentsResponse] = None

    class Config:
        orm_mode = True


''' Student Admission Application Schemas End '''



''' Agent Application Commision Start '''

class AgentApplicationCommissionBase(BaseModel):
    student_fee: int
    commission: int
    commission_rate: int


class AgentApplicationCommissionUpdate(BaseModel):
    student_fee: Optional[int] = None
    commission: Optional[int] = None
    commission_rate: Optional[int] = None


class AgentApplicationCommissionResponse(AgentApplicationCommissionBase):
    id: int
    admission_application_id: int

    class Config:
        orm_mode = True

        

''' Agent Application Commission End '''


''' Agent Admission Application Schemas Start'''



class AgentAdmissionApplicationBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str
    passport_no: str
    last_graduation: Optional[str] = None
    status: Optional[str] = None


class AgentAdmissionApplicationCreate(AgentAdmissionApplicationBase):
    country_id: int
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
    country_id: Optional[int] = None
    course_id: Optional[int] = None
    university_one_id: Optional[int] = None
    university_two_id: Optional[int] = None
    university_three_id: Optional[int] = None
    last_graduation: Optional[str] = None
    status: Optional[str] = None
    status: Optional[str] = None


class AgentAdmissionApplicationResponse(AgentAdmissionApplicationBase):
    id: int
    agent_id: int
    country_id: Optional[int] = None
    course: Optional[CourseResponse] = None
    university_one: Optional[UniversityResponse] = None
    university_two: Optional[UniversityResponse] = None
    university_three: Optional[UniversityResponse] = None
    documents: Optional[AgentApplicationDocumentsResponse] = None
    commission: Optional[AgentApplicationCommissionResponse] = None

    class Config:
        orm_mode = True


''' Agent Admission Application Schemas End'''




''' Blogs, Events and Offers SCHEMA Start '''

class BlogAndEventBase(BaseModel):
    type: str
    title: str
    description: str


class BlogAndEventCreate(BlogAndEventBase):
    pass

class BlogAndEventUpdate(BaseModel):
    type: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None


class BlogAndEventResponse(BlogAndEventBase):
    id: int
    image: Optional[str] = None
    published_at: datetime

    class Config:
        orm_mode = True

class OffersResponse(BaseModel):
    id: int
    image: str

''' Blogs, Events and Offers SCHEMA End '''

class Base64FileUpload(BaseModel):
    file_data: str  # base64 encoded file
    filename: str