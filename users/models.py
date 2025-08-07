from tortoise import fields, models

class User(models.Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(50, unique=True)
    email = fields.CharField(100, unique=True)
    password_hash = fields.CharField(128)
    is_admin = fields.BooleanField(default=False)
    is_verified = fields.BooleanField(default=False)

    profile: fields.ReverseRelation["UserProfile"]

    def __str__(self):
        return self.username



class UserProfile(models.Model):
    id = fields.IntField(pk=True)
    user = fields.OneToOneField("models.User", related_name="profile", on_delete=fields.CASCADE)
    full_name = fields.CharField(100)
    phone = fields.CharField(25)
    whatsapp =  fields.CharField(25)
    address = fields.CharField(500)
    occupation = fields.CharField(255)
    experience = fields.BooleanField(default=False)
    exp_description = fields.TextField(null=True, blank=True)
    initial_refffer = fields.CharField(255)
    no_of_deal = fields.IntField(default=0)
    office = fields.BooleanField(default=False)
    office_address = fields.CharField(255, null=True, blank=True)
    special_service = fields.TextField(null=True, blank=True)
    nid_passport_file = fields.CharField(500, null=True)


    def __str__(self):
        return f"Profile of {self.user.username}"