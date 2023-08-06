"""
This module defines mappings from airports. The structure is designed to mimic the mathmatic 'graph' objects, however,
it was coded quickly to solve a single use case (equivalent to a single test case).

It remains to be optimized, and to correct certain bugs not covered by the original use case. (Possibly replace; Neil
has a Core Dictionary use-case that performs the same operations, but much less code, and does not require loading in
this monster of a constant 'AIRPORT_CODE' into memory for each function call).
"""
import json
import os
from typing import Optional, List, Union


####################################################################################################################
# Load the city names
####################################################################################################################
with open(os.path.dirname(os.path.abspath(__file__)) + '/airport_codes.json', encoding="utf-8") as file:
    CITY_NAMES = json.load(file)


def city_name_to_code(airline_code: str, city: str) -> Union[Optional[str], List[str]]:
    """
    With the provided information, returns the given airport code, or, in unpredictable circumstances, returns a list
    of city or airport codes.

    The airport codes from CITY_NAMES is not a comprehensive list. Some airports are deliberately missing, and should
    be parsed through as special cases.

    :param airline_code:
    :param market: Unused.
    :param city:
    :return:
    """
    ####################################################################################################################
    # Performance adjustment (len(string) is faster than dict.get() returning None) for cases where airport_code already
    # is assigned (which should be the usual case)
    ####################################################################################################################
    if isinstance(city, str) and len(city) > 3:
        airport_codes = CITY_NAMES.get(city)
    else:
        # If not, then return None
        return None
    ####################################################################################################################
    # If nothing could be found, return None
    ####################################################################################################################
    if airport_codes is None:
        return None
    ####################################################################################################################
    # Special Case: default to SJO for 4O
    ####################################################################################################################
    elif airline_code == '4O' and 'SJO' in airport_codes:
        return 'SJO'
    elif airline_code == "4O" and "LGA" in airport_codes:
        return "NYC"
    ####################################################################################################################
    # Volaris special cases; default to airports known to be flown to
    ####################################################################################################################
    elif airline_code == "Y4" and "SMF" in airport_codes:
        # Sacramento Int'l Airport
        return "SMF"
    elif airline_code == "Y4" and "IAH" in airport_codes:
        # Houston
        return "IAH"
    elif airline_code == "Y4" and "DFW" in airport_codes:
        # Dallas Ft Worth
        return "DFW"
    elif airline_code == "Y4" and "MCO" in airport_codes:
        # Orlando
        return "MCO"
    elif airline_code == "Y4" and "JFK" in airport_codes:
        # New York
        return "JFK"
    ####################################################################################################################
    # Special case: UO
    ####################################################################################################################
    elif airline_code == "UO" and "KIX" in airport_codes:
        return "KIX"
    elif airline_code == "UO" and "HND" in airport_codes:
        return "HND"
    elif airline_code == "UO" and "GMP" in airport_codes:
        return "GMP"
    ####################################################################################################################
    # Usual case: return the airport code[s]
    ####################################################################################################################
    else:
        if len(airport_codes) == 1:
            return airport_codes[0]
        else:
            return airport_codes

