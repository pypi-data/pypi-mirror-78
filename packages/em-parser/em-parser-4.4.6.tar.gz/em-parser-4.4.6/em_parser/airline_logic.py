"""
This module defines client-specific logic.

FOR MUNDO EYES ONLY, DO NOT SHARE WITH CLIENT
"""
from typing import Dict, Optional
from em_parser.airports_graph import CITY_NAMES, city_name_to_code


def air_berlin_parse_logic(parsing: Dict[str, Optional[str]]) -> None:
    """
    Applies airberlin-specific logic to the near-final parsing object, and applies the change in-place.

    :param parsing:
    :return:
    """
    # If match type, keyword group, location type are not given, there is a default to apply.
    if parsing.get('MatchType') is None:
        parsing.update({'MatchType': 'PX'})
    if parsing.get('KeywordGroup') is None:
        parsing.update({'KeywordGroup': 'General'})
    if parsing.get('LocationType') is None:
        parsing.update({'LocationType': 'CC'})
    if parsing.get('RouteType') is 'X':
        parsing.update({'RouteType': 'XX'})
    else:
        parsing.update({'RouteType': '00'})
    if parsing.get('MarketingNetwork') == 'RK':
        parsing['MarketingNetwork'] = 'L'
    else:
        parsing.update({'MarketingNetwork': 'S'})
    if parsing.get('Destination') is not None:
        parsing.update({'Destination': parsing.get('Destination').strip()})
    if parsing.get('Market') == 'RW':
        parsing.update({'Market': 'WW'})


def interjet_parse_logic(parsing):
    """
    Old style parsing logic to isolate and correct the pattern-breaking cases of interjet's parsing.

    :param parsing:
    :return:
    """
    if parsing.get('MarketingNetwork') == 'BRGSP':
        parsing.update({'MarketingNetwork': 'E'})
        parsing.update({'CampaignType': 'Brand'})
    elif parsing.get('MarketingNetwork') == 'RMKT':
        parsing.update({'MarketingNetwork': 'L'})
    elif parsing.get('MarketingNetwork') == 'DSA':
        parsing.update({'MarketingNetwork': 'Y'})
    elif parsing.get('MarketingNetwork') == 'DISP':
        parsing.update({'MarketingNetwork': 'Display'})

    if parsing.get('Market') == 'RW':
        parsing.update({'Market': 'WW'})

    if not parsing.get('KeywordType'):
        parsing.update({'KeywordType': 'Route'})
    elif parsing.get('KeywordType') == 'Competencia':
        parsing.update({'KeywordType': 'Competitors'})
    elif parsing.get('KeywordType') == 'Gen':
        parsing.update({'KeywordType': 'Generic'})

    if parsing.get('CampaignType') == 'BRANDHYB':
        parsing.update({'CampaignType': 'Hybrid Brand'})
    elif parsing.get('CampaignType') == 'COMHYBY4':
        parsing.update({'CampaignType': 'Hybrid Brand'})
        parsing.update({'KeywordType': 'Competitors'})
    elif parsing.get('CampaignType') == 'NBGSP':
        parsing.update({'CampaignType': 'Non-Brand'})
        parsing.update({'MarketingNetwork': 'GSP'})
    elif parsing.get('CampaignType') == 'RMKTV':
        parsing.update({'CampaignType': 'Non-Brand'})
        parsing.update({'MarketingNetwork': 'Display Remarketing'})
    elif parsing.get('CampaignType') == 'COMHYB':
        parsing.update({'CampaignType': 'Hybrid Brand'})
        parsing.update({'MatchType': 'PX'})
    elif parsing.get('CampaignType') == 'BRDISP':
        parsing.update({'CampaignType': 'Brand'})
        parsing.update({'MarketingNetwork': 'Display'})

    if parsing.get('Origin') == '0' and parsing.get('Destination').strip() == '0':
        parsing.update({'RouteType': 'Nonstop'})

    if parsing.get('ParseRegexId'):
        if (parsing.get('MatchType') is None) and ('Brand' in parsing.get('ParseRegexId')):
            parsing.update({'MatchType': 'PX'})

        if parsing.get('KeywordGroup') is None and ('GSP' in parsing.get('ParseRegexId')):
            parsing.update({'KeywordGroup': 'All'})

        if parsing.get('MarketingNetwork') == 'Display':
            parsing.update({'KeywordType': None})
            parsing.update({'MatchType': None})


def aegean_parse_logic(parsing):
    """
    Applies specific parsing for pattern-defying cases for A3 after regex matching.

    :param parsing:
    :return:
    """
    # Depreciated
    if '8207251616' == parsing.get('cc_id'):
        parsing.update({'MarketingNetwork': 'D'})
    ################################################################################################################
    # Normalize old campaign style Route locale and UK
    ################################################################################################################
    if parsing.get('RouteLocale') is not None:
        if 'Greece - Greece' in parsing.get('RouteLocale'):
            parsing.update({'RouteLocale': 'D'})
        else:
            parsing.update({'RouteLocale': 'I'})
    if parsing.get('Market') == 'UK':
        # Country code = GB from back in the old empire days.
        parsing['Market'] = 'GB'
    if parsing.get('Market') == 'RW':
        parsing.update({'Market': 'WW'})


def copa_parse_logic(parsing):
    """
    Applies specific logic to exceptions from the regex matching.
    :param parsing:
    :return:
    """
    ####################################################################################################################
    # Establish remarketing special cases from old formatting
    ####################################################################################################################
    if parsing.get('CampaignType') == 'RMK':
        # Display remarketing specific case
        parsing.update(
            {
                'MarketingNetwork': 'Display Remarketing',
                'KeywordType': None,
                'KeywordGroup': None,
                'CampaignType': 'Non-Brand',
                'Market': 'WW',
                'GeoTarget': 'WW'
            }
        )
    elif parsing.get('MarketingNetwork') == 'Rmkt-':
        # RLSA Remarketing specific case
        parsing.update(
            {
                'MarketingNetwork': 'RLSA',
                'CampaignType': 'Non-Brand'
            }
        )
    ####################################################################################################################
    # Special campaign type for old parsing is just Non-Brand
    ####################################################################################################################
    if parsing.get('CampaignType') == 'COM':
        parsing.update(
            {'CampaignType': 'Non-Brand'}
        )
    ####################################################################################################################
    # Standardize outliers of KeywordType, and expand where necessary
    ####################################################################################################################
    try:
        if parsing.get('KeywordType') == 'Interest':
            # Interest >> Interests
            parsing['KeywordType'] = 'Interests'
        elif parsing.get('KeywordType') == 'COMPETENCIA':
            # Spanish 'COMPETENCIA' >> engligh 'Competitor'
            parsing.update({'KeywordType': 'Competitor'})
        elif parsing.get('KeywordType') == 'ND':
            parsing.update(
                {
                    'KeywordType': 'Destination',
                    'LocationType': 'Nation>City'
                }
            )
        elif parsing.get('KeywordType') == 'PANAMA':
            parsing.update(
                {
                    'KeywordType': 'Destination',
                    'Destination': 'Panama'
                }
            )
        elif 'Villahermosa' in parsing.get('KeywordType'):
            parsing.update(
                {
                    'KeywordType': 'Destination',
                    'Destination': 'Villahermosa'
                }
            )
        elif parsing.get('KeywordType') == 'Comp':
            parsing.update(
                {'KeywordType': 'Competitor'}
            )
    except TypeError:
        pass
    ####################################################################################################################
    # Uniform Rest of World market
    ####################################################################################################################
    if parsing.get('Market') == 'RW':
        parsing.update({'Market': 'WW'})
    ####################################################################################################################
    # Specific parsing cases
    ####################################################################################################################
    if parsing.get('ParseRegexId') == 'CopaBrand2':
        if parsing.get('KeywordType').lower() == 'misspellings':
            # Sanitize string cases.
            if parsing.get('KeywordGroup').lower() in {'core', "copa"}:
                parsing.update(
                    {
                        'KeywordType': 'Core',
                        'KeywordGroup': 'Misspellings'
                    }
                )
            elif parsing.get('KeywordGroup').lower() == 'website':
                parsing.update(
                    {'KeywordType': 'Modifiers'}
                )
    ####################################################################################################################
    # This regex case returns null market for Rest of World campaigns
    ####################################################################################################################
    if parsing.get('ParseRegexId') == 'CopaNonbrand6' and parsing.get('Market') is None:
        parsing.update({'Market': 'WW'})
    ####################################################################################################################
    # If the campaign type is Display, remove the destination field.
    ####################################################################################################################
    if parsing.get('Destination') == 'Display':
        parsing.pop('Destination')


def jet_airways_logic(parsing):
    """
    Applies specific jet airways logic for certain special cases coming out of the parser.

    :param parsing:
    :return:
    """
    ####################################################################################################################
    # Normalize match type
    ####################################################################################################################
    if 'BD' == parsing.get('MatchType'):
        # [B]road[D] match -> [B]road [M]atch
        parsing['MatchType'] = 'BM'
    elif parsing.get('MatchType', "").upper() not in {'PH', 'EX', 'BM', 'HIGH', 'LOW', 'MEDIUM', 'MED', 'UNKNOWN'}:
        # Assume PX case
        parsing['MatchType'] = 'PX'
    ####################################################################################################################
    # Campaigns with no language assigned are en
    ####################################################################################################################
    if 'Language' not in parsing:
        parsing['Language'] = 'en'
    ####################################################################################################################
    # Normalize KW Type and Rte Locale
    ####################################################################################################################
    if parsing.get('KeywordType') == 'Comp':
        parsing.update({'KeywordType': 'Competitor'})
    if parsing.get('RouteLocale') == 'DR':
        parsing.update({'RouteLocale': 'Domestic'})


