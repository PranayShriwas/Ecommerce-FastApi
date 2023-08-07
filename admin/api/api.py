import passlib
import typing
from json import JSONEncoder
from fastapi.encoders import jsonable_encoder
from fastapi_login.exceptions import InvalidCredentialsException
from fastapi_login import LoginManager
from passlib.context import CryptContext
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Request, status, Depends, Form, UploadFile, File
from .models import *
from .pydantic_models import User,Login,Token,Info,Dlt_catogry,Update,categoryitem,update_categoryitem,Subcatogryitem,deletesubcatogry,Subcatogryitemupdate,Addbrand,brand,updatebrand
# from slugify import slugify
import os
from datetime import datetime, timedelta


app = APIRouter()
SECRET = b'your-secret-key'
manager = LoginManager(SECRET, token_url='/user_login')
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


manager = LoginManager(SECRET, token_url='/login')


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)





@app.get('/all_catogry_data/')
async def all():
    cat_obj = await Category.filter(is_active=True)
    return cat_obj


@app.delete("/delete_category/")
async def delete(data:Dlt_catogry):
    catogry_obj = await Category.filter(id=data.id).delete()
    return {"message": "catogry item deleted"}

@app.put('/update_catogry/')
async def update_catogry(data:update_categoryitem = Depends(), category_image: UploadFile = File(...)):
    cat_obj = await Category.get(id=data.id)
    if not cat_obj:
        return {"status": False, "message": "catogry not exists"}
    
    else:
        # slug = slugify(data.name)
        # print(slug)
        FILEPATH = "static/images/category/"

        if not os.path.isdir(FILEPATH):
            os.mkdir(FILEPATH)

        filename = category_image.filename
        extension = filename.split(".")[1]
        imagename = filename.split(".")[0]

        if extension not in ["png", "jpg", "jpeg"]:
            return {"status": "error", "detials": "file Extension not allowed"}

        dt = datetime.now()
        dt_timestamp = round(datetime.timestamp(dt))

        modified_image_name = imagename+"-"+str(dt_timestamp)+"."+extension
        genrated_name = FILEPATH + modified_image_name
        file_content = await category_image.read()

        with open(genrated_name, "wb") as file:
            file.write(file_content)
            file.closed
        cat_obj = await Category.filter(id=data.id).update(name=data.name, description=data.descripiton,category_image=genrated_name,)
        return cat_obj



@app.post("/add_category/")
async def create_category(data: categoryitem = Depends(), category_image: UploadFile = File(...)):
    if await Category.exists(name=data.name):
        return {"status": False, "message": "categosy already Exista"}
        
        
    else:
        # slug = slugify(data.name)
        # print(slug)
        FILEPATH = "static/images/category/"

        if not os.path.isdir(FILEPATH):
            os.mkdir(FILEPATH)

        filename = category_image.filename
        extension = filename.split(".")[1]
        imagename = filename.split(".")[0]

        if extension not in ["png", "jpg", "jpeg"]:
            return {"status": "error", "detials": "file Extension not allowed"}

        dt = datetime.now()
        dt_timestamp = round(datetime.timestamp(dt))

        modified_image_name = imagename+"-"+str(dt_timestamp)+"."+extension
        genrated_name = FILEPATH + modified_image_name
        file_content = await category_image.read()

        with open(genrated_name, "wb") as file:
            file.write(file_content)
            file.closed

        category_obj = await Category.create(
            category_image=genrated_name,
            description=data.descripiton,
            name=data.name,
            # slug=slug
        )

        return category_obj



#sub catogry
@app.post('/add_subcatogry/')
async def add_sub(data:Subcatogryitem = Depends(),subcategory_image:UploadFile = File(...)):
    if await Category.exists(id=data.catogry_id):
        catogry_obj = await Category.get(id=data.catogry_id)
        if await SubCategory.exists(name=data.name):
            return {"status": False, "message": "subcatogry already exist"}

        else:
             FILEPATH = "static/images/subcategory/"

        if not os.path.isdir(FILEPATH):
            os.mkdir(FILEPATH)

        filename = subcategory_image.filename
        extension = filename.split(".")[1]
        imagename = filename.split(".")[0]

        if extension not in ["png", "jpg", "jpeg"]:
            return {"status": "error", "detials": "file Extension not allowed"}

        dt = datetime.now()
        dt_timestamp = round(datetime.timestamp(dt))

        modified_image_name = imagename+"-"+str(dt_timestamp)+"."+extension
        genrated_name = FILEPATH + modified_image_name
        file_content = await subcategory_image.read()

        with open(genrated_name, "wb") as file:
            file.write(file_content)
            file.closed

        subCategory_obj = await SubCategory.create(subcategory_image=genrated_name,
                                                   category=catogry_obj,description=data.descripiton,
                                                   name=data.name)
        return subCategory_obj
    

