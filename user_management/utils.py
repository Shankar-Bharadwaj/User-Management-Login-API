from django.core.exceptions import ValidationError
import re

def get_object(model, id):
    try:
        return model.objects.get(pk=id)
    except model.DoesNotExist:
        return None

def validate_aadhar_number(aadhar_number):
    aadhar_number = aadhar_number.strip()
    aadhar_number = aadhar_number.replace(" ", "")
    if not re.match(r'^\d{12}$', aadhar_number):
        raise ValidationError('Aadhar number must be exactly 12 digits long.')
    
def validate_pan_number(pan_number):
    pan_number = pan_number.strip()
    if not re.match(r'^[A-Z]{5}[0-9]{4}[A-Z]$', pan_number):
        raise ValidationError('PAN number must be in the format ABCDE1234F.')
    
def validate_gst_number(gst_number):
    gst_number = gst_number.strip()
    if not re.match(r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z][A-Z0-9][Z][A-Z0-9]$', gst_number):
        raise ValidationError('GST number is in invalid format.')
