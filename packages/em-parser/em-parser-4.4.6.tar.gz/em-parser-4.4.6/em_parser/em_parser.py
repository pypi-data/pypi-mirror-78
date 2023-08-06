"""
Main logic module.

Other modules serve as helpers to this module.

Methods and classes used here should be made importable from the package level (ie., as new methods are defined, add to
.__init__.py __all__ attribute, as appropriate).
"""
import os
import json
import re
import time
from typing import Dict, Optional, Tuple, Union
from urllib.parse import unquote_plus

from em_parser.airline_logic import (aegean_parse_logic, air_berlin_parse_logic, copa_parse_logic,
                                     interjet_parse_logic, jet_airways_logic, volaris_parse_logic,
                                     hong_kong_express_parse_logic)
from em_parser.oldcopanames import OLD_COPA
from em_parser.olduonames import OLD_UO_GOOGLE, OLD_UO_YAHOO, OLD_UO_BING, OLD_UO_BAIDU, OLD_UO_NAVER
from em_parser.regexes import REGEXES, CAMP_REGEXES
from em_parser.clean_functions import scrub_parsing, update_origin_destination


# Parsing type
Parsing = Dict[str, Optional[str]]

# Parser version
with open(os.path.dirname(os.path.abspath(__file__)) + '/version.txt', 'r') as file:
    __version__ = file.readline().strip()
parser_version = __version__


