from tortoise import fields, models
from enum import Enum


class VarsityType(str, Enum):
    PUBLIC = 'Public'
    PRIVATE = 'Private'
    SEMI_PUBLIC = 'Semi_Public'



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