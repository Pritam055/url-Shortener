import string, random
from django.conf import settings

SHORTCODE_MIN = getattr(settings, 'SHORTCODE_MIN', 6)

def code_generator(size=6, chars=string.ascii_lowercase+string.digits):
    return ''.join([random.choice(chars) for _ in range(size)])

# calling the BitURL class from here will cause an error so we'll be passing it as an argument variable
def code_check(instance, size=SHORTCODE_MIN):
    new_code = code_generator(size=size)
    # print(instance)
    # print(instance.__class__)

    BitURLClass = instance.__class__
    obj_exists = BitURLClass.objects.filter(shortcode=new_code).exists()
    if obj_exists:
        return code_check(instance)
    return new_code


    