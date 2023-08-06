'''
Created on 21 Apr 2020

@author: jacklok
'''

from datetime import date
import phonenumbers
from phonenumbers import carrier
from phonenumbers.phonenumberutil import number_type
import json, logging
from trex.conf import junk_conf
from math import log
import string
import random
import logging
from six import string_types

UNIT_LIST = zip(['bytes', 'kB', 'MB', 'GB', 'TB', 'PB'], [0, 0, 1, 2, 2, 2])

logger = logging.getLogger('application:common_util')

def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")


def str2int(str, default_value=0):
    if str:
        try:
            return int(str)
        except:
            return default_value
    else:
        return default_value
    
def str2float(str, default_value=0):
    if str:
        try:
            return float(str)
        except:
            return float(default_value)
    else:
        return float(default_value)
    
    
def list_exist_in_list(list1=[], list2=[]):
    for i in list1:
        if i in list2:
            return True
    
    return False
'''
def sort_list(list, sort_attr_name=None, reverse_order=False, key_lambda=None):
    if list:
        new_list = sorted(list, key=lambda x: getattr(x, sort_attr_name), reverse=reverse_order)
        return new_list
    else:
        return list
'''
def sort_list(list, sort_attr_name=None, reverse_order=False, key_lambda=None):
    if list:
        logging.debug('sort_attr_name=%s', sort_attr_name)
        new_list = sort_list_by_condition(list, condition=lambda x: getattr(x, sort_attr_name), reverse_order=reverse_order)
        return new_list
    else:
        return list

def sort_dict_list(list, sort_attr_name=None, reverse_order=False, key_lambda=None):
    if list:
        logging.debug('sort_attr_name=%s', sort_attr_name)
        new_list = sort_list_by_condition(list, condition=lambda x: x.get(sort_attr_name), reverse_order=reverse_order)
        return new_list
    else:
        return list


def sort_list_by_condition(list, condition=None, reverse_order=False):
    if list:
        new_list = sorted(list, key=condition, reverse=reverse_order)
        return new_list
    else:
        return list


def sizeof_fmt(num):
    """Human friendly file size"""
    if isinstance(num, str):
        num = float(num)

    if num > 1:
        exponent = min(int(log(num, 1024)), len(UNIT_LIST) - 1)
        quotient = float(num) / 1024**exponent
        unit, num_decimals = UNIT_LIST[exponent]
        format_string = '{:.%sf} {}' % (num_decimals)
        return format_string.format(quotient, unit)
    if num == 0:
        return '0 bytes'
    if num == 1:
        return '1 byte'

def calculate_age(born):
    if born:
        today = date.today()
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))
    else:
        return None

age_groups=[
    [0,19],
    [20,29],
    [30,39],
    [40,49],
    [50,59],
    [60,69],
    [70,79],
    [80,100]
]

def create_age_group_label(age_group):
    if isinstance(age_group, (tuple, list)) and len(age_group)>=2:
        return '%s-%s' % (age_group[0], age_group[1])
    return None

def create_age_group_label_from_birth_date(birth_date):
    if birth_date:
        age             = calculate_age(birth_date)
        age_group       = get_age_group(age)
        return create_age_group_label(age_group)
    else:
        return 'Unknown'

def get_age_group(age):
    if age:
        for g in age_groups:
            age_floor      = g[0]
            age_ceiling    = g[1]
            if age>=age_floor and age<=age_ceiling:
                return g
    return None

def gender_label(gender):
    if 'm'==gender:
        return 'Male'
    elif 'f'==gender:
        return 'Female'
    else:
        return gender

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


def parse_json_str(json_string):
    try:
        json_string = json_string.replace('\n','')
        #json_string = json_string.replace(' ','')
        return json.loads(json_string)
    except:
        #return {}
        raise

def generateEAN13CheckDigit(prefix, first9digits):

    final_digits = '%s%s' % (prefix, first9digits)
    charList = [char for char in final_digits]
    ean13 = [1,3]
    total = 0
    for order, char in enumerate(charList):
        total += int(char) * ean13[order % 2]

    checkDigit = 10 - total % 10
    if (checkDigit == 10):
        return 0

    return checkDigit

def sort_dict_by_value(original_dict):
    if original_dict:
        from collections import OrderedDict
        d_sorted_by_value = OrderedDict(sorted(original_dict.items(), key=lambda x: x[1]))
        return d_sorted_by_value
    else:
        return original_dict

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def get_offset_by_page_no(page_no, limit=junk_conf.PAGINATION_SIZE):
    logger.debug('---get_offset_by_page_no---')
    
    if page_no is not None:
        if isinstance(page_no, string_types):
            try:
                page_no = int(page_no, 10)
                
            except:
                logging.warn('invalid value of page_no')
                page_no = 0
        
        logging.debug('page_no=%d', page_no)
        
        if limit is not None:
            if isinstance(limit, string_types):
                try:
                    limit = int(limit, 10)
                    
                except:
                    logging.warn('invalid value of limit')
                    limit = junk_conf.PAGINATION_SIZE
        else:
            limit = junk_conf.PAGINATION_SIZE 
        
        if page_no>0:
            return (page_no-1) * limit
        else:
            return 0
    else:
        return 0
        
    






