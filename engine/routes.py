from fastapi import APIRouter, HTTPException, status, Depends, UploadFile, File, Form
from typing import List, Optional, Union
from .cruds import *
from .schemas import *
from .models import University, Course, AgentAdmissionApplication, AgentApplicationDocuments, StudentAdmissionApplication, StudentApplicationDocuments, AgentApplicationCommission
from users.cruds import upload_file
from users.dependencies import get_admin_user, get_agent_user, get_active_user

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


''' AgentAdmissionApplication CRUD Start '''

@router.post('/agent/admission-application', response_model=AgentAdmissionApplicationResponse)
async def create_admission_application(
    application: AgentAdmissionApplicationCreate, 
    agent_user=Depends(get_agent_user)
):
    if not agent_user:
        raise HTTPException(status_code=403, detail='Unauthorized access!')

    application_obj = await create_agent_admission_application(application.dict(), agent_user.id)
    if not application_obj:
        raise HTTPException(status_code=400, detail='Could not create admission application!')

    # Create commission for the application
    await AgentApplicationCommission.get_or_create(admission_application=application_obj)

    return application_obj




@router.get('/agent/admission-application', response_model=List[AgentAdmissionApplicationResponse])
async def list_admission_applications(status: Optional[str] = None, active_user=Depends(get_active_user)):
    if not active_user:
        raise HTTPException(status_code=403, detail='Unauthorized access!')

    applications = None
    if active_user.is_admin:
        # applications = await AgentAdmissionApplication.all().prefetch_related(
        #     'course', 
        #     'course__university', 
        #     'course__university__country',
        #     'university_one', 
        #     'university_one__country',
        #     'university_two', 
        #     'university_two__country',
        #     'university_three', 
        #     'university_three__country',
        #     'documents',
        #     'commission'
        # )
        applications = await list_agent_admission_applications(status=status)

    else:
        applications = await list_agent_admission_applications(agent_id=active_user.id, status=status)
    
    if not applications:
        raise HTTPException(status_code=404, detail='No admission applications found.')


    return applications




@router.get('/agent/admission-application/{application_id}', response_model=AgentAdmissionApplicationResponse)
async def retrieve_admission_application(
    application_id: int, 
    active_user=Depends(get_active_user)
):
    if not active_user:
        raise HTTPException(status_code=403, detail='Unauthorized access!')

    # If admin, can view any application; if agent, only their own
    if active_user.is_admin:
        application = await AgentAdmissionApplication.get_or_none(id=application_id).prefetch_related(
            'course', 
            'course__university', 
            'course__university__country',
            'university_one', 
            'university_one__country',
            'university_two', 
            'university_two__country',
            'university_three', 
            'university_three__country',
            'documents',
            'commission'
        )
    else:
        application = await retrieve_agent_admission_application(application_id, active_user.id)
    
    if not application:
        raise HTTPException(status_code=404, detail='Admission application not found.')
    return application


@router.patch('/agent/admission-application/{application_id}', response_model=AgentAdmissionApplicationResponse)
async def update_admission_application(
    application_id: int, 
    application: AgentAdmissionApplicationUpdate, 
    active_user=Depends(get_active_user)
):
    if not active_user:
        raise HTTPException(status_code=403, detail='Unauthorized access!')

    application_obj = await update_agent_admission_application(application_id, application.dict())
    if not application_obj:
        raise HTTPException(status_code=404, detail='Admission application not found.')
    return application_obj


@router.delete('/agent/admission-application/{application_id}')
async def delete_admission_application(
    application_id: int, 
    active_user=Depends(get_active_user)
):
    if not active_user:
        raise HTTPException(status_code=403, detail='Unauthorized access!')

    application_deleted = await delete_agent_admission_application(application_id)
    if not application_deleted:
        raise HTTPException(status_code=404, detail='Admission application not found.')
    return {'detail': 'Admission application deleted.'}


''' AgentAdmissionApplication CRUD End '''


''' AgentApplicationDocuments CRUD Start '''


@router.post('/agent/application-documents/{application_id}/upload', response_model=AgentApplicationDocumentsResponse)
async def upload_application_documents(
    application_id: int,
    files: List[UploadFile] = File(...),
    field_names: List[str] = Form(...),
    agent_user=Depends(get_agent_user)
):
    if not agent_user:
        raise HTTPException(status_code=403, detail='Unauthorized access!')

    # Verify the application belongs to the agent
    application = await AgentAdmissionApplication.get_or_none(
        id=application_id, 
        agent_id=agent_user.id
    )
    if not application:
        raise HTTPException(status_code=404, detail="Admission application not found")
    
    # Get or create documents record for this application
    documents, created = await AgentApplicationDocuments.get_or_create(
        admission_application_id=application_id
    )
    
    # Parse field names from comma-separated string
    field_names_list = [name.strip() for name in field_names[0].split(',') if name.strip()]
    
    # Validate field names
    valid_fields = [
        'passport', 'masters_certificate', 'masters_transcript', 'honers_certificate',
        'honers_transcript', 'hsc_certificate', 'hsc_transcript', 'ssc_certificate',
        'ssc_transcript', 'ielts_certificate', 'cv', 'resume', 'lor', 'job_letter', 'others'
    ]
    
    # Check if number of files matches number of field names
    if len(files) != len(field_names_list):
        raise HTTPException(
            status_code=400, 
            detail=f"Number of files ({len(files)}) must match number of field names ({len(field_names_list)}). Field names: {field_names_list}"
        )
    
    try:
        for file, field_name in zip(files, field_names_list):
            # Validate field name
            if field_name not in valid_fields:
                raise HTTPException(status_code=400, detail=f"Invalid field name: {field_name}")
            
            # Skip if file is empty
            if not file or file.filename == "":
                continue
                
            file_path = await upload_file(
                file=file,
                file_type=f'document_{field_name}',
                allowed_types=['image/', 'application/pdf'],
                max_size_mb=5,
                media_dir='documents'
            )
            setattr(documents, field_name, file_path)
        
        await documents.save()
        await documents.fetch_related('admission_application')
        return documents
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


