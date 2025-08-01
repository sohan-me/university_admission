from .models import *
from tortoise.exceptions import DoesNotExist
from fastapi import UploadFile, HTTPException
from typing import Optional

''' Country CRUD Start '''


async def create_country(country: dict):
	country = await Country.create(**country)
	return country


async def update_country(country_id: int, country: dict):
	try:
		country_obj = await Country.get_or_none(id=country_id)
		if not country_obj:
			return None
			
		for key, value in country.items():
			if value is not None:
				setattr(country_obj, key, value)
		await country_obj.save()
		return country_obj

	except DoesNotExist:
		return None


async def country_list():
	try:
		country = await Country.all()
		return country
	except DoesNotExist:
		return None


async def retrieve_country(country_id: int):
	try:
		country = await Country.get_or_none(id=country_id)
		return country
	except DoesNotExist:
		return None	



async def delete_country(country_id: int):
	try:
		country = await Country.get_or_none(id=country_id)
		await country.delete()
		return True
	except DoesNotExist:
		return None	



''' Country CRUD End '''




''' University CRUD Start '''

async def create_university(university_data: dict):
	country_id = university_data.pop('country_id', None)
	if not country_id:
		raise HTTPException(status_code=400, detail="country_id is required")
		
	country = await Country.get_or_none(id=country_id)
	if not country:
		raise HTTPException(status_code=404, detail="Country not found")

	university_data['country'] = country
	university = await University.create(**university_data)
	await university.fetch_related('country')
	return university



async def update_university(university_id: int, university_data: dict):
	university = await University.get_or_none(id=university_id)
	if not university:
		return None

	country_id = university_data.pop('country_id', None)
	if country_id:
		country = await Country.get_or_none(id=country_id)
		if country:
			university.country = country
		else:
			raise HTTPException(status_code=404, detail="Country not found")

	for key, value in university_data.items():
		if value is not None:
			setattr(university, key, value)

	await university.save()
	await university.fetch_related('country')
	return university


async def retrieve_university(university_id: int):
	university = await University.get_or_none(id=university_id).prefetch_related('country')
	if not university:
		return None

	return university



async def list_universities(university_type: Optional[str] = None, country: Optional[int] = None):
    try:
        universities = University.all()
        if country is not None:
            universities = universities.filter(country=country)
        
        if university_type is not None:
            universities = universities.filter(varsity_type=university_type)

        universities = await universities.prefetch_related('country')
        if not universities:
            raise HTTPException(status_code=404, detail="No universities found for the given filters.")
        return universities
    
    except DoesNotExist:
        raise HTTPException(status_code=404, detail='no country objects found.')



async def delete_university(university_id: int):
	university = await University.get_or_none(id=university_id)
	if not university:
		return None
	await university.delete()
	return True


''' University CRUD End '''


''' Course CRUD Start '''

async def create_course(course_data: dict):
	university_id = course_data.pop('university_id', None)
	if not university_id:
		raise HTTPException(status_code=400, detail="university_id is required")
		
	university = await University.get_or_none(id=university_id).prefetch_related('country')
	if not university:
		raise HTTPException(status_code=404, detail="University not found")

	course_data['university'] = university
	course = await Course.create(**course_data)
	await course.fetch_related('university', 'university__country')
	return course


async def update_course(course_id: int, course_data: dict):
	course = await Course.get_or_none(id=course_id)
	if not course:
		return None

	university_id = course_data.pop('university_id', None)
	if university_id:
		university = await University.get_or_none(id=university_id).prefetch_related('country')
		if university:
			course.university = university
		else:
			raise HTTPException(status_code=404, detail="University not found")

	for key, value in course_data.items():
		if value is not None:
			setattr(course, key, value)

	await course.save()
	await course.fetch_related('university', 'university__country')
	return course


async def retrieve_course(course_id: int):
	course = await Course.get_or_none(id=course_id).prefetch_related('university', 'university__country')
	if not course:
		return None
	return course


async def list_courses():
	try:
		courses = await Course.all().prefetch_related('university', 'university__country')
		return courses
	except DoesNotExist:
		return None


async def get_courses_by_university(university_id: int):
	university = await University.get_or_none(id=university_id)
	if not university:
		return None

	courses = await Course.filter(university=university).prefetch_related('university', 'university__country')
	return list(courses) if courses else []


async def delete_course(course_id: int):
	course = await Course.get_or_none(id=course_id)
	if not course:
		return None
	await course.delete()
	return True


''' Course CRUD End '''




''' AgentAdmissionApplication CRUD Start '''

