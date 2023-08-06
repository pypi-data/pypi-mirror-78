"""
This module defines a series of methods using in data scrubbing.

"""

import re
from typing import Dict, Optional

from em_parser.airports_graph import city_name_to_code


def scrub_parsing(raw_parsing: Dict[str, str]) -> Dict[str, str]:
    """
    Returns a field-by-field scrubbing of the parsing dictionary with raw fields.

    Note: the order of the update() calls is important. The original author depended on each call being made in
    succession, as, although this module seems to define simply 'scrubbing' logic, there is assignment logic applied
    within here as well. It should be refactored out for the most stable implmentation changes possible.

    :param raw_parsing: Preliminary raw pausing.
    :return:
    """
    # Instantiate base values
    return_dict = {**raw_parsing}
    # Update the values that are possible to update.
    # Use raw_parsing.get(key) instead of raw_parsing[key] -- keys not guarenteed to be in each row.
    return_dict.update({"Network": clean_network(return_dict.get("Network"))})
    return_dict.update({"MatchType": clean_match_type(return_dict.get("MatchType"))})
    return_dict.update({"KeywordType": clean_keyword_type(return_dict.get("KeywordType"))})
    # @TODO: replace the logic in the following method into the em_parser rather than in the scrubbing module
    return_dict.update(
        clean_keyword_group_with_campaign_type(
            return_dict.get("KeywordGroup"),
            return_dict.get("CampaignType")
        )
    )
    return_dict.update({"Language": clean_language(return_dict.get("Language"))})
    return_dict.update({"SearchEngine": clean_search_engine(return_dict.get("SearchEngine"))})
    return_dict.update({"RouteLocale": clean_route_locale(return_dict.get("RouteLocale"))})
    return_dict.update({"RouteType": clean_route_type(return_dict.get("RouteType"))})
    return_dict.update(
        clean_marketing_network(
            return_dict.get("MarketingNetwork"),
            campaign_name=return_dict.get("CampaignName")
        )
    )
    return_dict.update({"CampaignType": clean_campaign_type(return_dict.get("CampaignType"))})
    return_dict.update({"LocationType": clean_location_type(return_dict.get("LocationType"))})
    return_dict.update({"Market": clean_market(return_dict.get("Market", "")).upper()})
    return_dict.update({"GeoTarget": clean_geo_target(return_dict.get("GeoTarget"))})
    return return_dict


def clean_network(network_value: Optional[str]) -> Optional[str]:
    """
    Scrubber method for 'Network' parsed value.
    :param network_value: Network string raw parsing.
    :return:
    """
    network = network_value
    if network:
        if network.upper() == 'DSA':
            network = 'Dynamic Remarketing'
    return network


def clean_match_type(match_type_value: Optional[str]) -> Optional[str]:
    """
    Scrubber method for 'MatchType' parsed value.
    :param match_type_value: Match type string raw parsing.
    :return:
    """
    match_type = match_type_value
    if match_type:
        if match_type.lower() in {"high", "medium", "low", "unknown", "med"}:
            pass
        else:
            # MatchType is always capitalized. Return dictionary with this field always upper'ed.
            match_type = match_type.upper()
            if 'BMM' == match_type:
                match_type = 'BM'
    else:
        # Case when
        match_type = 'PX'
    return match_type


def clean_keyword_type(keyword_type_value: Optional[str]) -> Optional[str]:
    """
    Scrubber method for 'KeywordType' parsed value.
    :param keyword_type_value: Keyword type string raw parsing.
    :return:
    """
    keyword_type = keyword_type_value
    if keyword_type:
        # Standardize output casing if the keyword_type is a usual case
        if keyword_type.lower() == 'competitor':
            keyword_type = 'Competitors'
        elif keyword_type.lower() == 'generics':
            keyword_type = 'Generic'
        elif keyword_type == "Co":
            keyword_type = 'Core'
        elif keyword_type == "Ge":
            keyword_type = 'Generic'
        elif keyword_type.lower() == "seasonalitygeneric":
            keyword_type = "SeasonalityGeneric"
        else:
            # If the keyword_type follows another deviation from the main structure, translate to an expected output.
            keyword_type_trans = {
                'Routes': 'Route',
                'Copa': 'Core',
                'Genc': 'Generic',
                'Dest': 'Destination',
                'Cc': 'Route'
            }
            # Try to obtain a translated value.
            trans_val = keyword_type_trans.get(keyword_type)
            if trans_val:
                # If so, we are good.
                keyword_type = trans_val
            else:
                # If we have some other kind of value, standardize the output. Remove Non-alphanum chars, and big camel
                # case it.
                keyword_type = re.sub(r'[^a-zA-Z0-9áéíóúñü ]', ' ', keyword_type).title().replace(" ", "")
    return keyword_type


