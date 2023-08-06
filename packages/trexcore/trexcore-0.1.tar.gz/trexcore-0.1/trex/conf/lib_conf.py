import logging, os

PRODUCTION_MODE                                     = "PROD"
DEMO_MODE                                           = "DEMO"
LOCAL_MODE                                          = "LOCAL"


#DEPLOYMENT_MODE                                     = PRODUCTION_MODE
DEPLOYMENT_MODE                                     = DEMO_MODE
#DEPLOYMENT_MODE                                     = LOCAL_MODE


SECRET_KEY                                          = os.environ['SECRET_KEY']
MAX_PASSWORD_LENGTH                                 = os.environ['MAX_PASSWORD_LENGTH']

SENDGRID_API_KEY                                    = os.environ['SENDGRID_API_KEY']


MAILJET_API_KEY                                     = os.environ['MAILJET_API_KEY']
MAILJET_SECRET_KEY                                  = os.environ['MAILJET_SECRET_KEY']

LOGIN_URL_FOR_PATH                                 = 'security_bp.signin_page'
LOGIN_CONTENT_URL_FOR_PATH                         = 'security_bp.signin_content'

#-----------------------------------------------------------------
# Mail Server settings
#-----------------------------------------------------------------
MAIL_SERVER     = 'localhost'
MAIL_PORT       = 25
MAIL_USERNAME   = None
MAIL_PASSWORD   = None
MAIL_USE_TLS    = False
MAIL_USE_SSL    = True
MAIL_ADMINS     = ['you@example.com']

DEFAULT_SENDER = os.environ['DEFAULT_SENDER']

DEFAULT_COUNTRY_CODE                                = 'my'
DEFAULT_GMT                                         = 8


DEFAULT_DATETIME_FORMAT                             = '%d/%m/%Y %H:%M:%S'
DEFAULT_DATE_FORMAT                                 = '%d/%m/%Y'
DEFAULT_TIME_FORMAT                                 = '%H:%M:%S'


DEFAULT_ETAG_VALUE                              = '68964759a96a7c876b7e'

DEFAULT_COUNTRY_CODE                            = 'my'

MODEL_CACHE_ENABLED                             = False

INTERNAL_MAX_FETCH_RECORD                       = 9999
MAX_FETCH_RECORD_FULL_TEXT_SEARCH               = 1000
MAX_FETCH_RECORD_FULL_TEXT_SEARCH_PER_PAGE      = 10
MAX_FETCH_RECORD                                = 99999999
MAX_FETCH_IMAGE_RECORD                          = 100
MAX_CHAR_RANDOM_UUID4                           = 20
PAGINATION_SIZE                                 = 2
VISIBLE_PAGE_COUNT                              = 10

GENDER_MALE_CODE                                = 'm'
GENDER_FEMALE_CODE                              = 'f'



APPLICATION_ACCOUNT_PROVIDER                    = 'app'

SUPPORT_LANGUAGES                               = ['en','zh']

#-----------------------------------------------------------------
# Web Beacon settings
#-----------------------------------------------------------------
WEB_BEACON_TRACK_EMAIL_OPEN   = 'eo'

#-----------------------------------------------------------------
# Miliseconds settings
#-----------------------------------------------------------------
MILLISECONDS_ONE_MINUTES    = 60
MILLISECONDS_FIVE_MINUTES   = 300
MILLISECONDS_TEN_MINUTES    = 600
MILLISECONDS_TWENTY_MINUTES = 1200
MILLISECONDS_THIRTY_MINUTES = 1800
MILLISECONDS_ONE_HOUR       = 3600
MILLISECONDS_TWO_HOUR       = 7200
MILLISECONDS_FOUR_HOUR      = 14400
MILLISECONDS_EIGHT_HOUR     = 28800
MILLISECONDS_TEN_HOUR       = 36000
MILLISECONDS_TWELVE_HOUR    = 43200
MILLISECONDS_TWENTY_HOUR    = 72000
MILLISECONDS_ONE_WEEK       = 604800
MILLISECONDS_ONE_DAY        = 86400
MILLISECONDS_HALF_DAY       = 43200
MILLISECONDS_ONE_HOUR       = 3600
MILLISECONDS_TWO_HOUR       = 7200
MILLISECONDS_HALF_AN_HOUR   = 1800
MILLISECONDS_QUATER_AN_HOUR = 900    
    
    