@app.delete("/delete_subcatogry/")
async def delete(data:deletesubcatogry):
    catogry_obj = await SubCategory.filter(id=data.catogry_id).delete()
    return {"message": "catogry item deleted"}


@app.get('/all_subcatogry_data/')
async def all():
    cat_obj = await SubCategory.filter(is_active=True)
    return cat_obj

@app.put('/update_subcatogry/')
async def update_sub(data:Subcatogryitemupdate = Depends(),subcategory_image:UploadFile = File(...)):
    catogry_obj = await SubCategory.get(id=data.id)
    if not catogry_obj:
        return {"status": False, "message": "catogry not exists"}
    
    else:
        # slug = slugify(data.name)
        # print(slug)
        FILEPATH = "static/images/subcategory/"

        if not os.path.isdir(FILEPATH):
            os.mkdir(FILEPATH)

        filename = subcategory_image.filename
        extension = filename.split(".")[1]
        imagename = filename.split(".")[0]

        if extension not in ["png", "jpg", "jpeg"]:
            return {"status": "error", "detials": "file Extension not allowed"}

        dt = datetime.now()
        dt_timestamp = round(datetime.timestamp(dt))

        modified_image_name = imagename+"-"+str(dt_timestamp)+"."+extension
        genrated_name = FILEPATH + modified_image_name
        file_content = await subcategory_image.read()

        with open(genrated_name, "wb") as file:
            file.write(file_content)
            file.closed
        cat_obj = await SubCategory.filter(id=data.id).update(name=data.name, description=data.descripiton,subcategory_image=genrated_name,)
        return cat_obj






@app.post('/')
async def register(data: User):
    if await Userr.exists(phone=data.phone):
        return {"status": False, "message": "mobile number already exist"}
    elif await Userr.exists(email=data.email):
        return {"status": False, "message": "email already exist"}
    else:
        user_obj = await Userr.create(name=data.name, email=data.email, phone=data.phone, password=get_password_hash(data.password), shopname=data.shopname,
                                      gst=data.gst)
        return user_obj


@app.get('/all/')
async def all():
    user_obj = await Userr.all()
    return user_obj


@app.post('/daata/')
async def daata(data: Info):
    user_obj = await Userr.filter(id=data.id)
    return user_obj


@app.delete('/delete/')
async def delete(data: Info):
    user_obj = await Userr.filter(id=data.id).delete()
    return {"message": "user deleted"}


@app.put('/update/')
async def update(data: Update):
    user_obj = await Userr.get(id=data.id)
    if not user_obj:
        return {"status": False, "message": "user not register"}
    else:
        user_obj = await Userr.filter(id=data.id).update(name=data.name, email=data.email, phone=data.phone,
                                                         shopname=data.shopname, updated_at=data.updated_at, gst=data.gst)
        return user_obj


@manager.user_loader()  # type: ignore
async def load_user(email: str):
    if await Userr.exists(email=email):
        user = await Userr.get(email=email)
        return user


@app.post('/login/')
async def login(data: Login):
    email = data.email
    user = await load_user(email)

    if not user:
        return JSONResponse({'status': False, 'message': 'User not Registered'}, status_code=403)
    elif not verify_password(data.password, user.password):
        return JSONResponse({'status': False, 'message': 'Invalid password'}, status_code=403)
    access_token = manager.create_access_token(data={'sub': {'id': user.id}})
    new_dict = jsonable_encoder(user)
    new_dict.update({'access_token': access_token})
    return Token(access_token=access_token, token_type='bearer')

@app.post('/add_brand/')
async def create_brand(data:Addbrand):
    if await AddBrand.exists(brand_name=data.brand_name):
        return{"status":False,"message":"Brand Already Exists"}
    else:
        brand_obj=await AddBrand.create(brand_name=data.brand_name)
        return brand_obj
    
@app.get('/all_brand_data/')
async def all_brand_data():
    brand_obj=await AddBrand.all()
    return brand_obj

@app.delete('/brand_delete/')
async def delete_brand(data:brand):
    brand_obj=await AddBrand.filter(id=data.id).delete()
    return {'message':'Brand Deleted Successfully'}


@app.put('/update_brands/')
async def update_brand(data:updatebrand):
    brand_obj = await AddBrand.get(id=data.id)
    if not brand_obj:
        return {"status": False, "message": "brand not register"}
    else:
        brand_obj = await AddBrand.filter(id=data.id).update(brand_name=data.brand_name
                                                         )
        return brand_obj