''' AgentApplicationDocuments CRUD End '''


''' AgentApplicationCommission CRUD Start '''

@router.patch('/agent/commission/{application_id}', response_model=AgentApplicationCommissionResponse)
async def patch_commission(
    application_id: int, 
    commission: AgentApplicationCommissionUpdate,
    admin_user=Depends(get_admin_user)
):
    if not admin_user:
        raise HTTPException(status_code=403, detail='Unauthorized access!')

    application = await AgentAdmissionApplication.get_or_none(id=application_id)
    if not application:
        raise HTTPException(status_code=404, detail="Admission application not found")

    commission_obj = await update_commission(application_id, commission.dict())
    if not commission_obj:
        raise HTTPException(status_code=404, detail='Commission not found or could not be updated.')
    return commission_obj


''' AgentApplicationCommission CRUD End '''


''' StudentAdmissionApplication CRUD Start '''

@router.post('/student/admission-application', response_model=StudentAdmissionApplicationResponse)
async def create_student_admission_application(
    application: StudentAdmissionApplicationCreate
):
    application_obj = await create_student_admission_application_crud(application.dict())
    if not application_obj:
        raise HTTPException(status_code=400, detail='Could not create admission application!')
    return application_obj


@router.get('/student/admission-application', response_model=List[StudentAdmissionApplicationResponse])
async def list_student_admission_applications(admin_user=Depends(get_admin_user)):
    if not admin_user:
        raise HTTPException(status_code=403, detail='Unauthorized access!')

    applications = await list_student_admission_applications_crud()
    if not applications:
        raise HTTPException(status_code=404, detail='No admission applications found.')
    return applications


@router.get('/student/admission-application/{application_id}', response_model=StudentAdmissionApplicationResponse)
async def retrieve_student_admission_application(
    application_id: int, 
    admin_user=Depends(get_admin_user)
):
    if not admin_user:
        raise HTTPException(status_code=403, detail='Unauthorized access!')

    application = await retrieve_student_admission_application_crud(application_id)
    if not application:
        raise HTTPException(status_code=404, detail='Admission application not found.')
    return application


@router.patch('/student/admission-application/{application_id}', response_model=StudentAdmissionApplicationResponse)
async def update_student_admission_application(
    application_id: int, 
    application: StudentAdmissionApplicationUpdate,
    admin_user=Depends(get_admin_user)
):
    if not admin_user:
        raise HTTPException(status_code=403, detail='Unauthorized access!')

    application_obj = await update_student_admission_application_crud(application_id, application.dict())
    if not application_obj:
        raise HTTPException(status_code=404, detail='Admission application not found.')
    return application_obj


@router.delete('/student/admission-application/{application_id}')
async def delete_student_admission_application(
    application_id: int,
    admin_user=Depends(get_admin_user)
):
    if not admin_user:
        raise HTTPException(status_code=403, detail='Unauthorized access!')

    application_deleted = await delete_student_admission_application_crud(application_id)
    if not application_deleted:
        raise HTTPException(status_code=404, detail='Admission application not found.')
    return {'detail': 'Admission application deleted.'}


@router.post('/student/application-documents/{application_id}/upload', response_model=StudentApplicationDocumentsResponse)
async def upload_student_application_documents(
    application_id: int,
    files: List[UploadFile] = File(...),
    field_names: List[str] = Form(...),
):
    # Verify the application exists
    application = await StudentAdmissionApplication.get_or_none(id=application_id)
    if not application:
        raise HTTPException(status_code=404, detail="Admission application not found")
    
    # Get or create documents record for this application
    documents, created = await StudentApplicationDocuments.get_or_create(
        admission_application_id=application_id
    )
    
    # Parse field names from comma-separated string
    field_names_list = [name.strip() for name in field_names[0].split(',') if name.strip()]
    
    # Validate field names
    valid_fields = ['passport', 'last_graduation_certificate']
    
    # Check if number of files matches number of field names
    if len(files) != len(field_names_list):
        raise HTTPException(
            status_code=400, 
            detail=f"Number of files ({len(files)}) must match number of field names ({len(field_names_list)}). Field names: {field_names_list}"
        )
    
    try:
        for file, field_name in zip(files, field_names_list):
            # Validate field name
            if field_name not in valid_fields:
                raise HTTPException(status_code=400, detail=f"Invalid field name: {field_name}")
            
            # Skip if file is empty
            if not file or file.filename == "":
                continue
                
            file_path = await upload_file(
                file=file,
                file_type=f'document_{field_name}',
                allowed_types=['image/', 'application/pdf'],
                max_size_mb=5,
                media_dir='documents'
            )
            setattr(documents, field_name, file_path)
        
        await documents.save()
        await documents.fetch_related('admission_application')
        return documents
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


''' StudentAdmissionApplication CRUD End '''

