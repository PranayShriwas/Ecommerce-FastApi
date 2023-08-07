from tortoise.models import Model
from tortoise import Tortoise,fields


class Userr(Model):
    id=fields.IntField(pk=True)
    name=fields.CharField(100)
    email=fields.CharField(100)
    phone=fields.CharField(10)
    password=fields.CharField(100)
    shopname=fields.CharField(50)
    gst=fields.IntField()
    is_active = fields.BooleanField(default=True)
    last_login = fields.DatetimeField(auto_now_add=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

class Category(Model):
    id=fields.IntField(pk=True)
    name=fields.CharField(200,unique=True)
    # slug=fields.CharField(200)
    category_image=fields.TextField()
    description=fields.TextField()
    is_active = fields.BooleanField(default=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)


class SubCategory(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(200, unique=True)
    subcategory_image = fields.TextField()
    description = fields.TextField()
    category = fields.ForeignKeyField(
    "models.Category", related_name="subcategory", on_delete="CASCADE")
    is_active = fields.BooleanField(default=True)
    updated_at = fields.DatetimeField(auto_now=True)
    created_at = fields.DatetimeField(auto_now_add=True)

class AddBrand(Model):
    id=fields.IntField(pk=True)
    brand_name=fields.CharField(200,unique=True)
    is_active = fields.BooleanField(default=True)
    updated_at = fields.DatetimeField(auto_now=True)
    created_at = fields.DatetimeField(auto_now_add=True)



    