def clean_keyword_group_with_campaign_type(keyword_group_value: str=None, campaign_type_value: str=None) -> \
        Dict[str, Optional[str]]:
    """
    Scrubber method for 'KeywordGroup' parsed value.

    This method should ALWAYS be called after the clean_campaign_type() method has been called as a last-ditch parsing
    effort for very specific use cases where the original keyword_group and campaign_type associations have been
    reversed.

    :param keyword_group_value: Keyword group string raw parsing.
    :param campaign_type_value: Extracted CampaignType value.
    :return:
    """
    keyword_group = keyword_group_value
    campaign_type = campaign_type_value
    if keyword_group:
        # Replace non-alphanumeric characters (ie., '_') with spaces.
        keyword_group = re.sub(r'[^a-zA-Záéíóúñü ]', ' ', keyword_group).title()
        if keyword_group == 'Promo':
            keyword_group = 'Deal'
            if campaign_type is None:
                # We know that if the keyword_group is Deal and the campaign_type is none then it should be set to
                # non-brand.
                campaign_type = 'Non-Brand'
        elif keyword_group == 'Brand':
            keyword_group = 'General'
            if campaign_type is None:
                # We know that if the keyword_group is General and the campaign_type is none then it should be set to
                # brand.
                campaign_type = 'Brand'
        elif keyword_group.lower() == 'tcpa':
            keyword_group = "tCPA"
        # Finally update the dictionary with cleaned keyword_group
    else:
        keyword_group = "General"
    return {
        'KeywordGroup': keyword_group,
        'CampaignType': campaign_type
    }


def clean_language(language_value: Optional[str]) -> Optional[str]:
    """
    Scrubber method for 'Language' parsed value.

    :param language_value: Language string raw parsing.
    :return:
    """
    language_codes = {
        "english": "en",
        "spanish": "es",
    }
    language = language_value
    if language:
        # Try to get the language from the above mapping to language codes.
        language = language_codes.get(language_value.lower(), language_value)
        language = language.lower()
        # Finally update cleaned Language
    return language


def clean_search_engine(search_engine_value: Optional[str]) -> Optional[str]:
    """
    Scrubber method for 'SearchEngine' parsed value.
    :param search_engine_value: Search engine string raw parsing.
    :return:
    """
    search_engine_trans = {
        'G': 'Google',
        'B': 'Bing',
        'Y': 'Yandex',
        'D': 'Baidu',
        'N': 'Naver',
        'J': 'Yahoo! Japan'
    }
    search_engine = search_engine_value
    if search_engine:
        trans_val = search_engine_trans.get(search_engine.upper())
        if trans_val:
            search_engine = trans_val
        # Finally update with cleaned search_engine
    elif search_engine in search_engine_trans.keys():
        # If the value is already correct, do not change it.
        pass
    else:
        search_engine = 'Google'
        # Default to Google if can't figure out search_engine
    return search_engine


def clean_route_locale(route_locale_value: Optional[str]) -> Optional[str]:
    """
    Scrubber method for 'RouteLocaled parsed value.

    Expected output should include: 'International', 'Domestic'

    :param route_locale_value: Route locale string raw parsing.
    :return:
    """
    route_locale = route_locale_value
    if route_locale:
        # Standardize the obtained value (casing inconsistencies is common in old structure.)
        route_locale = route_locale.upper() if len(route_locale) == 1 else route_locale
        locale_trans = {
            'I': 'International',
            'D': 'Domestic'
        }
        trans_val = locale_trans.get(route_locale)
        if trans_val:
            route_locale = trans_val
    return route_locale


