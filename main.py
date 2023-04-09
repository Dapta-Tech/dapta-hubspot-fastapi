from fastapi import FastAPI, Body
from hubspot import HubSpot
from dotenv import load_dotenv
import os
from hubspot.crm.contacts import SimplePublicObjectInput
from hubspot.crm.contacts.exceptions import ApiException
from hubspot.auth.oauth import ApiException

# Environment variable setup
env_path = ".env"
load_dotenv(env_path)

# API Keys
HUBSPOT_KEY = os.environ["HUBSPOT_TOKEN"]

# Hubspot setup
api_client = HubSpot(access_token=HUBSPOT_KEY)

app = FastAPI()


@app.get("/")
def index():
    return "This is the Hubspot API"


@app.get("/get-contacts")
def get_all_contacts():
    all_contacts = api_client.crm.contacts.get_all()
    print(all_contacts)
    # TODO fix recursion depth exceeded error
    return all_contacts


@app.post("/create-contact")
def create_contact(email: str = Body(), firstname: str = Body(), lastname: str = Body(), phone: str = Body(), company: str = Body()):
    try:
        simple_public_object_input = SimplePublicObjectInput(
            properties={
                "email": email,
                "firstname": firstname,
                "lastname": lastname,
                "phone": phone,
                "company": company,
            }
        )
        api_response = api_client.crm.contacts.basic_api.create(
            simple_public_object_input=simple_public_object_input
        )
        return True
    except ApiException as e:
        print("Exception when creating contact: %s\n" % e)
        return False
