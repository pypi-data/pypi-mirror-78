'''
Created on 3 Sep 2020

@author: jacklok
'''
from datetime import date
import phonenumbers
from phonenumbers import carrier
from phonenumbers.phonenumberutil import number_type
from trex.conf import junk_conf
import logging 
from six import string_types

logger = logging.getLogger('phone_util')

def is_mobile_phone(phone_no):
    if phone_no:
        is_valid = False
        try:
            phone_no_obj = phonenumbers.parse(phone_no)
            logging.info('phone_no_obj=%s', phone_no_obj)
            ntype = number_type(phone_no_obj)
            logging.info('ntype=%s', ntype)
            return carrier._is_mobile(ntype)
        except:
            return False
    else:
        return False

def normalized_mobile_phone(phone_no, default_country_code=junk_conf.DEFAULT_COUNTRY_CODE.upper()):
    if is_mobile_phone(phone_no):
        try:
            parsed_mobile_phone = phonenumbers.parse(phone_no, region=default_country_code)
            return '+%s%s' % (parsed_mobile_phone.country_code, parsed_mobile_phone.national_number)
        except:
            return None
    return None

def format_mobile_phone(phone_no, default_country_code=junk_conf.DEFAULT_COUNTRY_CODE.upper()):
    parsed_mobile_phone = phonenumbers.parse(phone_no, region=default_country_code)
    return '+%s%s' % (parsed_mobile_phone.country_code, parsed_mobile_phone.national_number)
