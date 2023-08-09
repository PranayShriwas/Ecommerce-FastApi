from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    name:str
    email:str
    phone:str
    password:str
    shopname:str
    gst:int

class Login(BaseModel):
    email : str
    password : str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class Info(BaseModel):
    id:int
    
class Dlt_catogry(BaseModel):
    id:int

class Update(BaseModel):
    id:int
    name:str
    email:str
    phone:str
    shopname:str
    gst:int
    updated_at: datetime


class categoryitem(BaseModel):
    name:str
    descripiton: str    

class update_categoryitem(BaseModel):
    id:int
    name:str
    descripiton: str    

class Subcatogryitem(BaseModel):
    catogry_id: int
    name:str
    descripiton:str

class deletesubcatogry(BaseModel):
    catogry_id: int

class Subcatogryitemupdate(BaseModel):
    id: int
    name:str
    descripiton:str


class Addbrand(BaseModel):
    brand_name:str

class brand(BaseModel):
    id:int

class updatebrand(BaseModel):
    id:int
    brand_name:str

class AddProduct(BaseModel):
    catogry_id: int
    subcatogry_id: int
    brand_id: int
    name:str
    manufacturer_sku:str
    product_code:int
    model_no:str
    description :str
    mrp:int
    base_price :int
    gst :int
    offer_price:int

class DeleteProduct(BaseModel):
    id:int

class UpdateProduct(BaseModel):
    id:int
    name:str
    manufacturer_sku:str
    product_code:int
    model_no:str
    description :str
    mrp:int
    base_price :int
    gst :int
    offer_price:int





