from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

def validate_url(value):
    urlvalidator = URLValidator()
    new_value = value 
    if not "http" in value:
        new_value = "http://"+value
        
    try:
        urlvalidator(new_value)
    except:
        raise ValidationError("Invalid URL for the field !!!")
    return new_value
    

def validate_dot_com(value):
    if not '.com' in value:
        raise ValidationError("This is not valid because of no '.com'")
    return value 