from fastapi import FastAPI, Query
from typing import Union
import phonenumbers
from phonenumbers import geocoder
from pydantic import BaseModel
import markdown2
from fastapi.responses import HTMLResponse
from phonenumbers import carrier
from phonenumbers import timezone
class PhoneNumberDetail(BaseModel):
    country: Union[str, None]
    countryOrLocation: Union[str, None]
    carrier: Union[str, None]
    country_code: Union[int, None]
    national_number: Union[int, None]
    country_code_source: Union[int, None]
    country_code_source: Union[int, None]
    is_possible_number: Union[bool] = False
    is_valid_number: Union[bool] = False
    time_zones_for_number: Union[list, None]



app = FastAPI()

@app.get("/",include_in_schema=False,response_class=HTMLResponse)
def root():
    with open("README.md","r",encoding="utf-8") as file:
        readme_content=file.read()
    return markdown2.markdown(readme_content)

@app.get("/get_phone_number_details",response_model=PhoneNumberDetail,description="Checks if phone number is valid and returns country of number. Example: (+442083661177)")
def get_phone_number_details(phone_number:str=Query(description="Phone number starting with +")):
    if(phone_number.startswith(" ")):
        phone_number="+"+phone_number[1:]
    try:
        phone_number_details=phonenumbers.parse(phone_number)
        phone_number_details_dict=phone_number_details.__dict__
        phone_number_details_dict['country']=geocoder.country_name_for_number(phone_number_details, "en")
        phone_number_details_dict['countryOrLocation']=geocoder.description_for_number(phone_number_details,"en")
        phone_number_details_dict['carrier']=carrier.name_for_number(phone_number_details, "en")
        phone_number_details_dict['is_possible_number']=phonenumbers.is_possible_number(phone_number_details)
        phone_number_details_dict['is_valid_number']=phonenumbers.is_valid_number(phone_number_details)
        phone_number_details_dict['time_zones_for_number'] = timezone.time_zones_for_number(phone_number_details)
    except:
        return PhoneNumberDetail()
    return phone_number_details_dict

