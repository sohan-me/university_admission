from users.dependencies import get_current_user, get_active_user, get_admin_user
from fastapi import APIRouter, HTTPException, status, Depends, UploadFile, File
from typing import List
from .cruds import *
from .schemas import *
from .models import University, Course
from users.cruds import upload_file

router = APIRouter()


''' Country CRUD Start '''

@router.post('/country', response_model=CountryResponse)
async def add_a_country(country: CountryBase, admin_user=Depends(get_admin_user)):
    if not admin_user:
        raise HTTPException(status_code=403, detail='Unauthorized access!')

    country_obj = await create_country(country.dict())
    if not country_obj:
        raise HTTPException(status_code=400, detail='Could not create country!')
    return country_obj


@router.get('/country', response_model=List[CountryResponse])
async def list_of_countries():
    countries = await country_list()
    if not countries:
        raise HTTPException(status_code=404, detail='No countries found.')
    return countries


@router.get('/country/{country_id}', response_model=CountryResponse)
async def retrieve_a_country(country_id: int):
    country = await retrieve_country(country_id)
    if not country:
        raise HTTPException(status_code=404, detail='Country not found.')
    return country


@router.patch('/country/{country_id}', response_model=CountryResponse)
async def update_a_country(country_id: int, country: CountryBase, admin_user=Depends(get_admin_user)):
    if not admin_user:
        raise HTTPException(status_code=403, detail='Unauthorized access!')

    country_obj = await update_country(country_id, country.dict())
    if not country_obj:
        raise HTTPException(status_code=404, detail='Country not found.')
    return country_obj


@router.delete('/country/{country_id}')
async def delete_a_country(country_id: int, admin_user=Depends(get_admin_user)):
    if not admin_user:
        raise HTTPException(status_code=403, detail='Unauthorized access!')

    country_deleted = await delete_country(country_id)
    if not country_deleted:
        raise HTTPException(status_code=404, detail='Country not found.')
    return {'detail': 'Country deleted.'}


''' Country CRUD End '''


''' University CRUD Start '''

@router.get('/university', response_model=List[UniversityResponse])
async def list_of_universities():
    universities = await list_universities()
    if not universities:
        raise HTTPException(status_code=404, detail='No universities found.')
    return universities


@router.get('/country/{country_id}/university', response_model=List[UniversityResponse])
async def universities_by_country(country_id: int):
    universities = await get_universities_by_country(country_id)
    if universities is None:
        raise HTTPException(status_code=404, detail='Country not found!')
    return universities



@router.get('/university/{university_id}', response_model=UniversityResponse)
async def retrieve_a_university(university_id: int):
    university = await retrieve_university(university_id)
    if not university:
        raise HTTPException(status_code=404, detail='University not found.')
    return university


@router.post('/university', response_model=UniversityResponse)
async def add_a_university(university_data: UniversityCreate, admin_user=Depends(get_admin_user)):
    if not admin_user:
        raise HTTPException(status_code=403, detail='Unauthorized access!')
    
    university = await create_university(university_data.dict())
    if not university:
        raise HTTPException(status_code=400, detail='Could not create university.')
    return university


@router.patch('/university/{university_id}', response_model=UniversityResponse)
async def update_a_university(university_id: int, university_data: UniversityUpdate, admin_user=Depends(get_admin_user)):
    if not admin_user:
        raise HTTPException(status_code=403, detail='Unauthorized access!')

    university = await update_university(university_id, university_data.dict())
    if not university:
        raise HTTPException(status_code=404, detail='University not found.')
    return university


@router.delete('/university/{university_id}')
async def delete_a_university(university_id: int, admin_user=Depends(get_admin_user)):
    if not admin_user:
        raise HTTPException(status_code=403, detail='Unauthorized access!')
    
    university_deleted = await delete_university(university_id)
    if not university_deleted:
        raise HTTPException(status_code=404, detail='University not found.')
    return {'detail': 'University deleted.'}



@router.post('/university/{university_id}/upload-image/', response_model=UniversityResponse)
async def upload_university_image(university_id: int, university_image: UploadFile = File(...), admin_user=Depends(get_admin_user)):
    if not admin_user:
        raise HTTPException(status_code=403, detail='Unauthorized access!')

    university = await University.get_or_none(id=university_id).prefetch_related('country')
    if not university:
        raise HTTPException(status_code=404, detail='Not found!')

    try:
        file_path = await upload_file(
            file=university_image,
            file_type='university_image',
            allowed_types=['image/'],
            max_size_mb=5,
            media_dir='images'
        )

        university.image = file_path
        await university.save(update_fields=['image'])
        return university

    except HTTPException as e:
        return e




''' University CRUD End '''


''' Course CRUD Start '''

@router.get('/course', response_model=List[CourseResponse])
async def list_of_courses():
    courses = await list_courses()
    if not courses:
        raise HTTPException(status_code=404, detail='No courses found.')
    return courses


@router.get('/course/{course_id}', response_model=CourseResponse)
async def retrieve_a_course(course_id: int):
    course = await retrieve_course(course_id)
    if not course:
        raise HTTPException(status_code=404, detail='Course not found.')
    return course


@router.get('/university/{university_id}/course', response_model=List[CourseResponse])
async def courses_by_university(university_id: int):
    courses = await get_courses_by_university(university_id)
    if courses is None:
        raise HTTPException(status_code=404, detail='University not found!')
    return courses


@router.post('/course', response_model=CourseResponse)
async def add_a_course(course_data: CourseCreate, admin_user=Depends(get_admin_user)):
    if not admin_user:
        raise HTTPException(status_code=403, detail='Unauthorized access!')
    
    course = await create_course(course_data.dict())
    if not course:
        raise HTTPException(status_code=400, detail='Could not create course.')
    return course


@router.patch('/course/{course_id}', response_model=CourseResponse)
async def update_a_course(course_id: int, course_data: CourseUpdate, admin_user=Depends(get_admin_user)):
    if not admin_user:
        raise HTTPException(status_code=403, detail='Unauthorized access!')

    course = await update_course(course_id, course_data.dict())
    if not course:
        raise HTTPException(status_code=404, detail='Course not found.')
    return course


@router.delete('/course/{course_id}')
async def delete_a_course(course_id: int, admin_user=Depends(get_admin_user)):
    if not admin_user:
        raise HTTPException(status_code=403, detail='Unauthorized access!')
    
    course_deleted = await delete_course(course_id)
    if not course_deleted:
        raise HTTPException(status_code=404, detail='Course not found.')
    return {'detail': 'Course deleted.'}


@router.post('/course/{course_id}/upload-image', response_model=CourseResponse)
async def upload_course_image(course_id: int, course_image: UploadFile=File(...), admin_user=Depends(get_admin_user)):
    if not admin_user:
        raise HTTPException(status_code=403, detail='Unauthorized access!')

    course = await Course.get_or_none(id=course_id).prefetch_related('university', 'university__country')
    if not course:
        raise HTTPException(status_code=404, detail='Not found!')


    try:
        file_path = await upload_file(
            file=course_image,
            file_type='course_image',
            allowed_types = ['image/'],
            max_size_mb=5,
            media_dir='images'
        )


        course.image = file_path
        await course.save(update_fields=['image'])
        return course

    except HTTPException as e:
        return e





''' Course CRUD End '''