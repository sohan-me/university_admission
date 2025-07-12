from pydantic import BaseModel, EmailStr
from typing import Optional



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