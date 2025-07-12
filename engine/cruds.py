from .models import *
from tortoise.exceptions import DoesNotExist
from fastapi import UploadFile, HTTPException

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



async def list_universities():
	try:
		universities = await University.all().prefetch_related('country')
		return universities
	except DoesNotExist:
		return None



async def get_universities_by_country(country_id: int):
	country = await Country.get_or_none(id=country_id)
	if not country:
		return None

	universities = await University.filter(country=country).prefetch_related('country')
	return list(universities) if universities else []



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