def volaris_parse_logic(parsing: Dict[str, Optional[str]]) -> None:
    """
    In style and form of the other methods above, this alters the dictionary in-place.

    Applies volaris-specific parsing logic to the parsing row.

    Flow:
    1. account name resolution if old account
    2. further segmentation identification from the regex matching if old account

    :param parsing: Parsing, right out of regex parsing logic, before scrubbing.
    :return:
    """
    # Declare the specific campaigns that are both display and select (no other general rule for this)
    search_with_display_select_campaigns = [
        # All are explicitly named.
        "SF - Route: Guadalajara - San José",
        "SF - Airplane to: Monterrey",
        "SF - Route: Reynosa - Guadalajara",
        "S-R LAX",
        "SF - Route: Morelia - Chicago Midway",
        "SF - Route: Mexico df - San Jose",
        "Destino_Acapulco",
        "SF - Route: Hermosillo - Mexico df",
        "SF - Route: Mexico df - Reynosa (new)",
        "SF - Airplane to: León",
        "Destino_Mexico",
        "SF - Route: Cancún - tuxtla gutiérrez",
        "SF - Airplane to: San Francisco (GUA)",
        "SF - Airplane to: Monterrey (Mobile)",
        "SF - Airplane to: New York",
        "GUA - SF - Airplane to: Villahermosa",
        "SF - Route: Vallarta - mexico city",
        "SF - Route: Guadalajara - mexico city",
        "SF - Route: Culiacan - Phoenix",
        "SF - Route: Los Cabos - Toluca",
        "SF - Route: Guadalajara - Los Mochis",
        "SF - Route: Mexico df - Mazatlán",
        "SF - Route: Chihuahua - Denver",
        "SF - Route: Mexico - Durango",
        "SF - Route: mexico city - Puerto Vallarta",
        "SF - Route: Tuxtla Gutiérrez - Monterrey",
        "SF - Route: Guadalajara - Chicago",
        "Volaris_Max_Sur de CA - Promo tarifa Solo Hoy",
        "SF - Route: Cancún - Querétaro",
        "SF - Route: Cancún - Guatemala",
        "SF - Airplane to: Veracruz",
        "SF - Airplane to: Portland",
        "SF - Route: Chihuahua - Tijuana",
        "SF - Route: Guadalajara - Hermosillo",
        "SF - Route: mexico city - Fort Lauderdale",
        "SF - Airplane to: Guatemala City (Desktop)",
        "SF - Airplane to: San Luis Potosí",
        "SF - Route: Monterrey - Acapulco",
        "SF - Route: Huatulco - mexico city",
        "SF - Route: Cancún - tuxtla gutiérrez",
        "SF - Route: Guadalajara - Chicago",
        "SF - Airplane to: Culiacán (Mobile)",
        "SF - Route: Los Mochis - Mexico df",
        "SF - Route: Mexico df - Los Angeles",
        "SF - Route: Culiacán - mexico city",
        "SF - Route: San José - Managua",
        "SF - Route: Chihuahua - mexico city",
        "SF - Airplane to: San Antonio",
        "SF - Route: Mexico df - Villahermosa",
        "GUA - SF - Airplane to: Mexicali",
        "S-R SJC",
        "SF - Route: mexico city - Oaxaca",
        "SF - Route: Cancún - Los Angeles",
        "SF - Route: mexico city - Huatulco",
        "SF - Airplane to: Hermosillo",
        "SF - Route: Guadalajara - Denver",
        "SF - Route: San José - Guatemala",
        "SF - Route: Mexico df - Chetumal",
        "SF - Airplane to: Orlando",
        "SF - Airplane to: Oaxaca (Desktop)",
        "SF - Route: Cancún - San Juan",
        "SF - Route: Mexico df - Fort Lauderdale",
        "S-D Houston",
        "SF - Airplane to: Oaxaca (Mobile)",
        "SF - Route: Guadalajara - Torreón",
        "SF - Airplane to: Dallas",
        "SF - Airplane to: Acapulco",
        "GUA - SF - Airplane to: Las Vegas",
        "SF - Route: Tijuana - San Francisco",
        "GUA - SF - Airplane to: Portland",
        "SF - Route: Monterrey - Hermosillo",
        "SF - Airplane to: Mexico (PR)",
        "GUA - SF - Airplane to: Guadalajara",
        "SF - Route: Acapulco - Monterrey",
        "SF - Route: Los Mochis - Tijuana",
        "SF - Route: Toluca - Puerto Vallarta",
        "SF - Airplane to: Ontario",
        "SF - Route: Chicago - Ixtapa",
        "GUA - SF - Airplane to: Culiacán",
        "SF - Route: Chihuahua - mexico city",
        "SF - Airplane to: Culiacán (Desktop)",
        "SF - Airplane to: Hermosillo",
        "SF - Airplane to: San José (CR)",
        "SF - Route: mexico city - Las Vegas",
        "SF - Airplane to: San Francisco",
        "SF - Airplane to: San Francisco",
        "SF - Route: mexico city - Durango",
        "GUA - SF - Airplane to: La Paz",
        "SF - Route: La Paz - Tijuana",
        "SF - Route: Mexico df - San Antonio",
        "SF - Airplane to: Querétaro",
        "SF - Route: Chihuahua - Mexico df",
        "SF - Route: Acapulco - Tijuana",
        "SF - Route: Guadalajara - Villahermosa",
        "GUA - SF - Airplane to: Tijuana",
        "SF - Route: Guadalajara - Guatemala",
        "SF - Route: Veracruz - Guadalajara",
        "Destino_SanLuisPotosi",
        "SF - Route: Mexico df - New York",
        "GUA - SF - Route: Guatemala - San Salvador",
        "SF - Airplane to: Torreón",
        "SF - Route: Guadalajara - Monterrey",
        "GUA - SF - Airplane to: Dallas",
        "SF - Route: Puebla - Tijuana",
        "SF - Route: Guadalajara - Reno",
        "SF - Route: Mexico df - Tapachula",
        "SF - Route: Cancún - Villahermosa",
        "Volaris Chicago México",
        "SF - Route: Cancún - Villahermosa",
        "SF - Route: Mexico df - Puerto Vallarta",
        "SF - Route: Tijuana - Uruapan",
        "SF - Route: mexico city - San Francisco",
        "SF - Route: Cancún - Chihuahua",
        "SF - Route: Guadalajara - Cozumel",
        "GUA - SF - Airplane to: Phoenix",
        "SF - Airplane to: Las Vegas",
        "SF - Route: Cancún - mexico city",
        "SF - Route: Monterrey - Culiacán",
        "SF - Route: Guadalajara - Reno",
        "SF - Route: Culiacán - Monterrey",
        "Volaris_Max_Sur de CA",
        "SF - Route: Hermosillo - Phoenix",
        "Navidad",
        "SF - Route: León - Chicago Midway",
        "SF - Airplane to: Mexico City (Mobile)",
        "SF - Route: Guadalajara - Cancun",
        "SF - Route: mexico city - Las Vegas",
        "SF - Route: Mazatlán - Tijuana",
        "SF - Route: San Juan - Guadalajara",
        "SF - Route: Mexico df - Tijuana",
        "SF - Route: Guatemala - Cancun",
        "SF - Airplane to: Villahermosa",
        "SF - Route: Monterrey - Dallas",
        "SF - Route: León - Tijuana",
        "SF - Route: Los Angeles - Durango",
        "SF - Route: León - Los Angeles",
        "SF - Route: mexico city - Orlando",
        "SF - Route: mexico city - Chicago",
        "GUA - SF - Airplane to: Los Cabos",
        "SF - Airplane to: Sacramento",
        "SF - Route: Culiacán - La Paz",
        "SF - Airplane to: Denver",
        "SF - Route: Monterrey - Mexico Df",
        "SF - Route: mexico city - vallarta",
        "SF - Route: Tijuana - Torreon",
        "SF - Route: mexico city - Denver",
        "M-S-O Escápate",
        "SF - Route: Mexico df - Torreon",
        "S-O Escápate",
        "SF - Airplane to: Cancún (Desktop) (2.9)",
        "SF - Airplane to: Guadalajara (Desktop)",
        "Campaign #1",
        "SF - Airplane to: Chihuahua",
        "Destino_Aguascalientes",
        "S-R MDW",
        "SF - Route: Los Angeles - Durango",
        "SF - Route: San Juan - Cancún",
        "SF - Route: Cancún - Guatemala",
        "SF - Route: León - Cancún",
        "SF - Airplane to: Oakland",
        "SF - Route: Cancún - mexico city",
        "SF - Airplane to: San Francisco",
        "S-R LAS",
        "SF - Airplane to: Guadalajara (Mobile)",
        "SF - Route: mexico city - Orlando",
        "SF - Route: Los Angeles - Querétaro",
        "SF - Route: San Juan - Cancún",
        "S-R OAK",
        "SF - Route: Mexico df - Miami",
        "SF - Route: Cancún - Monterrey",
        "SF - Route: mexico city - Tapachula",
        "SF - Route: mexico city - Tijuana",
        "SF - Route: Guadalajara - Sacramento",
        "SF - Route: Hermosillo - Monterrey",
        "SF - Route: mexico city - San Diego",
        "SF - Route: San José - Cancun",
        "Aniversario",
        "SF - Route: Guadalajara - Milwaukee",
        "SF - Route: Guadalajara - Phoenix (new)",
        "SF - Airplane to: Huatulco",
        "SF - Airplane to: Cancún (Mobile)",
        "SF - Route: Mexico df - Ixtapa",
        "SF - Airplane to: Sacramento",
        "SF - Route: Guadalajara - Los Mochis",
        "SF - Route: Acapulco - Mexico df",
        "SF - Airplane to: Zacatecas",
        "SF - Route: mexico city - Fort Lauderdale (new)",
        "Volaris",
        "SF - Airplane to: Fresno",
        "SF - Route: Chihuahua - Tijuana",
        "SF - Route: mexico city - Huatulco",
        "SF - Route: Monterrey - Denver",
        "SF - Route: Cancún - Villahermosa -",
        "SF - Route: Mexico df - Mexicali",
        "SF - Route: Mexico df - Las Vegas",
        "SF - Route: Guatemala - Cancun",
        "SF - Route: Mexico df - Reynosa",
        "SF - Route: Guadalajara - Fort Lauderdale",
        "SF - Route: Tuxtla Gutiérrez - Guadalajara",
        "SF - Route: Chihuahua - Guadalajara",
        "GUA - SF - Route: Guatemala - San Jose",
        "SF - Airplane to: Colima",
        "SF - Route: Hermosillo - Tijuana",
        "SF - Route: Reynosa - Guadalajara",
        "SF - Airplane to: Sacramento (GUA)",
        "SF - Route: Monterrey - Puerto Vallarta",
        "GUA - SF - Route: Guatemala - Guadalajara",
        "SF - Route: Tijuana - Veracruz",
        "SF - Route: Culiacán - Los Cabos",
        "SF - Route: Morelia - Tijuana",
        "SF - Airplane to: Reno (GUA)",
        "Destino_Tijuana",
        "SF - Route: Guadalajara - Dallas",
        "SF - Route: Guatemala - Guadalajara",
        "SF - Route: Los Cabos - Mexico City",
        "SF - Route: Mexico df - Tuxtla Gutiérrez",
        "SF - Route: San Luis Potosí - Tijuana",
        "SF - Airplane to: Toluca",
        "Destino_DF",
        "SF - Route: Culiacán - Tijuana",
        "SF - Airplane to: Los Ángeles",
        "SF - Route: Toluca - Los Cabos",
        "SF - Route: mexico city - Los Cabos",
        "SF - Route: Monterrey - Puebla",
        "SF - Airplane to: Ciudad Obregón",
        "SF - Route: mexico city - Los Cabos",
        "SF - Route: Guadalajara - Monterrey",
        "GUA - SF - Airplane to: San Francisco",
        "SF - Airplane to: Tijuana (Mobile)",
        "SF - Route: Mexico df - Miami",
        "SF - Route: Guadalajara - Fort Lauderdale",
        "SF - Route: Mexico df - Villahermosa",
        "GUA - SF - Airplane to: Mexico City",
        "SF - Route: Ciudad Juárez - mexico city",
        "SF - Route: Mexico df - San Francisco",
        "SF - Airplane to: Morelia",
        "SF - Route: Mexico df - Orlando",
        "S-R SMF",
        "SF - Route: mexico city - Mérida",
        "SF - Route: mexico city - guadalajara",
        "SF - Airplane to: Los Cabos",
        "SF - Airplane to: chicago",
        "SF - Airplane to: Las Vegas",
        "SF - Airplane to: Tijuana",
        "SF - Route: Guadalajara - Fresno",
        "SF - Route: Cancún - San Luis Potosí",
        "Destino_Ciudad_de_Mexico",
        "SF - Route: Guadalajara - mexico city",
        "Volaris Chicago Inglés",
        "SF - Route: Guadalajara - Oaxaca",
        "SF - Route: Zacatecas - Chicago Midway",
        "SF - Route: Mexico df - Veracruz",
        "SF - Route: Querétaro - Tijuana",
        "Destino_Puebla",
        "SF - Route: Acapulco - mexico city",
        "SF - Airplane to: Puebla",
        "SF - Route: Guatemala - Cancun",
        "Volaris Chicago México Banners",
        "SF - Airplane to: Guadalajara",
        "SF - Route: Mexico df - Los Cabos",
        "SF - Route: Puerto Vallarta - Tijuana",
        "S-R FAT",
        "SF - Route: Aguascalientes - Cancún",
        "SF - Route: Monterrey - Acapulco",
        "SF - Route: Mexico df - Tijuana",
        "SF - Route: Cancún - Tuxtla Gutierrez",
        "Destino_Vallarta",
        "SF - Route: Guadalajara - New York",
        "SF - Airplane to: Portland",
        "SF - Route: Guadalajara - Mexicali",
        "SF - Route: Cancún - Puebla",
        "SF - Route: Guadalajara - San Bernardino",
        "SF - Route: Culiacan - Phoenix",
        "SF - Route: Mexico df - Fort Lauderdale",
        "SF - Route: Culiacán - Guadalajara",
        "GUA - SF - Airplane to: New York",
        "SF - Airplane to: Reno",
        "SF - Airplane to: Tepic",
        "SF - Route: Guadalajara - Miami",
        "GUA - SF - Airplane to: Los Ángeles",
        "SF - Route: Aguascalientes - Los Angeles",
        "SF - Airplane to: Mazatlán",
        "SF - Route: Monterrey - Hermosillo",
        "GUA - SF - Airplane to: Costa Rica",
        "SF - Route: Guadalajara - Los Cabos",
        "SF - Route: Cancún - Veracruz",
        "SF - Route: Monterrey - Guadalajara",
        "SF - Route: Monterrey - Tijuana",
        "SF - Route: Guadalajara - Miami",
        "SF - Route: Guadalajara - Ontario",
        "SF - Route: Guadalajara - Huatulco",
        "SF - Route: mexico city - Houston",
        "SF - Route: Aguascalientes - Tijuana",
        "SF - Route: Guadalajara - Puebla",
        "SF - Airplane to: Fort Lauderdale",
        "SF - Route: Culiacán - Mexico df",
        "SF - Route: Mexico df - San Francisco",
        "SF - Route: Guadalajara - Austin",
        "S-R MCO",
        "SF - Airplane to: Culiacán",
        "SF - Route: Mexico df - Mexicali",
        "SF - Route: León - Los Angeles",
        "SF - Route: Guadalajara - Houston",
        "SF - Route: Guadalajara - Veracruz",
        "SF - Concierto a Bordo",
        "SF - Route: Tijuana - Zacatecas",
        "SF - Airplane to: Monterrey (Desktop)",
        "SF - Route: Mexico df - San Juan",
        "SF - Route: mexico city - Chihuahua",
        "SF - Route: Guadalajara - Mexico df",
        "SF - Route: mexico city - Monterrey",
        "SF - Route: Guatemala - Guadalajara",
        "SF - Route: mexico df- guadalajara",
        "Destino_Veracruz",
        "SF - Airplane to: Mérida (Mobile)",
        "Destino_Los_Cabos",
        "SF - Route: mexico city - Durango",
        "SF - Airplane to: Querétaro",
        "SF - Route: Chicago - Durango",
        "Branding - already bought",
        "SF - Route: mexico city - Mexicali",
        "SF - Route: Colima - Tijuana",
        "SF - Route: Tijuana - Vallarta",
        "SF - Airplane to: durango",
        "SF - Route: Guadalajara - San Diego",
        "SF - Route: Reynosa - Cancun",
        "SF - Route: Zacatecas - Los Angeles",
        "SF - Route: Oaxaca - Los Angeles",
        "SF - Route: San Salvador - Managua",
        "SF - Route: Mexico df - Guatemala",
        "SF - Route: Huatulco - Mexico df",
        "SF - Route: Monterrey - Dallas",
        "SF - Airplane to: Guadalajara From Guatemala",
        "SF - Airplane to: Costa Rica",
        "SF - Airplane to: San José",
        "SF - Airplane to: Puerto Vallarta",
        "SF - Route: mexico city - Los Angeles",
        "SF - Route: Guadalajara - Los Cabos",
        "SF - Airplane to: San Francisco",
        "SF - Route: Los Cabos - Tijuana",
        "SF - Route: Monterrey - Los Cabos",
        "SF - Airplane to: Tapachula",
        "SF - Route: Chihuahua - Denver",
        "SF - Airplane to: Tuxtla Gutiérrez",
        "SF - Route: Chihuahua - Mexico df",
        "SF - Airplane to: Ciudad Juárez",
        "SF - Route: Tijuana - Torreon",
        "SF - Route: Mexico df - Tampico",
        "SF - Airplane to: Uruapan",
        "SF - Route: Monterrey - Merida",
        "SF - Route: Guadalajara - San Antonio",
        "SF - Route: La Paz - Mexico df",
        "SF - Route: Monterrey - Querétaro",
        "Destino_Cancun",
        "SF - Route: Guadalajara - Veracruz",
        "SF - Airplane to: San Juan (PR) - To mexico",
        "SF - Route: Guadalajara - Portland",
        "SF - Airplane to: Los Cabos",
        "SF - Route: Guadalajara - New York",
        "SF - Route: Guadalajara - Tijuana",
        "SF - Route: Oaxaca - Monterrey",
        "SF - Route: Morelia - San Francisco",
        "SF - Route: León - San Francisco",
        "SF - Route: Mexico df - Reynosa",
        "SF - Route: Mexico df - Mazatlán",
        "GUA - SF - Airplane to: Sacramento",
        "SF - Route: Chicago - Monterrey",
        "SF - Route: Cancún - San José",
        "SF - Route: mexico city - Tampico",
        "SF - Route: Guatemala - San Jose",
        "SF - Airplane to: Mexicali",
        "SF - Route: Ciudad Juárez - Mexico df",
        "SF - Route: Guadalajara - Phoenix",
        "Destino_Monterrey",
        "SF - Route: Guadalajara - San Francisco",
        "SF - Route: Toluca - Puerto Vallarta",
        "SF - Route: Mérida - Monterrey",
        "SF - Route: Monterrey - Oaxaca",
        "SF - Route: Guadalajara - San Antonio",
        "SF - Route: Mexico df - Tapachula",
        "SF - Airplane to: Tijuana",
        "SF - Airplane to: Mexicali",
        "SF - Route: Guadalajara - Phoenix",
        "SF - Airplane to: chicago",
        "SF - Airplane to: Phoenix",
        "SF - Airplane to: Cancún",
        "SF - Airplane to: Reynosa",
        "SF - Route: San José - Guadalajara",
        "SF - Route: Chicago - Guadalajara",
        "SF - Route: Hermosillo - Monterrey",
        "SF - Route: Guadalajara - La Paz",
        "SF - Route: León - Oakland",
        "SF - Route: León - Ontario",
        "SF - Route: Cihcago- Denver",
        "SF - Airplane to: Villahermosa",
        "SF - Airplane to: Chetumal",
        "SF - Route: Acapulco - Monterrey",
        "SF - Route: Mexico df - Torreon",
        "SF - Route: Los Angeles - Oaxaca",
        "SF - Route: Chicago - Huatulco",
        "SF - Route: Guadalajara - Oakland",
        "SF - Route: Guadalajara - Las Vegas",
        "SF - Airplane to:Reynosa",
        "SF - Route: Mexico df - Tampico",
        "SF - Route: Phoenix - Durango",
        "SF - Route: Guadalajara - Las Vegas",
        "Destinos_Oaxaca",
        "SF - Airplane to: Aguascalientes",
        "SF - Route: mexico city - Mexicali",
        "SF - Route: Monterrey - Chihuahua",
        "SF - Airplane to: La Paz",
        "SF - Route: Monterrey - Oaxaca",
        "cSF - Route: Cancún - Guadalajara",
        "SF - Route: Culiacán - La Paz",
        "SF - Route: Hermosillo - Mexico df",
        "SF - Route: mexico city - Villahermosa",
        "SF - Airplane to: Reno",
        "SF - Route: Los Mochis - Guadalajara",
        "SF - Route: mexico city - Fort Lauderdale",
        "SF - Airplane to: Mérida (Desktop)",
        "SF - Airplane to: Tijuana (Desktop)",
        "SF - Route: Hermosillo - Phoenix",
        "SF - Route: Los Mochis - mexico city",
        "SF - Route: mexico city - Tuxtla Gutiérrez",
        "SF - Route: Monterrey - Tuxtla Gutiérrez",
        "SF - Route: Mexico df - Denver",
        "SF - Route: Mexico - New York",
        "SF - Route: Guadalajara - Mexico df",
        "SF - Route: Hermosillo - mexico city",
        "SF - Route: Cancún - Puerto Rico",
        "GUA - SF - Airplane to: Reno",
        "SF - Route: Uruapan - Los Angeles",
        "SF - Route: Phoenix - Durango",
        "SF - Route: Guadalajara - Dallas",
        "SF - Route: Mexico df - Las Vegas",
        "SF - Route: San José - San Salvador",
        "GUA - SF - Airplane to: Monterrey",
        "SF - Route: Tijuana - Tepic",
        "SF - Route: Toluca - Los Cabos",
        "SF - Route: Mexicali - Guadalajara",
        "SF - Route: Mexico df - Oaxaca",
        "SF - Route: Ciudad Juárez - Cancún",
        "SF - Route: Guatemala - Guadalajara",
        "SF - Route: Mexico df - Tuxtla Gutiérrez",
        "SF - Route: mexico df- vallarta",
        "SF - Route: Ciudad Obregón - Tijuana",
        "GUA - SF - Route: Guatemala - Cancun",
        "SF - Route: Cancún - Guadalajara",
        "SF - Route: Mexico df - Oaxaca",
        "GUA - SF - Airplane to: Fresno",
        "SF - Route: Guadalajara - Seattle",
        "SF - Route: Monterrey - Toluca",
        "SF - Airplane to: Puebla",
        "GUA - SF - Airplane to: Cancún",
        "SF - Airplane to: San Juan (PR)",
        "SF - Route: La Paz - mexico city",
        "SF - Route: Cancún - Mexico df",
        "SF - Airplane to: Hermosillo (GUA)",
        "S-R SAN",
        "SF - Route: Monterrey - Tuxtla Gutiérrez",
        "SF - Route: Cancún - Tijuana",
        "SF - Route: Culiacan - Mexicali",
        "GUA - SF - Airplane to: Puebla",
        "SF - Route: Guadalajara - Orlando",
        "SF - Route: Mexico df - Monterrey",
        "SF - Route: Cancún - Mexico df",
        "SF - Route: Cancún - Toluca",
        "Destino_Guadalajara",
        "SF - Airplane to: Monterrey",
        "SF - Route: Mérida - Tijuana",
        "SF - Route: Mexico df - Los Cabos",
        "SF - Airplane to: Guatemala City (Mobile)",
        "SF - Route: Mexico df - Ixtapa",
        "Volaris Chicago Hispanos",
        "GUA - SF - Airplane to: chicago",
        "SF - Airplane to: Mexico City (Desktop)",
        "SF - Airplane to: chicago",
        "SF - Route: Tuxtla Gutiérrez - Tijuana",
        "SF - Route: Monterrey - León",
        "SF - Airplane to: Guadalajara",
        "SF - Route: mexico city - Tampico",
        "SF - Airplane to: Cancún",
        "Destinos_Otros_Top",
        "SF - Route: Mexico df - Chicago",
        "SF - Route: Chihuahua - Monterrey",
        "SF - Airplane to: Houston",
        "SF - Route: Morelia - Oakland",
        "SF - Airplane to: Dallas",
        "SF - Airplane to: Fresno",
        "SF - Route: Mexico df - Durango",
        "SF - Airplane to: Los Mochis",
        "SF - Route: Monterrey - Cancun",
        "SF - Airplane to: chicago",
        "SF - Route: Oaxaca - Tijuana",
        "SF - Airplane to: La Paz",
        "GUA - SF - Airplane to: Querétaro",
        "SF - Route: Ciudad Obregón - Guadalajara",
        "SF - Route: Guadalajara - Tuxtla Gutiérrez",
        "San Diego",
        "SF - Airplane to: Mexico City",
        "SF - Airplane to: Phoenix",
        "SF - Airplane to: Ixtapa",
        "SF - Route: Culiacán - Guadalajara",
        "SF - Route: Los Cabos - Tijuana",
        "GUA - SF - Airplane to: Hermosillo",
        "SF - Airplane to: Los Cabos (GUA)",
        "SF - Airplane to: Mexico City",
        "SF - Route: Guadalajara - Los Angeles",
        "SF - Route: Monterrey - Guadalajara",
        "SF - Route: Chihuahua - Guadalajara",
        "SF - Airplane to: San José (CR)",
        "SF - Airplane to: Los Ángeles",
        "SF - Route: Monterrey - Veracruz",
        "SF - Airplane to: New York",
        "Carrera Volaris 5K & 10K",
        "SF - Route: mexico city - Mazatlán",
        "SF - Route: Guadalajara - San Francisco",
        "SF - Airplane to: Miami",
        "SF - Route: Mexico df - San Diego",
        "SF - Route: Reynosa - Cancun",
        "SF - Route: Guatemala - San Salvador",
        "SF - Route: Culiacán - Mexico df",
        "SF - Route: Chicago - Querétaro",
        "SF - Route: Cancún - Monterrey",
        "SF - Airplane to: Fresno (GUA)",
        "SF - Route: Hermosillo - Tijuana",
    ]

    ####################################################################################################################
    # Declare the methods used to break down the individual parsings.
    ####################################################################################################################
    def _volaris_old_non_brand_1_and_2(parsing: Dict[str, Optional[str]]) -> None:
        """
        Applies specific decision logic for the parsing that is impractical to apply in pure regex. Corresponds to
        ParseRegexId 'VolarisOldNonBrand1', which has been specifically isolated for this case. This is existing,
        pre-restructure format of Volaris' naming convention.

        Makes changes in-place to keep with the format of the logic of the module.

        :param parsing: Current state of parsing, fresh out of regex matching.
        :return:
        """
        ################################################################################################################
        # Defaults and determined by the parseregexid
        ################################################################################################################
        parsing["MatchType"] = "N/A"
        parsing["CampaignType"] = "Non-Brand"
        ################################################################################################################
        # Route vs Destination
        ################################################################################################################
        if parsing.get("KeywordType") == "Airplane to":
            parsing["KeywordType"] = "Destination"
        elif parsing.get("KeywordType") == "Route":
            parsing["KeywordType"] = "Route"
            parsing["LocationType"] = "City>City"
        ################################################################################################################
        # Market and GeoTarget (if available)
        ################################################################################################################
        if parsing.get("Market") in {"USA", "GUA", "PR", "CR"}:
            # USA and GUA are not IATA country codes
            if parsing["Market"] == "USA":
                parsing["Market"] = "US"
            elif parsing["Market"] == "GUA":
                parsing["Market"] = "GT"
            # If no geo target otherwise available, set it to be the market
            if not parsing.get("GeoTarget"):
                parsing["GeoTarget"] = parsing["Market"]
        ################################################################################################################
        # All the origin/ destination campaigns are in the city name. We must normalize these values for later.
        ################################################################################################################
        if "Origin" in parsing.keys():
            parsing["Origin"] = volaris_normalize_city_name(parsing["Origin"])
        if "Destination" in parsing.keys():
            parsing["Destination"] = volaris_normalize_city_name(parsing["Destination"])
        ################################################################################################################
        # Final step: Validate marketing network
        ################################################################################################################
        _volaris_old_nb_marketing_network(parsing)

    def _volaris_old_non_brand_3(parsing: Dict[str, Optional[str]]) -> None:
        """
        Case: 'S-R Monterrey&&CUU'

        :param parsing:
        :return:
        """
        ################################################################################################################
        # Default for the parser match
        ################################################################################################################
        parsing["CampaignType"] = "Non-Brand"
        parsing["MatchType"] = "N/A"
        parsing["KeywordType"] = "Route"
        parsing["LocationType"] = "City>City"
        parsing["Language"] = "es"
        parsing["GeoTarget"] = parsing.get("Market") if parsing.get("Market") else "N/A"
        ################################################################################################################
        # About 50% Of these campaigns are SearchWithDisplaySelect
        ################################################################################################################
        # List of those that are not MarketingNetwork = Search Only
        display_select = [
            "S-R LAX",
            "S-R SJC",
            "S-R MDW",
            "S-R LAS",
            "S-R OAK",
            "S-R SMF",
            "S-R FAT",
            "S-R MCO",
            "S-R SAN",
        ]
        campaign_name = parsing["CampaignName"]
        parsing["MarketingNetwork"] = "Search with Display select" if campaign_name in display_select else "Search"
        ################################################################################################################
        # Direct or connecting?
        ################################################################################################################
        connecting = {
            "conexión",
            "conexion",
            "coneccion",
            "connect",
            "connecting"
        }
        if parsing.get("RouteType", "") and parsing["RouteType"].lower() in connecting:
            parsing["RouteType"] = "Connecting"
        else:
            parsing["RouteType"] = "Nonstop"

    def _volaris_old_non_brand_4(parsing: Dict[str, Optional[str]]) -> None:
        """
        Applies the specific logic to the destination campaign case:

        'M-S-D AguasCalientes&&Aguascalientes - Vuelo'

        :param parsing:
        :return:
        """
        ################################################################################################################
        # Defaults
        ################################################################################################################
        parsing["MatchType"] = "N/A"
        parsing["GeoTarget"] = parsing.get("Market")
        parsing["RouteType"] = "Nonstop"
        parsing["KeywordType"] = "Destination"
        ################################################################################################################
        # Conditionals
        ################################################################################################################
        # These keywords are in english for the US version of these campaigns (may be SOME es keywords, but it seems
        # the intention was to have these be in english
        parsing["CampaignType"] = "Non-Brand" if "brand" not in parsing.get("AdGroupName", "").lower() else "Hybrid Brand"
        parsing["Language"] = "en" if parsing.get("Market") == "US" else "es"
        ################################################################################################################
        # Address the city name inconsistancies.
        ################################################################################################################
        if "mexico" in parsing["Destination"].lower() or "méxico" in parsing["Destination"].lower():
            parsing["Destination"] = parsing["Destination"].lower().replace("méxico d.f", "MEX")
            parsing["Destination"] = parsing["Destination"].replace("mexico d.f", "MEX")
            parsing["Destination"] = parsing["Destination"].replace("méxico df", "MEX")
            parsing["Destination"] = parsing["Destination"].replace("mexico df", "MEX")

    def _volaris_old_non_brand_5(parsing: Dict[str, Optional[str]]) -> None:
        """
        Special exception to OldNonBrand4.

        Only 1 campaign name: 'S-D-OAnti-camión'

        :param parsing:
        :return:
        """
        parsing["MatchType"] = "N/A"
        parsing["GeoTarget"] = parsing.get("Market")
        parsing["CampaignType"] = "Non-Brand"
        parsing["KeywordType"] = "Generic"
        parsing["KeywordGroup"] = "Destination"
        parsing["RouteType"] = "Nonstop"

    def _volaris_old_non_brand_6(parsing: Dict[str, Optional[str]]) -> None:
        """
        Applies the logic specific to OldNonBrand6.

        Case: 'Destino_Cancun&&Autobuses cancun'

        :param parsing:
        :return:
        """
        ################################################################################################################
        # Match defaults
        ################################################################################################################
        parsing["MatchType"] = "N/A"
        parsing["RouteType"] = "Nonstop"
        parsing["KeywordType"] = "Generic"
        parsing["KeywordGroup"] = "Destination"
        parsing["GeoTarget"] = parsing.get("Market")
        ################################################################################################################
        # Conditionals
        ################################################################################################################
        parsing["CampaignType"] = "Non-Brand" \
            if "brand" not in parsing.get("AdGroupName", "").lower() \
            else "Hybrid Brand"
        # Pure search for Bus Switching; search w/ display for Volaris Mexico
        if parsing.get("AccountName") == "Volaris Mexico":
            parsing["MarketingNetwork"] = "Search with Display select"
        else:
            parsing["MarketingNetwork"] = "Search"
        ################################################################################################################
        # Fix Destination field formatting
        ################################################################################################################
        # MEX synonyms
        parsing["Destination"] = parsing["Destination"].replace("DF", "MEX")
        parsing["Destination"] = parsing["Destination"].replace("Ciudad_de_Mexico", "MEX")
        # Spaces and CamelCases
        parsing["Destination"] = parsing["Destination"].replace("SanLuisPotosi", "SLP")
        parsing["Destination"] = parsing["Destination"].replace("Los_Cabos", "SJD")

    def _volaris_old_non_brand_7(parsing: Dict[str, Optional[str]]) -> None:
        """
        Applies specific parsing logic to VolarisOldNonBrand7 matches.

        Case: 'SEM | Destinos: Multiples | GEO: Monterrey&&Acapulco | Vuelos - Oferta'

        :param parsing:
        :return:
        """
        ################################################################################################################
        # Defaults
        ################################################################################################################
        parsing["MatchType"] = "N/A"
        parsing["KeywordType"] = "Destination"
        parsing["RouteType"] = "Nonstop"
        parsing["MarketingNetwork"] = "Search"
        parsing["CampaignType"] = "Non-Brand"
        ################################################################################################################
        # Conditionals + Formatting
        ################################################################################################################
        # GeoTarget is either a city name, 'MX', or 'Multiples'
        if parsing.get("GeoTarget") in {"Multiples", "MX"}:
            parsing["GeoTarget"] = "MX"
        else:
            parsing["GeoTarget"] = volaris_normalize_city_name(parsing.get("GeoTarget", ""))
            parsing["GeoTarget"] = city_name_to_code(parsing.get("AirlineCode"), parsing["GeoTarget"])
        # Sometimes destination has a trailing whitespace character
        parsing["Destination"] = volaris_normalize_city_name(parsing.get("Destination", "").strip())
        parsing["KeywordType"] = parsing.get("KeywordType", "").strip()

    def _volaris_old_non_brand_8(parsing: Dict[str, Optional[str]]) -> None:
        """
        Applies specific parsing logic to VolarisOldNonBrand8 matches.

        Case: 'SEM | Rutas | GEO: MX&&Tampico-Monterrey | Boleto Avion'

        :param parsing:
        :return:
        """
        ################################################################################################################
        # Defaults
        ################################################################################################################
        parsing["MatchType"] = "N/A"
        parsing["KeywordType"] = "Route"
        parsing["RouteType"] = "Nonstop"
        parsing["MarketingNetwork"] = "Search"
        parsing["CampaignType"] = "Non-Brand"
        ################################################################################################################
        # Conditionals
        ################################################################################################################
        # Remove leading and trailing whitespace.
        parsing["Destination"] = parsing.get("Destination", "").strip() if parsing.get("Destination") else ""
        parsing["Origin"] = parsing.get("Origin", "").strip() if parsing.get("Origin") else ""
        parsing["KeywordType"] = parsing.get("KeywordType", "").strip() if parsing.get("KeywordType") else ""
        # Origin or Dest values of 'Df' need to be made uniform.
        parsing["Destination"] = parsing["Destination"] if parsing["Destination"].lower() != "df" else "MEX"
        parsing["Origin"] = parsing["Origin"] if parsing["Origin"].lower() != "df" else "MEX"

    def _volaris_old_non_brand_9(parsing: Dict[str, Optional[str]]) -> None:
        """
        Applies specific parsing logic to VolarisOldNonBrand9 matches.

        Case: ''


        :param parsing:
        :return:
        """
        ################################################################################################################
        # Defaults
        ################################################################################################################
        parsing["MatchType"] = "N/A"
        parsing["CampaignType"] = "Non-Brand"
        parsing["Language"] = "en"
        parsing["GeoTarget"] = parsing["Origin"]
        parsing["RouteType"] = "Nonstop"
        ################################################################################################################
        # Conditionals
        ################################################################################################################
        if parsing.get("Destination"):
            parsing["KeywordType"] = "Route"
        else:
            parsing["KeywordType"] = "Origin"

    def _volaris_old_non_brand_10(parsing: Dict[str, Optional[str]]) -> None:
        """
        Applies specific parsing logic to VolarisOldNonBrand10 matches.

        Case: 'SF-Oakland-Cancun_EN&&Vuelos'

        :param parsing:
        :return:
        """
        ################################################################################################################
        # Defaults for this match
        ################################################################################################################
        parsing["Market"] = "US"
        parsing["MatchType"] = "N/A"
        parsing["KeywordType"] = "Route"
        parsing["MarketingNetwork"] = "Search"
        parsing["CampaignType"] = "Non-Brand"
        parsing["GeoTarget"] = parsing["Market"]
        ################################################################################################################
        # Conditionals
        ################################################################################################################
        # 'SP' is not a recognized language code. 'ES' is.
        language = parsing.get("Language").lower() if parsing.get("Language") else ""
        parsing["Language"] = language.replace("sp", "es")
        # Normalize fields
        parsing["Origin"] = volaris_normalize_city_name(parsing.get("Origin", ""))
        parsing["Destination"] = volaris_normalize_city_name(parsing.get("Destination"))

    def _volaris_old_non_brand_11(parsing: Dict[str, Optional[str]]) -> None:
        """
        Applies specific parsing logic to VolarisOldNonBrand11 matches.

        Case: 'Mobile / San Diego_US&&San Diego - Brand_US'

        Some adgroups have full route, but in an inconsistant format. (Ie., both 'GDL - San Diego_MX' and
            'GDL - San Diego_us' are SAN-GDL routes in the US (no clear difference between _us and _MX here).


        Adgroups in english have: {'Price', 'Brand', 'Ticket', 'Flight', 'Package', 'Attractions'} in adgroup name.
        Adgroups in spanish have: {'Precio', 'Marca', 'Boleto', 'Vuelo', 'Paquete', 'Atracciones'} in adgroup name.
        Only 'Brand' and 'Marca' are Hybrid, rest are Non-Brand.

        Only 'Atracciones'/ 'Attractions' are Generic.

        Both 'Mobile / San Diego_US' and 'San Diego_US' have a GDL route adgroup or two.

        Some have 'Mobile /' prefix, which can be safely be ignored.

        :param parsing:
        :return:
        """
        ################################################################################################################
        # Defaults for this match
        ################################################################################################################
        parsing["Market"] = "US"
        parsing["MatchType"] = "N/A"
        parsing["MarketingNetwork"] = "Search"
        # Just an enforcement of string type
        origin = parsing.get("Origin", "") if parsing.get("Origin") else ""
        ################################################################################################################
        # Conditionals
        ################################################################################################################
        # First: GDL in adgroup name?
        if "GDL" in parsing.get("AdGroupName", ""):
            # Then its a route campaign
            parsing["Destination"] = "GDL"
            parsing["KeywordType"] = "Route"
            parsing["CampaignType"] = "Non-Brand"
            if "_us" in parsing["AdGroupName"].lower():
                # _US = "English"
                parsing["Language"] = "en"
            elif "_mx" in parsing["AdGroupName"].lower():
                # _MX = "Spanish"
                parsing["Language"] = "es"
            parsing["Origin"] = volaris_normalize_city_name(origin.replace("San José", "SJC"))
        else:
            # No destination
            parsing["KeywordType"] = "Origin"
            ############################################################################################################
            # Adgroup name langauge determines the language of the adgroup
            ############################################################################################################
            english = {"price", "brand", "ticket", "flight", "package", "attractions"}
            spanish = {"precio", "marca", "boleto", "vuelo", "paquete", "atracciones"}
            group = parsing.get("AdGroupName", "").lower()
            group = group.lower().replace(origin.lower(), "").replace(" - ", "").replace("_us", "").strip()
            if group in english:
                parsing["Language"] = "en"
            elif group in spanish:
                parsing["Language"] = "es"
            else:
                assert False, str((parsing, group))
            ############################################################################################################
            # Campaign type
            ############################################################################################################
            if group in {"brand", "marca"}:
                parsing["CampaignType"] = "Hybrid Brand"
            else:
                parsing["CampaignType"] = "Non-Brand"
            if group in {"attractions", "atracciones"}:
                # The one case where origin becomes dest
                parsing["KeywordType"] = "Generic"
                parsing["KeywordGroup"] = "Attractions"
                # Add dest
                parsing["Destination"] = volaris_normalize_city_name(origin.replace("San José", "SJC"))
                # Remove origin
                parsing.pop("Origin")
            else:
                parsing["KeywordType"] = "Origin"
                parsing["Origin"] = volaris_normalize_city_name(origin.replace("San José", "SJC"))
        parsing["GeoTarget"] = parsing.get("Market")

    def _volaris_old_non_brand_12(parsing: Dict[str, Optional[str]]) -> None:
        """
        Applies specific parsing logic to VolarisOldNonBrand12 matches.

        Case: 'SanFrancisco-Guadalajara'

        :param parsing:
        :return:
        """
        ################################################################################################################
        # Pattern match defaults
        ################################################################################################################
        parsing["MatchType"] = "N/A"
        parsing["CampaignType"] = "Non-Brand"
        parsing["KeywordType"] = "Route"
        # We guarenteed Or/ Dest
        parsing["GeoTarget"] = "California"
        parsing["Origin"] = parsing["Origin"].replace("SanFrancisco", "San Francisco").replace("LosAngeles", "Los Angeles")
        parsing["Destination"] = volaris_normalize_city_name(parsing["Destination"])

    def _volaris_old_non_brand_13(parsing: Dict[str, Optional[str]]) -> None:
        """
        Applies specific parsing logic to VolarisOldNonBrand12 matches.

        Case: 'Los Angeles-Cancun-SP&&' and 'Los Angeles-Cancun-EN&&'

        :param parsing:
        :return:
        """
        ################################################################################################################
        # Defaults for match
        ################################################################################################################
        parsing["MatchType"] = "N/A"
        parsing["CampaignType"] = "Non-Brand"
        parsing["Market"] = "US"
        # Set these here; it is faster than looking them up in the airports_graph
        parsing["GeoTarget"] = "LAX"
        parsing["Destination"] = "CUN"
        parsing["Origin"] = "LAX"
        ################################################################################################################
        # Conditional assignments
        ################################################################################################################
        adgroup_name = parsing.get("AdGroupName", "")
        if not adgroup_name:
            pass
        elif "Spring Break" in adgroup_name:
            # Dest camp these 2 cases only
            parsing["Language"] = "en"
            parsing["KeywordType"] = "Destination"
            parsing["Origin"] = "N/A"
        elif "Carga Aerea" in adgroup_name:
            # Dest camp these 2 cases only
            parsing["KeywordType"] = "Destination"
            parsing["Origin"] = "N/A"
        elif "English" in adgroup_name:
            parsing["Language"] = "en"
            parsing["KeywordType"] = "Route"
        else:
            parsing["KeywordType"] = "Route"

    def _volaris_old_non_brand_14(parsing: Dict[str, Optional[str]]) -> None:
        """
        Applies specific parsing logic to VolarisOldNonBrand12 matches.

        Case: 'SanFrancisco-Guadalajara'

        :param parsing:
        :return:
        """
        parsing["MatchType"] = "N/A"
        parsing["CampaignType"] = "Non-Brand"
        parsing["RouteType"] = "Nonstop"
        if parsing.get("CampaignName") in ["CD Mexico", "Mexico - DF"]:
            # Synonyms, same idea for both. One generic adgroup in each, rest are destination keywords
            parsing["Destination"] = "MEX"
            if "Mexico - DF" in parsing.get("AdGroupName"):
                parsing["KeywordType"] = "Generic"
                parsing["KeywordGroup"] = "Destination"
            else:
                parsing["KeywordType"] = "Destination"
        elif parsing.get("CampaignName") in {"Pto Vallarta"}:
            # Shorthand for Puerto Vallarta. One generic adgroup, couple of routes, rest are destination
            if parsing.get("AdGroupName") == "Pto Vallarta":
                parsing["Destination"] = "PVR"
                parsing["KeywordType"] = "Generic"
                parsing["KeywordGroup"] = "Destination"
            elif "puerto vallarta" in parsing["AdGroupName"].lower():
                parsing["Origin"] = "PVR"
                parsing["KeywordType"] = "Route"
                parsing["Destination"] = volaris_normalize_city_name(
                    parsing.get("AdGroupName").replace("Puerto Vallarta", "").strip()
                )
            else:
                parsing["Destination"] = "PVR"
                parsing["KeywordType"] = "Destination"
        elif parsing.get("CampaignName") in {"Mexicali - Mèxico"}:
            # Mexicali is geotarget not origin
            parsing["GeoTarget"] = "MXL"
            parsing["Destination"] = "MEX"
            parsing["KeywordType"] = "Destination"
        elif parsing.get("CampaignName") == "Acapulco-Target Acapulco/Tijuana":
            # Simple route case
            parsing["Origin"] = "Acapulco"
            parsing["Destination"] = "Tijuana"
            parsing["KeywordType"] = "Route"
        elif "LAX" in parsing.get("CampaignName"):
            # Given Destination (LAX) in campaignname
            parsing["Origin"] = parsing["CampaignName"].replace("LAX", "").strip()
            parsing["Destination"] = "LAX"
            parsing["KeywordType"] = "Route"
        elif parsing.get("CampaignName") == "Mexicalli":
            # Special case, adgroup with same name is not generic, but is a destination campaign
            if parsing.get("CampaignName") == parsing.get("AdGroupName"):
                parsing["KeywordType"] = "Destination"
                parsing["Destination"] = "MXL"
            else:
                parsing["KeywordType"] = "Route"
                parsing["Origin"] = "MXL"
                if "guadalajara" in parsing.get("AdGroupName"):
                    parsing["Destination"] = "GDL"
                elif "toluca" in parsing.get("AdGroupName"):
                    parsing["Origin"] = "TLC"
        else:
            if parsing.get("CampaignName") == parsing.get("AdGroupName"):
                # Generic destination case
                parsing["KeywordType"] = "Generic"
                parsing["Destination"] = volaris_normalize_city_name(parsing["CampaignName"])
                parsing["KeywordGroup"] = "Destination"
            elif parsing.get("CampaignName").lower() in parsing.get("AdGroupName").lower():
                # Probably a route case
                loc = parsing.get("AdGroupName").lower().replace(parsing["CampaignName"].lower(), "").strip().title()
                if loc in CITY_NAMES.keys():
                    parsing["Destination"] = loc
                    parsing["Origin"] = volaris_normalize_city_name(parsing["CampaignName"])
                    parsing["KeywordType"] = "Route"
                elif parsing.get("AdGroupName") == "Acapulco USA":
                    # SPecific case
                    parsing["Destination"] = "OAK"
                    parsing["Origin"] = "ACA"
                    parsing["KeywordType"] = "Route"
                else:
                    # In case its not, it must be a destination
                    parsing["KeywordType"] = "Destination"
                    parsing["Destination"] = volaris_normalize_city_name(parsing["CampaignName"])
                    if parsing["CampaignName"] == "Los Cabos":
                        raise Exception(loc)
            else:
                parsing["KeywordType"] = "Destination"
                parsing["Destination"] = volaris_normalize_city_name(parsing["CampaignName"])
        if not parsing.get("GeoTarget"):
            parsing["GeoTarget"] = parsing.get("Market")

    def _volaris_old_brand_geo(parsing: Dict[str, Optional[str]]) -> None:
        """
        Applies specific decision logic for the parsing that is impractical to apply in pure regex. Corresponds to
        ParseRegexId 'VolarisOldBrandGeoTarget', which has been specifically isolated for this case. This is existing,
        pre-restructure format of Volaris' naming convention.

        Makes changes in-place to keep with the format of the logic of the module.

        :param parsing: Current state of parsing, fresh out of regex matching.
        :return:
        """
        ################################################################################################################
        # Isolate geo target and market.
        ################################################################################################################
        # If market has been set already, then we know which one GT
        market = parsing.get("Market") if parsing.get("Market") else ""
        if "GUA" in market:
            parsing["Market"] = "GT"
            parsing["GeoTarget"] = "GT"
        # If GeoTarget has been set, strip off the irrelevant characters.
        if parsing.get("GeoTarget"):
            # GeoTarget should now be full city names.
            geo_target = parsing["GeoTarget"].replace("(", "").replace(")", "").strip()
            # Only two known cases for this: Chicago and Los Angeles
            if geo_target.lower() == "chicago":
                geo_target = "ORD"
                parsing["Market"] = "US"
            elif geo_target.lower() == "los angeles":
                geo_target = "LAX"
                parsing["Market"] = "US"
            parsing["GeoTarget"] = geo_target
        # Set the MatchType to N/A - is indeterminate
        ################################################################################################################
        # Normalize campaign type, match type and keyword group/ type
        ################################################################################################################
        # MatchType is indeterminate from the adgroup level in this parsing case
        parsing["MatchType"] = "N/A"
        # Core VS Modifiers
        if parsing.get("KeywordGroup") in {"Volaris", "Brand"}:
            parsing["KeywordGroup"] = "Core"
            parsing["KeywordType"] = "Volaris"
        elif parsing.get("KeywordGroup") in {"Mispeling", "Mispelling"}:
            parsing["KeywordGroup"] = "Core"
            parsing["KeywordType"] = "Mispellings"
        else:
            parsing["KeywordGroup"] = "Modifiers"
        # Branding != Brand
        parsing["CampaignType"] = parsing.get("CampaignType", "").replace("Branding", "Brand")

    def _volaris_mexico_old_brand(parsing: Dict[str, Optional[str]]) -> None:
        """
        Helper method that applies the logic specific to the parseregexid value 'VolarisMexicoOldBrand'.

        Elaborates on information provided from regex, but with slightly more complex if/else logic trees, so the
        execution is performed in Python instead.

        :param parsing:
        :return:
        """
        # First, identify if the "Brand" is actually a Hybrid Brand
        cities = [
            "Tijuana",
            "Los Angeles",
            "México DF",
            "Cancun",
            "Aguascalientes",
            "Cancún",
            "Las Vegas"
        ]
        if "ingles" in parsing.get("KeywordGroup", "").lower() or "inglés" in parsing.get("KeywordGroup", "").lower():
            # Override account-level language
            parsing["Language"] = "en"
        for city in cities:
            # If any of the above cities are in the 'keyword group' then, that is a destination for hybrid brand
            # campaign.
            if city.lower() in parsing.get("KeywordGroup", "").lower():
                # Hybrid
                parsing["CampaignType"] = "Hybrid Brand"
                # Set destination
                parsing["Destination"] = city.replace("México DF", "Mexico City").replace("Cancún", "Cancun")
                # Set keyword type to destination
                parsing["KeywordType"] = "Destination"
                # Reset the keyword group.
                parsing["KeywordGroup"] = parsing["KeywordGroup"].replace(city, "").replace("-", "").strip()
                break
        else:
            keyword_group = parsing.get("KeywordGroup") if parsing.get("KeywordGroup") else ""
            if keyword_group in {"Volaris", "Brand", "Mispeling"}:
                parsing["KeywordGroup"] = "Core"
                parsing["KeywordType"] = "Volaris"
            elif "Vuelos" in keyword_group:
                parsing["KeywordType"] = "Flights"
                parsing["KeywordGroup"] = "Modifiers"
            elif "Boletos" in keyword_group:
                parsing["KeywordType"] = "Tickets"
                parsing["KeywordGroup"] = "Modifiers"
            else:
                parsing["KeywordGroup"] = "Modifiers"
        # Set the MatchType to N/A - is indeterminate
        parsing["MatchType"] = "N/A"

    def _volaris_old_brand_lang(parsing: Dict[str, Optional[str]]) -> None:
        """
        Helper method that applies the logic specific to the parseregexid value 'VolarisOldBrandLang'.

        Elaborates on information provided from regex, but with slightly more complex if/else logic trees, so the
        execution is performed in Python instead.

        :param parsing:
        :return:
        """
        core_adgroups = {
            "Volaris_US",
            "Volaris_US_ES",
            "Volaris_US_EN",
            "Volaris_US - volaris",
            "Volaris_US - volaris airlines"
        }
        # Standardize the campaign type. This regex id should only match brand campaigns.
        parsing["CampaignType"] = "Brand"
        keyword_group = parsing.get("KeywordGroup", "").strip() if parsing.get("KeywordGroup") else ""
        if keyword_group in core_adgroups:
            parsing["KeywordType"] = "Volaris"
            parsing["KeywordGroup"] = "Core"
        elif "Mispeling" in keyword_group:
            parsing["KeywordType"] = "Mispellings"
            parsing["KeywordGroup"] = "Core"
        else:
            parsing["KeywordGroup"] = "Modifiers"
        parsing["MatchType"] = "N/A"

    def _volaris_old_brand_ancillary(parsing: Dict[str, Optional[str]]) -> None:
        """
        Adds further parsing logic.

        :param parsing: Parsing out of regex
        :return:
        """
        ################################################################################################################
        # Match is Brand, Ancillary
        ################################################################################################################
        # Branding -> Brand
        parsing["CampaignType"] = "Brand"
        # These are remarketed ancillary campaigns
        if parsing.get("KeywordGroup") == "Compradores":
            parsing["KeywordGroup"] = "Ancillary"
        # Match type indeterminate
        parsing["MatchType"] = "N/A"
        # Remarketing to recent purchasers
        parsing["MarketingNetwork"] = "Search with Display select"
        # Indeterminate keyword type
        parsing["KeywordType"] = None

    def _volaris_old_brand_other(parsing: Dict[str, Optional[str]]) -> None:
        """
        Last-case logic to apply to the final brand campaign matches.

        :param parsing:
        :return:
        """
        ################################################################################################################
        # Default values that come from just matching here
        ################################################################################################################
        parsing["MatchType"] = "N/A"
        parsing["CampaignType"] = "Brand"
        parsing["KeywordType"] = "Core"
        parsing["GeoTarget"] = parsing.get("Market")

    def _volaris_old_display_2(parsing: Dict[str, Optional[str]]) -> None:
        """
        Fill in the gaps of information that are textually missing from the display campaigns' regex matching with what we
        know about the display campaigns.

        VolarisOldBrandDisplay2 refers to the 'Content Blast' type of nomenclature.

        :param parsing:
        :return:
        """
        parsing["MatchType"] = "N/A"
        ################################################################################################################
        # First things first, these are display, so assign the correct values.
        ################################################################################################################
        parsing["MarketingNetwork"] = "Display"
        ################################################################################################################
        # Sometimes they geo target outside of the market of the account
        ################################################################################################################
        if parsing.get("GeoTarget", "") == "Chicago":
            # Geo target to airport not to city
            parsing["GeoTarget"] = "ORD"
            # Override market.
            parsing["Market"] = "US"
        ################################################################################################################
        # Other inferences
        ################################################################################################################
        if parsing.get("CampaignType") == "B":
            # Case: 'D-B Blast 03.13 Mar 21-22'
            parsing["CampaignType"] = "Brand"
        elif not parsing.get("CampaignType"):
            # Assume non brand interest targeting
            parsing["CampaignType"] = "Non-Brand"

    def _volaris_old_display_3(parsing: Dict[str, Optional[str]]) -> None:
        """
        Case: 'Smart Display'

        :param parsing:
        :return:
        """
        parsing["MatchType"] = "N/A"
        parsing["Market"] = "MX" if not parsing.get("Market") else parsing.get("Market")
        parsing["Language"] = "es"
        parsing["MarketingNetwork"] = "Display"

    def _volaris_old_display_4(parsing: Dict[str, Optional[str]]) -> None:
        """
        Case: '2da Ola'

        :param parsing:
        :return:
        """
        parsing["MarketingNetwork"] = "Display"
        parsing["Market"] = "MX" if not parsing.get("Market") else parsing.get("Market")
        parsing["Language"] = "es" if not parsing.get("Language") else parsing.get("Language")
        parsing["MatchType"] = "N/A"

    def _volaris_old_display_5(parsing: Dict[str, Optional[str]]) -> None:
        """
        Case: No other display match pattern would work. In the regex, each case is explicitly listed out.

        Some of these cases have GeoTarget information embedded in the campaignname, so we much extract those, as well
        as assign the correct values for Market, MarketingNetwork, etc.

        :param parsing:
        :return:
        """
        ################################################################################################################
        # Prevent other accounts with similar generic campaignnames from using this regex match  type
        ################################################################################################################
        account = parsing.get("AccountName", "") if parsing.get("AccountName") else ""
        if "Volaris" not in account:
            # We must escape out of this kind of parsing
            return None
        ################################################################################################################
        # Old parsing defaults
        ################################################################################################################
        parsing["MatchType"] = "N/A"
        parsing["Language"] = "es"
        parsing["MarketingNetwork"] = "Display"
        ################################################################################################################
        # GeoTarget/ Market from Geo (if applicable)
        ################################################################################################################
        # All of the possible options from this limited matchings
        if parsing["CampaignName"][-3:].upper() in {"USA"}:
            # First, if the campaign ends with _USA or _MEX, then those are the geotargets/ markets.
            parsing["GeoTarget"] = "US"
            parsing["Market"] = "US"
            if "Guadalajara" in parsing["CampaignName"]:
                parsing["KeywordType"] = "Destination"
                parsing["Destination"] = "GDL"
                parsing["CampaignType"] = "NB"
        elif parsing["CampaignName"][-3:].upper() in {"MEX"}:
            # Same case, but in mexico
            parsing["GeoTarget"] = "MX"
            parsing["Market"] = "MX"
            if "Guadalajara" in parsing["CampaignName"]:
                parsing["KeywordType"] = "Destination"
                parsing["Destination"] = "GDL"
                parsing["CampaignType"] = "NB"
        else:
            # In any other case from this set, the location is the GeoTarget/ Market
            targets = {
                "California": "US",
                "Mexico": "MX",
                "Cancún": "MX",
                "Tijauana": "MX"
            }
            for key in targets:
                if key in parsing["CampaignName"]:
                    parsing["GeoTarget"] = key
                    parsing["Market"] = targets[key]

    def _volaris_old_display_6(parsing: Dict[str, Optional[str]]) -> None:
        """
        Case: No other display match pattern would work. In the regex, each case is explicitly listed out.

        These are all generic nb campaigns

        :param parsing:
        :return:
        """
        ################################################################################################################
        # Pattern match default values
        ################################################################################################################
        parsing["MatchType"] = "N/A"
        parsing["CampaignType"] = "Non-Brand"
        parsing["KeywordType"] = "Generic"
        parsing["MarketingNetwork"] = "Search with Display select" if "DSA" not in parsing.get("CampaignName") else "DSA"
        parsing["GeoTarget"] = parsing.get("Market")

    def _volaris_old_display_gsp(parsing: Dict[str, Optional[str]]) -> None:
        """
        Case: "GSP"
        :param parsing:
        :return:
        """
        ################################################################################################################
        # Old parsing defaults
        ################################################################################################################
        parsing["MatchType"] = "N/A"
        parsing["Language"] = "es"
        ################################################################################################################
        # Normalize/ assign marketing network as GSP
        ################################################################################################################
        network = parsing.get("MarketingNetwork", "GSP")
        if network.lower() == "gsp":
            network = "GSP"
        parsing["MarketingNetwork"] = network
        ################################################################################################################
        # Depending on which OR case the parsing took we have GeoTarget or GeoTarget1; KeywordType or KeywordType1
        ################################################################################################################
        if parsing.get("GeoTarget") or parsing.get("GeoTarget1"):
            geo = parsing.get("GeoTarget") if parsing.get("GeoTarget") else parsing.pop("GeoTarget1")
            target_countries = {
                "Costa Rica": "CR",
                "Costa_Rica": "CR",
                "Guatemala": "GT",
                "Texas": "US",
                "FLL": "US"
            }
            # Try to assign market from the given geo target, if possible.
            market = target_countries.get(geo)
            if market:
                # If the market is just the country, reset the geo target to be the country code for uniformity
                parsing["Market"] = market
            if geo in {"Costa Rica", "Costa_Rica", "Guatemala"}:
                geo = market
            # In case we had the GeoTarget1 instead of GeoTarget, or we have the country-only geo targeting
            parsing["GeoTarget"] = geo
        if parsing.get("KeywordType") or parsing.get("KeywordType1"):
            keyword_type = parsing.get("KeywordType") if parsing.get("KeywordType") else parsing.pop("KeywordType1")
            parsing["KeywordType"] = keyword_type

    def _volaris_old_video(parsing: Dict[str, Optional[str]]) -> None:
        """
        Applies specific logic to the VolarisOldVideo1 and VolarisOldVideo2 matches.

        In general, not much can be obtained from the matching, although there are some cases where we can gain simple
        information, like market.

        These campaigns all have 'Video' as their marketing network.

        :param parsing:
        :return:
        """
        parsing["MatchType"] = "N/A"
        parsing["MarketingNetwork"] = "Video"
        parsing["SearchEngine"] = "Google"
        if parsing.get("Market") == "Costa Rica":
            # When we can learn the market, which is the only thing that can be learned from name alone.
            parsing["Market"] = "CR"
            parsing["GeoTarget"] = "CR"
        elif "US to" in parsing["CampaignName"]:
            parsing["Market"] = "US"
            parsing["GeoTarget"] = "US"
        else:
            parsing["Market"] = "MX"

    def _volaris_old_nb_marketing_network(parsing:Dict[str, Optional[str]]) -> None:
        """
        This method takes the parsing, in the special case of the campaigns listed below, and marks them as having
        MarketingNetwork = 'Search with Display select'. In any other case, this method does nothing.

        :param parsing:
        :return:
        """
        camp = parsing.get("CampaignName", "")
        if camp in search_with_display_select_campaigns:
            parsing["MarketingNetwork"] = "Search with Display select"

    def _volaris_old_generic_1(parsing: Dict[str, Optional[str]]) -> None:
        """
        Applies specific contextual details to the Volaris_Max archetype of generic campaigns from the old naming
        convention.

        :param parsing:
        :return:
        """
        ################################################################################################################
        # Default values that come from just matching here
        ################################################################################################################
        parsing["MatchType"] = "N/A"
        parsing["Language"] = "es"
        ################################################################################################################
        # Campaign type is NB default unless the adgroup has Volaris in the adgroup's name
        ################################################################################################################
        parsing["CampaignType"] = "Non-Brand" if "volaris" not in parsing.get("AdGroupName", "").lower() else "Brand"
        ################################################################################################################
        # Identify Marketing
        ################################################################################################################
        if parsing.get("MarketingNetwork") == "Sur de CA":
            # Volaris_Max is SearchOnly, Volaris_Max_Sur de CA & other is Search with Display
            parsing["MarketingNetwork"] = "Search with Display select"
            parsing["Market"] = "US"
            parsing["GeoTarget"] = "California"
        elif parsing.get("MarketingNetwork") == "Sur de TX":
            parsing["Market"] = "US"
            parsing["GeoTarget"] = "Texas"
            parsing["MarketingNetwork"] = "Search"
        else:
            parsing["MarketingNetwork"] = "Search"
            parsing["Market"] = "MX"
        ################################################################################################################
        # Identify Locations
        ################################################################################################################
        # Route vs Dest vs Generic based on inconsistant adgroup name.
        context = parsing.get("AdGroupName").replace("Shuttle ", "")
        if context:
            # Case 1: Pure generic
            if "Sur de California" in context or context.lower() == "volaris":
                # 3 such adgroups, all generic terms
                parsing["KeywordType"] = "Generic"
            elif context.lower() == "df":
                # [D]istricto [F]ederal (Mexico City)
                parsing["KeywordType"] = "Destination"
                parsing["Destination"] = "MEX"
            elif context.lower() in {"english", "inglés"}:
                # Another generic, overwrites language
                parsing["Language"] = "en"
                parsing["KeywordType"] = "Generic"
            elif "volaris" in context.lower():
                # Semi-generic brand case
                parsing["KeywordType"] = "Modifiers"
                parsing["CampaignType"] = "Brand"
            elif context.lower() in {"tickets", "flights"}:
                parsing["KeywordType"] = "Generic"
            else:
                ########################################################################################################
                # Route/ destination case (Possibly exhaustive)
                ########################################################################################################
                parsing["CampaignType"] = "Non-Brand"
                # [{"airport": "", "index": int()},]
                airports = []
                for name in CITY_NAMES.keys():
                    # Iterate through the city names, check the context for substring, grab index of substring and
                    # airport code value
                    city = name.lower()
                    index = context.lower().find(city)
                    if index > -1:
                        # add the airport to the list
                        airports.append(
                            {
                                "city": name,
                                "index": index
                            }
                        )
                if not airports:
                    # False positive
                    parsing["KeywordType"] = "Generic"
                elif len(airports) == 1:
                    # Destination campaign case
                    parsing["KeywordType"] = "Destination"
                    parsing["Destination"] = airports[0]["city"]
                elif len(airports) == 2:
                    # Route campaign case
                    # Sort by index (first in the list is the origin)
                    airports = sorted(airports, key=lambda row: row["index"])
                    parsing["KeywordType"] = "Route"
                    parsing["Origin"] = airports[0]["city"]
                    parsing["Destination"] = airports[1]["city"]
                # Multiple cities case (error)
                else:
                    raise Exception(
                        "Too many airports",
                        (airports, parsing,)
                    )

        else:
            # Default to indeterminate
            parsing["MarketingNetwork"] = "N/A"

    def _volaris_old_generic_2(parsing: Dict[str, Optional[str]]) -> None:
        """
        Applies specific contextual details to those generic campaigns that are listed explicitly in regexes.py under
        ParseRegexId 'VolarisOldGeneric2'.

        :param parsing:
        :return:
        """
        ################################################################################################################
        # Default values that come from just matching here
        ################################################################################################################
        parsing["MatchType"] = "N/A"
        parsing["Language"] = "es"
        parsing["KeywordType"] = "Generic"
        parsing["MarketingNetwork"] = "Search with Display select"
        parsing["Market"] = "MX"
        parsing["CampaignType"] = "Non-Brand"
        ################################################################################################################
        # Special cases
        ################################################################################################################
        if parsing["CampaignName"] == "Volaris Chicago Hispanos":
            # Overwrite market to US, geolocation to ORD
            parsing["Market"] = "US"
            parsing["GeoTarget"] = "ORD"
        elif parsing["CampaignName"] == "Volaris Chicago Inglés":
            # Overwrite market to US, geolocation to ORD, language to en
            parsing["Market"] = "US"
            parsing["GeoTarget"] = "ORD"
            parsing["Language"] = 'en'

    def _volaris_old_generic_3(parsing: Dict[str, Optional[str]]) -> None:
        """
        Case: 'Genéricos_Futura&&Autobuses', or,
        'Genericas_Omnibus&&Venta de Boletos', or,
        'Genericas_Bus&&Boletos Bus'

        :param parsing:
        :return:
        """
        ################################################################################################################
        # Defaults
        ################################################################################################################
        parsing["CampaignType"] = "Non-Brand"
        parsing["KeywordType"] = "Generic"
        parsing["MarketingNetwork"] = "Search"
        parsing["MatchType"] = "N/A"

    def _volaris_old_generic_4(parsing: Dict[str, Optional[str]]) -> None:
        """
        Case:

        'M-G Genérico&&Genérico - Boleto'
        'E-Generic&&Generic_US'
        etc

        :return:
        """
        ################################################################################################################
        # Defaults
        ################################################################################################################
        parsing["CampaignType"] = "Non-Brand"
        parsing["KeywordType"] = "Generic"
        parsing["MarketingNetwork"] = "Search"
        parsing["MatchType"] = "N/A"
        ################################################################################################################
        # Conditionals
        ################################################################################################################
        parsing["Language"] = "en" if parsing.get("Market") == "US" else "es"

    def _volaris_old_generic_other(parsing: Dict[str, Optional[str]]) -> None:
        """
        Final case for old generic campaigns.

        Very inconsistant keywords, even within the adgroups. Very little can be determined, so they are matched
        explicitly in the regexes to have the appropriate values applied here.

        :param parsing:
        :return:
        """
        ################################################################################################################
        # Defaults for match
        ################################################################################################################
        parsing["MatchType"] = "N/A"
        parsing["CampaignType"] = "Non-Brand"
        parsing["KeywordType"] = "Generic"
        parsing["MarketingNetwork"] = "Search"
        ################################################################################################################
        # Conditionals
        ################################################################################################################
        # Many specifics are determined by  the adgroup, wherever possible. No consistant convention, so specific if
        # cases are used
        adgroup_name = parsing.get("AdGroupName", "")
        adgroup_name = adgroup_name if adgroup_name else ""
        if len(adgroup_name) >= 3 and adgroup_name[-3:] == "/LA":
            # Case: Zacatecas/LA
            # keywords in this adgroup are MOSTLY route keywords.
            parsing["KeywordType"] = "Route"
            parsing["Destination"] = "LAX"
            parsing["Origin"] = volaris_normalize_city_name(adgroup_name[:-3])
        if "Inglés" in parsing.get("CampaignName"):
            # Should be clear
            parsing["Language"] = "en"
            # Don't know why this is not in Volaris USA
            parsing["Market"] = "US"
        elif "Remarketing" in parsing.get("CampaignName"):
            parsing["MarketingNetwork"] = "RLSA"
        parsing["GeoTarget"] = parsing.get("Market")

    def _volaris_carga(parsing: Dict[str, Optional[str]]) -> None:
        """
        Applies the limited logic needed for VolarisCarga matches.

        :param parsing:
        :return:
        """
        # All cases are the same, so only defaults.
        parsing["MatchType"] = "N/A"
        parsing["CampaignType"] = "Non-Brand"
        parsing["KeywordType"] = "Generic"
        parsing["KeywordGroup"] = "Encargas"
        parsing["MarketingNetwork"] = "Search"

    def _volaris_vclub(parsing: Dict[str, Optional[str]]) -> None:
        """
        Applies the limited logic needed for VolarisVClub matches.

        :param parsing:
        :return:
        """
        # Only one case, so everything here is default
        parsing["MatchType"] = "N/A"
        parsing["CampaignType"] = "Brand"
        parsing["KeywordGroup"] = "Rewards"
        parsing["KeywordType"] = "Modifiers"
        parsing["MarketingNetwork"] = "Search"

    def _volaris_app_download(parsing: Dict[str, Optional[str]]) -> None:
        """
        7 Campaigns total fit this match.

        Mobile App (Search) <Device>
        Volaris Android App - Search - <One of: Branded, Competition Terms, Generic Terms>
        Volaris Android App - Universal Download

        :param parsing:
        :return:
        """
        ################################################################################################################
        # Defaults
        ################################################################################################################
        parsing["MatchType"] = "N/A"
        parsing["KeywordGroup"] = "App Download"
        parsing["GeoTarget"] = "MX"
        parsing["Market"] = "MX"
        parsing["Language"] = "es"
        ################################################################################################################
        # Conditionals
        ################################################################################################################
        # CampaignType
        if parsing.get("CampaignType"):
            # It is already set
            pass
        elif parsing.get("AdGroupName", "") == "Ad group #1":
            # Only present in two of the matched campaigns, always means brand
            parsing["CampaignType"] = "Brand"
        elif "Opti" in parsing.get("CampaignName", ""):
            parsing["CampaignType"] = "Brand"
        else:
            parsing["CampaignType"] = "Non-Brand"
        # Marketing network
        if "Universal" in parsing.get("CampaignName", ""):
            parsing["MarketingNetwork"] = "Universal App Download"
        else:
            parsing["MarketingNetwork"] = "Search"
        # KeywordType: Generic, Competitors, Modifiers
        keyword_type = parsing.get("KeywordType", "") if parsing.get("KeywordType", "") else ""
        if "Competition" in keyword_type:
            # Named in CampaignName
            parsing["KeywordType"] = "Competitors"
        elif "Generic" in keyword_type:
            # Named in CampaignName
            parsing["KeywordType"] = "Generic"
        elif parsing.get("CampaignType") == "Brand":
            # Example keyword: 'volaris app'
            parsing["KeywordType"] = "Modifiers"
        elif parsing.get("AdGroupName", "") == "San José (CR)":
            # Singular destination case
            parsing["KeywordType"] = "Destination"
            parsing["Destination"] = "SJO"
        elif parsing.get("Origin") and parsing.get("Destination"):
            # Route campaigns
            parsing["KeywordType"] = "Route"
            parsing["Origin"] = volaris_normalize_city_name(parsing["Origin"])
            parsing["Destination"] = volaris_normalize_city_name(parsing["Destination"])
        else:
            # Case: Mobile App (Search) Ipad&&...
            parsing["KeywordType"] = "Generic"

    def _volaris_old_competition(parsing: Dict[str, Optional[str]]) -> None:
        """
        Applies necesary logic to the lone competitors case from old volaris naming conventions.

        :param parsing:
        :return:
        """
        ################################################################################################################
        # Defaults
        ################################################################################################################
        parsing["MatchType"] = "N/A"
        parsing["CampaignType"] = "Non-Brand"
        parsing["KeywordType"] = "Generic"
        parsing["KeywordGroup"] = "Competitors"

    def _volaris_invex(parsing: Dict[str, Optional[str]]) -> None:
        """
        Applies necesary logic to the single invex case from old volaris naming conventions.

        Volaris - Invex is a campaign which advertises on generic terms and whose desired conversion is not a ticket
        but rather is an application to the airline's travel rewards credit card.

        :param parsing:
        :return:
        """
        ################################################################################################################
        # Defaults
        ################################################################################################################
        parsing["MatchType"] = "N/A"
        parsing["KeywordType"] = "Generic"
        parsing["CampaignType"] = "Non-Brand"
        parsing["KeywordGroup"] = "Credit Card Application"
        parsing["MarketingNetwork"] = "Search"
        parsing["GeoTarget"] = parsing.get("Market", "")

    def _volaris_old_vacations(parsing: Dict[str, Optional[str]]) -> None:
        """
        Non-exhaustive match of vacation package-related campaigns.

        :param parsing:
        :return:
        """
        ################################################################################################################
        # Defaults
        ################################################################################################################
        parsing["MatchType"] = "N/A"
        parsing["KeywordGroup"] = "Vacations"
        parsing["GeoTarget"] = parsing.get("Market")
        ################################################################################################################
        # Conditionals
        ################################################################################################################
        adgroup_name = parsing.get("AdGroupName", "")
        if adgroup_name == "Brand":
            # Brand Case
            parsing["CampaignType"] = parsing["AdGroupName"]
            parsing["KeywordType"] = "Modifiers"
        elif adgroup_name == "General":
            # Generic keywords
            parsing["CampaignType"] = "Non-Brand"
            parsing["KeywordType"] = "Generic"
        elif "cancún" in adgroup_name.lower() or "cancun" in adgroup_name.lower():
            parsing["CampaignType"] = "Non-Brand"
            parsing["Destination"] = "CUN"
            parsing["KeywordType"] = "Destination"
        elif "los cabos" in adgroup_name.lower():
            parsing["CampaignType"] = "Non-Brand"
            parsing["Destination"] = "SJT"
            parsing["KeywordType"] = "Destination"
        elif "playa del carmen" in adgroup_name.lower():
            parsing["CampaignType"] = "Non-Brand"
            parsing["KeywordType"] = "Destination"
            parsing["Destination"] = "CUN"
        elif "puerto vallarta" in adgroup_name.lower():
            parsing["CampaignType"] = "Non-Brand"
            parsing["KeywordType"] = "Destination"
            parsing["Destination"] = "PVR"
        elif "acapulco" in adgroup_name.lower():
            parsing["CampaignType"] = "Non-Brand"
            parsing["KeywordType"] = "Destination"
            parsing["Destination"] = "ACA"
        else:
            parsing["CampaignType"] = "Non-Brand"
            parsing["KeywordType"] = "Generic"

    def _volaris_old_dsa(parsing: Dict[str, Optional[str]]) -> None:
        """
        Isolates and parses through the old DSA campaign match cases. Only 2 Campaigns match here.

        Case: Dynamic&&Cancun
        Case: Dynamic Search Ads&&

        All ad groups that can be applied here are each destinations.

        :param parsing:
        :return:
        """
        ################################################################################################################
        # Defaults
        ################################################################################################################
        parsing["MatchType"] = "N/A"
        parsing["GeoTarget"] = parsing.get("Market")
        parsing["MarketingNetwork"] = "DSA"
        parsing["CampaignType"] = "Non-Brand"

        ################################################################################################################
        # Conditionals
        ################################################################################################################
        # If we are given an adgroup
        if parsing.get("Destination"):
            # Normalize the destination
            parsing["Destination"] = volaris_normalize_city_name(
                parsing["Destination"].replace("Mexico", "Mexico City")
            )
            parsing["KeywordType"] = "Destination"

    def _old_parsing(parsing: Dict[str, Optional[str]]) -> None:
        """
        Isolates the old parsing matches and applies the specific logic that is required for each.

        :param parsing:
        :return:
        """
        regex_id = parsing.get("ParseRegexId")
        if "EveryMundo" in parsing.get("ParseRegexId", ""):
            # Is not an "old" pattern, so we do not need to apply the old_parsing logics.
            return None
        elif regex_id in {"VolarisOldNonBrand1", "VolarisOldNonBrand2", "VolarisOldNonBrand1-CampaignOnly",
                        "VolarisOldNonBrand2-CampaignOnly"}:
            _volaris_old_non_brand_1_and_2(parsing)
        elif regex_id in {"VolarisOldNonBrand3", "VolarisOldNonBrand3-CampaignOnly"}:
            _volaris_old_non_brand_3(parsing)
        elif regex_id in {"VolarisOldNonBrand4", "VolarisOldNonBrand4-CampaignOnly"}:
            _volaris_old_non_brand_4(parsing)
        elif regex_id in {"VolarisOldNonBrand5", "VolarisOldNonBrand5-CampaignOnly"}:
            _volaris_old_non_brand_5(parsing)
        elif regex_id in {"VolarisOldNonBrand6", "VolarisOldNonBrand6-CampaignOnly"}:
            _volaris_old_non_brand_6(parsing)
        elif regex_id in {"VolarisOldNonBrand7", "VolarisOldNonBrand7-CampaignOnly"}:
            _volaris_old_non_brand_7(parsing)
        elif regex_id in {"VolarisOldNonBrand8", "VolarisOldNonBrand8-CampaignOnly"}:
            _volaris_old_non_brand_8(parsing)
        elif regex_id in {"VolarisOldNonBrand9", "VolarisOldNonBrand9-CampaignOnly"}:
            _volaris_old_non_brand_9(parsing)
        elif regex_id in {"VolarisOldNonBrand10", "VolarisOldNonBrand10-CampaignOnly"}:
            _volaris_old_non_brand_10(parsing)
        elif regex_id in {"VolarisOldNonBrand11", "VolarisOldNonBrand11-CampaignOnly"}:
            _volaris_old_non_brand_11(parsing)
        elif regex_id in {"VolarisOldNonBrand12", "VolarisOldNonBrand12-CampaignOnly"}:
            _volaris_old_non_brand_12(parsing)
        elif regex_id in {"VolarisOldNonBrand13", "VolarisOldNonBrand13-CampaignOnly"}:
            _volaris_old_non_brand_13(parsing)
        elif regex_id in {"VolarisOldNonBrand14", "VolarisOldNonBrand14-CampaignOnly"}:
            _volaris_old_non_brand_14(parsing)
        elif regex_id in {"VolarisMexicoOldBrand", "VolarisMexicoOldBrand-CampaignOnly"}:
            _volaris_mexico_old_brand(parsing)
        elif regex_id in {"VolarisOldBrandLang", "VolarisOldBrandLang-CampaignOnly"}:
            _volaris_old_brand_lang(parsing)
        elif regex_id in {"VolarisOldBrandGeoTarget", "VolarisOldBrandGeoTarget-CampaignOnly"}:
            _volaris_old_brand_geo(parsing)
        elif regex_id in {"VolarisOldBrandAncillary", "VolarisOldBrandAncillary-CampaignOnly"}:
            _volaris_old_brand_ancillary(parsing)
        elif regex_id in {"VolarisOldBrandOther", "VolarisOldBrandOther-CampaignOnly"}:
            _volaris_old_brand_other(parsing)
        elif regex_id in {"VolarisOldDisplay2", "VolarisOldDisplay2-CampaignOnly"}:
            _volaris_old_display_2(parsing)
        elif regex_id in {"VolarisOldDisplay3", "VolarisOldDisplay3-CampaignOnly"}:
            _volaris_old_display_3(parsing)
        elif regex_id in {"VolarisOldDisplay4", "VolarisOldDisplay4-CampaignOnly"}:
            _volaris_old_display_4(parsing)
        elif regex_id in {"VolarisOldDisplay5", "VolarisOldDisplay5-CampaignOnly"}:
            _volaris_old_display_5(parsing)
        elif regex_id in {"VolarisOldDisplay6", "VolarisOldDisplay6-CampaignOnly"}:
            _volaris_old_display_6(parsing)
        elif regex_id in {"VolarisOldVideo1", "VolarisOldVideo2", "VolarisOldVideo1-CampaignOnly",
                          "VolarisOldVideo2-CampaignOnly"}:
            _volaris_old_video(parsing)
        elif regex_id in {"VolarisOldGeneric1", "VolarisOldGeneric1-CampaignOnly"}:
            _volaris_old_generic_1(parsing)
        elif regex_id in {"VolarisOldGeneric2", "VolarisOldGeneric2-CampaignOnly"}:
            _volaris_old_generic_2(parsing)
        elif regex_id in {"VolarisOldGeneric3", "VolarisOldGeneric3-CampaignOnly"}:
            _volaris_old_generic_3(parsing)
        elif regex_id in {"VolarisOldGeneric4", "VolarisOldGeneric4-CampaignOnly"}:
            _volaris_old_generic_4(parsing)
        elif regex_id in {"VolarisOldDisplayGSP", "VolarisOldDisplayGSP-CampaignOnly"}:
            _volaris_old_display_gsp(parsing)
        elif regex_id in {"VolarisOldGenericOther", "VolarisOldGenericOther-CampaignOnly"}:
            _volaris_old_generic_other(parsing)
        elif regex_id in {"VolarisCarga", "VolarisCarga-CampaignOnly"}:
            _volaris_carga(parsing)
        elif regex_id in {"VolarisVClub", "VolarisVClub-CampaignOnly"}:
            _volaris_vclub(parsing)
        elif regex_id in {"VolarisOldCompetitors", "VolarisOldCompetitors-CampaignOnly"}:
            _volaris_old_competition(parsing)
        elif regex_id in {"VolarisAppDownload", "VolarisAppDownload-CampaignOnly"}:
            _volaris_app_download(parsing)
        elif regex_id in {"VolarisInvex", "VolarisInvex-CampaignOnly"}:
            _volaris_invex(parsing)
        elif regex_id in {"VolarisOldVacations", "VolarisOldVacations-CampaignOnly"}:
            _volaris_old_vacations(parsing)
        elif regex_id in {"VolarisOldDSA", "VolarisOldDSA-CampaignOnly"}:
            _volaris_old_dsa(parsing)

    def _account_name_resolution(parsing) -> None:
        """
        Resolves information from the account name (if possible)
        :param parsing:
        :return:
        """
        account_name = parsing.get("AccountName")
        if account_name == "Volaris Mexico":
            parsing["Market"] = "MX" if not parsing.get("Market") else parsing["Market"]
            parsing["Language"] = "es"
        elif account_name == "Volaris Puerto Rico":
            parsing["Language"] = "es"
            parsing["Market"] = "PR" if not parsing.get("Market") else parsing["Market"]
        elif account_name == "Volaris USA":
            parsing["Market"] = "US" if not parsing.get("Market") else parsing["Market"]
        elif account_name == "Volaris":
            parsing["Market"] = "MX" if not parsing.get("Market") else parsing["Market"]
            parsing["Language"] = "es" if not parsing.get("Language") else parsing["Language"]
        elif account_name == "Volaris Costa Rica":
            # Be careful here, there are GT marketed and geo-targeted campaigns (BR and NB) in this account!
            # Ignore market if we already have it.
            if not parsing.get("Market"):
                parsing["Market"] = "CR"
            parsing["Language"] = "es"
        elif account_name == "Volaris Guatemala":
            parsing["Market"] = "GT" if not parsing.get("Market") else parsing["Market"]
            parsing["Language"] = "es"
        elif account_name == "Volaris Content Blast":
            # Campaigns override market here.
            parsing["Market"] = "MX" if not parsing.get("Market") else parsing["Market"]
            parsing["Language"] = "es"
        elif account_name == "Bus Switching":
            # All bus switching are MX-es
            parsing["Market"] = "MX"
            parsing["Language"] = "es"
            parsing["KeywordType"] = "Generic"
        elif account_name == "Volaris Carga":
            # MX-es
            parsing["Market"] = "MX"
            parsing["Language"] = "es"
        elif account_name == "VClub Volaris":
            # Rewards program Brand Modifiers
            parsing["Market"] = "MX"
            parsing["Language"] = "es"
        elif account_name in {"Aplicación Volaris", "Aplicacion Volaris"}:
            # Keep the accent-less version JIC, but normalize too.
            parsing["Market"] = "MX"
            parsing["Language"] = "es"
            parsing["AccountName"] = "Aplicación Volaris"
        elif account_name == "Promotions Volaris":
            parsing["Market"] = "MX"
            parsing["Language"] = "es"
        elif account_name == "Volaris - Invex":
            parsing["Market"] = "MX"
            parsing["Language"] = "es"

    ####################################################################################################################
    # Account name resolution
    ####################################################################################################################
    _account_name_resolution(parsing)
    ####################################################################################################################
    # Old structure corrections.
    ####################################################################################################################
    _old_parsing(parsing)