class Parser(object):
    """
    Parsing class.

    This class should be explicitly declared when many parsings are expected to be performed for performance and
    execution run time.

    The upsert is a reference dictionary for either very difficult or impossible to parse entries with their expected
    output.

    The _cache
    """
    with open(os.path.dirname(os.path.abspath(__file__)) + '/upsert.json', 'r', encoding='UTF8', newline="\n") as jfile:
        upsert = json.load(jfile)
    airline_codes = {
        'Interjet': '4O',
        'Aegean Airlines': 'A3',
        'Olympic Air': 'OA',
        'Jet Airways': '9W',
        'Copa Airlines': 'CM',
        'airberlin': 'AB',
        'Volaris': 'Y4',
        'Hong Kong Express': 'UO',
        'Aeromexico': "AM",
        'Cape Air': '9K',
        'United Airlines': 'UA',
        'Xiamen': 'MF',
        'EVA': 'BR',
        'Ernest': 'EG'
    }

    def __init__(self, cached: bool=True):
        """
        Class instantiation. Currently, nothing happens on instantiation.

        :param cached: (Default True) if True, then use the cached data for performance optimized parsings. This will
            also allow the execution of "new" campaigns/ adgroups to be placed into the reference file.
        """
        # self.cached = cached
        self.cached = cached
        self.cache = self.load_cache() if cached else {}

    def load_cache(self) -> Dict[Tuple[str, Optional[str]], Parsing]:
        """
        Loads and returns cache from file.

        :return:
        """
        with open(os.path.dirname(os.path.abspath(__file__)) + '/cache.json', 'r', encoding='UTF8', newline="\n") as fl:
            return json.load(fl)

    def dump_cache(self) -> None:
        """
        Dumps cache to file OVERWRITING existing data.

        :param cache:
        :return:
        """
        try:
            with open(os.path.dirname(os.path.abspath(__file__)) + '/cache.json', 'w', encoding='UTF8', newline="\n") as fl:
                return json.dump(self.cache, fl)
        except Exception:
            try:
                time.sleep(0.01)
                with open(os.path.dirname(os.path.abspath(__file__)) + '/cache.json', 'w', encoding='UTF8', newline="\n") as fl:
                    return json.dump(self.cache, fl)
            except Exception as error:
                raise error

    def load_upsert(self):
        """
        This method returns the upsert shelf used to store cached parsings on disk.
        :return:
        """
        filepath = os.path.dirname(os.path.abspath(__file__)) + '/upsert.json'
        with open(filepath, 'r', encoding='UTF8', newline="\n") as jfile:
            return json.load(jfile)

    def dump_upsert(self):
        """
        This method dumps the current state of the upsert shelf to disk.

        :return:
        """
        filepath = os.path.dirname(os.path.abspath(__file__)) + '/upsert.json'
        with open(filepath, 'w', encoding='UTF8', newline="\n") as jfile:
            return json.dump(self.upsert, jfile)

    def parse(self, campaign_name: str='', adgroup_name: str='', account_name: str=None, airline_name: str=None,
              airline_code: str=None, search_engine: str=None, return_names: bool=False,
              na: bool=False, **kwargs) -> Parsing:
        """
        Main parsing method.

        Returns a dictionary representation of the parsing. Expected keys should include:

        :param campaign_name: Campaign name (required)
        :param adgroup_name: Ad group name (recommended for best accuracy)
        :param airline_name: Either airline_name or airline_code recommended
        :param airline_code: Either airline_name or airline_code recommended
        :param search_engine: Search engine name (ie., Google)
        :param return_names: If true, returns the CampaignName and AdGroupName fields in the parsing. (Default True)
        :param na: If True, returns fields that are indeterminate or Null as the string 'N/A'. (Default False)
        :return:
        """
        # Scrub input
        if airline_code:
            airline_code = airline_code.upper()
        # If using cached values:
        if self.cached:
            to_parse = "{A}&&{s}&&{c}&&{a}".format(
                A=airline_code,
                s=search_engine,
                c=campaign_name,
                a=adgroup_name
            )
            if self.get_from_cache(to_parse) is None:
                try:
                    parsed = self._item_parser(
                        campaign_name=campaign_name,
                        adgroup_name=adgroup_name,
                        airline_name=airline_name,
                        airline_code=airline_code,
                        account_name=account_name,
                        search_engine=search_engine,
                        return_names=True,
                        na=True
                    )
                    parsed = self._na_return_names_logic(parsed, na=na, return_names=return_names)
                except Exception as error:
                    raise Exception(
                        "Error parsing",
                        {
                            "campaign_name": campaign_name,
                            "adgroup_name": adgroup_name,
                            "airline_name": airline_name,
                            "airline_code": airline_code,
                            "account_name": account_name,
                            "search_engine": search_engine,
                            "return_names": return_names,
                            "na": na
                        }
                    ) from error
                if parsed.get("ParseRegexId"):
                    return parsed
                else:
                    # self.add_to_cache(to_parse, parsed)
                    return parsed
            else:
                return self.get_from_cache(to_parse)

        else:
            try:
                return self._item_parser(
                    campaign_name=campaign_name,
                    adgroup_name=adgroup_name,
                    airline_name=airline_name,
                    airline_code=airline_code,
                    account_name=account_name,
                    search_engine=search_engine,
                    return_names=return_names,
                    na=na
                )
            except Exception as error:
                raise Exception(
                    "Error parsing",
                    {
                        "campaign_name": campaign_name,
                        "adgroup_name": adgroup_name,
                        "airline_name": airline_name,
                        "airline_code": airline_code,
                        "account_name": account_name,
                        "search_engine": search_engine,
                        "return_names": return_names,
                        "na": na
                    }
                ) from error

    def add_to_cache(self, key: str, value: Parsing, on_file: bool=True) -> None:
        """
        Adds the given key, value pair to the cache, in memory, and in file, if selected.

        :param key: Tuple in the form of (campaign_name, adgroup_name,)
        :param value: Parsing (completed) to add to cache
        :param on_file: (Default True) also update the file
        :return:
        """
        self.cache[key] = value
        if on_file:
            self.dump_cache()

    def get_from_cache(self, key: str) -> Optional[Parsing]:
        """
        Attempts to retrieve an entry from the given key. If not possible, then returns

        :param key:
        :return:
        """
        return self.cache.get(key)

    def _item_parser(self, campaign_name: str=None, adgroup_name: str=None, airline_name: str=None,
                     airline_code: str=None, account_name: str=None, search_engine: str=None, return_names: bool=False,
                     na: bool=False) -> Parsing:
        """
        Primary parsing unit. For the given units of campaign_name, adgroup_name, and airline_name/ airline_code, returns
        the parsing dictionary, returning as many values as possible from the available data.

        :param campaign_name: Campaign name to parse through
        :param adgroup_name: Adgroup name to parse through
        :param airline_name: Airline name to identify patterns. Should be added for any 'old pattern' accounts.
        :param airline_code: Airline code to identify airline patterns. Should always be added for any 'old pattern'
            accounts.
        :param account_name: Name of the account. (Optional)
        :param search_engine: Search engine of SEM campaign/ adgroup
        :param return_names: If true, returns campaign and adgroup names as well. Defaults to True.
        :param na: Set to True, if "N/A" is to be returned for empty or indeterminate fields. Defaults to False.
        :return:
        """
        ################################################################################################################
        # Instantiate some prelimanary values
        ################################################################################################################
        # Source string
        raw_camp_adg = "{c}&&{a}".format(c=campaign_name, a=adgroup_name)
        # Instantiated return value.
        if airline_code == "AM" and "GS:" in campaign_name and "GS:" not in str(adgroup_name):
            parsing = {
                'ParserVersion': parser_version,
                'AirlineName': airline_name,
                'AirlineCode': airline_code,
                "CampaignName": campaign_name,
                "AdGroupName": None,
                "AccountName": account_name,
                "SearchEngine": search_engine
            }
        else:
            parsing = {
                'ParserVersion': parser_version,
                'AirlineName': airline_name,
                'AirlineCode': airline_code,
                "CampaignName": campaign_name,
                "AdGroupName": adgroup_name,
                "AccountName": account_name,
                "SearchEngine": search_engine
            }
        ################################################################################################################
        # Begin parsing of the campaign name, etc
        ################################################################################################################
        # Ensure airline name and airline code is in output
        parsing = self._ensure_airline_name(
            parsing,
            airline_name=airline_name,
            airline_code=airline_code,
            account_name=account_name
        )
        # Special campaign string (ie., experiment campaign name suffix, '[EXP]', etc)
        parsing = self._special_campaign_suffix(parsing, campaign_name=campaign_name)
        special_prefix = parsing.get("SpecialCampaign", "")
        ################################################################################################################
        # Apply given  values to regex logic tree
        ################################################################################################################
        campaign_name = campaign_name if campaign_name else parsing.get("CampaignName", "")
        if airline_code == "AM" and "GS:" in campaign_name and "GS:" not in str(adgroup_name):
            matching = self._find_regex_match(
                parsing,
                campaign_name=campaign_name,
                adgroup_name=None
            )
        else:
            matching = self._find_regex_match(
                parsing,
                campaign_name=campaign_name,
                adgroup_name=adgroup_name
            )
        # Parsing to be updated with the match
        match = matching["match"]  # type: re.match
        # Match key (which pattern did it match to?
        id_key = matching["id_key"]
        # Campaign name (normalized if the url encoding damaged the original structure)
        campaign_name = matching["campaign_name"]
        ################################################################################################################
        # If a match was found, use the regex group naming defined in the regexes.py module to update the parsing
        ################################################################################################################
        if match is not None and not isinstance(match, dict) and not isinstance(match, str):
            match_dict = match.groupdict()
        else:
            match_dict = match
        if match_dict is not None:
            parsing.update(match_dict)
            # Re-attach the special part back to the front of the campaign after parsing has completed
            parsing.update({'ParseRegexId': id_key})
            parsing["AdGroupName"] = adgroup_name
        # Assign this local variable here, just in case.
        airline = parsing.get('AirlineName') if parsing.get('AirlineName') else ''
        ################################################################################################################
        # Now that we have airline isolated, apply airline-specific logic.
        ################################################################################################################
        parsing = self._apply_airline_logic(
            parsing,
            airline_name=airline,
            airline_code=airline_code,
            raw_camp_adg=raw_camp_adg
        )
        ################################################################################################################
        # Scrub the parsing for uniformity.
        ################################################################################################################
        parsing = scrub_parsing(parsing)
        parsing = self._final_scrub_through(parsing, search_engine=search_engine)
        parsing = update_origin_destination(parsing)
        parsing["CampaignName"] = special_prefix + campaign_name if special_prefix else campaign_name
        ################################################################################################################
        # Return complete parsing.
        ################################################################################################################
        try:
            parsing = self._na_return_names_logic(parsing, na=na, return_names=return_names)
        except Exception as error:
            raise Exception("No parsing", parsing) from error
        return parsing

    def _na_return_names_logic(self, parsing: Parsing, na: bool=True, return_names: bool=True) -> Parsing:
        """
        Applies 'na' (as in 'N/A' values) parameter logic and return_names parameter logic.

        Final formatting.

        :return:
        """
        if parsing is None:
            raise Exception("No parsing", parsing)
        # Remove whitespace, replace null values with 'N/A' (by default)
        final_parsing = {
            key: item.strip()
            if item else ""
            for key, item in parsing.items()
        }
        return_fields = {
            'SpecialCampaign',
            'AccountName',
            'AdGroupName',
            'AirlineCode',
            'AirlineName',
            'CampaignName',
            'CampaignType',
            'Audience',
            'KeywordGroup',
            'RouteLocale',
            'SearchEngine',
            'Destination',
            'Origin',
            'MatchType',
            'Language',
            'RouteType',
            'Market',
            'MarketingNetwork',
            'Network',
            'LocationType',
            'GeoTarget',
            'KeywordType',
        }
        if na:
            for field in return_fields:
                value = final_parsing.get(field)
                if not value:
                    final_parsing[field] = 'N/A'
        # Otherwise, it'll pop off the Nones
        else:
            keys_to_pop = [] if return_names else ["CampaignName", "AdGroupName", "AccountName"]
            for key, value in final_parsing.items():
                if not value or value == 'N/A':
                    keys_to_pop.append(key)
            for key in keys_to_pop:
                if key in final_parsing.keys():
                    final_parsing.pop(key)
        return final_parsing

    def _final_scrub_through(self, raw_parsing: Parsing, search_engine: str=None) -> Parsing:
        """
        A series of miscellaneous parsing methods that depend on the basic parsing to have completed. Some are final
        sieves of correction; others assign values based on implicit business logic (ie.,
        Modifiers |-> CampaignType=Brand).

        An updated parsing dictionary is returned. (Does NOT occur in-place).

        :param raw_parsing:
        :param search_engine:
        :return:
        """
        ################################################################################################################
        # Instantiate output
        ################################################################################################################
        parsing = {**raw_parsing}
        ################################################################################################################
        # Assign values that exist, but haven't been input in into the output dictionary
        ################################################################################################################
        if search_engine is not None:
            parsing['SearchEngine'] = search_engine
        if parsing['AirlineCode'] is None:
            parsing['AirlineCode'] = self.airline_codes.get(parsing.get('AirlineName'))
        if parsing.get('RouteType') is None and parsing.get('KeywordType') in ('Route', 'Destination'):
            parsing['RouteType'] = 'Nonstop'
        ################################################################################################################
        # Specific case of special campaign re-naming
        ################################################################################################################
        try:
            if 'tCPA New' in parsing.get('SpecialCampaign'):
                parsing['SpecialCampaign'] = 'CPA'
        except TypeError:
            pass
        ################################################################################################################
        # Normalize KeywordType and KeywordGroup output values (case and plurality -- grammar)
        ################################################################################################################
        if parsing['KeywordType'] and parsing['KeywordType'].lower() in {'misspellings', 'misspelling'}:
            parsing['KeywordType'] = 'Modifiers'
            parsing['KeywordGroup'] = 'Misspellings'
        ################################################################################################################
        # If keyword type is core or modifiers, then we know that the campaign is a brand campaign
        ################################################################################################################
        keyword_type = parsing.get('KeywordType')
        campaign_type = parsing.get('CampaignType')
        campaign_name = parsing.get('CampaignName')

        if keyword_type:
            if campaign_type is None:
                if keyword_type.lower() == 'core':
                    parsing['CampaignType'] = 'Brand'
                elif keyword_type.lower() == 'modifiers':
                    parsing['CampaignType'] = 'Brand'
            if campaign_type == 'Non-Brand' and keyword_type.lower() == 'generic':
                parsing['CampaignType'] = 'Generic'
        ################################################################################################################
        # Final specific cases resolution.
        ################################################################################################################
        if parsing.get('CampaignType'):
            if 'COMHYB' in parsing['CampaignType']:
                parsing['CampaignType'] = 'Hybrid Brand'
                parsing['KeywordType'] = 'Competitors'
            if 'DISP' in parsing['CampaignType']:
                parsing['CampaignType'] = 'Brand'
                parsing['MarketingNetwork'] = 'Display'
                
        # Special cases for campaign names, (Dynamic re-marketing).
        if campaign_name and all([
            campaign_name.endswith('[GDRMKT]') or campaign_name.endswith('DynRmk'),
            campaign_name.startswith('GY')
        ]):
            parsing['CampaignType'] = 'DRMKT'
        
        ################################################################################################################
        # Update for route types
        ################################################################################################################
        parsing = {
            key: 'N/A' if item == '000' or item == '00' or item == '0' else item
            for key, item in parsing.items()
        }
        ################################################################################################################
        # Return the output
        ################################################################################################################
        return parsing

    def _find_regex_match(self, parsing: Parsing, campaign_name: str=None, adgroup_name: str=None) -> \
            Dict[str, Union[re.match, str]]:
        """
        This method finds and returns the corresponding regex match for the given parsing, campaign_name, and
        adgroup_name. It does not mutate or change the parsing, so the parsing should be updated correspondingly after.

        :param parsing:
        :param campaign_name:
        :param adgroup_name:
        :return:
        """
        ################################################################################################################
        # Instantiate some local vars
        ################################################################################################################
        # Decision tree 'success' var
        match = None
        # Index
        id_key = None
        # Replace campaign_name if it is a special campaign
        special = parsing.get("SpecialCampaign", "") if parsing.get("SpecialCampaign") else ""
        campaign_name = campaign_name.replace(
            special,
            ""
        ) if campaign_name else ""
        ################################################################################################################
        # Attempt to find a match within the regexes. (Order is important here.)
        ################################################################################################################
        # Case 1: Both campaign name and adgroup name are provided.
        if campaign_name and adgroup_name:
            regexes_list = list(REGEXES.keys())
            # Create a unique key from campaign name and adgroup name
            campaign_adgroup_string = campaign_name + '&&' + adgroup_name
            ############################################################################################################
            # Try EveryMundo naming conventions
            ############################################################################################################
            for id_key, regex in REGEXES['EveryMundo'].items():
                # Attempt to match the regex in the standard EM naming convention
                try:
                    match = regex.match(campaign_adgroup_string)
                except Exception as error:
                    raise Exception("Regex match error", (id_key, campaign_adgroup_string,)) from error
                if match:
                    break
            regexes_list.remove('EveryMundo')
            ############################################################################################################
            # Try airline specific naming conventions if EM failed
            ############################################################################################################
            if not match:
                # Get the specific set of cases for the given airline
                regexes = REGEXES.get(parsing.get('AirlineName'))
                if regexes:
                    # If there are such cases, try to match.
                    for id_key, regex in regexes.items():
                        try:
                            match = regex.match(campaign_adgroup_string)
                        except Exception as error:
                            raise Exception("Regex match error", (id_key, campaign_adgroup_string,)) from error
                        if match:
                            break
                    regexes_list.remove(parsing.get('AirlineName'))
            ############################################################################################################
            # Try other other given regex conventions
            ############################################################################################################
            done = False
            conflict_patterns = ['Xiamen']
            if not match:
                for reg in regexes_list:
                    if reg in {"LastHope", "Copa Airlines"} or not parsing.get("AirlineName"):
                        for id_key, regex in REGEXES[reg].items():
                            try:
                                match = regex.match(campaign_adgroup_string)
                            except Exception as error:
                                raise Exception("Regex match error", (id_key, campaign_adgroup_string)) from error
                            if match:
                                if parsing.get('AirlineName') is None:
                                    parsing.update({'AirlineName': reg})
                                    parsing.update(
                                        {'AirlineCode': self.airline_codes.get(parsing.get('AirlineName'))}
                                    )
                                done = True
                                break
                    if done:
                        break
            ############################################################################################################
            # Try the hardcoded conventions
            ############################################################################################################
            if not match:
                # Try copa
                match = OLD_COPA.get(campaign_adgroup_string)
                if match:
                    id_key = 'CopaDictionary'
                else:
                    # Try uo
                    if parsing.get("AirlineCode") == "UO":
                        if parsing.get("SearchEngine") == "Google":
                            match = OLD_UO_GOOGLE.get(campaign_adgroup_string)
                        elif parsing.get("SearchEngine") in {"Yahoo", "Yahoo! Japan"}:
                            match = OLD_UO_YAHOO.get(campaign_adgroup_string)
                        elif parsing.get("SearchEngine") == "Baidu":
                            match = OLD_UO_BAIDU.get(campaign_adgroup_string)
                        elif parsing.get("SearchEngine") == "Naver":
                            match = OLD_UO_NAVER.get(campaign_adgroup_string)
                        elif parsing.get("SearchEngine") == "Bing":
                            match = OLD_UO_BING.get(campaign_adgroup_string)
                        if match:
                            id_key = 'UODictionary'

        # Case 2: Only the campaign name is provided.
        elif campaign_name:
            # Keep ahold of the 'raw'  campaign name while we create a scrubbed version
            raw_campaign_name = campaign_name
            # Remove duplicate \\ characters
            campaign_name = campaign_name.replace('\\\\', '\\')
            # Remove the '.txt' suffixes (if present), and anything that might follow the .txt
            campaign_name = campaign_name.split('.txt')[0]
            # Special case: when campaign name is not properly tagged/ tracked in the url params from where it came
            if '?d1=' in campaign_name:
                campaign_name = campaign_name.split('?d1=')[1]
            # Decode url characters into something useable
            campaign_name = unquote_plus(campaign_name, encoding='utf-8')
            # Manually try to match some patterns:
            if re.match(r'^.*?\\.*?\\.*$', campaign_name):
                # If the campaign name is of the form '<stuff>\<stuff1>\<stuff2>', then, change it to
                # '<stuff>/<stuff1>\<stuff2>
                campaign_name = re.sub(r'^(.*?\\.*?)\\', r'\1/', campaign_name)
            elif re.match(r'^.*?/.*?/.*$', campaign_name):
                # Similarly, if the camp name is of the form '<stuff>/<stuff1>/<stuff2>' change to
                # '<stuff>/<stuff1>\<stuff2>'
                campaign_name = campaign_name.replace('/', '\\', 1)
            if re.match(r'.*?=\{?[A-Za-z0-9]+\}?-[A-Za-z0-9]+?-[A-Za-z0-9]+/.*', campaign_name):
                # If the campaign name is of the form:
                # '<stuff>{<alphanumstuff>}-<alphanumstuff>-<alphanumstuff>/<stuff> or
                # '<stuff><alphanumstuff>-<alphanumstuff>-<alphanumstuff>/<stuff>
                # This would be the case if route-encoding is 'or-leg-dest' instead of 'or>leg>dest'. If so, make it
                # the latter.
                campaign_name = campaign_name[::-1].replace('-', '>', 2)[::-1]
            # Create campaign_adgroup_string (campaign name level uniqueness)
            campaign_adgroup_string = campaign_name + '&&'
            # Create the analogue for the raw campaign name
            raw_campaign_adgroup_string = raw_campaign_name + '&&'
            # Main regex logic (campaign name only) vars
            done = False
            match = None
            regexes_list = list(CAMP_REGEXES.keys())
            ############################################################################################################
            # Try EveryMundo naming conventions
            ############################################################################################################
            for id_key, regex in CAMP_REGEXES['EveryMundo'].items():
                if type(regex) == str:
                    raise Exception(id_key, regex)
                match = regex.match(campaign_adgroup_string)
                if match:
                    break
            regexes_list.remove('EveryMundo')
            ############################################################################################################
            # Try airline-specific matching
            ############################################################################################################
            if not match:
                regexes = CAMP_REGEXES.get(parsing.get('AirlineName'))
                if regexes:
                    for id_key, regex in regexes.items():
                        match = regex.match(campaign_adgroup_string)
                        if match:
                            break
                    regexes_list.remove(parsing.get('AirlineName'))
                done = False
            ############################################################################################################
            # Try all the other kinds of matching
            ############################################################################################################
            if not match:
                for reg in regexes_list:
                    if reg in {"LastHope", "Copa Airlines"} or not parsing.get("AirlineName"):
                        for id_key, regex in CAMP_REGEXES[reg].items():
                            match = regex.match(campaign_adgroup_string)
                            if match:
                                if parsing.get('AirlineName') is None:
                                    parsing.update({'AirlineName': reg})
                                    parsing.update(
                                        {'AirlineCode': self.airline_codes.get(parsing.get('AirlineName'))})
                                done = True
                                break
                    if done:
                        break
            ############################################################################################################
            # Try the hardcoded conventions
            ############################################################################################################
            if not match:
                # Try copa
                match = OLD_COPA.get(campaign_adgroup_string)
                if match:
                    id_key = 'CopaDictionary'
                else:
                    # Try uo
                    if parsing.get("AirlineCode") == "UO":
                        if parsing.get("SearchEngine") == "Google":
                            match = OLD_UO_GOOGLE.get(campaign_adgroup_string)
                        elif parsing.get("SearchEngine") in {"Yahoo", "Yahoo! Japan"}:
                            match = OLD_UO_YAHOO.get(campaign_adgroup_string)
                        elif parsing.get("SearchEngine") == "Baidu":
                            match = OLD_UO_BAIDU.get(campaign_adgroup_string)
                        elif parsing.get("SearchEngine") == "Naver":
                            match = OLD_UO_NAVER.get(campaign_adgroup_string)
                        elif parsing.get("SearchEngine") == "Bing":
                            match = OLD_UO_BING.get(campaign_adgroup_string)
                        if match:
                            id_key = 'UODictionary'
        return {
            "id_key": id_key,
            "match": match,
            "campaign_name": campaign_name
        }

    @staticmethod
    def _special_campaign_suffix(dictionary: Parsing, campaign_name: str=None) -> Parsing:
        """
        NOTE: THIS APPEARS TO DO NOTHING

        Applies and assigns 'special' campaign suffixes to the parsing. Special campaign suffices are those used in,
        for example, campaign experiment suffixes.

        :param dictionary: Current state of parsing.
        :param campaign_name: Campaign name to be parsed.
        :return:
        """
        ################################################################################################################
        # Instantiate local vars & output
        ################################################################################################################
        parsing = {**dictionary}
        ################################################################################################################
        # Isolate said suffix.
        ################################################################################################################
        if parsing['AirlineName'] != 'Copa Airlines':
            # If the campaign/adgroup is not from Copa Airlines
            # Lazy match of one or more GS or BS starting string.
            prefix_pattern = re.compile(r'^(.+?)GS:|^(.+?)BS:|^(.+?)GY:|^(.+?)GL:')
            # If regex match returns 'True' (ie., the campaign is a campaign trial/ experiment of the old style, with
            # a prefix instead of a suffix) "New_tCPA_GS:..."
            if prefix_pattern.match(campaign_name):
                m = prefix_pattern.search(campaign_name)
                special_campaign = m.groups()[0]
                # If the special campaign matched, then remove the special campaign component.
                parsing['SpecialCampaign'] = special_campaign
        return parsing

    @staticmethod
    def _ensure_airline_name(dictionary: Parsing, airline_name: str=None, airline_code: str=None,
                             account_name: str=None) -> Parsing:
        """
        Ensure we can identify the airline by either airline_name or airline_code. If we cannnot, then we must set that
        value to Null.

        :param dictionary:
        :param airline_name:
        :param airline_code:
        :return:
        """
        ####################################################################################################################
        # Local vars & Instantiate output
        ####################################################################################################################
        airlines = [
            'Interjet',
            'Aegean Airlines',
            'Olympic Air',
            'Jet Airways',
            'Copa Airlines',
            'airberlin',
            'Hong Kong Express',
            'Volaris',
            'Aeromexico',
            'Cape Air',
            "Xiamen",
            "Havana Air",
            "American Airlines",
            "United Airlines",
            "Ernest",
            "Kuwait"
        ]
        airline_codes = {
            'Interjet': '4O',
            'Aegean Airlines': 'A3',
            'Olympic Air': 'OA',
            'Jet Airways': '9W',
            'Copa Airlines': 'CM',
            'airberlin': 'AB',
            'Volaris': 'Y4',
            'Hong Kong Express': 'UO',
            'Aeromexico': 'AM',
            'Cape Air': '9K',
            "Xiamen": "MF",
            "Havana Air": "11",
            "American Airlines": "AA",
            "United Airlines": "UA",
            "Ernest": "EG",
            "Kuwait": "KU"
        }
        parsing = {**dictionary}
        ####################################################################################################################
        # Ensure one of the two is provided and update output
        ####################################################################################################################
        if airline_name:
            # If we have the airline name
            if airline_name.lower() == 'jet':
                # For support of legacy applications that would pass in "Jet" instead of "Jet Airways"
                parsing['AirlineName'] = 'Jet Airways'
                parsing['AirlineCode'] = airline_codes[parsing['AirlineName']]
            else:
                # Standard use case (any other airline)
                for airline in airlines:
                    # Retrieve the airline code
                    if airline_name.lower() in airline.lower():
                        parsing['AirlineName'] = airline
                        parsing['AirlineCode'] = airline_codes[parsing['AirlineName']]
                        break
        elif airline_code:
            # If we have only the airline code, then populate using that
            for name, code in airline_codes.items():
                if code.lower() in airline_code.lower():
                    parsing['AirlineName'] = name
                    parsing['AirlineCode'] = code
                    break
        else:
            if account_name:
                # Try to get airline name from account name, as a last-ditch effort
                for name, code in airline_codes.items():
                    if name.lower() in account_name.lower():
                        parsing["AirlineName"] = name
                        parsing["AirlineCode"] = code
                        break
                else:
                    # If we can't get the airline from the account name, default to null
                    parsing['AirlineName'] = None
                    parsing['AirlineCode'] = None
            else:
                # If we are given neither airline name nor code and can't get it from the account name...
                parsing['AirlineName'] = None
                parsing['AirlineCode'] = None
        return parsing

    def _apply_airline_logic(self, dictionary: Parsing, airline_name: str=None, airline_code: str=None,
                             raw_camp_adg: str=None) -> Parsing:
        """
        As per the methods defined in airline_logic.py, this method, which exists as a helper therein, returns an
        updated state of the parsing based on the logic.

        :param dictionary: Current state of parsing
        :param airline_name: Airline name
        :param airline_code: IATA Code
        :param raw_camp_adg: Concat of campaign + adgroup
        :return:
        """
        parsing = {**dictionary}
        airline = airline_name
        if 'airberlin' in airline:
            air_berlin_parse_logic(parsing)
        elif 'Interjet' in airline:
            interjet_parse_logic(parsing)
        elif 'Aegean Airlines' in airline:
            aegean_parse_logic(parsing)
        elif 'Copa Airlines' in airline:
            copa_parse_logic(parsing)
        elif 'Jet Airways' in airline:
            jet_airways_logic(parsing)
        elif "Volaris" in airline:
            volaris_parse_logic(parsing)
        elif "Hong Kong Express" in airline:
            hong_kong_express_parse_logic(parsing)
        self._remove_omniture_slashes(parsing, raw_camp_adg, airline_name=airline, airline_code=airline_code)
        return parsing

    def _remove_omniture_slashes(self, parsing: Parsing, raw_camp_adg: str, airline_name: str=None,
                                 airline_code: str=None) -> None:
        """
        Removes duplicate backslashes from campaign names that occur from data coming from Omniture.

        Makes changes in parsing from data in the upsert_shelf into the return dict.

        All changes are made in-place.

        :param parsing: current state of parsing.
        :param raw_camp_adg: Same as raw_camp_adg in _item_parser(), namely, a string= '<campname>&&<adgroupname>'
        :param airline_name: Airline
        :param airline_code: IATA Code.
        """
        if parsing.get('ParseRegexId') not in ('CopaNonBrand16-CampaignOnly', 'EveryMundoNonBrand1-CampaignOnly'):
            try:
                if '.txt' in raw_camp_adg:
                    raw_camp_adg = raw_camp_adg.split('.txt')[0] + '.txt&&'
                d = self.upsert[raw_camp_adg.replace('\\\\', '\\')]
                if airline_name or airline_code:
                    try:
                        d.pop('AirlineName')
                        d.pop('AirlineCode')
                    except KeyError:
                        pass
                parsing.update(d)
            except KeyError:
                pass


def parse(*args, **kwargs):
    """
    Returns a dictionary representation of the parsing.

    Does not use caching.

    Expected kwargs:

    campaign: Campaign name (required)
    adgroup: Ad group name (recommended for best accuracy)
    airline_name: Either airline_name or airline_code recommended
    airline_code: Either airline_name or airline_code recommended
    search_engine: Search engine name (ie., Google)
    return_names: If true, returns the CampaignName and AdGroupName fields in the parsing. (Default True)
    na: If True, returns fields that are indeterminate or Null as the string 'N/A'. (Default False)

    Parsing method. For more information, see Parser.parse()

    :param args:
    :param kwargs:
    :return:
    """
    return Parser(cached=False).parse(*args, **kwargs)