def clean_route_type(route_type_value: Optional[str]) -> Optional[str]:
    """
    Scrubber method for 'RouteType' parsed value.

    Expected output should include: 'Connecting', 'Nonstop', 'Codeshare', 'Connecting'

    :param route_type_value: Route locale string raw parsing.
    :return:
    """
    route_type = route_type_value
    if route_type:
        route_trans = {
            'XX': 'Connecting',
            '00': 'Nonstop',
            '11': 'Codeshare',
            '22': 'Connecting',
            "X": "Connecting",
            "0": "Nonstop",
            "1": "Codeshare",
            "2": "Connecting"
        }
        # Map the raw value to the word value
        trans_val = route_trans.get(route_type.upper())
        if trans_val:
            route_type = trans_val
    return route_type


def clean_marketing_network(marketing_network_value: Optional[str], campaign_name: str=None) \
        -> Dict[str, Optional[str]]:
    """
    Scrubber method for 'MarketingNetwork' parsed value.

    Expected output should include: 'Search', 'RLSA', 'Dynamic Remarketing', 'GSP', 'Display'

    :param marketing_network_value: Route locale string raw parsing.
    :param campaign_name: (recommended) Campaign name
    :return:
    """
    marketing_network = marketing_network_value
    if marketing_network:
        network_trans = {
            'S': 'Search',
            'L': 'RLSA',
            'Y': 'Dynamic Remarketing',
            'E': 'GSP',
            'D': 'Display'
        }
        trans_val = network_trans.get(marketing_network.upper())
        if trans_val:
            marketing_network = trans_val
            clean_dict = {'MarketingNetwork': marketing_network}
        elif marketing_network == 'BRANDHYB':
            campaign_type = 'Hybrid Brand'
            marketing_network = 'Search'
            clean_dict = {
                'MarketingNetwork': marketing_network,
                'CampaignType': campaign_type
            }
        elif marketing_network == 'BRDISP':
            campaign_type = 'Brand'
            marketing_network = 'Display'
            clean_dict = {
                'MarketingNetwork': marketing_network,
                'CampaignType': campaign_type
            }
        elif marketing_network == 'COMHYB':
            campaign_type = 'Hybrid Brand'
            keyword_type = 'Competitors'
            marketing_network = 'Search'
            clean_dict = {
                'MarketingNetwork': marketing_network,
                'CampaignType': campaign_type,
                'KeywordType': keyword_type
            }
        else:
            clean_dict = {'MarketingNetwork': marketing_network}
    else:
        # If no info came in from regex parse, then use campaign name
        if campaign_name:
            if 'GSP' in campaign_name:
                marketing_network = 'GSP'
        # If still none then default to Search for marketing network
        if marketing_network is None:
            marketing_network = 'Search'
        clean_dict = {'MarketingNetwork': marketing_network}
    return clean_dict


def clean_campaign_type(campaign_type_value: Optional[str]) -> Optional[str]:
    """
    Scrubber method for 'CampaignType' parsed value.
    
    Expected values should include 'Brand', 'Non-Brand', 'Hybrid Brand', 'Competitor'
    
    :param campaign_type_value: Campaign type string raw parsing.
    :return:
    """
    campaign_type = campaign_type_value
    if campaign_type:
        # Translated the raw values into the normalized cases.
        campaign_trans = {
            'NB': 'Non-Brand', 
            'BR': 'Brand', 
            'HB': 'Hybrid Brand', 
            'CO': 'Competitor',
            'Non Brand': 'Non-Brand'
        }
        trans_val = campaign_trans.get(campaign_type.upper())
        if trans_val:
            campaign_type = trans_val
        # Finally update cleaned campaign type
    return campaign_type


