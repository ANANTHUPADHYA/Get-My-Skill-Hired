from accounts import settings
from jsonschema import validate, ValidationError, SchemaError

consumer_profile = {
    "$schema": "http://json-schema.org/draft-07/schema#",    
    "type" : "object",
    "properties" : {
        "firstName" : {
            "type" : "string"
        },
        "lastName" : {
            "type" : "string"
        },
        "email" : {
            "type" : "string"
        },
        "phone" : {
            "type" : "string"
        },
        "userType" : {
            "type" : "string",
            "enum": settings.VALID_USER_TYPES
        },
        "address":{
            "type" : "string"
        },
        "city":{
            "type" : "string"
        },
        "area":{
            "type" : "string"
        },
        "image":{
            "type" : "string"
        },
        "appointments":{
            "type" : "array",
            "items": { 
                "type" : "array",
                "items": { 
                    "type": "string"
                }
            }
        }
    },
    "required": ["firstName", "lastName", "email", "phone", "userType", "address", "city", "area"]
}

update_consumer_profile = {
    "$schema": "http://json-schema.org/draft-07/schema#",    
    "type" : "object",
    "properties" : {
        "firstName" : {
            "type" : "string"
        },
        "lastName" : {
            "type" : "string"
        },
        "email" : {
            "type" : "string"
        },
        "phone" : {
            "type" : "string"
        },
        "userType" : {
            "type" : "string",
            "enum": settings.VALID_USER_TYPES
        },
        "address":{
            "type" : "string"
        },
        "city":{
            "type" : "string"
        },
        "area":{
            "type" : "string"
        },
        "image":{
            "type" : "string"
        },
        "appointments":{
            "type" : "array",
            "items": { 
                "type" : "array",
                "items": { 
                    "type": "string"
                }
            }
        }
    }
}

provider_profile = {
    "$schema": "http://json-schema.org/draft-07/schema#",    
    "type" : "object",
    "properties" : {
        "firstName" : {
            "type" : "string"
        },
        "lastName" : {
            "type" : "string"
        },
        "email" : {
            "type" : "string"
        },
        "phone" : {
            "type" : "string"
        },
        "userType" : {
            "type" : "string",
            "enum": settings.VALID_USER_TYPES
        },
        "address":{
            "type" : "string"
        },
        "city":{
            "type" : "string"
        },
        "area":{
            "type" : "string"
        },
        "days":{
            "type" : "array",
            "items": { "type": "string"}
        },
        "time":{
            "type" : "string"
        },
        "rating":{
            "type" : "number"
        },
        "image":{
            "type" : "string"
        },
        "appointments":{
            "type" : "array",
            "items": { 
                "type" : "array",
                "items": { 
                    "type": "string"
                }
            }
        },
        "skillSet":{
            "type": "array",
            "items": { 
                "name": {
                    "type": "string",
                    "enum": settings.VALID_SKILL_TYPES
                },
                "price": {
                    "type": "number"
                }
             }
        }
    },
    "required": ["firstName", "lastName", "email", "phone", "userType", "address", "city", "area", "days", "time", "skillSet"]
}

update_provider_profile = {
    "$schema": "http://json-schema.org/draft-07/schema#",    
    "type" : "object",
    "properties" : {
        "firstName" : {
            "type" : "string"
        },
        "lastName" : {
            "type" : "string"
        },
        "email" : {
            "type" : "string"
        },
        "phone" : {
            "type" : "string"
        },
        "userType" : {
            "type" : "string",
            "enum": settings.VALID_USER_TYPES
        },
        "address":{
            "type" : "string"
        },
        "city":{
            "type" : "string"
        },
        "area":{
            "type" : "string"
        },
        "days":{
            "type" : "array",
            "items": { "type": "string"}
        },
        "time":{
            "type" : "string"
        },
        "rating":{
            "type" : "number"
        },
        "image":{
            "type" : "string"
        },
        "appointments":{
            "type" : "array",
            "items": { 
                "type" : "array",
                "items": { 
                    "type": "string"
                }
            }
        },
        "skillSet":{
            "type": "array",
            "items": { 
                "name": {
                    "type": "string",
                    "enum": settings.VALID_SKILL_TYPES
                },
                "price": {
                    "type": "number"
                }
             }
        }
    }
}


def ValidateRegistrationData(data, userType=None, update=False):
    try:
        if (not update) and not data.get("userType", None):
            raise ValidationError("User type was not provided !!!")

        if not update:
            if data["userType"].lower() == "consumer":
                validate(data, consumer_profile)
            else:
                validate(data, provider_profile)
        else:
            if userType == "consumer":
                validate(data, update_consumer_profile)
            else:
                validate(data, update_provider_profile)

        return True, None
    except SchemaError as e:
        return False, "Invalid user registration data" + str(e)
    except ValidationError as e:  
        return False, "User registration data validation error, " + str(e)
