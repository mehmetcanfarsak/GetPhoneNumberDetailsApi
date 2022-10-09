from fastapi import FastAPI, Query
from typing import Union
import phonenumbers
from phonenumbers import geocoder
from pydantic import BaseModel
import markdown2
from fastapi.responses import HTMLResponse

class PhoneNumberDetail(BaseModel):
    country: Union[str, None]
    country_code: Union[int, None]
    national_number: Union[int, None]
    country_code_source: Union[int, None]
    country_code_source: Union[int, None]


app = FastAPI()

@app.get("/",include_in_schema=False,response_class=HTMLResponse)
def root():
    with open("README.md","r",encoding="utf-8") as file:
        readme_content=file.read()
    return markdown2.markdown(readme_content)

@app.get("/get_phone_number_details",response_model=PhoneNumberDetail,description="Checks if phone number is valid and returns country of number.")
def get_phone_number_details(phone_number:str=Query(description="Phone number starting with +")):
    try:
        phone_number_details=phonenumbers.parse(phone_number)
        phone_number_details_dict=phone_number_details.__dict__
        phone_number_details_dict['country']=geocoder.description_for_number(phone_number_details,"en")
    except:
        return PhoneNumberDetail()
    return phone_number_details_dict

