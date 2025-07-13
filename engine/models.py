from tortoise import fields, models
from enum import Enum
from users.models import User


class VarsityType(str, Enum):
    PUBLIC = 'Public'
    PRIVATE = 'Private'
    SEMI_PUBLIC = 'Semi Public'



class Country(models.Model):
	id = fields.IntField(pk=True)
	name = fields.CharField(100)


	def __str__(self):
		return self.name



class University(models.Model):
	id = fields.IntField(pk=True)
	country = fields.ForeignKeyField('models.Country', on_delete=fields.CASCADE, related_name='universities')
	varsity_type = fields.CharEnumField(VarsityType, default=VarsityType.PUBLIC)
	name = fields.CharField(300)
	location = fields.CharField(300)
	image = fields.CharField(255, null=True, blank=True)

	def __str__(self):
		return self.name


class Course(models.Model):
	id = fields.IntField(pk=True)
	university = fields.ForeignKeyField('models.University', on_delete=fields.CASCADE, related_name='courses')
	course_type = fields.CharField(200, null=True, blank=True)
	fee = fields.IntField(null=True, blank=True)
	image = fields.CharField(255, null=True, blank=True)

	def __str__(self):
		return self.course_type




class AgentAdmissionApplication(models.Model):
	id = fields.IntField(pk=True)
	agent = fields.ForeignKeyField('models.User', on_delete=fields.SET_NULL, null=True, related_name='student_applications')
	first_name = fields.CharField(55)
	last_name = fields.CharField(55)
	email = fields.CharField(55)
	phone = fields.CharField(20)
	passport_no = fields.CharField(100)
	course = fields.ForeignKeyField('models.Course', on_delete=fields.SET_NULL, null=True)
	university_one = fields.ForeignKeyField('models.University', on_delete=fields.SET_NULL, null=True, related_name='applications_one')
	university_two = fields.ForeignKeyField('models.University', on_delete=fields.SET_NULL, null=True, related_name='applications_two')
	university_three = fields.ForeignKeyField('models.University', on_delete=fields.SET_NULL, null=True, related_name='applications_three')
	last_graduation = fields.CharField(55, null=True, blank=True)

	def __str__(self):
		return f'{self.first_name} {self.last_name}'




class AgentApplicationDocuments(models.Model):
	id = fields.IntField(pk=True)
	admission_application = fields.OneToOneField('models.AgentAdmissionApplication', on_delete=fields.CASCADE, related_name='documents')
	passport = fields.CharField(300, null=True, blank=True)
	masters_certificate = fields.CharField(300, null=True, blank=True)
	masters_transcript = fields.CharField(300, null=True, blank=True)
	honers_certificate = fields.CharField(300, null=True, blank=True)
	honers_transcript = fields.CharField(300, null=True, blank=True)
	hsc_certificate = fields.CharField(300, null=True, blank=True)
	hsc_transcript = fields.CharField(300, null=True, blank=True)
	ssc_certificate = fields.CharField(300, null=True, blank=True)
	ssc_transcript = fields.CharField(300, null=True, blank=True)
	ielts_certificate = fields.CharField(300, null=True, blank=True)
	cv = fields.CharField(300, null=True, blank=True)
	resume = fields.CharField(300, null=True, blank=True)
	lor = fields.CharField(300, null=True, blank=True)
	job_letter = fields.CharField(300, null=True, blank=True)
	others = fields.CharField(300, null=True, blank=True)


	def __str__(self):
		return self.admission_application





class StudentAdmissionApplication(models.Model):
	id = fields.IntField(pk=True)
	name = fields.CharField(100)
	phone = fields.CharField(20)
	email = fields.CharField(100, null=True, blank=True)
	residence_country = fields.CharField(50)
	interest_country = fields.CharField(50)
	intake_interest = fields.CharField(200)
	last_graduation = fields.CharField(200)
	interested_course = fields.CharField(200)
	current_stage = fields.CharField(200, null=True, blank=True)

	def __str__(self):
		return self.name


class StudentApplicationDocuments(models.Model):
	id = fields.IntField(pk=True)
	admission_application = fields.OneToOneField('models.StudentAdmissionApplication', on_delete=fields.CASCADE, related_name='documents')
	passport = fields.CharField(300, null=True, blank=True)
	last_graduation_certificate = fields.CharField(300, null=True, blank=True)


	def __str__(self):
		return self.admission_application

