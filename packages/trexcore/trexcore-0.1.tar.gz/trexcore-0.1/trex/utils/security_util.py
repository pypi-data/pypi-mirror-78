import hashlib, hmac, time, logging, uuid, json
from trex.conf import lib_conf
#from django.utils import simplejson as json


#-----------------------------------------------------------------
# Password Hashing & Blending
# DO NOT CHANGE AFTER DEPLOYED TO PRODUCTION
#-----------------------------------------------------------------
def hash_password(unique_id, password):
    # sha512 hashing with custom algorithm
    hashed_password = ""
    
    if password and unique_id:
        #password = password.decode('utf-8')
        logging.debug('unique_id=%s', unique_id)
        logging.debug('password=%s', password)
        blended_password = blend_password(unique_id, password)
        logging.debug('blended_password=%s', blended_password)
        
        password_salt = lib_conf.SECRET_KEY 
        
        hash = hashlib.sha512()
        hash.update(('%s%s' % (password_salt, password)).encode('utf-8'))
        hashed_password = hash.hexdigest()
        
        
        
    return hashed_password[0: lib_conf.MAX_PASSWORD_LENGTH]

def blend_password(unique_id, password):
    return unique_id + '!7' + password
#-----------------------------------------------------------------

#-----------------------------------------------------------------
# User ID generation
#-----------------------------------------------------------------

def generate_user_id ():
    user_id=generate_unique_random_characters()
    #return user_id[ len(user_id)-12:len(user_id) ]
    return user_id
    
#-----------------------------------------------------------------



#-----------------------------------------------------------------
# <<<<< Others >>>>>
#-----------------------------------------------------------------
def generate_unique_random_characters(limit=lib_conf.MAX_CHAR_RANDOM_UUID4):
    return str( uuid.uuid4() )[:limit]

def get_issued_time():
    return int(time.time())

def is_time_expired (issued_time, expiration_miliseconds):
    return issued_time < (time.time() - expiration_miliseconds)
#-----------------------------------------------------------------





def __ascii2Int(value):
    if value:
        int_keys = []
        for a in value:
            int_keys.append(ord(a))

        return int_keys


def __int2ascii(value):
    if value:
        ascii_keys = ''
        for a in value:
            ascii_keys+=chr(a)

        return ascii_keys