def volaris_normalize_city_name(city: str) -> Optional[str]:
    """
    For the given raw city name, this method returns a normalized version, as best possible.

    This method is defined outside of volaris_parse_logic to test against known outliers.

    :param city:
    :return:
    """
    ####################################################################################################################
    # Prevent Null case errors
    ####################################################################################################################
    if not city:
        return None
    ####################################################################################################################
    # Remove ambiguities from the name.
    ####################################################################################################################
    # Work through using all lower-case city names, then return normalize.title()
    normalized = city.lower().strip()
    # Distinguish between SJO  and SJC here. SJO has the accent (no other distinguishing features)
    normalized = "SJO" if "san josé" in normalized else normalized
    normalized = "SJC" if "san jose" in normalized else normalized
    # Remove accented characters
    normalized = normalized.replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")
    # Normalize the output format here (skips formatting steps later for efficiency)
    normalized = normalized.replace("mexico df", "MEX")
    normalized = normalized.replace("chicago o'hare", "ORD")
    normalized = normalized.replace("cihcago", "ORD")
    normalized = normalized.replace("chicago midway", "MDW")
    normalized = normalized.replace("san francisco oakland", "OAK")
    normalized = normalized.replace("mexicalli", "MXL").replace("Mexicalli", "MXL")
    normalized = "SJO" if "costa rica" in normalized else normalized
    normalized = "DGO" if "durango" in normalized else normalized
    normalized = "SAL" if "el salvador" in normalized else normalized
    normalized = "TGZ" if "tuxtla" in normalized else normalized
    normalized = "IAH" if "texas" in normalized else normalized
    normalized = "PDX" if "portland" in normalized else normalized
    normalized = "CUN" if "quintana" in normalized else normalized
    normalized = "MDW" if "illinois" in normalized else normalized
    normalized = "MEX" if normalized == "df" else normalized
    normalized = "TLC" if "toluca" in normalized else normalized
    # Case: NoSpaces
    normalized = normalized.replace("losangeles", "los angeles")
    ####################################################################################################################
    # For entries that struggle in the airport_codes JSON
    ####################################################################################################################
    if "chicago" in normalized:
        normalized = "ORD"
    elif "puerto rico" in normalized:
        normalized = "SJU"
    elif "vallarta" in normalized:
        normalized = "PVR"
    ####################################################################################################################
    # Re-upper case the city names (if it isn't already an IATA code)
    ####################################################################################################################
    if len(normalized) > 3:
        normalized = normalized.title()
        normalized.replace(" De ", " de ")
    else:
        normalized = normalized.upper()
    return normalized


def hong_kong_express_parse_logic(parsing: Dict[str, Optional[str]]) -> None:
    """
    In style and form of the other methods above, this alters the dictionary in-place.

    Applies UO-specific parsing logic to the parsing row.

    :param parsing: Parsing, right out of regex parsing logic, before scrubbing.
    :return:
    """
    if parsing.get("ParseRegexId") == "UODictionary":
        adgroup = parsing.get("AdGroupName").lower() if parsing.get("AdGroupName") not in {None, "None", "N/A", ""} else ""
        if "exact" in adgroup:
            parsing["MatchType"] = "EX"
        elif "phrase" in adgroup:
            parsing["MatchType"] = "PH"
        elif "broad" in adgroup:
            parsing["MatchType"] = "BM"
    elif parsing.get("ParseRegexId") == "BaiduAbbreviated":
        parsing["Market"] = "CN"
        parsing["Language"] = "zh"
        if not parsing.get("GeoTarget"):
            parsing["GeoTarget"] = "CN"
        if "{" in parsing["Origin"]:
            parsing["Origin"] = parsing["Origin"].replace("{", "").replace("}", "")
