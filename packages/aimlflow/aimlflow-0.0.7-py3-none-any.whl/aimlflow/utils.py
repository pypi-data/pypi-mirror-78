import re
import json
from colorama import Fore, Style

def check_email(email):
    # for validating an Email
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
    if re.search(regex, email):
        return True
    else:
        return False

def color_print(string, color=None):
    if not color:
        print(string)
    if color == 'RED':
        print(Fore.RED + string)
    elif color == 'GREEN':
        print(Fore.GREEN + string)
    elif color == 'BLUE':
        print(Fore.BLUE + string)
    elif color == 'BLACK':
        print(Fore.BLACK + string)
    else:
        print(string)
    #cleanup the color print
    print(Style.RESET_ALL)


def expand_all_response(response):
    if not isinstance(response, dict):
        return response
    for key, value in response.items():
        try:
            # Do it only for feature engineering
            if key == 'status' and value == 'ready' and 'fe_data_id' in response:
                response[key] = 'Completed'
            response[key] = json.loads(value)
        except:
            # Not everything is a string so its fine to not complain about it
            pass
    return response