def clean_location_type(location_type_value: Optional[str]) -> Optional[str]:
    """
    Scrubber method for 'LocationType' parsed value.

    Expected values should include: 'City>Nation', 'Nation>Nation>, 'Nation>City', 'City>City'

    :param location_type_value: Campaign type string raw parsing.
    :return:
    """
    location_type = location_type_value
    if location_type:
        location_type_trans = {
            # Keys here are the default encoding for location type in campaign names
            'CN': 'City>Nation',
            'NN': 'Nation>Nation',
            'NC': 'Nation>City',
            'CC': 'City>City'
        }
        trans_val = location_type_trans.get(location_type.upper())
        if trans_val:
            location_type = trans_val
        # Finally update cleaned location type
    return location_type


def clean_market(market_value: Optional[str]) -> Optional[str]:
    """
    Returns the made-uniform scrubbing of the raw market value.
    
    :param market_value: Raw market string.
    :return: 
    """
    market = market_value
    if market:
        # Market codes for uniformity.
        market_codes = {
            'Argentina': 'AR', 
            'Brazil': 'BR', 
            'Canada': 'CA', 
            'Caribe': 'WW', 
            'Chile': 'CL',
            'Colombia': 'CO',
            'Costa Rica': 'CR', 
            'Ecuador': 'EC', 
            'El Salvador': 'SV', 
            'Guatemala': 'GT', 
            'Honduras': 'HN',
            'Mexico': 'MX', 
            'Nicaragua': 'NI', 
            'Panama': 'PA', 
            'Peru': 'PE', 
            'Puerto Rico': 'PR',
            'Uruguay': 'UY', 
            'USA': 'US', 
        }
        trans_val = market_codes.get(market.title())
        if trans_val:
            market = trans_val
    else:
        # Default to None
        market = "N/A"
    # Finally update with cleaned market
    return market


def clean_geo_target(geo_target_value: Optional[str]) -> Optional[str]:
    """
    Returns the made-uniform scrubbing of the raw market value.

    :param geo_target_value: Raw market string.
    :return:
    """
    geo_target = geo_target_value
    if geo_target:
        geo_target.replace(" ", "")
        if len(geo_target) <= 3:
            geo_target = geo_target.upper()
    # Finally update with cleaned geo target
    return geo_target


def clean_leg_end(raw_leg_end_value: Optional[str], airline_code: str=None) -> Optional[str]:
    """
    Scrubber method for leg ends parsed values (ie., Origin or Destination).

    Expected output should include: IATA airport codes, IATA country codes.

    :param raw_leg_end_value: Route locale string raw parsing.
    :return:
    """
    # Specific cases where city names could be extracted, but still need to be normalized.
    city_trans = {
        'Crete': 'HER',
        'Limnos': 'LXS',
        'Borg El': 'HBE',
        'Larnaca': 'Larnaka'
    }
    if city_trans.get(raw_leg_end_value):
        raw_leg_end_value = city_trans.get(raw_leg_end_value)
    code = city_name_to_code(
        airline_code,
        raw_leg_end_value
    )
    if type(code) == list:
        code = code[0]
    return code


def update_origin_destination(parsing: Dict[str, Optional[str]]) -> Dict[str, Optional[str]]:
    """
    Applies a similar logic to clean_leg_end, but uses the whole dictionary and returns a whole dictionary.

    If either leg end would yield no values in the JSON object used in clean_leg_end(), then keep the current value;
    assume that it is already IATA conforming.

    :param parsing: Parsing as-is so far.
    :return:
    """
    output = {**parsing}
    airline_code = parsing.get('AirlineCode')
    origin = parsing.get('Origin', "")
    destination = parsing.get('Destination', "")
    if origin:
        code = clean_leg_end(origin.strip(), airline_code)
        if code:
            # Only reassign origin if we are returned a value (Assume the value is already IATA conforming)
            output["Origin"] = code
    if destination:
        code = clean_leg_end(destination.strip(), airline_code)
        if code:
            # Only reassign destination if we are returned a value (Assume the value is already IATA conforming)
            output['Destination'] = code
    return output