async def create_agent_admission_application(application_data: dict, agent_id: int):
    # Set the agent
    application_data['agent_id'] = agent_id
    
    # Handle foreign key relationships
    course_id = application_data.pop('course_id', None)
    if course_id:
        course = await Course.get_or_none(id=course_id).prefetch_related('university', 'university__country')
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")
        application_data['course'] = course
    
    university_one_id = application_data.pop('university_one_id', None)
    university_two_id = application_data.pop('university_two_id', None)
    university_three_id = application_data.pop('university_three_id', None)
    
    # Get universities and their countries for validation
    universities = []
    if university_one_id:
        university_one = await University.get_or_none(id=university_one_id).prefetch_related('country')
        if not university_one:
            raise HTTPException(status_code=404, detail="University one not found")
        application_data['university_one'] = university_one
        universities.append(university_one)
    
    if university_two_id:
        university_two = await University.get_or_none(id=university_two_id).prefetch_related('country')
        if not university_two:
            raise HTTPException(status_code=404, detail="University two not found")
        application_data['university_two'] = university_two
        universities.append(university_two)
    
    if university_three_id:
        university_three = await University.get_or_none(id=university_three_id).prefetch_related('country')
        if not university_three:
            raise HTTPException(status_code=404, detail="University three not found")
        application_data['university_three'] = university_three
        universities.append(university_three)
    
    # Validate university count based on country
    if universities:
        # Check if all universities are from the same country
        countries = set(uni.country.name for uni in universities)
        if len(countries) > 1:
            raise HTTPException(status_code=400, detail="All universities must be from the same country")
        
        country_name = universities[0].country.name
        university_count = len(universities)
        
        # Malaysia and Cyprus can only have 1 university
        if country_name in ['Malaysia', 'Cyprus'] and university_count > 1:
            raise HTTPException(
                status_code=400, 
                detail=f"For {country_name}, only one university is allowed"
            )
        
        # Other countries can have 1-3 universities
        elif country_name not in ['Malaysia', 'Cyprus'] and university_count > 3:
            raise HTTPException(
                status_code=400, 
                detail=f"For {country_name}, maximum 3 universities are allowed"
            )
    
    application = await AgentAdmissionApplication.create(**application_data)
    await application.fetch_related(
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
    return application


async def update_agent_admission_application(application_id: int, application_data: dict):
    application = await AgentAdmissionApplication.get_or_none(id=application_id)
    if not application:
        return None
    
    # Handle foreign key relationships
    course_id = application_data.pop('course_id', None)
    if course_id is not None:
        if course_id:
            course = await Course.get_or_none(id=course_id).prefetch_related('university', 'university__country')
            if not course:
                raise HTTPException(status_code=404, detail="Course not found")
            application.course = course
        else:
            application.course = None
    
    university_one_id = application_data.pop('university_one_id', None)
    university_two_id = application_data.pop('university_two_id', None)
    university_three_id = application_data.pop('university_three_id', None)
    
    # Get universities and their countries for validation
    universities = []
    
    if university_one_id is not None:
        if university_one_id:
            university_one = await University.get_or_none(id=university_one_id).prefetch_related('country')
            if not university_one:
                raise HTTPException(status_code=404, detail="University one not found")
            application.university_one = university_one
            universities.append(university_one)
        else:
            application.university_one = None
    
    if university_two_id is not None:
        if university_two_id:
            university_two = await University.get_or_none(id=university_two_id).prefetch_related('country')
            if not university_two:
                raise HTTPException(status_code=404, detail="University two not found")
            application.university_two = university_two
            universities.append(university_two)
        else:
            application.university_two = None
    
    if university_three_id is not None:
        if university_three_id:
            university_three = await University.get_or_none(id=university_three_id).prefetch_related('country')
            if not university_three:
                raise HTTPException(status_code=404, detail="University three not found")
            application.university_three = university_three
            universities.append(university_three)
        else:
            application.university_three = None
    
    # If universities are being updated, validate the count
    if universities:
        # Check if all universities are from the same country
        countries = set(uni.country.name for uni in universities)
        if len(countries) > 1:
            raise HTTPException(status_code=400, detail="All universities must be from the same country")
        
        country_name = universities[0].country.name
        university_count = len(universities)
        
        # Malaysia and Cyprus can only have 1 university
        if country_name in ['Malaysia', 'Cyprus'] and university_count > 1:
            raise HTTPException(
                status_code=400, 
                detail=f"For {country_name}, only one university is allowed"
            )
        
        # Other countries can have 1-3 universities
        elif country_name not in ['Malaysia', 'Cyprus'] and university_count > 3:
            raise HTTPException(
                status_code=400, 
                detail=f"For {country_name}, maximum 3 universities are allowed"
            )
    
    # Update other fields
    for key, value in application_data.items():
        if value is not None:
            setattr(application, key, value)
    
    await application.save()
    await application.fetch_related(
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
    return application


async def retrieve_agent_admission_application(application_id: int):
    application = await AgentAdmissionApplication.get_or_none(
        id=application_id,
    ).prefetch_related(
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
    if not application:
        return None
    return application


async def list_agent_admission_applications(agent_id: Optional[int] = None, status: Optional[str] = None):
    try:
        if not agent_id:
            applications = AgentAdmissionApplication.all()
        else:
            applications = AgentAdmissionApplication.filter(agent_id=agent_id)

        if status is not None:
            applications = applications.filter(status=status)

        # Only await at the end, after prefetch_related and all filters
        return await applications.prefetch_related(
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
        ).all()
    except DoesNotExist:
        return None


async def delete_agent_admission_application(application_id: int):
    application = await AgentAdmissionApplication.get_or_none(id=application_id)
    if not application:
        return None
    await application.delete()
    return True


''' AgentAdmissionApplication CRUD End '''




''' StudentAdmissionApplication CRUD Start '''

async def create_student_admission_application_crud(application_data: dict):
    country_name = application_data.get('interest_country', None)
    preferred_university_id = application_data.get('preferred_university_id')
    course_name = application_data.get('interested_course')

    country = await Country.get_or_none(name=country_name)
    if not country:
        raise HTTPException(status_code=404, detail='Country not found')

    preferred_university = await University.get_or_none(id=preferred_university_id)
    if not preferred_university:
        raise HTTPException(status_code=404, detail='Preferred university not found')

    if preferred_university.country_id != country.id:
        raise HTTPException(status_code=400, detail='Invalid university for selected country')

    course = await Course.get_or_none(name=course_name)
    if not course:
        raise HTTPException(status_code=404, detail='Course not found')

    if course.university_id != preferred_university.id:
        raise HTTPException(status_code=404, detail='Course not found')

    application = await StudentAdmissionApplication.create(**application_data)
    await application.fetch_related('documents', 'preferred_university', 'preferred_university__country')
    return application




async def update_student_admission_application_crud(application_id: int, application_data: dict):
    application = await StudentAdmissionApplication.get_or_none(id=application_id)
    if not application:
        raise HTTPException(status_code=404, detail='Application not found')

    country_name = application_data.get('interest_country')
    preferred_university_id = application_data.get('preferred_university_id')
    course_name = application_data.get('interested_course')

    if country_name:
        country = await Country.get_or_none(name=country_name)
        if not country:
            raise HTTPException(status_code=404, detail='Country not found')
    else:
        country = await Country.get_or_none(name=application.interest_country)

    if preferred_university_id:
        preferred_university = await University.get_or_none(id=preferred_university_id)
        if not preferred_university:
            raise HTTPException(status_code=404, detail='Preferred university not found')
    else:
        preferred_university = await University.get_or_none(id=application.preferred_university_id)

    if preferred_university and country and preferred_university.country_id != country.id:
        raise HTTPException(status_code=400, detail='University not found or invalid university for selected country')

    if course_name:
        course = await Course.get_or_none(name=course_name)
        if not course or course.university_id != preferred_university.id:
            raise HTTPException(status_code=404, detail='Course not found or invalid course for selected university')

    for key, value in application_data.items():
        if value is not None:
            setattr(application, key, value)

    await application.save()
    await application.fetch_related('documents', 'preferred_university', 'preferred_university__country')
    return application



async def retrieve_student_admission_application_crud(application_id: int):
    application = await StudentAdmissionApplication.get_or_none(id=application_id).prefetch_related('documents', 'preferred_university', 'preferred_university__country')
    if not application:
        return None
    return application


async def list_student_admission_applications_crud():
    try:
        applications = await StudentAdmissionApplication.all().prefetch_related('documents', 'preferred_university', 'preferred_university__country')
        return applications
    except DoesNotExist:
        return None


async def delete_student_admission_application_crud(application_id: int):
    application = await StudentAdmissionApplication.get_or_none(id=application_id)
    if not application:
        return None
    await application.delete()
    return True


''' StudentAdmissionApplication CRUD End '''





''' Agent Application Commision Start '''

async def create_commission(application_id: int):
    commisison = await AgentApplicationCommission.create(admission_application=application_id)
    return commisison



async def update_commission(application_id: int, commission_data: dict):
    application = await AgentAdmissionApplication.get_or_none(id=application_id)
    if not application:
        return None

    commission, created = await AgentApplicationCommission.get_or_create(admission_application=application)
    for key, value in commission_data.items():
        if value is not None:
            setattr(commission, key, value)
    await commission.save()
    return commission



''' Agent Application Commision End '''







