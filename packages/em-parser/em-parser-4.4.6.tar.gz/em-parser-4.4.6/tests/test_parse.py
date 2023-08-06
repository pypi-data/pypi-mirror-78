import re
import unittest

from em_parser import Parser
from em_parser.airline_logic import volaris_normalize_city_name
from em_parser.airports_graph import city_name_to_code
from em_parser.clean_functions import clean_network
from em_parser.em_parser import __version__
from em_parser.regexes import REGEXES
import em_parser.airline_logic as airline_logic


class TestParsing(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_clean_network(self):
        """
        Provides a test case for clean_network() functionality.
        :return:
        """
        with self.subTest("Not DSA -- Null case"):
            value = None
            test = clean_network(value)
            expected = None
            self.assertEqual(
                test, expected
            )
        with self.subTest("Not DSA -- Random"):
            value = "RandomValue"
            test = clean_network(value)
            expected = "RandomValue"
            self.assertEqual(
                test, expected
            )
        with self.subTest("DSA"):
            value = "dsa"
            test = clean_network(value)
            expected = "Dynamic Remarketing"
            self.assertEqual(
                test, expected
            )

    def test_parse_1(self):
        test_1 = {
            'AirlineCode': '9W',
            'AirlineName': 'Jet Airways',
            'CampaignType': 'Non-Brand',
            'Destination': 'DAC',
            'GeoTarget': 'BD',
            'KeywordType': 'Route',
            'Language': 'en',
            'KeywordGroup': 'General',
            'LocationType': 'Nation>City',
            'Market': 'BD',
            'MarketingNetwork': 'Search',
            'MatchType': 'BM',
            'Origin': 'CA',
            'ParseRegexId': 'EveryMundoNonBrand1',
            'ParserVersion': __version__,
            'RouteLocale': 'International',
            'RouteType': 'Connecting',
            'SearchEngine': 'Google'}
        self.assertDictEqual(
            test_1,
            Parser(cached=False).parse(
                r'GS:en-BD_NB\NC-Route=CA>XX>DAC/Geo@BD',
                r'GS:en-BD_NB\IR=CA>XX>DAC/BM',
                airline_name='Jet Airways',
                search_engine='Google'
            )
        )

    def test_parse_2(self):
        test_2 = {
            'AirlineCode': '9W',
            'AirlineName': 'Jet Airways',
            'CampaignType': 'Non-Brand',
            'Destination': 'DAC',
            'GeoTarget': 'BD',
            'KeywordType': 'Route',
            'Language': 'en',
            'LocationType': 'Nation>City',
            'Market': 'BD',
            'MarketingNetwork': 'Search',
            'MatchType': 'BM',
            'KeywordGroup': 'General',
            'Origin': 'CA',
            'ParseRegexId': 'EveryMundoNonBrand1',
            'ParserVersion': __version__,
            'RouteLocale': 'International',
            'RouteType': 'Connecting',
            'SearchEngine': 'Google'
        }
        self.assertDictEqual(
            test_2,
            Parser(cached=False).parse(
                r'GS:en-BD_NB\NC-Route=CA>XX>DAC/Geo@BD',
                r'GS:en-BD_NB\IR=CA>XX>DAC/BM',
                airline_name='Jet',
                search_engine='Google'
            )
        )

    def test_parse_3(self):
        test_3 = {
            'AirlineName': 'airberlin',
            'AirlineCode': 'AB',
            'CampaignType': 'Non-Brand',
            'Destination': 'MUC',
            'GeoTarget': 'DE',
            'KeywordGroup': 'General',
            'KeywordType': 'Route',
            'Language': 'de',
            'LocationType': 'City>City',
            'Market': 'DE',
            'MatchType': 'PX',
            'MarketingNetwork': 'Search',
            'Origin': 'CGN',
            'ParseRegexId': 'AirBerlinNonBrand1',
            'ParserVersion': __version__,
            'RouteType': 'Nonstop',
            'SearchEngine': 'Google'
        }
        self.assertDictEqual(
            test_3,
            Parser(cached=False).parse(
                r'G-DE_NB|Route=DE>DE[de|Geo:DE]',
                'R|NB_Cologne>Munich (de)',
                airline_name='airberlin'
            )
        )

    def test_parse_4(self):
        test_4 = {
            'AirlineName': 'airberlin',
            'AirlineCode': 'AB',
            'GeoTarget': 'DE',
            'KeywordGroup': 'General',
            'Language': 'de',
            'LocationType': 'City>City',
            'Market': 'DE',
            'MatchType': 'PX',
            'MarketingNetwork': 'Search',
            'ParseRegexId': 'AirBerlinNonBrand3',
            'ParserVersion': __version__,
            'RouteType': 'Nonstop',
            'SearchEngine': 'Google'
        }
        self.assertDictEqual(
            test_4,
            Parser(cached=False).parse(
                r'RE||DE_DynRemarketing=00>00 [de|Geo:DE]',
                '3_Cart_Bouncer_[DE]',
                airline_name='airberlin'
            )
        )

    def test_parse_5(self):
        test = {
            'ParseRegexId': 'AegeanBrand1',
            'AirlineName': 'Aegean Airlines',
            'ParserVersion': __version__,
            'AirlineCode': 'A3',
            'KeywordGroup': 'Deal',
            'MatchType': 'PX',
            'Language': 'de',
            'CampaignType': 'Non-Brand',
            'Market': 'DE',
            'MarketingNetwork': 'Search',
            'SearchEngine': 'Google'
        }
        self.assertDictEqual(
            test,
            Parser(cached=False).parse(
                'DE_Dest|NB|DE||GEO:MUC - Greece',
                'D|Munich - Thessaloniki||Deal',
                airline_name='Aegean'
            )
        )

    def test_parse_6(self):
        test = {
            'ParseRegexId': 'AirBerlinNonBrand1',
            'GeoTarget': 'DE',
            'AirlineCode': 'AB',
            'MarketingNetwork': 'Search',
            'Destination': 'MUC',
            'LocationType': 'City>City',
            'RouteType': 'Nonstop',
            'CampaignType': 'Non-Brand',
            'AirlineName': 'airberlin',
            'Language': 'de',
            'KeywordType': 'Route',
            'ParserVersion': __version__,
            'KeywordGroup': 'General',
            'MatchType': 'PX',
            'SearchEngine': 'Google',
            'Market': 'DE',
            'Origin': 'CGN'
        }
        self.assertDictEqual(
            test,
            Parser(cached=False).parse(
                'G-DE_NB|Route=DE>DE[de|Geo:DE]',
                'R|NB_Cologne>Munich (de)'
            )
        )

    def test_parse_7(self):
        test = {
            'AdGroupName': 'Santiago de Chile',
            'AirlineCode': 'CM',
            'AirlineName': 'Copa Airlines',
            'CampaignName': 'RMK - Colombia',
            'CampaignType': 'Remarketing',
            'KeywordGroup': 'General',
            'MatchType': 'PX',
            'Language': 'es',
            'Market': 'CO',
            'MarketingNetwork': 'RLSA',
            'ParseRegexId': 'CopaDictionary',
            'ParserVersion': __version__,
            'SearchEngine': 'Google'
        }
        self.assertDictEqual(
            test,
            Parser(cached=False).parse(
                'RMK - Colombia',
                'Santiago de Chile',
                return_names=True
            )
        )

    def test_parse_8(self):
        test = {
            'AirlineName': 'airberlin',
            'AirlineCode': 'AB',
            'CampaignType': 'Non-Brand',
            'Destination': 'VLC',
            'GeoTarget': 'IT',
            'KeywordGroup': 'General',
            'KeywordType': 'Route',
            'Language': 'it',
            'LocationType': 'City>City',
            'Market': 'IT',
            'MatchType': 'PX',
            'MarketingNetwork': 'Search',
            'Origin': 'IBZ',
            'ParseRegexId': 'AirBerlinNonBrand1',
            'ParserVersion': __version__,
            'RouteType': 'Connecting',
            'SearchEngine': 'Google'
        }
        self.assertDictEqual(
            test,
            Parser(cached=False).parse(
                'G-IT_NB|Route=ES>ES [it|Geo:IT]',
                'R|NB_Ibiza>X>Valencia (it)'
            )
        )

    def test_parse_9(self):
        test = {
            'AirlineName': 'airberlin',
            'AirlineCode': 'AB',
            'CampaignType': 'Non-Brand',
            'GeoTarget': 'DE',
            'KeywordGroup': 'General',
            'KeywordType': 'Ge',
            'Language': 'de',
            'LocationType': 'City>City',
            'Market': 'DE',
            'MatchType': 'PX',
            'MarketingNetwork': 'RLSA',
            'Origin': 'DE',
            'ParseRegexId': 'AirBerlinNonBrand1',
            'ParserVersion': __version__,
            'RouteType': 'Nonstop',
            'SearchEngine': 'Google'
        }
        value = Parser(cached=False).parse('G-DE_NB|RK-GE=[DE]>00 [de|Geo:DE]', 'RK-G|NB_[DE]>0-Ticket (de)')
        if test != value:
            print(test)
            print(value)
        self.assertDictEqual(
            test,
            value
        )

    def test_parse_10(self):
        test = {
            'AirlineCode': 'A3',
            'AirlineName': 'Aegean Airlines',
            'CampaignType': 'Non-Brand',
            'Destination': 'EFL',
            'KeywordType': 'Route',
            'Language': 'en',
            'KeywordGroup': 'General',
            'Market': 'AU',
            'MarketingNetwork': 'Search',
            'MatchType': 'PX',
            'Origin': 'ATH',
            'ParseRegexId': 'AegeanNonBrand3',
            'ParserVersion': __version__,
            'RouteLocale': 'Domestic',
            'RouteType': 'Nonstop',
            'SearchEngine': 'Google'
        }
        self.assertDictEqual(
            test,
            Parser(cached=False).parse(
                'AU_Routes|NB|EN||Greece - Greece',
                'R|Athens - Kefalonia||',
                return_names=False
            )
        )

    def test_parse_11(self):
        # Makes sure market name to code translator works
        test = {
            'AdGroupName': 'Argentina_Trips',
            'AirlineCode': 'CM',
            'AirlineName': 'Copa Airlines',
            'CampaignName': 'No Marca EN_PANAMA',
            'CampaignType': 'Non-Brand',
            'KeywordGroup': 'General',
            'MatchType': 'PX',
            'Language': 'en',
            'Market': 'PA',
            'MarketingNetwork': 'Search',
            'ParseRegexId': 'CopaDictionary',
            'ParserVersion': __version__,
            'SearchEngine': 'Google'
        }
        self.assertDictEqual(
            test,
            Parser(cached=False).parse(
                'No Marca EN_PANAMA',
                'Argentina_Trips',
                return_names=True
            )
        )

    def test_parse_12(self):
        # resolved github issue #17
        test = {
            'AdGroupName': r'GS:en-IN_NB\DR=BOM>00>GOI/BM@Bombay',
            'AirlineName': 'Jet Airways',
            'AirlineCode': '9W',
            'CampaignName': 'tCPA_New_GS:en-IN_NB\\CC-Route=BOM>00>GOI/Geo@IN',
            'Origin': 'BOM',
            'Destination': 'GOI',
            'MarketingNetwork': 'Search',
            'Market': 'IN',
            'RouteType': 'Nonstop',
            'Language': 'en',
            'MatchType': 'BM',
            'SearchEngine': 'Google',
            'LocationType': 'City>City',
            'KeywordType': 'Route',
            'GeoTarget': 'IN',
            'RouteLocale': 'Domestic',
            'KeywordGroup': 'Bombay',
            'CampaignType': 'Non-Brand',
            'ParseRegexId': 'EveryMundoNonBrand1',
            'SpecialCampaign': 'CPA',
            'ParserVersion': __version__
        }
        self.assertDictEqual(
            test,
            Parser(cached=False).parse(
                r'tCPA_New_GS:en-IN_NB\CC-Route=BOM>00>GOI/Geo@IN',
                r'GS:en-IN_NB\DR=BOM>00>GOI/BM@Bombay',
                airline_name='Jet Airways',
                return_names=True
            )
        )

    def test_parse_13(self):
        # resolved github issue #18
        test = {
            'AdGroupName': 'GS:en-AE_NB\\CC-OR=IDR>xx>BHO/PX',
            'AirlineCode': '9W',
            'AirlineName': 'Jet Airways',
            'CampaignName': 'GS:en-AE_NB\\Route=IN>xx>IN/Geo~AE',
            'CampaignType': 'Non-Brand',
            'Destination': 'BHO',
            'GeoTarget': 'AE',
            'KeywordType': 'Route',
            'Language': 'en',
            'LocationType': 'City>City',
            'Market': 'AE',
            'KeywordGroup': 'General',
            'MarketingNetwork': 'Search',
            'MatchType': 'PX',
            'Origin': 'IDR',
            'ParseRegexId': 'JetAirwaysNonbrand1',
            'ParserVersion': __version__,
            'RouteType': 'Connecting',
            'SearchEngine': 'Google'
        }
        self.assertDictEqual(
            test,
            Parser(cached=False).parse(
                r'GS:en-AE_NB\Route=IN>xx>IN/Geo~AE',
                r'GS:en-AE_NB\CC-OR=IDR>xx>BHO/PX',
                airline_name='Jet Airways',
                return_names=True
            )
        )

    def test_parse_14(self):
        # resolved github issue #19
        test = {
            'AdGroupName': 'GS:en-US_NB\\ID={CLE}>11>IXE/PH',
            'AirlineName': 'Jet Airways',
            'AirlineCode': '9W',
            'CampaignName': 'GS:en-US_NB\\Dest={CLE}>11>IXE/Geo@CLE',
            'CampaignType': 'Non-Brand',
            'Destination': 'IXE',
            'GeoTarget': 'CLE',
            'KeywordType': 'Destination',
            'Language': 'en',
            'LocationType': 'City>City',
            'Market': 'US',
            'MarketingNetwork': 'Search',
            'MatchType': 'PH',
            'Origin': 'CLE',
            'ParseRegexId': 'JetAirwaysBrand2',
            'KeywordGroup': 'General',
            'ParserVersion': __version__,
            'RouteType': 'Codeshare',
            'RouteLocale': 'International',
            'SearchEngine': 'Google'
        }
        self.assertDictEqual(
            test,
            Parser(cached=False).parse(
                r'GS:en-US_NB\Dest={CLE}>11>IXE/Geo@CLE',
                r'GS:en-US_NB\ID={CLE}>11>IXE/PH',
                airline_name='Jet Airways',
                return_names=True
            )
        )

    def test_parse_15(self):
        # resolved github issue #21
        test = {
            'AdGroupName': 'GS:ar-BH_HB\\NC-LD={00}>00>DXB/BD',
            'AirlineCode': '9W',
            'AirlineName': 'Jet Airways',
            'CampaignName': 'GS:ar-BH_HB\\Dest={00}>00>AE/Geo~BH',
            'CampaignType': 'Hybrid Brand',
            'Destination': 'DXB',
            'GeoTarget': 'BH',
            'KeywordType': 'Destination',
            'Language': 'ar',
            'KeywordGroup': 'General',
            'LocationType': 'Nation>City',
            'Market': 'BH',
            'MarketingNetwork': 'Search',
            'MatchType': 'BM',
            'ParseRegexId': 'JetAirwaysNonbrand1',
            'ParserVersion': __version__,
            'RouteType': 'Nonstop',
            'SearchEngine': 'Google'
        }
        self.assertDictEqual(
            test,
            Parser(cached=False).parse(
                'GS:ar-BH_HB\\Dest={00}>00>AE/Geo~BH',
                'GS:ar-BH_HB\\NC-LD={00}>00>DXB/BD',
                airline_name='Jet Airways',
                return_names=True
            )
        )

    def test_parse_16(self):
        # resolved github issue #21
        test = {
            'AdGroupName': 'GS:en-SG_CO=TB{SG}/SG~General',
            'AirlineName': 'Jet Airways',
            'AirlineCode': '9W',
            'CampaignName': 'GS:en-SG_CO=TB/Geo~SG',
            'CampaignType': 'Competitor',
            'GeoTarget': 'SG',
            'KeywordGroup': 'General',
            'Language': 'en',
            'Market': 'SG',
            'MarketingNetwork': 'Search',
            'MatchType': 'PX',
            'ParseRegexId': 'JetAirwaysBrand1',
            'ParserVersion': __version__,
            'SearchEngine': 'Google'
        }
        self.assertDictEqual(
            test,
            Parser(cached=False).parse(
                'GS:en-SG_CO=TB/Geo~SG',
                'GS:en-SG_CO=TB{SG}/SG~General',
                airline_name='Jet Airways',
                return_names=True
            )
        )

    def test_parse_17(self):
        # resolved github issue #20
        test = {
            'AdGroupName': '30-540 days-From-10th-Dec2014-9th-Jan2015',
            'AirlineName': 'Jet Airways',
            'AirlineCode': '9W',
            'CampaignName': 'Remarketing -  Nepal 30+',
            'Audience': '30-540 days-From-10th-Dec2014-9th-Jan2015',
            'Language': 'en',
            'MarketingNetwork': 'Dynamic Remarketing',
            'KeywordGroup': 'General',
            'MatchType': 'PX',
            'ParserVersion': __version__,
            'SearchEngine': 'Google'
        }
        self.assertDictEqual(
            test,
            Parser(cached=False).parse(
                'Remarketing -  Nepal 30+',
                '30-540 days-From-10th-Dec2014-9th-Jan2015',
                airline_name='Jet Airways',
                return_names=True
            )
        )

    def test_parse_18(self):
        # for github issue #22
        # however was resolved by closing issue 21
        test = {
            'AdGroupName': 'GS:en-US_NB\\CC-LD={EWR}>00>BRU/PX',
            'AirlineCode': '9W',
            'AirlineName': 'Jet Airways',
            'CampaignName': 'GS:en-US_NB\\Dest={US}>00>BE/Geo~EWR',
            'CampaignType': 'Non-Brand',
            'Destination': 'BRU',
            'GeoTarget': 'EWR',
            'KeywordType': 'Destination',
            'Language': 'en',
            'KeywordGroup': 'General',
            'LocationType': 'City>City',
            'Market': 'US',
            'MarketingNetwork': 'Search',
            'MatchType': 'PX',
            'Origin': 'EWR',
            'ParseRegexId': 'JetAirwaysNonbrand1',
            'ParserVersion': __version__,
            'RouteType': 'Nonstop',
            'SearchEngine': 'Google'
        }
        self.assertDictEqual(
            test,
            Parser(cached=False).parse(
                'GS:en-US_NB\\Dest={US}>00>BE/Geo~EWR',
                'GS:en-US_NB\\CC-LD={EWR}>00>BRU/PX',
                airline_name='Jet Airways',
                return_names=True
            )
        )

    def test_parse_19(self):
        # resolves github issue #23
        test = {
            'AdGroupName': 'GS:en-IN_HB\\NC-LD={00}>00>IXL/BM',
            'AirlineCode': '9W',
            'AirlineName': 'Jet Airways',
            'CampaignName': 'GS:en-IN_HB\\Dest={00}>00>IN/Geo~IN',
            'CampaignType': 'Hybrid Brand',
            'Destination': 'IXL',
            'GeoTarget': 'IN',
            'KeywordType': 'Destination',
            'Language': 'en',
            'LocationType': 'Nation>City',
            'KeywordGroup': 'General',
            'Market': 'IN',
            'MarketingNetwork': 'Search',
            'MatchType': 'BM',
            'RouteLocale': 'Domestic',
            'ParseRegexId': 'JetAirwaysNonbrand1',
            'ParserVersion': __version__,
            'RouteType': 'Nonstop',
            'SearchEngine': 'Google'
        }
        self.assertDictEqual(
            test,
            Parser(cached=False).parse(
                'GS:en-IN_HB\\Dest={00}>00>IN/Geo~IN',
                'GS:en-IN_HB\\NC-LD={00}>00>IXL/BM',
                airline_name='Jet Airways',
                return_names=True
            )
        )

    def test_parse_20(self):
        # test resolution of github issue #24
        test = {
            'AdGroupName': 'GL:en-IN_NB\\CO=AI/PH@PS-PY(1-3d)',
            'AirlineName': 'Jet Airways',
            'AirlineCode': '9W',
            'Audience': 'PS-PY(1-3d)',
            'CampaignName': 'GL:en-IN_NB\\00-Comp=AI/Geo@IN',
            'CampaignType': 'Non-Brand',
            'GeoTarget': 'IN',
            'KeywordGroup': 'Ai',
            'KeywordType': 'Competitors',
            'Language': 'en',
            'Market': 'IN',
            'MarketingNetwork': 'RLSA',
            'MatchType': 'PH',
            'ParseRegexId': 'EveryMundoRLSA1',
            'ParserVersion': __version__,
            'SearchEngine': 'Google'
        }
        self.assertDictEqual(
            test,
            Parser(cached=False).parse(
                'GL:en-IN_NB\\00-Comp=AI/Geo@IN',
                'GL:en-IN_NB\\CO=AI/PH@PS-PY(1-3d)',
                airline_name='Jet Airways',
                return_names=True
            )
        )

    def test_parse_21(self):
        # test resolution of github issue #24
        test = {
            'AdGroupName': 'GS:en-IN_NB\\DR=BOM>00>GOI/PH',
            'AirlineName': 'Jet Airways',
            'AirlineCode': '9W',
            'CampaignName': 'GS:en-IN_NB\\CC-Route=BOM>00>GOI/Geo@IN - CPA',
            'CampaignType': 'Non-Brand',
            'Destination': 'GOI',
            'GeoTarget': 'IN',
            'KeywordType': 'Route',
            'Language': 'en',
            'Market': 'IN',
            'MarketingNetwork': 'Search',
            'KeywordGroup': 'General',
            'MatchType': 'PH',
            'Origin': 'BOM',
            'LocationType': 'City>City',
            'RouteLocale': 'Domestic',
            'ParseRegexId': 'JetAirwaysNonbrand2',
            'SpecialCampaign': 'CPA',
            'RouteType': 'Nonstop',
            'ParserVersion': __version__,
            'SearchEngine': 'Google'
        }
        self.assertDictEqual(
            test,
            Parser(cached=False).parse(
                'GS:en-IN_NB\\CC-Route=BOM>00>GOI/Geo@IN - CPA',
                'GS:en-IN_NB\\DR=BOM>00>GOI/PH',
                airline_name='Jet Airways',
                return_names=True
            )
        )

    def test_parse_22(self):
        # test resolution of github issue #26
        test = {
            'AdGroupName': 'B|DISP > Books & Literature',
            'AirlineCode': '4O',
            'AirlineName': 'Interjet',
            'CampaignName': 'G-MX_BRDISP|00=MX [es|Geo:MX]',
            'CampaignType': 'Brand',
            'GeoTarget': 'MX',
            'KeywordGroup': 'General',
            'Language': 'es',
            'MatchType': 'PX',
            'Market': 'MX',
            'MarketingNetwork': 'Display',
            'ParseRegexId': 'InterjetBrand2',
            'ParserVersion': __version__,
            'SearchEngine': 'Google'
        }
        self.assertDictEqual(
            test,
            Parser(cached=False).parse(
                'G-MX_BRDISP|00=MX [es|Geo:MX]',
                'B|DISP > Books & Literature',
                airline_name='Interjet',
                return_names=True
            )
        )

    def test_parse_23(self):
        test = {
            'AdGroupName': 'D|BRANDHYB_0>San Jose (en)',
            'AirlineCode': '4O',
            'AirlineName': 'Interjet',
            'CampaignName': 'G-CR_BRANDHYB|Dest=00>CR [en|Geo:CR]',
            'CampaignType': 'Hybrid Brand',
            'Destination': 'SJO',
            'GeoTarget': 'CR',
            'KeywordGroup': 'General',
            'KeywordType': 'Destination',
            'Language': 'en',
            'MatchType': 'PX',
            'Market': 'CR',
            'MarketingNetwork': 'Search',
            'ParseRegexId': 'InterjetDest1',
            'ParserVersion': __version__,
            'RouteType': 'Nonstop',
            'SearchEngine': 'Google'
        }
        self.assertDictEqual(
            test,
            Parser(cached=False).parse(
                test['CampaignName'],
                test['AdGroupName'],
                airline_name=test['AirlineName'],
                return_names=True
            )
        )

    def test_parse_24(self):
        test = {
            'AdGroupName': 'R|COMHYBY4_Monterrey>Mexico City (es',
            'AirlineName': 'Interjet',
            'AirlineCode': '4O',
            'CampaignName': 'G-MX_COMHYBY4|Route=MX>MX [es|Geo:MX]',
            'CampaignType': 'Hybrid Brand',
            'Destination': 'MEX',
            'GeoTarget': 'MX',
            'KeywordType': 'Competitors',
            'Language': 'es',
            'Market': 'MX',
            'MarketingNetwork': 'Search',
            'MatchType': 'PX',
            'KeywordGroup': 'General',
            'Origin': 'MTY',
            'ParseRegexId': 'InterjetDDR1',
            'ParserVersion': __version__,
            'SearchEngine': 'Google'
        }
        self.assertDictEqual(
            test,
            Parser(cached=False).parse(
                test['CampaignName'],
                test['AdGroupName'],
                airline_name=test['AirlineName'],
                return_names=True
            )
        )

    def test_parse_25(self):
        # github issue #28
        test = {
            'AdGroupName': 'D|NBGSP_San Antonio>Monterrey (en)',
            'AirlineCode': '4O',
            'AirlineName': 'Interjet',
            'CampaignName': 'G-US_NBGSP|Dest=US>MX [en|Geo:San Antonio]',
            'CampaignType': 'Non-Brand',
            'Destination': 'MTY',
            'GeoTarget': 'San Antonio',
            'KeywordGroup': 'General',
            'KeywordType': 'Destination',
            'Language': 'en',
            'Market': 'US',
            'MatchType': 'PX',
            'MarketingNetwork': 'GSP',
            'Origin': 'SAT',
            'ParseRegexId': 'InterjetDest1',
            'ParserVersion': __version__,
            'RouteType': 'Nonstop',
            'SearchEngine': 'Google'
        }
        self.assertDictEqual(
            test,
            Parser(cached=False).parse(
                test['CampaignName'],
                test['AdGroupName'],
                airline_name=test['AirlineName'],
                return_names=True
            )
        )

    def test_parse_26(self):
        # github issue #28
        test = {
            'AdGroupName': 'D|BRDISP_San Jose>0 (es) - T|Environment',
            'AirlineCode': '4O',
            'AirlineName': 'Interjet',
            'CampaignName': 'G-CR_BRDISP|Dest=CR>MX [es|Geo:CR]',
            'CampaignType': 'Brand',
            'Destination': '0',
            'GeoTarget': 'CR',
            'KeywordGroup': 'General',
            'Language': 'es',
            'MatchType': 'PX',
            'Market': 'CR',
            'MarketingNetwork': 'Display',
            'Origin': 'SJO',
            'ParseRegexId': 'InterjetDest1',
            'ParserVersion': __version__,
            'SearchEngine': 'Google'
        }
        self.assertDictEqual(
            test,
            Parser(cached=False).parse(
                test['CampaignName'],
                test['AdGroupName'],
                airline_name=test['AirlineName'],
                return_names=True
            )
        )

    def test_parse_27(self):
        pass
        # github issue #28
        # This campaign-adgroup turned out to be too weird
        # test = {'AdGroupName': 'B|BRDISP_MX>0 (es) - T|Travel',
        #         'AirlineName': 'Interjet',
        #         'AirlineCode': '4O',
        #         'CampaignName': 'G-MX_DISP|T-Travel=MX>MX [es|Geo:MX]',
        #         'CampaignType': 'Non-Brand',
        #         'Origin': 'MX',
        #         'Destination': 'MX',
        #         'GeoTarget': 'MX',
        #         'Language': 'es',
        #         'Market': 'MX',
        #         'KeywordGroup': 'General',
        #         'MarketingNetwork': 'Display',
        #         'ParseRegexId': 'InterjetDDR1',
        #         'ParserVersion': __version__,
        #         'SearchEngine': 'Google'}
        # self.assertDictEqual(test, Parser(cached=False).parse(test['CampaignName'],
        #                                         test['AdGroupName'],
        #                                         airline_name=test['AirlineName'], return_names=True))

    def test_parse_28(self):
        # github issue #28
        test = {'AdGroupName': 'B|NB_GSP Competencia',
                'AirlineName': 'Interjet',
                'AirlineCode': '4O',
                'CampaignName': 'G-GT_BRGSP|00=MX>00 [es|Geo:GT]',
                'GeoTarget': 'GT',
                'KeywordGroup': 'All',
                'KeywordType': 'Competitors',
                'Language': 'es',
                'Market': 'GT',
                'MarketingNetwork': 'GSP',
                'CampaignType': 'Brand',
                'Origin': 'MX',
                'MatchType': 'PX',
                'ParseRegexId': 'InterjetGSP1',
                'ParserVersion': __version__,
                'SearchEngine': 'Google'}
        self.assertDictEqual(test, Parser(cached=False).parse(test['CampaignName'],
                                                              test['AdGroupName'],
                                                              airline_name=test['AirlineName'], return_names=True))

    def test_parse_29(self):
        # github issue #29
        test = {'AdGroupName': 'Static RMKT - All Visits Minus Converters',
                'AirlineName': 'Interjet',
                'AirlineCode': '4O',
                'Audience': 'All Visits Minus Converters',
                'CampaignName': 'G-MX_RMKTV|00=MX>00 [es|Geo:MX]',
                'CampaignType': 'Non-Brand',
                'Origin': 'MX',
                'GeoTarget': 'MX',
                'KeywordType': 'Route',
                'Language': 'es',
                'Market': 'MX',
                'MatchType': 'PX',
                'KeywordGroup': 'General',
                'MarketingNetwork': 'Display Remarketing',
                'ParseRegexId': 'InterjetRLSA1',
                'ParserVersion': __version__,
                'SearchEngine': 'Google',
                'RouteType': 'Nonstop', }
        self.assertDictEqual(test, Parser(cached=False).parse(test['CampaignName'],
                                                              test['AdGroupName'],
                                                              airline_name=test['AirlineName'], return_names=True))

    def test_parse_30(self):
        # github issue #30
        test = {'AdGroupName': 'G|COMHYB_0>0 (es) - Buen Fin_AM',
                'AirlineCode': '4O',
                'AirlineName': 'Interjet',
                'CampaignName': 'G-MX_COMHYB|Gen=00>00 [es|Geo:MX]',
                'CampaignType': 'Hybrid Brand',
                'Destination': '0',
                'GeoTarget': 'MX',
                'KeywordGroup': 'Buen Fin Am',
                'KeywordType': 'Generic',
                'Language': 'es',
                'Market': 'MX',
                'MarketingNetwork': 'Search',
                'MatchType': 'PX',
                'ParseRegexId': 'InterjetHybrid1',
                'ParserVersion': __version__,
                'RouteType': 'Nonstop',
                'SearchEngine': 'Google'}
        self.assertDictEqual(test, Parser(cached=False).parse(test['CampaignName'],
                                                              test['AdGroupName'],
                                                              airline_name=test['AirlineName'], return_names=True))

    def test_parse_31(self):
        # Github issue #31
        test = {'MatchType': 'PB',
                'CampaignName': 'gs:pt-us_br\\core/pb@us',
                'CampaignType': 'Brand',
                'GeoTarget': 'US',
                'KeywordGroup': 'General',
                'KeywordType': 'Core',
                'Language': 'pt',
                'Market': 'US',
                'MarketingNetwork': 'Search',
                'ParseRegexId': 'EveryMundoBrand1C-CampaignOnly',
                'ParserVersion': __version__,
                'SearchEngine': 'Google'}
        self.assertDictEqual(test, Parser(cached=False).parse(test['CampaignName'], return_names=True))

    def test_parse_32(self):
        # Interjet DDR1 Test
        test = {
            'AdGroupName': 'R|NB_Mexico City>Zihuatanejo (es)',
            'AirlineName': 'Interjet',
            'AirlineCode': '4O',
            'CampaignName': 'G-CR_NB|Route=MX>MX [es|Geo:CR]',
            'CampaignType': 'Non-Brand',
            'Origin': 'MEX',
            'Destination': 'ZIH',
            'GeoTarget': 'CR',
            'Language': 'es',
            'MatchType': 'PX',
            'Market': 'CR',
            'KeywordGroup': 'General',
            'MarketingNetwork': 'Search',
            'ParseRegexId': 'InterjetDDR1',
            'ParserVersion': __version__,
            'SearchEngine': 'Google',
            'KeywordType': 'Route',
            'RouteType': 'Nonstop',
        }
        self.assertDictEqual(
            test,
            Parser(cached=False).parse(
                'G-CR_NB|Route=MX>MX [es|Geo:CR]',
                'R|NB_Mexico City>Zihuatanejo (es)',
                airline_name='Interjet',
                return_names=True
            )
        )

    def test_parse_33(self):
        # Github issue #32
        test = {'CampaignName': r'GS:en-CO_NB\CC-Dest={BOG}>00>CUN/Geo@BOG[MOB]',
                'AdGroupName': r'GS:en-CO_NB\ID={BOG}>00>CUN/BM',
                'RouteLocale': 'International',
                'AirlineCode': 'CM',
                'AirlineName': 'Copa Airlines',
                'CampaignType': 'Non-Brand',
                'Destination': 'CUN',
                'GeoTarget': 'BOG',
                'KeywordGroup': 'General',
                'KeywordType': 'Destination',
                'Language': 'en',
                'LocationType': 'City>City',
                'Market': 'CO',
                'MarketingNetwork': 'Search',
                'MatchType': 'BM',
                'Origin': 'BOG',
                'ParseRegexId': 'CopaNonbrand1',
                'ParserVersion': __version__,
                'RouteType': 'Nonstop',
                'SearchEngine': 'Google',
                'SpecialCampaign': 'MOB'}
        self.assertDictEqual(test,
                             Parser(cached=False).parse(test['CampaignName'], test['AdGroupName'], return_names=True))

    def test_parse_34(self):
        # Github issue #33
        test = {'AdGroupName': r'GS:en-BR_NB\MODIFIERS/BR@BM',
                'AirlineCode': 'CM',
                'AirlineName': 'Copa Airlines',
                'CampaignName': r'GS:en-BR_NB\MODIFIERS/@BR',
                'KeywordGroup': 'General',
                'MatchType': 'BM',
                'CampaignType': 'Non-Brand',
                'KeywordType': 'Modifiers',
                'GeoTarget': 'BR',
                'Language': 'en',
                'Market': 'BR',
                'MarketingNetwork': 'Search',
                'ParseRegexId': 'CopaNonbrand10',
                'ParserVersion': __version__,
                'SearchEngine': 'Google'}
        self.assertDictEqual(test,
                             Parser(cached=False).parse(test['CampaignName'], test['AdGroupName'], return_names=True))

    def test_parse_35(self):
        # Github issue #34
        test = {'AdGroupName': 'GS:es-CO_BR\\SeasonalityGeneric/CO@NAVIDAD',
                'AirlineCode': 'CM',
                'AirlineName': 'Copa Airlines',
                'CampaignName': 'GS:es-CO_NB\\SeasonalityGeneric/@CO | MOB',
                'CampaignType': 'Non-Brand',
                'GeoTarget': 'CO',
                'KeywordGroup': 'Navidad',
                'KeywordType': 'SeasonalityGeneric',
                'Language': 'es',
                'Market': 'CO',
                'MatchType': 'PX',
                'MarketingNetwork': 'Search',
                'ParseRegexId': 'CopaNonbrand11',
                'ParserVersion': __version__,
                'SearchEngine': 'Google'}
        self.assertDictEqual(test,
                             Parser(cached=False).parse(test['CampaignName'], test['AdGroupName'], return_names=True))

    def test_parse_46(self):
        # Github issue #35
        test = {'AdGroupName': 'GD:pt-BR_RM\\Miami/@BR',
                'AirlineCode': 'CM',
                'AirlineName': 'Copa Airlines',
                'CampaignName': 'GD:pt-BR_RM\\Rmkt-Keywords/@BR',
                'CampaignType': 'Display Remarketing',
                'Destination': 'MIA',
                'GeoTarget': 'BR',
                'KeywordGroup': 'General',
                'Language': 'pt',
                'Market': 'BR',
                'MatchType': 'PX',
                'MarketingNetwork': 'Display',
                'ParseRegexId': 'CopaNonbrand12',
                'ParserVersion': __version__,
                'SearchEngine': 'Google'}
        self.assertDictEqual(test,
                             Parser(cached=False).parse(test['CampaignName'], test['AdGroupName'], return_names=True))

    def test_parse_47(self):
        # Github issue #36
        test = {'AdGroupName': 'General/PX',
                'AirlineCode': 'CM',
                'AirlineName': 'Copa Airlines',
                'CampaignName': 'GS:es_NB\\Generics/-ATP',
                'CampaignType': 'Generic',
                'KeywordGroup': 'General',
                'KeywordType': 'Generic',
                'Language': 'es',
                'Market': 'WW',
                'MarketingNetwork': 'Search',
                'MatchType': 'PX',
                'ParseRegexId': 'CopaNonbrand6',
                'ParserVersion': __version__,
                'SearchEngine': 'Google',
                'SpecialCampaign': 'ATP'}
        self.assertDictEqual(test,
                             Parser(cached=False).parse(test['CampaignName'], test['AdGroupName'], return_names=True))

    def test_parse_48(self):
        # Github issue #37
        test = {'CampaignName': 'GS:es-CO_BR\\Modifiers/Geo@CLO',
                'CampaignType': 'Brand',
                'GeoTarget': 'CLO',
                'KeywordGroup': 'General',
                'KeywordType': 'Modifiers',
                'Language': 'es',
                'Market': 'CO',
                'MarketingNetwork': 'Search',
                'MatchType': 'PX',
                'ParseRegexId': 'EveryMundoBrand1-CampaignOnly',
                'ParserVersion': __version__,
                'SearchEngine': 'Google'}
        self.assertDictEqual(test, Parser(cached=False).parse(r'GS:es-CO_BR\Modifiers\Geo@CLO', return_names=True))

    def test_parse_49(self):
        # Github issue #38
        test = {'CampaignName': 'BS:en-US_BR\\Core/Geo@US',
                'CampaignType': 'Brand',
                'GeoTarget': 'US',
                'KeywordGroup': 'General',
                'MatchType': 'PX',
                'KeywordType': 'Core',
                'Language': 'en',
                'Market': 'US',
                'MarketingNetwork': 'Search',
                'ParseRegexId': 'EveryMundoBrand1-CampaignOnly',
                'ParserVersion': __version__,
                'SearchEngine': 'Bing'}
        self.assertDictEqual(test, Parser(cached=False).parse('BS:en-US_BR/Core/Geo@US', return_names=True))

    def test_parse_50(self):
        # Tests nonbrand sheet in copa DB
        test = {'AdGroupName': 'GS:en-US_NB\\ID={FLL}>00>PA/BM',
                'AirlineCode': 'CM',
                'AirlineName': 'Copa Airlines',
                'CampaignName': 'GS:en-US_NB\\CN-Dest={FLL}>00>PA/Geo@FLL[ATP]',
                'CampaignType': 'Non-Brand',
                'Destination': 'PA',
                'GeoTarget': 'FLL',
                'KeywordGroup': 'General',
                'KeywordType': 'Destination',
                'Language': 'en',
                'LocationType': 'City>Nation',
                'Market': 'US',
                'MarketingNetwork': 'Search',
                'MatchType': 'BM',
                'Origin': 'FLL',
                'ParseRegexId': 'CopaNonbrand1',
                'ParserVersion': __version__,
                'RouteLocale': 'International',
                'RouteType': 'Nonstop',
                'SearchEngine': 'Google',
                'SpecialCampaign': 'ATP'}
        self.assertDictEqual(test,
                             Parser(cached=False).parse(test['CampaignName'], test['AdGroupName'], return_names=True))

    def test_parse_51(self):
        # Tests nonbrand sheet in copa DB
        test = {'CampaignName': 'GS:es-CO\\DSA/@CO',
                'AdGroupName': 'GS:es-CO_NB\\DSA-VSA/',
                'AirlineCode': 'CM',
                'AirlineName': 'Copa Airlines',
                'MatchType': 'PX',
                'Destination': 'VSA',
                'GeoTarget': 'CO',
                'KeywordType': 'Destination',
                'KeywordGroup': 'General',
                'Language': 'es',
                'Market': 'CO',
                'MarketingNetwork': 'Search',
                'CampaignType': 'Non-Brand',
                'ParseRegexId': 'CopaNonbrand9',
                'RouteType': 'Nonstop',
                'ParserVersion': __version__,
                'SearchEngine': 'Google',
                'SpecialCampaign': 'DSA'}
        self.assertDictEqual(test,
                             Parser(cached=False).parse(test['CampaignName'], test['AdGroupName'], return_names=True))

    def test_parse_52(self):
        # Tests new-old copa convention
        test = {'AdGroupName': 'GS:es-PA_NB\\Generics={PA}>XX>BZE/BM',
                'AirlineCode': 'CM',
                'AirlineName': 'Copa Airlines',
                'CampaignName': 'GS:es-PA_NB\\ND={PA}>XX>BZ/Geo@PA',
                'CampaignType': 'Non-Brand',
                'Destination': 'BZ',
                'GeoTarget': 'PA',
                'KeywordGroup': 'Generics',
                'Language': 'es',
                'Market': 'PA',
                'MarketingNetwork': 'Search',
                'MatchType': 'BM',
                'Origin': 'PA',
                'ParseRegexId': 'CopaNonbrand13',
                'ParserVersion': __version__,
                'RouteType': 'Connecting',
                'SearchEngine': 'Google'}
        self.assertDictEqual(test,
                             Parser(cached=False).parse(test['CampaignName'], test['AdGroupName'], return_names=True))

    def test_parse_53(self):
        # Tests new-old copa convention
        test = {'AirlineCode': 'CM',
                'AirlineName': 'Copa Airlines',
                'CampaignType': 'Brand',
                'GeoTarget': 'CO',
                'KeywordGroup': 'Copa Vacaciones',
                'CampaignName': 'GS:en-CO_BR\\Core/Geo@CO[MOB]',
                'AdGroupName': 'GS:en-CO_BR\\Core=CV/EX@Copa_Vacaciones',
                'KeywordType': 'Core',
                'Language': 'en',
                'Market': 'CO',
                'MarketingNetwork': 'Search',
                'MatchType': 'EX',
                'ParseRegexId': 'CopaBrand6',
                'ParserVersion': __version__,
                'SearchEngine': 'Google',
                'SpecialCampaign': 'MOB'}
        self.assertDictEqual(test,
                             Parser(cached=False).parse(test['CampaignName'], test['AdGroupName'], return_names=True))

    def test_parse_54(self):
        # Tests new-old copa convention
        test = {'AdGroupName': 'GS:es-US_NB\\LD={MCO}>00>PTY/PX',
                'AirlineCode': 'CM',
                'AirlineName': 'Copa Airlines',
                'CampaignName': 'GS:es-US_NB\\Dest={US}>00>PA/Geo@MCO-ATP',
                'CampaignType': 'Non-Brand',
                'Destination': 'PTY',
                'GeoTarget': 'MCO',
                'KeywordGroup': 'General',
                'KeywordType': 'Destination',
                'Language': 'es',
                'Market': 'US',
                'MarketingNetwork': 'Search',
                'MatchType': 'PX',
                'Origin': 'MCO',
                'ParseRegexId': 'CopaNonBrand14',
                'ParserVersion': __version__,
                'RouteType': 'Nonstop',
                'SearchEngine': 'Google',
                'SpecialCampaign': 'ATP'}
        self.assertDictEqual(test,
                             Parser(cached=False).parse(test['CampaignName'], test['AdGroupName'], return_names=True))

    def test_parse_55(self):
        # Tests new-old copa convention
        test = {'AirlineCode': 'CM',
                'AirlineName': 'Copa Airlines',
                'CampaignName': 'GS:en-US_NB\\00-Genc=Travel/Geo@US',
                'CampaignType': 'Generic',
                'GeoTarget': 'US',
                'KeywordGroup': 'Travel',
                'MatchType': 'PX',
                'KeywordType': 'Generic',
                'Language': 'en',
                'Market': 'US',
                'MarketingNetwork': 'Search',
                'ParseRegexId': 'EveryMundoRLSA1-CampaignOnly',
                'ParserVersion': __version__,
                'SearchEngine': 'Google'}

        self.assertDictEqual(test,
                             Parser(cached=False).parse(test['CampaignName'], return_names=True,
                                                        airline_code=test['AirlineCode']))

    def test_parse_56(self):
        # Tests new-old copa convention
        test = {'AdGroupName': 'GS:en-US_NB\\Generic/PH@Attractions',
                'AirlineCode': 'CM',
                'AirlineName': 'Copa Airlines',
                'CampaignName': 'GS:en-US_NB\\Search=Generic/Geo@US[ATP]',
                'CampaignType': 'Generic',
                'GeoTarget': 'US',
                'KeywordGroup': 'Attractions',
                'KeywordType': 'Generic',
                'Language': 'en',
                'Market': 'US',
                'MarketingNetwork': 'Search',
                'MatchType': 'PH',
                'ParseRegexId': 'CopaBrand7',
                'ParserVersion': __version__,
                'SearchEngine': 'Google',
                'SpecialCampaign': 'ATP'}
        self.assertDictEqual(test,
                             Parser(cached=False).parse(test['CampaignName'], test['AdGroupName'], return_names=True))

    def test_parse_57(self):
        test = {'AirlineCode': 'CM',
                'AirlineName': 'Copa Airlines',
                'CampaignType': 'Non-Brand',
                'GeoTarget': 'IN',
                'KeywordGroup': 'General',
                'KeywordType': 'Origin',
                'MatchType': 'PX',
                'Language': 'fr',
                'LocationType': 'City>City',
                'Market': 'FR',
                'MarketingNetwork': 'Search',
                'Origin': 'FR',
                'ParseRegexId': 'CopaNonbrand1M-CampaignOnly',
                'ParserVersion': __version__,
                'RouteType': 'Nonstop',
                'SearchEngine': 'Google',
                'SpecialCampaign': 'gDSA'}
        self.assertDictEqual(test, Parser(cached=False).parse(r'GS:fr-FR_NB\CC-Origin=FR>00>000/Geo@IN[gDSA]'))

    def test_parse_58(self):
        test = {'AirlineCode': 'CM',
                'AirlineName': 'Copa Airlines',
                'CampaignName': r'GS:es-US_NB\Search=Generic/Geo@US[ATP]',
                'CampaignType': 'Generic',
                'GeoTarget': 'US',
                'KeywordGroup': 'General',
                'KeywordType': 'Generic',
                'Language': 'es',
                'MatchType': 'PX',
                'Market': 'US',
                'MarketingNetwork': 'Search',
                'ParseRegexId': 'CopaBrand7-CampaignOnly',
                'ParserVersion': __version__,
                'SearchEngine': 'Google',
                'SpecialCampaign': 'ATP'}
        self.assertDictEqual(test, Parser(cached=False).parse(r'GS:es-US_NB\\Search=Generic/Geo@US[ATP].txt',
                                                              airline_code='CM',
                                                              return_names=True))

    def test_parse_59(self):
        test = {
            'AirlineCode': 'CM',
            'AirlineName': 'Copa Airlines',
            'CampaignName': 'GS:en-CR\\Core/Geo@CR',
            'CampaignType': 'Brand',
            'GeoTarget': 'CR',
            'KeywordGroup': 'General',
            'KeywordType': 'Core',
            'MatchType': 'PX',
            'Language': 'en',
            'Market': 'CR',
            'MarketingNetwork': 'Search',
            'ParseRegexId': 'CopaBrand10-CampaignOnly',
            'ParserVersion': __version__,
            'SearchEngine': 'Google'
        }
        self.assertDictEqual(
            test,
            Parser(cached=False).parse(
                r'GS:en-CR/Core/Geo@CR.txt',
                airline_code='CM',
                return_names=True
            )
        )

    def test_parse_60(self):
        test = {'AirlineCode': 'CM',
                'AirlineName': 'Copa Airlines',
                'CampaignName': 'GS:en-US\\Modifiers/Geo@US',
                'GeoTarget': 'US',
                'CampaignType': 'Brand',
                'KeywordGroup': 'General',
                'KeywordType': 'Modifiers',
                'MatchType': 'PX',
                'Language': 'en',
                'Market': 'US',
                'MarketingNetwork': 'Search',
                'ParseRegexId': 'CopaBrand10-CampaignOnly',
                'ParserVersion': __version__,
                'SearchEngine': 'Google'}
        self.assertDictEqual(test, Parser(cached=False).parse(r'GS:en-US/Modifiers/Geo@US.txt',
                                                              airline_code='CM',
                                                              return_names=True))

    def test_parse_61(self):
        test = {'AirlineCode': 'CM',
                'AirlineName': 'Copa Airlines',
                'CampaignType': 'Non-Brand',
                'Destination': 'Panama',
                'KeywordGroup': 'General',
                'KeywordType': 'Destination',
                'Language': 'pt',
                'Market': 'BR',
                'MatchType': 'PX',
                'MarketingNetwork': 'Search',
                'ParseRegexId': 'CopaNonbrand6-CampaignOnly',
                'ParserVersion': __version__,
                'RouteType': 'Nonstop',
                'SearchEngine': 'Google',
                'SpecialCampaign': 'ATP'}
        self.assertDictEqual(test, Parser(cached=False).parse(r'GS:pt_NB/PANAMA/-ATP.txt'))

    def test_parse_62(self):
        test = {'AirlineCode': 'CM',
                'AirlineName': 'Copa Airlines',
                'CampaignType': 'Non-Brand',
                'Destination': 'Panama',
                'KeywordGroup': 'General',
                'KeywordType': 'Destination',
                'Language': 'pt',
                'MatchType': 'PX',
                'Market': 'BR',
                'MarketingNetwork': 'Search',
                'ParseRegexId': 'CopaNonbrand6-CampaignOnly',
                'ParserVersion': __version__,
                'RouteType': 'Nonstop',
                'SearchEngine': 'Google',
                'SpecialCampaign': 'ATP'}
        self.assertDictEqual(test, Parser(cached=False).parse(r'GS:pt_NB\\PANAMA/-ATP.txt'))

    def test_parse_63(self):
        test = {'AirlineCode': '4O',
                'AirlineName': 'Interjet',
                'CampaignType': 'Non-Brand',
                'Destination': 'ACA',
                'GeoTarget': 'MX',
                'KeywordGroup': 'General',
                'MatchType': 'PX',
                'KeywordType': 'Destination',
                'Language': 'en',
                'Market': 'MX',
                'MarketingNetwork': 'Search',
                'ParseRegexId': 'InterjetDest1',
                'ParserVersion': __version__,
                'RouteType': 'Nonstop',
                'SearchEngine': 'Google'}
        self.assertDictEqual(test, Parser(cached=False).parse('G-MX_NB|Dest=MX>MX [en|Geo:MX]',
                                                              'D|NB_0>Acapulco (en) - All Inclusive',
                                                              airline_code='4O'))

    def test_parse_64(self):
        test = {'AirlineCode': '4O',
                'AirlineName': 'Interjet',
                'CampaignType': 'Non-Brand',
                'Destination': 'MEX',
                'GeoTarget': 'Acapulco',
                'KeywordGroup': 'Deal',
                'KeywordType': 'Destination',
                'Language': 'es',
                'Market': 'MX',
                'MatchType': 'PX',
                'MarketingNetwork': 'Search',
                'Origin': 'ACA',
                'ParseRegexId': 'InterjetDest1',
                'ParserVersion': __version__,
                'RouteType': 'Nonstop',
                'SearchEngine': 'Google'}
        self.assertDictEqual(test, Parser(cached=False).parse('G-MX_NB|Dest=MX>MX [es|Geo:Acapulco]',
                                                              'D|NB_Acapulco>Mexico City-Deal (es) - BMM',
                                                              airline_code='4O'))

    def test_parse_65(self):
        test = {'AirlineCode': '4O',
                'AirlineName': 'Interjet',
                'CampaignType': 'Non-Brand',
                'Destination': 'MEX',
                'GeoTarget': 'New York',
                'KeywordGroup': 'Deal',
                'KeywordType': 'Destination',
                'Language': 'en',
                'LocationType': 'City>Nation',
                'Market': 'US',
                'MarketingNetwork': 'Search',
                'MatchType': 'PX',
                'Origin': 'NYC',
                'ParseRegexId': 'InterjetDest1',
                'ParserVersion': __version__,
                'RouteType': 'Nonstop',
                'SearchEngine': 'Google'}
        self.assertDictEqual(test, Parser(cached=False).parse('G-US_NB|CN-Dest=US>MX [en|Geo:New York]',
                                                              'D|NB_New York>Mexico-Deal (en)',
                                                              airline_code='4O'))

    def test_parse_66(self):
        test = {'AirlineCode': '4O',
                'AirlineName': 'Interjet',
                'CampaignType': 'Hybrid Brand',
                'Destination': 'CUN',
                'GeoTarget': 'GT',
                'KeywordGroup': 'General',
                'KeywordType': 'Route',
                'Language': 'en',
                'Market': 'GT',
                'MarketingNetwork': 'Search',
                'MatchType': 'PX',
                'Origin': 'GUA',
                'ParseRegexId': 'InterjetNonbrand1',
                'ParserVersion': __version__,
                'RouteType': 'Nonstop',
                'SearchEngine': 'Google'}
        self.assertDictEqual(test, Parser(cached=False).parse('G-GT_BRANDHYB|Route=GT>X>MX [en|Geo:GT]',
                                                              'R|BRANDHYB_Guatemala>X>Cancun (es)',
                                                              airline_code='4o'))

    def test_parse_67(self):
        test = {'AirlineCode': '4O',
                'AirlineName': 'Interjet',
                'CampaignType': 'Non-Brand',
                'GeoTarget': 'MX',
                'KeywordGroup': 'Agency',
                'Language': 'en',
                'Destination': '0',
                'Market': 'MX',
                'MarketingNetwork': 'Search',
                'MatchType': 'PX',
                'ParseRegexId': 'InterjetIntertours1',
                'ParserVersion': __version__,
                'RouteType': 'Nonstop',
                'SearchEngine': 'Google'}

        self.assertDictEqual(test, Parser(cached=False).parse('G-MX_NB|00=00>00 [en|Geo:MX]',
                                                              'O|NB_0>0 (en) - Agency',
                                                              airline_code='4o')
                             )

    def test_parse_68(self):
        test = {'AirlineCode': '4O',
                'AirlineName': 'Interjet',
                'CampaignType': 'Non-Brand',
                'GeoTarget': 'MX',
                'KeywordGroup': 'Agency',
                'Destination': '0',
                'Language': 'en',
                'Market': 'MX',
                'Origin': 'ACA',
                'MarketingNetwork': 'Search',
                'MatchType': 'PX',
                'ParseRegexId': 'InterjetIntertours1',
                'ParserVersion': __version__,
                'SearchEngine': 'Google'}

        self.assertDictEqual(test,
                             Parser(cached=False).parse('G-MX_NB|00=MX>00 [en|Geo:MX]', 'O|NB_Acapulco>0 (en) - Agency',
                                                        airline_code='4o'))

    def test_parse_69(self):
        test = {'AirlineCode': '4O',
                'AirlineName': 'Interjet',
                'CampaignType': 'Non-Brand',
                'Destination': 'PVR',
                'GeoTarget': 'GT',
                'KeywordGroup': 'General',
                'KeywordType': 'Route',
                'Language': 'es',
                'Market': 'GT',
                'MarketingNetwork': 'Search',
                'MatchType': 'PX',
                'Origin': 'GUA',
                'ParseRegexId': 'InterjetNonbrand1',
                'ParserVersion': __version__,
                'RouteType': 'Nonstop',
                'SearchEngine': 'Google'}

        self.assertDictEqual(
            test,
            Parser(cached=False).parse(
                'G-GT_NB|Route=GT>X>MX [es|Geo:GT]',
                'R|NB_Guatemala>X>Puerto Vallarta (es)',
                airline_code='4o'
            )
        )

    def test_parse_70(self):
        test = {'AirlineCode': '4O',
                'AirlineName': 'Interjet',
                'KeywordGroup': 'General',
                'GeoTarget': 'Guadalajara',
                'CampaignType': 'Brand',
                'Language': 'es',
                'KeywordType': 'Route',
                'MarketingNetwork': 'Display',
                'MatchType': 'PX',
                'Market': 'MX',
                'ParseRegexId': 'InterjetBrandDisp1',
                'ParserVersion': __version__,
                'RouteType': 'Nonstop',
                'SearchEngine': 'Google'}

        self.assertDictEqual(test, Parser(cached=False).parse(r'G-MX_BRDISP|00=MX [es|Geo:Guadalajara]',
                                                              r'B|DISP > Arts & Entertainment', airline_code='4O'))

    def test_parse_71(self):
        test = {'AirlineCode': '4O',
                'AirlineName': 'Interjet',
                'Audience': '3-10d',
                'CampaignType': 'Non-Brand',
                'GeoTarget': 'MX',
                'KeywordGroup': 'General',
                'KeywordType': 'Route',
                'Language': 'es',
                'Market': 'MX',
                'MarketingNetwork': 'Search',
                'MatchType': 'PX',
                'ParseRegexId': 'InterjetRMK1',
                'ParserVersion': __version__,
                'RouteType': 'Nonstop',
                'SearchEngine': 'Google'}
        self.assertDictEqual(test, Parser(cached=False).parse(r'G-MX_NB|RMKT>MX [es|Geo:MX]',
                                                              r'Passengers minus Payment > 3-10d',
                                                              airline_code='4O'))

    def test_parse_72(self):
        test = {'AirlineCode': '4O',
                'AirlineName': 'Interjet',
                'CampaignType': 'Non-Brand',
                'GeoTarget': 'US',
                'KeywordGroup': 'General',
                'KeywordType': 'Destination',
                'Language': 'en',
                'Market': 'US',
                'MarketingNetwork': 'Display',
                'MatchType': 'PX',
                'ParseRegexId': 'InterjetNBDisp',
                'ParserVersion': __version__,
                'RouteType': 'Nonstop',
                'SearchEngine': 'Google'}
        self.assertDictEqual(test, Parser(cached=False).parse('G-US_NBDISP|Dest=US>MX [en|Geo:US]', 'Interest',
                                                              airline_code='4o'))

    def test_parse_73(self):
        """
        Test against ParserRegexId 'CopaBrand2'.

        :return:
        """
        test = Parser(cached=False).parse(
            campaign_name=r"GS:es-GT_BR\MISSPELLINGS/EX@GT",
            adgroup_name=r"GS:es-GT_BR\MISSPELLINGS/GT@website",
            airline_code="CM",
            return_names=True
        )
        expected = {
            "CampaignName": r"GS:es-GT_BR\MISSPELLINGS/EX@GT",
            "AdGroupName": r"GS:es-GT_BR\MISSPELLINGS/GT@website",
            "CampaignType": "Brand",
            "AirlineName": "Copa Airlines",
            "AirlineCode": "CM",
            "SearchEngine": "Google",
            "Language": "es",
            "Market": "GT",
            "MatchType": "EX",
            "ParseRegexId": "CopaBrand2",
            "ParserVersion": __version__,
            "GeoTarget": "GT",
            "KeywordType": "Modifiers",
            "KeywordGroup": "Website",
            "MarketingNetwork": "Search"
        }
        self.assertDictEqual(
            test, expected
        )

    def test_parse_74(self):
        """
        Test against ParserRegexId 'CopaBrand2'.

        :return:
        """
        test = Parser(cached=False).parse(
            campaign_name=r"GS:es-GT_BR\MISSPELLINGS/EX@GT",
            adgroup_name=r"GS:es-GT_BR\MISSPELLINGS/GT@copa",
            airline_code="CM",
            return_names=True
        )
        expected = {
            "CampaignName": r"GS:es-GT_BR\MISSPELLINGS/EX@GT",
            "AdGroupName": r"GS:es-GT_BR\MISSPELLINGS/GT@copa",
            "CampaignType": "Brand",
            "AirlineName": "Copa Airlines",
            "AirlineCode": "CM",
            "SearchEngine": "Google",
            "Language": "es",
            "Market": "GT",
            "GeoTarget": "GT",
            "MatchType": "EX",
            "ParseRegexId": "CopaBrand2",
            "ParserVersion": __version__,
            "KeywordType": "Core",
            "KeywordGroup": "Misspellings",
            "MarketingNetwork": "Search"
        }
        self.assertDictEqual(
            test, expected
        )

    def test_parse_75(self):
        """
        This entry caused in one case Nonetype returns.
        :return:
        """
        expected = {
            'ParserVersion': __version__,
            'AccountName': '9W_AE (en)',
            'AdGroupName': 'GL:en-AE_NB\\GE=Deals/PH@FR-PS(4-30d)',
            'AirlineName': 'Jet Airways',
            'AirlineCode': '9W',
            'MatchType': 'PH',
            'Language': 'en',
            'Audience': 'FR-PS',
            'CampaignName': 'tCPA_GL:en-AE_NB\\00-Genc=Deals/Geo@AE',
            'CampaignType': 'Generic',
            'GeoTarget': 'AE',
            'KeywordGroup': 'Deals',
            'KeywordType': 'Generic',
            'Market': 'AE',
            'MarketingNetwork': 'RLSA',
            'ParseRegexId': 'JetAirways_tCPA2',
            'SearchEngine': 'Google'
        }
        test_input = {
            'campaignname': 'tCPA_GL:en-AE_NB\\00-Genc=Deals/Geo@AE',
            'adgroupname': 'GL:en-AE_NB\\GE=Deals/PH@FR-PS(4-30d)',
            'accountname': '9W_AE (en)',
            "searchengine": "Google",
            "airlinecode": "9W"
        }
        account_name = test_input["accountname"]
        campaign_name = test_input["campaignname"]
        adgroup_name = test_input["adgroupname"]
        airline_code = test_input["airlinecode"]
        search_engine = test_input["searchengine"]
        final = Parser(cached=False).parse(
            campaign_name=campaign_name,
            airline_code=airline_code,
            adgroup_name=adgroup_name,
            account_name=account_name,
            search_engine=search_engine,
            return_names=True
        )
        self.assertDictEqual(
            expected, final
        )

    def test_parse_76(self):
        """
        Another no-return (originally)
        :return:
        """
        expected = {
            "ParseRegexId": "JetAirways_DSA_OutOfConvention",
            'AccountName': '9W_IN (Dom)',
            'AdGroupName': 'Destination',
            'AirlineCode': '9W',
            'AirlineName': 'Jet Airways',
            'Audience': 'N/A',
            'CampaignName': 'DSA campaign based on Feed',
            'CampaignType': 'N/A',
            'Destination': 'N/A',
            'GeoTarget': 'N/A',
            'KeywordGroup': 'Destination',
            'KeywordType': 'N/A',
            'Language': 'en',
            'LocationType': 'N/A',
            'Market': 'N/A',
            'MarketingNetwork': 'DSA',
            'MatchType': 'PX',
            'Network': 'N/A',
            'Origin': 'N/A',
            'ParserVersion': __version__,
            'RouteLocale': 'N/A',
            'RouteType': 'N/A',
            'SearchEngine': 'Google',
            'SpecialCampaign': 'N/A'
        }
        test_input = {'campaign': 'DSA campaign based on Feed', 'ad_group': 'Destination', 'account': '9W_IN (Dom)'}
        account_name = test_input["account"]
        campaign_name = test_input["campaign"]
        adgroup_name = test_input["ad_group"]
        airline_code = "9W"
        search_engine = "Google"
        final = Parser(cached=False).parse(
            campaign_name=campaign_name,
            airline_code=airline_code,
            adgroup_name=adgroup_name,
            account_name=account_name,
            search_engine=search_engine,
            return_names=True,
            na=True
        )
        self.assertDictEqual(
            expected, final
        )

    def test_parse_77(self):
        """
        Addresses a bug where this campaign/ adgroup combo overwrites and removes the passed in airline code.

        :return:
        """
        campaign_name = "FR_Routes|NB|FR||Greece - Greece"
        adgroup_name = "R|Athens - Paros||"
        account_name = "Aegean Airlines - FR|BE|IT|RW|IE|IL (nl) (fr) (en) (it)"
        expected = {
            "AirlineCode": "A3",
            "AirlineName": "Aegean Airlines",
            "CampaignType": "Non-Brand",
            "Destination": "PAS",
            "KeywordGroup": "General",
            "KeywordType": "Route",
            "Language": "fr",
            "Market": "FR",
            "MarketingNetwork": "Search",
            "MatchType": "PX",
            "Origin": "ATH",
            "ParseRegexId": "AegeanNonBrand3",
            "ParserVersion": __version__,
            "RouteLocale": "Domestic",
            "RouteType": "Nonstop",
            "SearchEngine": "Google"
        }
        test = Parser(cached=False).parse(
            campaign_name=campaign_name,
            adgroup_name=adgroup_name,
            account_name=account_name,
            airline_code="A3"
        )
        self.assertDictEqual(
            test, expected
        )

    def test_parse_78(self):
        """
        Addresses a bug where this campaign/ adgroup combo overwrites and the passed in airline code to 'OA'
        (incorrectly).

        :return:
        """
        campaign_name = "CH_Routes|NB|IT||Greece - Other"
        adgroup_name = "R|Athens - Milan||"
        account_name = "Aegean Airlines - CH|US|SE|DK|CZ (en) (it) (fr) (de) (es)"
        expected = {
            "AirlineCode": "A3",
            "AirlineName": "Aegean Airlines",
            "CampaignType": "Non-Brand",
            "Destination": "BGY",
            "KeywordGroup": "General",
            "KeywordType": "Route",
            "Language": "it",
            "Market": "CH",
            "MarketingNetwork": "Search",
            "MatchType": "PX",
            "Origin": "ATH",
            "ParseRegexId": "AegeanNonBrand3",
            "ParserVersion": __version__,
            "RouteLocale": "International",
            "RouteType": "Nonstop",
            "SearchEngine": "Google"
        }
        test = Parser(cached=False).parse(
            campaign_name=campaign_name,
            adgroup_name=adgroup_name,
            account_name=account_name,
            airline_code="A3"
        )
        self.assertDictEqual(
            test, expected
        )

    def test_parse_79(self):
        """
        Addresses a case where SpecialCampaign is applied to GSP campaigns.

        :return:
        """
        campaign_name = "GE:el-GR_NB\GSP=Promotions/Geo@GR[promo_p2p_allinternational190219]"
        adgroup_name = "GE:el-GR_NB\GSP=Promotions@Keywords"
        account_name = "A3_GSP"
        expected = {
            "GeoTarget": "GR",
            "RouteLocale": "N/A",
            "CampaignName": campaign_name,
            "AdGroupName": adgroup_name,
            "AirlineName": "Aegean Airlines",
            "AirlineCode": "A3",
            "AccountName": account_name,
            "Origin": "N/A",
            "Destination": "N/A",
            "RouteType": "N/A",
            "SearchEngine": "Google",
            "CampaignType": "Non-Brand",
            "Market": "GR",
            "Language": "el",
            "KeywordGroup": "Keywords",
            "KeywordType": "Promotions",
            "Audience": "N/A",
            "SpecialCampaign": "N/A",
            "MarketingNetwork": "GSP",
            "Network": "N/A",
            "LocationType": "N/A",
            "MatchType": "PX",
            'ParseRegexId': 'EveryMundoGSP1',
            "ParserVersion": __version__
        }
        test = Parser(cached=False).parse(
            account_name=account_name,
            campaign_name=campaign_name,
            adgroup_name=adgroup_name,
            airline_code="A3",
            search_engine="Google",
            return_names=True,
            na=True
        )
        self.assertDictEqual(
            test, expected
        )


class TestParserCache(unittest.TestCase):
    """
    Tests the implementation of upsert/cache.
    """

    def __init__(self, *args, **kwargs):
        """
        Declare a 'parser' attribute. (Only declared here to prevent annoying syntax highlighting; this method
        has no functionality).

        :param args:
        :param kwargs:
        :return:
        """
        self.parser = None
        super().__init__(*args, **kwargs)

    def setUp(self):
        """
        Instantiate the parser instance and make available.

        :return:
        """
        self.parser = Parser(cached=False)

    def test_cache_parsing(self):
        """
        Tests that selected for cache does not break the parser.

        This method should be

        :return:
        """
        airline = "Y4"
        account_name = "Volaris Mexico"
        campaign_name = "Branding Campaign - June 28 (in) (was 65)"
        adgroup_name = "Volaris"
        test = self.parser.parse(
            campaign_name=campaign_name,
            adgroup_name=adgroup_name,
            airline_code=airline,
            account_name=account_name,
            return_names=True,
            _cache=True
        )
        expected = {
            "AirlineCode": "Y4",
            "AirlineName": "Volaris",
            "CampaignName": campaign_name,
            "AdGroupName": adgroup_name,
            "AccountName": account_name,
            "Market": "MX",
            "Language": "es",
            "CampaignType": "Brand",
            "KeywordGroup": "Core",
            "KeywordType": "Volaris",
            "ParseRegexId": "VolarisMexicoOldBrand",
            "ParserVersion": __version__,
            "SearchEngine": "Google",
            "MarketingNetwork": "Search"
        }
        self.assertDictEqual(test, expected)

    def test_upsert_exists(self):
        """
        This method should be changed and updated when the upsert/ cache method is the same.

        :return:
        """
        with self.subTest("Returns upsert."):
            self.parser.load_upsert()
            self.assertTrue(self.parser.upsert)
            self.parser.upsert["test_campaign&&test_adgroup"] = {}
        with self.subTest("Saves upsert"):
            self.parser.upsert["test_campaign&&test_adgroup"] = {"test": "value"}
            self.assertFalse(self.parser.dump_upsert())
        with self.subTest("Saved upsert is the same as the loaded upsert."):
            self.parser.load_upsert()
            self.assertDictEqual(
                self.parser.upsert["test_campaign&&test_adgroup"],
                {"test": "value"}
            )


class TestNewClientParsingY4(unittest.TestCase):
    """
    Where TestParsing tests macro-level parsing from existing clients/ accounts, new client's parsing should be tested
    component-wise here.
    """

    def __init__(self, *args, **kwargs):
        """
        Declare a 'parser' attribute. (Only declared here to prevent annoying syntax highlighting; this method
        has no functionality).

        :param args:
        :param kwargs:
        :return:
        """
        self.parser = None
        super().__init__(*args, **kwargs)

    def setUp(self):
        """
        Though it shouldn't be affected, set maxDiff to None (no limit to testing differences of strings in
        self.assertDictEqual).

        Instantiate the parser instance and make available.

        :return:
        """
        self.parser = Parser(cached=False)
        self.maxDiff = None

    def test_ensure_airline_name_with_account_name(self):
        """
        Tests conditions that allow assignment of airline name and code from account name.

        :return:
        """
        ensure_airline_name = self.parser._ensure_airline_name
        input = {}
        with self.subTest("Volaris name from account name"):
            account_name = "Volaris USA"
            test = ensure_airline_name(
                input,
                account_name=account_name
            )
            expected = {
                "AirlineName": "Volaris",
                "AirlineCode": "Y4"
            }
            self.assertDictEqual(
                test,
                expected
            )
        with self.subTest("No given name from account name"):
            account_name = "V0l@r1$"
            test = ensure_airline_name(
                input,
                account_name=account_name
            )
            expected = {
                "AirlineName": None,
                "AirlineCode": None
            }
            self.assertDictEqual(
                test,
                expected
            )
        with self.subTest("No given account name"):
            test = ensure_airline_name(input)
            expected = {
                "AirlineName": None,
                "AirlineCode": None
            }
            self.assertDictEqual(
                test,
                expected
            )

    def test_volaris_mexico_old_brand(self):
        """
        Tests basic volaris logic.
        :return:
        """
        airline = "Y4"
        account_name = "Volaris Mexico"
        campaign_name = "Branding Campaign - June 28 (in) (was 65)"
        with self.subTest("Pure brand adgroup 'Volaris'"):
            adgroup_name = "Volaris"
            test = self.parser.parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                airline_code=airline,
                account_name=account_name,
                return_names=True
            )
            expected = {
                "AirlineCode": "Y4",
                "AirlineName": "Volaris",
                "CampaignName": campaign_name,
                "AdGroupName": adgroup_name,
                "AccountName": account_name,
                "Market": "MX",
                "Language": "es",
                "CampaignType": "Brand",
                "KeywordGroup": "Core",
                "KeywordType": "Volaris",
                "ParseRegexId": "VolarisMexicoOldBrand",
                "ParserVersion": __version__,
                "SearchEngine": "Google",
                "MarketingNetwork": "Search"
            }
            self.assertDictEqual(test, expected)
        with self.subTest("Other brand adgroup - 'Vuelos - Comprar'"):
            adgroup_name = "Vuelos - Comprar"
            test = self.parser.parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                airline_code=airline,
                account_name=account_name,
                return_names=True
            )
            expected = {
                "AirlineCode": "Y4",
                "AirlineName": "Volaris",
                "CampaignName": campaign_name,
                "AdGroupName": adgroup_name,
                "AccountName": account_name,
                "Market": "MX",
                "Language": "es",
                "CampaignType": "Brand",
                "KeywordGroup": "Modifiers",
                "KeywordType": "Flights",
                "ParseRegexId": "VolarisMexicoOldBrand",
                "ParserVersion": __version__,
                "SearchEngine": "Google",
                "MarketingNetwork": "Search"
            }
            self.assertDictEqual(
                test,
                expected
            )
        with self.subTest("Other brand adgroup - 'Boletos - Comprar'"):
            adgroup_name = "Boletos - Comprar"
            test = self.parser.parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                airline_code=airline,
                account_name=account_name,
                return_names=True
            )
            expected = {
                "AirlineCode": "Y4",
                "AirlineName": "Volaris",
                "CampaignName": campaign_name,
                "AdGroupName": adgroup_name,
                "AccountName": account_name,
                "Market": "MX",
                "Language": "es",
                "CampaignType": "Brand",
                "KeywordGroup": "Modifiers",
                "KeywordType": "Tickets",
                "ParseRegexId": "VolarisMexicoOldBrand",
                "ParserVersion": __version__,
                "SearchEngine": "Google",
                "MarketingNetwork": "Search"
            }
            self.assertDictEqual(
                test,
                expected
            )
        with self.subTest("Hybrid brand adgroup - 'Cancún - Brand'"):
            adgroup_name = 'Cancún - Brand'
            test = self.parser.parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                airline_code=airline,
                account_name=account_name,
                return_names=True
            )
            expected = {
                "AirlineCode": "Y4",
                "AirlineName": "Volaris",
                "CampaignName": campaign_name,
                "AdGroupName": adgroup_name,
                "AccountName": account_name,
                "Language": "es",
                "Market": "MX",
                "CampaignType": "Hybrid Brand",
                "Destination": "CUN",
                "KeywordGroup": "General",
                "KeywordType": "Destination",
                "ParseRegexId": "VolarisMexicoOldBrand",
                "ParserVersion": __version__,
                "RouteType": "Nonstop",
                "SearchEngine": "Google",
                "MarketingNetwork": "Search"
            }
            self.assertDictEqual(
                test,
                expected
            )
        with self.subTest("Hybrid brand adgroup - 'Cancún - Brand'"):
            adgroup_name = 'Cancún - Inglés'
            test = self.parser.parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                airline_code=airline,
                account_name=account_name,
                return_names=True
            )
            expected = {
                "AirlineCode": "Y4",
                "AirlineName": "Volaris",
                "CampaignName": campaign_name,
                "AdGroupName": adgroup_name,
                "AccountName": account_name,
                "Language": "en",
                "Market": "MX",
                "CampaignType": "Hybrid Brand",
                "Destination": "CUN",
                "KeywordGroup": "Inglés",
                "KeywordType": "Destination",
                "ParseRegexId": "VolarisMexicoOldBrand",
                "ParserVersion": __version__,
                "RouteType": "Nonstop",
                "SearchEngine": "Google",
                "MarketingNetwork": "Search"
            }
            self.assertDictEqual(
                test,
                expected
            )

    def test_volaris_match_1(self):
        """
        Test that the match VolarisOldBrandLang matches the given adgroups and campaigns.

        :return:
        """
        campaign_adgroup_strings = [
            "E-English Branding&&Volaris_US_EN",
            "E-Spanish Branding&&Volaris_US",
            "E-Spanish Branding&&Volaris_US"
        ]
        for camp_adgp in campaign_adgroup_strings:
            with self.subTest(camp_adgp):
                self.assertTrue(
                    re.match(
                        REGEXES["Volaris"]["VolarisOldBrandLang"],
                        camp_adgp
                    )
                )

    def test_volaris_match_2(self):
        """
        Test that the match VolarisBrandOldGeoTarget matches correctly.

        :return:
        """
        campaign_adgroup_strings = [
            "TEST S-B Branding&&Mispeling",
            "S-B Branding (Chicago)&&Volaris_US",
            "GUA - TEST S-B Branding&&Pasajes",
            "TEST S-B Branding&&Volaris.com"
        ]
        for camp_adgp in campaign_adgroup_strings:
            with self.subTest(camp_adgp):
                self.assertTrue(
                    re.match(
                        REGEXES["Volaris"]["VolarisOldBrandGeoTarget"],
                        camp_adgp
                    )
                )

    def test_volaris_airport_code(self):
        """
        Tests that each of the cities that are given by volaris are giving the correct airport codes.

        :return:
        """
        with self.subTest("VolarisOldNonBrand1, VolarisOldNonBrand2 city names"):
            # Names retrieved from "SF" campaigns.
            expected = {'PVR': 'PVR', 'Queretaro': 'QRO', 'ORD': 'ORD', 'OAK': 'OAK', 'Mexico City': 'MEX',
                        'Phoenix': 'PHX',
                        'Colima': 'CLQ', 'SJC': 'SJC', 'Merida': 'MID', 'Torreon': 'TRC', 'Los Angeles': 'LAX',
                        'Ixtapa': 'ZIH',
                        'San Diego': 'SAN', 'IAH': 'IAH', 'Chihuahua': 'CUU', 'Culiacan': 'CUL', 'MDW': 'MDW',
                        'Mexico': 'MEX',
                        'MEX': 'MEX', 'Acapulco': 'ACA', 'Oaxaca': 'OAX', 'SJO': 'SJO', 'SAL': 'SAL', 'Cozumel': 'CZM',
                        'TGZ': 'TGZ', 'La Paz': 'LAP', 'San Antonio': 'SAT', 'Milwaukee': 'MKE',
                        'Guatemala City': 'GUA',
                        'Huatulco': 'HUX', 'Seattle': 'SEA', 'Tepic': 'TPQ', 'Guadalajara': 'GDL', 'San Juan': 'SJU',
                        'Reno': 'RNO', 'Zacatecas': 'ZCL', 'Aguascalientes': 'AGU', 'Austin': 'AUS', 'Veracruz': 'VER',
                        'Hermosillo': 'HMO', 'Mazatlan': 'MZT', 'Guatemala': 'GUA', 'Leon': 'BJX',
                        'Fort Lauderdale': 'FLL',
                        'Tapachula': 'TAP', 'Ciudad Obregon': 'CEN', 'Tijuana': 'TIJ', 'San Luis Potosi': 'SLP',
                        'Chetumal': 'CTM',
                        'Ontario': 'ONT', 'PDX': 'PDX', 'Houston': 'IAH', 'San Bernardino': 'SBD', 'Las Vegas': 'LAS',
                        'Tampico': 'TAM', 'Los Cabos': 'SJD', 'SJU': 'SJU', 'Cancun': 'CUN', 'Los Mochis': 'LMM',
                        'San Francisco': 'SFO', 'Denver': 'DEN', 'San Salvador': 'SAL', 'Ciudad Juarez': 'CJS',
                        'Reynosa': 'REX',
                        'Dallas': 'DFW', 'Uruapan': 'UPN', 'Toluca': 'TLC', 'Villahermosa': 'VSA', 'Sacramento': 'SMF',
                        'Orlando': 'MCO', 'Puebla': 'PBC', 'CUN': 'CUN', 'DGO': 'DGO', 'New York': 'JFK',
                        'Mexicali': 'MXL',
                        'Oakland': 'OAK', 'Managua': 'MGA', 'Monterrey': 'MTY', 'Fresno': 'FAT', 'Miami': 'MIA',
                        'Morelia': 'MLM'}
            for key, value in expected.items():
                with self.subTest("Cities"):
                    _name = volaris_normalize_city_name(key)
                    test = city_name_to_code(
                        "Y4",
                        _name
                    )
                    if not test:
                        test = _name
                    self.assertEqual(
                        test.upper(),
                        value.upper()
                    )
        with self.subTest("'chicago', 'puerto rice', 'vallarta'"):
            test = {
                volaris_normalize_city_name("chicago"),
                volaris_normalize_city_name("puerto rico"),
                volaris_normalize_city_name("puerto vallarta")
            }
            expected = {
                "ORD", "SJU", "PVR"
            }
            self.assertSetEqual(test, expected)

    def test_volaris_old_non_brand_1(self):
        """
        Case: "SF - Airplane to: San Francisco (GUA)", or, "SF - Route: Chihuahua - mexico city",

        :return:
        """
        parse = self.parser.parse
        parse_regex_id = "VolarisOldNonBrand1"
        with self.subTest("SF - Airplane to: San Francisco (GUA)&&San Francisco"):
            campaign_name = "SF - Airplane to: San Francisco (GUA)"
            adgroup_name = "San Francisco"
            account_name = "Volaris Mexico"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True
            )
            expected = {
                "AccountName": account_name,
                "AdGroupName": adgroup_name,
                "AirlineName": "Volaris",
                "AirlineCode": "Y4",
                "CampaignName": campaign_name,
                "CampaignType": "Non-Brand",
                "Destination": "SFO",
                "GeoTarget": "GT",
                "KeywordGroup": "General",
                "KeywordType": "Destination",
                "Language": "es",
                "Market": "GT",
                "MarketingNetwork": "Search with Display select",
                "ParseRegexId": parse_regex_id,
                "ParserVersion": __version__,
                "RouteType": "Nonstop",
                "SearchEngine": "Google"
            }
            self.assertDictEqual(
                test, expected
            )
        with self.subTest("SF - Airplane to: San Diego&&San Diego"):
            campaign_name = "SF - Airplane to: San Diego"
            adgroup_name = "San Diego"
            account_name = "Volaris Mexico"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True
            )
            expected = {
                "AccountName": account_name,
                "AdGroupName": adgroup_name,
                "AirlineName": "Volaris",
                "AirlineCode": "Y4",
                "CampaignName": campaign_name,
                "CampaignType": "Non-Brand",
                "Destination": "SAN",
                "KeywordGroup": "General",
                "KeywordType": "Destination",
                "Language": "es",
                "Market": "MX",
                "MarketingNetwork": "Search",
                "ParseRegexId": parse_regex_id,
                "ParserVersion": __version__,
                "RouteType": "Nonstop",
                "SearchEngine": "Google"
            }
            self.assertDictEqual(
                test, expected
            )
        with self.subTest("SF - Route: Los Cabos - Toluca&&Los Cabos - Tijuana"):
            campaign_name = "SF - Route: Los Cabos - Toluca"
            adgroup_name = "Los Cabos - Tijuana"
            account_name = "Volaris Mexico"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True
            )
            expected = {
                "AccountName": account_name,
                "AdGroupName": adgroup_name,
                "AirlineName": "Volaris",
                "AirlineCode": "Y4",
                "CampaignName": campaign_name,
                "CampaignType": "Non-Brand",
                "Destination": "TLC",
                "KeywordGroup": "General",
                "KeywordType": "Route",
                "Language": "es",
                "LocationType": "City>City",
                "Market": "MX",
                "MarketingNetwork": "Search with Display select",
                "Origin": "SJD",
                "ParseRegexId": parse_regex_id,
                "ParserVersion": __version__,
                "RouteType": "Nonstop",
                "SearchEngine": "Google"
            }
            self.assertDictEqual(
                test, expected
            )
        with self.subTest("'SF - Route: Los Cabos - Toluca&&Los Cabos - Tijuana' === With N/A"):
            campaign_name = "SF - Route: Los Cabos - Toluca"
            adgroup_name = "Los Cabos - Tijuana"
            account_name = "Volaris Mexico"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True,
                na=True
            )
            expected = {
                "AccountName": account_name,
                "AdGroupName": adgroup_name,
                "AirlineName": "Volaris",
                "AirlineCode": "Y4",
                "Audience": "N/A",
                "CampaignName": campaign_name,
                "CampaignType": "Non-Brand",
                "Destination": "TLC",
                "GeoTarget": "N/A",
                "KeywordGroup": "General",
                "KeywordType": "Route",
                "Language": "es",
                "LocationType": "City>City",
                "Market": "MX",
                "MarketingNetwork": "Search with Display select",
                "Network": "N/A",
                "MatchType": "N/A",
                "Origin": "SJD",
                "ParseRegexId": parse_regex_id,
                "ParserVersion": __version__,
                "RouteLocale": "N/A",
                "RouteType": "Nonstop",
                "SearchEngine": "Google",
                "SpecialCampaign": "N/A"
            }
            self.assertDictEqual(
                test, expected
            )
        with self.subTest("SF - Airplane to: Dallas (USA)&&Dallas"):
            campaign_name = "SF - Airplane to: Dallas (USA)"
            adgroup_name = "San Francisco"
            account_name = "Volaris Costa Rica"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True
            )
            expected = {
                "AccountName": account_name,
                "AdGroupName": adgroup_name,
                "AirlineName": "Volaris",
                "AirlineCode": "Y4",
                "CampaignName": campaign_name,
                "CampaignType": "Non-Brand",
                "Destination": "DFW",
                "GeoTarget": "US",
                "KeywordGroup": "General",
                "KeywordType": "Destination",
                "Language": "es",
                "Market": "US",
                "MarketingNetwork": "Search",
                "ParseRegexId": parse_regex_id,
                "ParserVersion": __version__,
                "RouteType": "Nonstop",
                "SearchEngine": "Google"
            }
            self.assertDictEqual(
                test, expected
            )

    def test_volaris_old_non_brand_2(self):
        """
        Case: "GUA - SF - Airplane to: Dallas", or, "GUA - SF - Route: Guatemala - Guadalajara",

        :return:
        """
        parse = self.parser.parse
        parse_regex_id = "VolarisOldNonBrand2"
        with self.subTest("GUA - SF - Airplane to: Dallas&&Dallas"):
            campaign_name = "GUA - SF - Airplane to: Dallas"
            adgroup_name = "San Francisco"
            account_name = "Volaris Costa Rica"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True
            )
            expected = {
                "AccountName": account_name,
                "AdGroupName": adgroup_name,
                "AirlineName": "Volaris",
                "AirlineCode": "Y4",
                "CampaignName": campaign_name,
                "CampaignType": "Non-Brand",
                "Destination": "DFW",
                "GeoTarget": "GT",
                "KeywordGroup": "General",
                "KeywordType": "Destination",
                "Language": "es",
                "Market": "GT",
                "MarketingNetwork": "Search with Display select",
                "ParseRegexId": parse_regex_id,
                "ParserVersion": __version__,
                "RouteType": "Nonstop",
                "SearchEngine": "Google"
            }
            self.assertDictEqual(
                test, expected
            )
        with self.subTest("GUA - SF - Route: Guatemala - Guadalajara&&Guatemala - Guadalajara"):
            campaign_name = "GUA - SF - Route: Guatemala - Guadalajara"
            adgroup_name = "Guatemala - Guadalajara"
            account_name = "Volaris Costa Rica"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True
            )
            expected = {
                "AccountName": account_name,
                "AdGroupName": adgroup_name,
                "AirlineName": "Volaris",
                "AirlineCode": "Y4",
                "CampaignName": campaign_name,
                "CampaignType": "Non-Brand",
                "Destination": "GDL",
                "GeoTarget": "GT",
                "KeywordGroup": "General",
                "KeywordType": "Route",
                "Language": "es",
                "LocationType": "City>City",
                "Market": "GT",
                "MarketingNetwork": "Search with Display select",
                "Origin": "GUA",
                "ParseRegexId": parse_regex_id,
                "ParserVersion": __version__,
                "RouteType": "Nonstop",
                "SearchEngine": "Google"
            }
            self.assertDictEqual(
                test, expected
            )

    def test_volaris_old_non_brand_3(self):
        """
        Tests another predominant non-brand campaign/adgroup structure.

        S-R SAN&&<Dest>

        :return:
        """
        parse = self.parser.parse
        parse_regex_id = "VolarisOldNonBrand3"
        with self.subTest("S-R SAN&&CUU (conexión)"):
            # US case (with connection)
            account_name = "Volaris USA"
            campaign_name = "S-R SAN"
            adgroup_name = "CUU (conexión)"
            test = parse(
                account_name=account_name,
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                airline_code="Y4",
                return_names=True
            )
            expected = {
                "AccountName": account_name,
                "AdGroupName": adgroup_name,
                "AirlineName": "Volaris",
                "AirlineCode": "Y4",
                "CampaignName": campaign_name,
                "CampaignType": "Non-Brand",
                "Destination": "CUU",
                "GeoTarget": "US",
                "KeywordGroup": "General",
                "KeywordType": "Route",
                "Language": "es",
                "LocationType": "City>City",
                "Market": "US",
                "MarketingNetwork": "Search with Display select",
                "Origin": "SAN",
                "ParseRegexId": parse_regex_id,
                "ParserVersion": __version__,
                "RouteType": "Connecting",
                "SearchEngine": "Google"
            }
            self.assertDictEqual(
                test, expected
            )
        with self.subTest("S-R Guadalajara&&MEX"):
            # Mexico case standard
            account_name = "Volaris Mexico"
            campaign_name = "S-R Guadalajara"
            adgroup_name = "MEX"
            test = parse(
                account_name=account_name,
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                airline_code="Y4",
                return_names=True
            )
            expected = {
                "AccountName": account_name,
                "AdGroupName": adgroup_name,
                "AirlineName": "Volaris",
                "AirlineCode": "Y4",
                "CampaignName": campaign_name,
                "CampaignType": "Non-Brand",
                "Destination": "MEX",
                "GeoTarget": "MX",
                "KeywordGroup": "General",
                "KeywordType": "Route",
                "Language": "es",
                "LocationType": "City>City",
                "Market": "MX",
                "MarketingNetwork": "Search",
                "Origin": "GDL",
                "ParseRegexId": parse_regex_id,
                "ParserVersion": __version__,
                "RouteType": "Nonstop",
                "SearchEngine": "Google"
            }
            self.assertDictEqual(
                test, expected
            )
        with self.subTest("S-R Monterrey NOT&&PVD"):
            # Mexico 'NOT' case
            account_name = "Volaris Mexico"
            campaign_name = "S-R Monterrey NOT"
            adgroup_name = "PVD"
            test = parse(
                account_name=account_name,
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                airline_code="Y4",
                return_names=True
            )
            expected = {
                "AccountName": account_name,
                "AdGroupName": adgroup_name,
                "AirlineName": "Volaris",
                "AirlineCode": "Y4",
                "CampaignName": campaign_name,
                "CampaignType": "Non-Brand",
                "Destination": "PVD",
                "GeoTarget": "MX",
                "KeywordGroup": "General",
                "KeywordType": "Route",
                "Language": "es",
                "LocationType": "City>City",
                "Market": "MX",
                "MarketingNetwork": "Search",
                "Origin": "MTY",
                "ParseRegexId": parse_regex_id,
                "ParserVersion": __version__,
                "RouteType": "Nonstop",
                "SearchEngine": "Google"
            }
            self.assertDictEqual(
                test, expected
            )

    def test_volaris_old_non_brand_4(self):
        """
        Tests against the predominant S-X syntax for destination campaigns.

        Case:

        M-S-D Aguascalientes&&Aguascalientes - Vuelo
        and
        S-D Aguascalientes&&Aguascalientes - Vuelo

        Very similar to S-R and S-B campaigns.

        :return:
        """
        parse = self.parser.parse
        parse_regex_id = "VolarisOldNonBrand4"
        with self.subTest("M-S-D Aguascalientes&&Aguascalientes - Vuelo"):
            account_name = "Volaris Mexico"
            campaign_name = "M-S-D Aguascalientes"
            adgroup_name = "Aguascalientes - Vuelo"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True
            )
            expected = {
                "AccountName": account_name,
                "AdGroupName": adgroup_name,
                "AirlineName": "Volaris",
                "AirlineCode": "Y4",
                "CampaignName": campaign_name,
                "CampaignType": "Non-Brand",
                "Destination": "AGU",
                "GeoTarget": "MX",
                "KeywordGroup": "General",
                "KeywordType": "Destination",
                "Language": "es",
                "Market": "MX",
                "MarketingNetwork": "Search",
                "ParseRegexId": parse_regex_id,
                "ParserVersion": __version__,
                "RouteType": "Nonstop",
                "SearchEngine": "Google"
            }
            self.assertDictEqual(
                test, expected
            )
        with self.subTest("S-D Cancún&&Cancún - Ticket_US"):
            account_name = "Volaris USA"
            campaign_name = "S-D Cancún"
            adgroup_name = "Cancún - Ticket_US"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True
            )
            expected = {
                "AccountName": account_name,
                "AdGroupName": adgroup_name,
                "AirlineName": "Volaris",
                "AirlineCode": "Y4",
                "CampaignName": campaign_name,
                "CampaignType": "Non-Brand",
                "Destination": "CUN",
                "GeoTarget": "US",
                "KeywordGroup": "General",
                "KeywordType": "Destination",
                "Language": "en",
                "Market": "US",
                "MarketingNetwork": "Search",
                "ParseRegexId": parse_regex_id,
                "ParserVersion": __version__,
                "RouteType": "Nonstop",
                "SearchEngine": "Google"
            }
            self.assertDictEqual(
                test, expected
            )
        with self.subTest("TEST S-D México DF&&Distrito Federal - Ofertas"):
            account_name = "Volaris Mexico"
            campaign_name = "TEST S-D México DF"
            adgroup_name = "Distrito Federal - Ofertas"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True
            )
            expected = {
                "AccountName": account_name,
                "AdGroupName": adgroup_name,
                "AirlineName": "Volaris",
                "AirlineCode": "Y4",
                "CampaignName": campaign_name,
                "CampaignType": "Non-Brand",
                "Destination": "MEX",
                "GeoTarget": "MX",
                "KeywordGroup": "General",
                "KeywordType": "Destination",
                "Language": "es",
                "Market": "MX",
                "MarketingNetwork": "Search",
                "ParseRegexId": parse_regex_id,
                "ParserVersion": __version__,
                "RouteType": "Nonstop",
                "SearchEngine": "Google"
            }
            self.assertDictEqual(
                test, expected
            )
        with self.subTest("M-S-D-Iphone-Ipod México D.F&&México D.F - Brand_US"):
            account_name = "Volaris USA"
            campaign_name = "M-S-D-Iphone-Ipod México D.F"
            adgroup_name = "México D.F - Brand_US"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True
            )
            expected = {
                "AccountName": account_name,
                "AdGroupName": adgroup_name,
                "AirlineName": "Volaris",
                "AirlineCode": "Y4",
                "CampaignName": campaign_name,
                "CampaignType": "Hybrid Brand",
                "Destination": "MEX",
                "GeoTarget": "US",
                "KeywordGroup": "General",
                "KeywordType": "Destination",
                "Language": "en",
                "Market": "US",
                "MarketingNetwork": "Search",
                "ParseRegexId": parse_regex_id,
                "ParserVersion": __version__,
                "RouteType": "Nonstop",
                "SearchEngine": "Google"
            }
            self.assertDictEqual(
                test, expected
            )
        with self.subTest("M-S-D-Ipad Morelia&&Morelia - Ticket_US"):
            account_name = "Volaris USA"
            campaign_name = "M-S-D-Ipad Morelia"
            adgroup_name = "Morelia - Ticket_US"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True
            )
            expected = {
                "AccountName": account_name,
                "AdGroupName": adgroup_name,
                "AirlineName": "Volaris",
                "AirlineCode": "Y4",
                "CampaignName": campaign_name,
                "CampaignType": "Non-Brand",
                "Destination": "MLM",
                "GeoTarget": "US",
                "KeywordGroup": "General",
                "KeywordType": "Destination",
                "Language": "en",
                "Market": "US",
                "MarketingNetwork": "Search",
                "ParseRegexId": parse_regex_id,
                "ParserVersion": __version__,
                "RouteType": "Nonstop",
                "SearchEngine": "Google"
            }
            self.assertDictEqual(
                test, expected
            )

    def test_volaris_old_non_brand_5(self):
        """
        Tests an unusual exception to VolarisOldNonBrand4:

        Case:

        :return:
        """
        parse = self.parser.parse
        parse_regex_id = "VolarisOldNonBrand5"
        account_name = "Volaris Mexico"
        campaign_name = "S-D-OAnti-camión"
        with self.subTest("S-D-OAnti-camión&&México DF"):
            adgroup_name = "México DF"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True
            )
            expected = {
                "AccountName": account_name,
                "AdGroupName": adgroup_name,
                "AirlineName": "Volaris",
                "AirlineCode": "Y4",
                "CampaignName": campaign_name,
                "CampaignType": "Generic",
                "Destination": "MEX",
                "GeoTarget": "MX",
                "KeywordGroup": "Destination",
                "KeywordType": "Generic",
                "Language": "es",
                "Market": "MX",
                "MarketingNetwork": "Search",
                "ParseRegexId": parse_regex_id,
                "ParserVersion": __version__,
                "RouteType": "Nonstop",
                "SearchEngine": "Google"
            }
            self.assertDictEqual(
                test, expected
            )
        with self.subTest("S-D-OAnti-camión&&Acapulco"):
            adgroup_name = "Acapulco"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True
            )
            expected = {
                "AccountName": account_name,
                "AdGroupName": adgroup_name,
                "AirlineName": "Volaris",
                "AirlineCode": "Y4",
                "CampaignName": campaign_name,
                "CampaignType": "Generic",
                "Destination": "ACA",
                "GeoTarget": "MX",
                "KeywordGroup": "Destination",
                "KeywordType": "Generic",
                "Language": "es",
                "Market": "MX",
                "MarketingNetwork": "Search",
                "ParseRegexId": parse_regex_id,
                "ParserVersion": __version__,
                "RouteType": "Nonstop",
                "SearchEngine": "Google"
            }
            self.assertDictEqual(
                test, expected
            )

    def test_volaris_old_non_brand_6(self):
        """
        Tests that the match cases for the 'Destino_<Dest>' naming convention pass correctly.

        :return:
        """
        parse = self.parser.parse
        parse_regex_id = "VolarisOldNonBrand6"
        with self.subTest("Destino_Cancun&&Autobuses cancun"):
            account_name = "Bus Switching"
            campaign_name = "Destino_Cancun"
            adgroup_name = "Autobuses cancun"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True
            )
            expected = {
                "AccountName": account_name,
                "AdGroupName": adgroup_name,
                "AirlineName": "Volaris",
                "AirlineCode": "Y4",
                "CampaignName": campaign_name,
                "CampaignType": "Generic",
                "Destination": "CUN",
                "GeoTarget": "MX",
                "KeywordGroup": "Destination",
                "KeywordType": "Generic",
                "Language": "es",
                "Market": "MX",
                "MarketingNetwork": "Search",
                "ParseRegexId": parse_regex_id,
                "ParserVersion": __version__,
                "RouteType": "Nonstop",
                "SearchEngine": "Google"
            }
            self.assertDictEqual(test, expected)
        with self.subTest("Destino_Los_Cabos&&Promociones Boletos Camiones los cabos"):
            account_name = "Bus Switching"
            campaign_name = "Destino_Los_Cabos"
            adgroup_name = "Promociones Boletos Camiones los cabos"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True
            )
            expected = {
                "AccountName": account_name,
                "AdGroupName": adgroup_name,
                "AirlineName": "Volaris",
                "AirlineCode": "Y4",
                "CampaignName": campaign_name,
                "CampaignType": "Generic",
                "Destination": "SJD",
                "GeoTarget": "MX",
                "KeywordGroup": "Destination",
                "KeywordType": "Generic",
                "Language": "es",
                "Market": "MX",
                "MarketingNetwork": "Search",
                "ParseRegexId": parse_regex_id,
                "ParserVersion": __version__,
                "RouteType": "Nonstop",
                "SearchEngine": "Google"
            }
            self.assertDictEqual(test, expected)
        with self.subTest("Destino_SanLuisPotosi&&Autobuses"):
            account_name = "Volaris Mexico"
            campaign_name = "Destino_SanLuisPotosi"
            adgroup_name = "Autobuses"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True
            )
            expected = {
                "AccountName": account_name,
                "AdGroupName": adgroup_name,
                "AirlineName": "Volaris",
                "AirlineCode": "Y4",
                "CampaignName": campaign_name,
                "CampaignType": "Generic",
                "Destination": "SLP",
                "GeoTarget": "MX",
                "KeywordGroup": "Destination",
                "KeywordType": "Generic",
                "Language": "es",
                "Market": "MX",
                "MarketingNetwork": "Search with Display select",
                "ParseRegexId": parse_regex_id,
                "ParserVersion": __version__,
                "RouteType": "Nonstop",
                "SearchEngine": "Google"
            }
            self.assertDictEqual(test, expected)
        with self.subTest("Destinos_Oaxaca&&Autobuses"):
            account_name = "Volaris Mexico"
            campaign_name = "Destinos_Oaxaca"
            adgroup_name = "Autobuses"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True
            )
            expected = {
                "AccountName": account_name,
                "AdGroupName": adgroup_name,
                "AirlineName": "Volaris",
                "AirlineCode": "Y4",
                "CampaignName": campaign_name,
                "CampaignType": "Generic",
                "Destination": "OAX",
                "GeoTarget": "MX",
                "KeywordGroup": "Destination",
                "KeywordType": "Generic",
                "Language": "es",
                "Market": "MX",
                "MarketingNetwork": "Search with Display select",
                "ParseRegexId": parse_regex_id,
                "ParserVersion": __version__,
                "RouteType": "Nonstop",
                "SearchEngine": "Google"
            }
            self.assertDictEqual(test, expected)

    def test_volaris_old_non_brand_7(self):
        """
        Tests the

        'SEM | Destino: <destination> | GEO: <geo target>'

        non brand case.

        (Only appears in 'Volaris Mexico')
        :return:
        """
        parse = self.parser.parse
        parse_regex_id = "VolarisOldNonBrand7"
        account_name = "Volaris Mexico"
        with self.subTest("SEM | Destinos: Mexico DF | GEO: Multiples&&DF | Pasajes - Aéreos Económicos"):
            campaign_name = "SEM | Destinos: Mexico DF | GEO: Multiples"
            adgroup_name = "DF | Pasajes - Aéreos Económicos"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True
            )
            expected = {
                "AccountName": account_name,
                "AdGroupName": adgroup_name,
                "AirlineName": "Volaris",
                "AirlineCode": "Y4",
                "CampaignName": campaign_name,
                "CampaignType": "Non-Brand",
                "Destination": "MEX",
                "GeoTarget": "MX",
                "KeywordGroup": "Pasajes   Aéreos Económicos",
                "KeywordType": "Destination",
                "Language": "es",
                "Market": "MX",
                "MarketingNetwork": "Search",
                "ParseRegexId": parse_regex_id,
                "ParserVersion": __version__,
                "RouteType": "Nonstop",
                "SearchEngine": "Google"
            }
            self.assertDictEqual(
                test, expected
            )
        with self.subTest("SEM | Destinos: Multiples | GEO: Monterrey&&Acapulco | Vuelos - Oferta"):
            # Multiple destinations, fixed geotargeting
            campaign_name = "SEM | Destinos: Multiples | GEO: Monterrey"
            adgroup_name = "Acapulco | Vuelos - Oferta"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True
            )
            expected = {
                "AccountName": account_name,
                "AdGroupName": adgroup_name,
                "AirlineName": "Volaris",
                "AirlineCode": "Y4",
                "CampaignName": campaign_name,
                "CampaignType": "Non-Brand",
                "Destination": "ACA",
                "GeoTarget": "MTY",
                "KeywordGroup": "Vuelos   Oferta",
                "KeywordType": "Destination",
                "Language": "es",
                "Market": "MX",
                "MarketingNetwork": "Search",
                "ParseRegexId": parse_regex_id,
                "ParserVersion": __version__,
                "RouteType": "Nonstop",
                "SearchEngine": "Google"
            }
            self.assertDictEqual(
                test, expected
            )
        with self.subTest("SEM | Destinos: Multiples | GEO: Monterrey&&Chihuahua | Pasajes - Económico"):
            campaign_name = "SEM | Destinos: Multiples | GEO: Monterrey"
            adgroup_name = "Chihuahua | Pasajes - Económico"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True
            )
            expected = {
                "AccountName": account_name,
                "AdGroupName": adgroup_name,
                "AirlineName": "Volaris",
                "AirlineCode": "Y4",
                "CampaignName": campaign_name,
                "CampaignType": "Non-Brand",
                "Destination": "CUU",
                "GeoTarget": "MTY",
                "KeywordGroup": "Pasajes   Económico",
                "KeywordType": "Destination",
                "Language": "es",
                "Market": "MX",
                "MarketingNetwork": "Search",
                "ParseRegexId": parse_regex_id,
                "ParserVersion": __version__,
                "RouteType": "Nonstop",
                "SearchEngine": "Google"
            }
            self.assertDictEqual(
                test, expected
            )

    def test_volaris_old_non_brand_8(self):
        """
        Tests against the

        'SEM | Rutas | GEO: <geotarget>&&<origin>-<destination> | <keyword group>'

        case.

        :return:
        """
        parse = self.parser.parse
        parse_regex_id = "VolarisOldNonBrand8"
        account_name = "Volaris Mexico"
        campaign_name = "SEM | Rutas | GEO: MX"
        with self.subTest("SEM | Rutas | GEO: MX&&Veracruz-Df | Viajes"):
            adgroup_name = "Veracruz-Df | Viajes"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True
            )
            expected = {
                "AccountName": account_name,
                "AdGroupName": adgroup_name,
                "AirlineName": "Volaris",
                "AirlineCode": "Y4",
                "CampaignName": campaign_name,
                "CampaignType": "Non-Brand",
                "Destination": "MEX",
                "GeoTarget": "MX",
                "KeywordGroup": "Viajes",
                "KeywordType": "Route",
                "Language": "es",
                "Market": "MX",
                "MarketingNetwork": "Search",
                "Origin": "VER",
                "ParseRegexId": parse_regex_id,
                "ParserVersion": __version__,
                "RouteType": "Nonstop",
                "SearchEngine": "Google"
            }
            self.assertDictEqual(
                test, expected
            )
        with self.subTest("SEM | Rutas | GEO: MX&&Tampico-Monterrey | Boleto Avion"):
            adgroup_name = "Tampico-Monterrey | Boleto Avion"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True
            )
            expected = {
                "AccountName": account_name,
                "AdGroupName": adgroup_name,
                "AirlineName": "Volaris",
                "AirlineCode": "Y4",
                "CampaignName": campaign_name,
                "CampaignType": "Non-Brand",
                "Destination": "MTY",
                "GeoTarget": "MX",
                "KeywordGroup": "Boleto Avion",
                "KeywordType": "Route",
                "Language": "es",
                "Market": "MX",
                "MarketingNetwork": "Search",
                "Origin": "TAM",
                "ParseRegexId": parse_regex_id,
                "ParserVersion": __version__,
                "RouteType": "Nonstop",
                "SearchEngine": "Google"
            }
            self.assertDictEqual(
                test, expected
            )

    def test_volaris_old_non_brand_9(self):
        """
        Tests against the

        'D-FAT&&GDL'

        case.

        :return:
        """
        parse = self.parser.parse
        parse_regex_id = "VolarisOldNonBrand9"
        account_name = "Volaris USA"
        with self.subTest("D-FAT&&GDL"):
            campaign_name = "D-FAT"
            adgroup_name = "GDL"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True
            )
            expected = {
                "AccountName": account_name,
                "AdGroupName": adgroup_name,
                "AirlineName": "Volaris",
                "AirlineCode": "Y4",
                "CampaignName": campaign_name,
                "CampaignType": "Non-Brand",
                "Destination": "GDL",
                "GeoTarget": "FAT",
                "KeywordGroup": "General",
                "KeywordType": "Route",
                "Language": "en",
                "Market": "US",
                "MarketingNetwork": "Search",
                "Origin": "FAT",
                "ParseRegexId": parse_regex_id,
                "ParserVersion": __version__,
                "RouteType": "Nonstop",
                "SearchEngine": "Google"
            }
            self.assertDictEqual(
                test, expected
            )
        with self.subTest("D-FAT&&Ad group #1"):
            # No destination
            adgroup_name = "Ad group #1"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True
            )
            expected = {
                "AccountName": account_name,
                "AdGroupName": adgroup_name,
                "AirlineName": "Volaris",
                "AirlineCode": "Y4",
                "CampaignName": campaign_name,
                "CampaignType": "Non-Brand",
                "GeoTarget": "FAT",
                "KeywordGroup": "General",
                "KeywordType": "Origin",
                "Language": "en",
                "Market": "US",
                "MarketingNetwork": "Search",
                "Origin": "FAT",
                "ParseRegexId": parse_regex_id,
                "ParserVersion": __version__,
                "RouteType": "Nonstop",
                "SearchEngine": "Google"
            }
            self.assertDictEqual(
                test, expected
            )

    def test_volaris_old_non_brand_10(self):
        """
        Case:

        'SF-Oakland-Cancun_EN'

        :return:
        """
        parse = self.parser.parse
        parse_regex_id = "VolarisOldNonBrand10"
        account_name = "Volaris"
        with self.subTest("SF-Oakland-Cancun-EN&&Vuelos"):
            campaign_name = "SF-Oakland-Cancun-EN"
            adgroup_name = "Vuelos"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True,
                na=True
            )
            expected = {
                'AccountName': account_name,
                'AdGroupName': adgroup_name,
                'AirlineCode': 'Y4',
                'AirlineName': 'Volaris',
                'Audience': 'N/A',
                'CampaignName': campaign_name,
                'CampaignType': 'Non-Brand',
                'Destination': 'CUN',
                'GeoTarget': 'US',
                'KeywordGroup': 'General',
                'KeywordType': 'Route',
                'Language': 'en',
                'LocationType': 'N/A',
                'Market': 'US',
                'MatchType': 'N/A',
                'Network': 'N/A',
                'Origin': 'OAK',
                'MarketingNetwork': 'Search',
                'ParseRegexId': parse_regex_id,
                'ParserVersion': __version__,
                'RouteLocale': 'N/A',
                'RouteType': 'Nonstop',
                'SearchEngine': 'Google',
                'SpecialCampaign': 'N/A'
            }
            self.assertDictEqual(test, expected)
        with self.subTest("SF-Oakland-Cancun-SP&&Vuelos Oakland"):
            campaign_name = "SF-Oakland-Cancun-SP"
            adgroup_name = "Vuelos Oakland"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True,
                na=True
            )
            expected = {
                'AccountName': account_name,
                'AdGroupName': adgroup_name,
                'AirlineCode': 'Y4',
                'AirlineName': 'Volaris',
                'Audience': 'N/A',
                'CampaignName': campaign_name,
                'CampaignType': 'Non-Brand',
                'Destination': 'CUN',
                'GeoTarget': 'US',
                'KeywordGroup': 'General',
                'KeywordType': 'Route',
                'Language': 'es',
                'LocationType': 'N/A',
                'Market': 'US',
                'MatchType': 'N/A',
                'Network': 'N/A',
                'Origin': 'OAK',
                'MarketingNetwork': 'Search',
                'ParseRegexId': parse_regex_id,
                'ParserVersion': __version__,
                'RouteLocale': 'N/A',
                'RouteType': 'Nonstop',
                'SearchEngine': 'Google',
                'SpecialCampaign': 'N/A'
            }
            self.assertDictEqual(test, expected)

    def test_volaris_old_non_brand_11(self):
        """
        Case:

        'Mobile / San Diego_US&&'

        Adgroups in english have: {'Price', 'Brand', 'Ticket', 'Flight', 'Package', 'Attractions'} in adgroup name.
        Adgroups in spanish have: {'Precio', 'Marca', 'Boleto', 'Vuelo', 'Paquete', 'Atracciones'} in adgroup name.
        Geo location is always the Origin and in the campaign name. Only 'Brand' and 'Marca' are Hybrid, rest are
        Non-Brand. Only 'Atracciones'/ 'Attractions' are Generic.

        Both 'Mobile / San Diego_US' and 'San Diego_US' have a GDL route adgroup or two.

        Some have 'Mobile /' prefix, which can be safely be ignored.

        :return:
        """
        parse = self.parser.parse
        parse_regex_id = "VolarisOldNonBrand11"
        account_name = "Volaris USA"
        with self.subTest("San José_US&&San José - Brand_US"):
            # BR en
            campaign_name = "San José_US"
            adgroup_name = "San José - Brand_US"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True,
                na=True
            )
            expected = {
                'AccountName': account_name,
                'AdGroupName': adgroup_name,
                'AirlineCode': 'Y4',
                'AirlineName': 'Volaris',
                'Audience': 'N/A',
                'CampaignName': campaign_name,
                'CampaignType': 'Hybrid Brand',
                'Destination': 'N/A',
                'GeoTarget': 'US',
                'KeywordGroup': 'General',
                'KeywordType': 'Origin',
                'Language': 'en',
                'LocationType': 'N/A',
                'Market': 'US',
                'MatchType': 'N/A',
                'Network': 'N/A',
                'Origin': 'SJC',
                'MarketingNetwork': 'Search',
                'ParseRegexId': parse_regex_id,
                'ParserVersion': __version__,
                'RouteLocale': 'N/A',
                'RouteType': 'N/A',
                'SearchEngine': 'Google',
                'SpecialCampaign': 'N/A'
            }
            self.assertDictEqual(test, expected)
        with self.subTest("San José_US&&San José - Marca_US"):
            # BR es
            campaign_name = "San José_US"
            adgroup_name = "San José - Marca_US"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True,
                na=True
            )
            expected = {
                'AccountName': account_name,
                'AdGroupName': adgroup_name,
                'AirlineCode': 'Y4',
                'AirlineName': 'Volaris',
                'Audience': 'N/A',
                'CampaignName': campaign_name,
                'CampaignType': 'Hybrid Brand',
                'Destination': 'N/A',
                'GeoTarget': 'US',
                'KeywordGroup': 'General',
                'KeywordType': 'Origin',
                'Language': 'es',
                'LocationType': 'N/A',
                'Market': 'US',
                'MatchType': 'N/A',
                'Network': 'N/A',
                'Origin': 'SJC',
                'MarketingNetwork': 'Search',
                'ParseRegexId': parse_regex_id,
                'ParserVersion': __version__,
                'RouteLocale': 'N/A',
                'RouteType': 'N/A',
                'SearchEngine': 'Google',
                'SpecialCampaign': 'N/A'
            }
            self.assertDictEqual(test, expected)
        with self.subTest("Mobile / San Diego_US&&GDL - San Diego_MX"):
            # NB Route es
            campaign_name = "Mobile / San Diego_US"
            adgroup_name = "GDL - San Diego_MX"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True,
                na=True
            )
            expected = {
                'AccountName': account_name,
                'AdGroupName': adgroup_name,
                'AirlineCode': 'Y4',
                'AirlineName': 'Volaris',
                'Audience': 'N/A',
                'CampaignName': campaign_name,
                'CampaignType': 'Non-Brand',
                'Destination': 'GDL',
                'GeoTarget': 'US',
                'KeywordGroup': 'General',
                'KeywordType': 'Route',
                'Language': 'es',
                'LocationType': 'N/A',
                'Market': 'US',
                'MatchType': 'N/A',
                'Network': 'N/A',
                'Origin': 'SAN',
                'MarketingNetwork': 'Search',
                'ParseRegexId': parse_regex_id,
                'ParserVersion': __version__,
                'RouteLocale': 'N/A',
                'RouteType': 'Nonstop',
                'SearchEngine': 'Google',
                'SpecialCampaign': 'N/A'
            }
            self.assertDictEqual(test, expected)
        with self.subTest("San Diego_US&&GDL - San Diego_us"):
            # NB Route en
            campaign_name = "San Diego_US"
            adgroup_name = "GDL - San Diego_us"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True,
                na=True
            )
            expected = {
                'AccountName': account_name,
                'AdGroupName': adgroup_name,
                'AirlineCode': 'Y4',
                'AirlineName': 'Volaris',
                'Audience': 'N/A',
                'CampaignName': campaign_name,
                'CampaignType': 'Non-Brand',
                'Destination': 'GDL',
                'GeoTarget': 'US',
                'KeywordGroup': 'General',
                'KeywordType': 'Route',
                'Language': 'en',
                'LocationType': 'N/A',
                'Market': 'US',
                'MatchType': 'N/A',
                'Network': 'N/A',
                'Origin': 'SAN',
                'MarketingNetwork': 'Search',
                'ParseRegexId': parse_regex_id,
                'ParserVersion': __version__,
                'RouteLocale': 'N/A',
                'RouteType': 'Nonstop',
                'SearchEngine': 'Google',
                'SpecialCampaign': 'N/A'
            }
            self.assertDictEqual(test, expected)
        with self.subTest("San Francisco_US&&San Francisco - Atracciones"):
            # NB Dest Generic
            campaign_name = "San Francisco_US"
            adgroup_name = "San Francisco - Atracciones"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True,
                na=True
            )
            expected = {
                'AccountName': account_name,
                'AdGroupName': adgroup_name,
                'AirlineCode': 'Y4',
                'AirlineName': 'Volaris',
                'Audience': 'N/A',
                'CampaignName': campaign_name,
                'CampaignType': 'Generic',
                'Destination': 'SFO',
                'GeoTarget': 'US',
                'KeywordGroup': 'Attractions',
                'KeywordType': 'Generic',
                'Language': 'es',
                'LocationType': 'N/A',
                'Market': 'US',
                'MatchType': 'N/A',
                'Network': 'N/A',
                'Origin': 'N/A',
                'MarketingNetwork': 'Search',
                'ParseRegexId': parse_regex_id,
                'ParserVersion': __version__,
                'RouteLocale': 'N/A',
                'RouteType': 'N/A',
                'SearchEngine': 'Google',
                'SpecialCampaign': 'N/A'
            }
            self.assertDictEqual(test, expected)
        with self.subTest("San Francisco_US&&San Francisco - Attractions"):
            # NB Dest Generic
            campaign_name = "San Francisco_US"
            adgroup_name = "San Francisco - Attractions"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True,
                na=True
            )
            expected = {
                'AccountName': account_name,
                'AdGroupName': adgroup_name,
                'AirlineCode': 'Y4',
                'AirlineName': 'Volaris',
                'Audience': 'N/A',
                'CampaignName': campaign_name,
                'CampaignType': 'Generic',
                'Destination': 'SFO',
                'GeoTarget': 'US',
                'KeywordGroup': 'Attractions',
                'KeywordType': 'Generic',
                'Language': 'en',
                'LocationType': 'N/A',
                'Market': 'US',
                'MatchType': 'N/A',
                'Network': 'N/A',
                'Origin': 'N/A',
                'MarketingNetwork': 'Search',
                'ParseRegexId': parse_regex_id,
                'ParserVersion': __version__,
                'RouteLocale': 'N/A',
                'RouteType': 'N/A',
                'SearchEngine': 'Google',
                'SpecialCampaign': 'N/A'
            }
            self.assertDictEqual(test, expected)
        with self.subTest("Las Vegas_US&&Las Vegas - Price_US"):
            # NB Origin Generic en
            campaign_name = "Las Vegas_US"
            adgroup_name = "Las Vegas - Price_US"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True,
                na=True
            )
            expected = {
                'AccountName': account_name,
                'AdGroupName': adgroup_name,
                'AirlineCode': 'Y4',
                'AirlineName': 'Volaris',
                'Audience': 'N/A',
                'CampaignName': campaign_name,
                'CampaignType': 'Non-Brand',
                'Destination': 'N/A',
                'GeoTarget': 'US',
                'KeywordGroup': 'General',
                'KeywordType': 'Origin',
                'Language': 'en',
                'LocationType': 'N/A',
                'Market': 'US',
                'MatchType': 'N/A',
                'Network': 'N/A',
                'Origin': 'LAS',
                'MarketingNetwork': 'Search',
                'ParseRegexId': parse_regex_id,
                'ParserVersion': __version__,
                'RouteLocale': 'N/A',
                'RouteType': 'N/A',
                'SearchEngine': 'Google',
                'SpecialCampaign': 'N/A'
            }
            self.assertDictEqual(test, expected)

    def test_volaris_old_non_brand_12(self):
        """
        Another major case.

        Case:
            LosAngeles-Mexicalli&&LosAngeles-Mexicalli
            SanFrancisco-Merida&&SanFrancisco-Merida

        :return:
        """
        parse = self.parser.parse
        parse_regex_id = "VolarisOldNonBrand12"
        account_name = "Volaris"
        with self.subTest("LosAngeles-Mexicalli&&LosAngeles-Mexicalli"):
            # NB Origin Generic en
            campaign_name = "LosAngeles-Mexicalli"
            adgroup_name = "LosAngeles-Mexicalli"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True,
                na=True
            )
            expected = {
                'AccountName': account_name,
                'AdGroupName': adgroup_name,
                'AirlineCode': 'Y4',
                'AirlineName': 'Volaris',
                'Audience': 'N/A',
                'CampaignName': campaign_name,
                'CampaignType': 'Non-Brand',
                'Destination': 'MXL',
                'GeoTarget': 'California',
                'KeywordGroup': 'General',
                'KeywordType': 'Route',
                'Language': 'es',
                'LocationType': 'N/A',
                'Market': 'MX',
                'MatchType': 'N/A',
                'Network': 'N/A',
                'Origin': 'LAX',
                'MarketingNetwork': 'Search',
                'ParseRegexId': parse_regex_id,
                'ParserVersion': __version__,
                'RouteLocale': 'N/A',
                'RouteType': 'Nonstop',
                'SearchEngine': 'Google',
                'SpecialCampaign': 'N/A'
            }
            self.assertDictEqual(test, expected)
        with self.subTest("LosAngeles-culiacan&&LosAngeles-culiacan"):
            # NB Origin Generic en
            campaign_name = "LosAngeles-culiacan"
            adgroup_name = "LosAngeles-culiacan"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True,
                na=True
            )
            expected = {
                'AccountName': account_name,
                'AdGroupName': adgroup_name,
                'AirlineCode': 'Y4',
                'AirlineName': 'Volaris',
                'Audience': 'N/A',
                'CampaignName': campaign_name,
                'CampaignType': 'Non-Brand',
                'Destination': 'CUL',
                'GeoTarget': 'California',
                'KeywordGroup': 'General',
                'KeywordType': 'Route',
                'Language': 'es',
                'LocationType': 'N/A',
                'Market': 'MX',
                'MatchType': 'N/A',
                'Network': 'N/A',
                'Origin': 'LAX',
                'MarketingNetwork': 'Search',
                'ParseRegexId': parse_regex_id,
                'ParserVersion': __version__,
                'RouteLocale': 'N/A',
                'RouteType': 'Nonstop',
                'SearchEngine': 'Google',
                'SpecialCampaign': 'N/A'
            }
            self.assertDictEqual(test, expected)
        with self.subTest("SanFrancisco-La Paz&&SanFrancisco-La Paz"):
            # NB Origin Generic en
            campaign_name = "SanFrancisco-La Paz"
            adgroup_name = "SanFrancisco-La Paz"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True,
                na=True
            )
            expected = {
                'AccountName': account_name,
                'AdGroupName': adgroup_name,
                'AirlineCode': 'Y4',
                'AirlineName': 'Volaris',
                'Audience': 'N/A',
                'CampaignName': campaign_name,
                'CampaignType': 'Non-Brand',
                'Destination': 'LAP',
                'GeoTarget': 'California',
                'KeywordGroup': 'General',
                'KeywordType': 'Route',
                'Language': 'es',
                'LocationType': 'N/A',
                'Market': 'MX',
                'MatchType': 'N/A',
                'Network': 'N/A',
                'Origin': 'SFO',
                'MarketingNetwork': 'Search',
                'ParseRegexId': parse_regex_id,
                'ParserVersion': __version__,
                'RouteLocale': 'N/A',
                'RouteType': 'Nonstop',
                'SearchEngine': 'Google',
                'SpecialCampaign': 'N/A'
            }
            self.assertDictEqual(test, expected)

    def test_volaris_old_non_brand_13(self):
        """
        Only 2 campaigns.

        Case:
            Los Angeles-Cancun-SP&&Spring Break
            Los Angeles-Cancun-EN&&Viajes en Grupo
        :return:
        """
        parse = self.parser.parse
        parse_regex_id = "VolarisOldNonBrand13"
        account_name = "Volaris"
        with self.subTest("Los Angeles-Cancun-SP&&Spring Break"):
            # Destination Campaign
            campaign_name = "Los Angeles-Cancun-SP"
            adgroup_name = "Spring Break"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True,
                na=True
            )
            expected = {
                'AccountName': account_name,
                'AdGroupName': adgroup_name,
                'AirlineCode': 'Y4',
                'AirlineName': 'Volaris',
                'Audience': 'N/A',
                'CampaignName': campaign_name,
                'CampaignType': 'Non-Brand',
                'Destination': 'CUN',
                'GeoTarget': 'LAX',
                'KeywordGroup': 'General',
                'KeywordType': 'Destination',
                'Language': 'en',
                'LocationType': 'N/A',
                'Market': 'US',
                'MatchType': 'N/A',
                'Network': 'N/A',
                'Origin': 'N/A',
                'MarketingNetwork': 'Search',
                'ParseRegexId': parse_regex_id,
                'ParserVersion': __version__,
                'RouteLocale': 'N/A',
                'RouteType': 'Nonstop',
                'SearchEngine': 'Google',
                'SpecialCampaign': 'N/A'
            }
            self.assertDictEqual(test, expected)
        with self.subTest("Los Angeles-Cancun-SP&&English"):
            # Destination Campaign
            campaign_name = "Los Angeles-Cancun-SP"
            adgroup_name = "English"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True,
                na=True
            )
            expected = {
                'AccountName': account_name,
                'AdGroupName': adgroup_name,
                'AirlineCode': 'Y4',
                'AirlineName': 'Volaris',
                'Audience': 'N/A',
                'CampaignName': campaign_name,
                'CampaignType': 'Non-Brand',
                'Destination': 'CUN',
                'GeoTarget': 'LAX',
                'KeywordGroup': 'General',
                'KeywordType': 'Route',
                'Language': 'en',
                'LocationType': 'N/A',
                'Market': 'US',
                'MatchType': 'N/A',
                'Network': 'N/A',
                'Origin': 'LAX',
                'MarketingNetwork': 'Search',
                'ParseRegexId': parse_regex_id,
                'ParserVersion': __version__,
                'RouteLocale': 'N/A',
                'RouteType': 'Nonstop',
                'SearchEngine': 'Google',
                'SpecialCampaign': 'N/A'
            }
            self.assertDictEqual(test, expected)
        with self.subTest("Los Angeles-Cancun-EN&&Carga Aerea"):
            # Destination Campaign
            campaign_name = "Los Angeles-Cancun-EN"
            adgroup_name = "Carga Aerea"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True,
                na=True
            )
            expected = {
                'AccountName': account_name,
                'AdGroupName': adgroup_name,
                'AirlineCode': 'Y4',
                'AirlineName': 'Volaris',
                'Audience': 'N/A',
                'CampaignName': campaign_name,
                'CampaignType': 'Non-Brand',
                'Destination': 'CUN',
                'GeoTarget': 'LAX',
                'KeywordGroup': 'General',
                'KeywordType': 'Destination',
                'Language': 'es',
                'LocationType': 'N/A',
                'Market': 'US',
                'MatchType': 'N/A',
                'Network': 'N/A',
                'Origin': 'N/A',
                'MarketingNetwork': 'Search',
                'ParseRegexId': parse_regex_id,
                'ParserVersion': __version__,
                'RouteLocale': 'N/A',
                'RouteType': 'Nonstop',
                'SearchEngine': 'Google',
                'SpecialCampaign': 'N/A'
            }
            self.assertDictEqual(test, expected)
        with self.subTest("Los Angeles-Cancun-EN&&Viajes en Grupo"):
            # Route Campaign
            campaign_name = "Los Angeles-Cancun-EN"
            adgroup_name = "Viajes en Grupo"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True,
                na=True
            )
            expected = {
                'AccountName': account_name,
                'AdGroupName': adgroup_name,
                'AirlineCode': 'Y4',
                'AirlineName': 'Volaris',
                'Audience': 'N/A',
                'CampaignName': campaign_name,
                'CampaignType': 'Non-Brand',
                'Destination': 'CUN',
                'GeoTarget': 'LAX',
                'KeywordGroup': 'General',
                'KeywordType': 'Route',
                'Language': 'es',
                'LocationType': 'N/A',
                'Market': 'US',
                'MatchType': 'N/A',
                'Network': 'N/A',
                'Origin': 'LAX',
                'MarketingNetwork': 'Search',
                'ParseRegexId': parse_regex_id,
                'ParserVersion': __version__,
                'RouteLocale': 'N/A',
                'RouteType': 'Nonstop',
                'SearchEngine': 'Google',
                'SpecialCampaign': 'N/A'
            }
            self.assertDictEqual(test, expected)

    def test_volaris_old_non_brand_14(self):
        """
        Validate the other NB cases.

        Case:

        :return:
        """
        parse = self.parser.parse
        parse_regex_id = "VolarisOldNonBrand14"
        with self.subTest("Los Cabos&&Aviones"):
            account_name = "Volaris"
            campaign_name = "Los Cabos"
            adgroup_name = "Aviones"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True,
                na=True
            )
            expected = {
                'AccountName': account_name,
                'AdGroupName': adgroup_name,
                'AirlineCode': 'Y4',
                'AirlineName': 'Volaris',
                'Audience': 'N/A',
                'CampaignName': campaign_name,
                'CampaignType': 'Non-Brand',
                'Destination': 'SJD',
                'GeoTarget': 'MX',
                'KeywordGroup': 'General',
                'KeywordType': 'Destination',
                'Language': 'es',
                'LocationType': 'N/A',
                'Market': 'MX',
                'MatchType': 'N/A',
                'Network': 'N/A',
                'Origin': 'N/A',
                'MarketingNetwork': 'Search',
                'ParseRegexId': parse_regex_id,
                'ParserVersion': __version__,
                'RouteLocale': 'N/A',
                'RouteType': 'Nonstop',
                'SearchEngine': 'Google',
                'SpecialCampaign': 'N/A'
            }
            self.assertDictEqual(test, expected)
        with self.subTest("Los Cabos&&los cabos toluca"):
            account_name = "Volaris"
            campaign_name = "Los Cabos"
            adgroup_name = "los cabos toluca"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True,
                na=True
            )
            expected = {
                'AccountName': account_name,
                'AdGroupName': adgroup_name,
                'AirlineCode': 'Y4',
                'AirlineName': 'Volaris',
                'Audience': 'N/A',
                'CampaignName': campaign_name,
                'CampaignType': 'Non-Brand',
                'Destination': 'TLC',
                'GeoTarget': 'MX',
                'KeywordGroup': 'General',
                'KeywordType': 'Route',
                'Language': 'es',
                'LocationType': 'N/A',
                'Market': 'MX',
                'MatchType': 'N/A',
                'Network': 'N/A',
                'Origin': 'SJD',
                'MarketingNetwork': 'Search',
                'ParseRegexId': parse_regex_id,
                'ParserVersion': __version__,
                'RouteLocale': 'N/A',
                'RouteType': 'Nonstop',
                'SearchEngine': 'Google',
                'SpecialCampaign': 'N/A'
            }
            self.assertDictEqual(test, expected)
        with self.subTest("La Paz&&La Paz"):
            account_name = "Volaris"
            campaign_name = "La Paz"
            adgroup_name = "La Paz"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True,
                na=True
            )
            expected = {
                'AccountName': account_name,
                'AdGroupName': adgroup_name,
                'AirlineCode': 'Y4',
                'AirlineName': 'Volaris',
                'Audience': 'N/A',
                'CampaignName': campaign_name,
                'CampaignType': 'Generic',
                'Destination': 'LAP',
                'GeoTarget': 'MX',
                'KeywordGroup': 'Destination',
                'KeywordType': 'Generic',
                'Language': 'es',
                'LocationType': 'N/A',
                'Market': 'MX',
                'MatchType': 'N/A',
                'Network': 'N/A',
                'Origin': 'N/A',
                'MarketingNetwork': 'Search',
                'ParseRegexId': parse_regex_id,
                'ParserVersion': __version__,
                'RouteLocale': 'N/A',
                'RouteType': 'Nonstop',
                'SearchEngine': 'Google',
                'SpecialCampaign': 'N/A'
            }
            self.assertDictEqual(test, expected)
        with self.subTest("CD Mexico&&CD Mexico - DF"):
            campaign_name = "CD Mexico"
            adgroup_name = "CD Mexico - DF"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True,
                na=True
            )
            expected = {
                'AccountName': account_name,
                'AdGroupName': adgroup_name,
                'AirlineCode': 'Y4',
                'AirlineName': 'Volaris',
                'Audience': 'N/A',
                'CampaignName': campaign_name,
                'CampaignType': 'Generic',
                'Destination': 'MEX',
                'GeoTarget': 'MX',
                'KeywordGroup': 'Destination',
                'KeywordType': 'Generic',
                'Language': 'es',
                'LocationType': 'N/A',
                'Market': 'MX',
                'MatchType': 'N/A',
                'Network': 'N/A',
                'Origin': 'N/A',
                'MarketingNetwork': 'Search',
                'ParseRegexId': parse_regex_id,
                'ParserVersion': __version__,
                'RouteLocale': 'N/A',
                'RouteType': 'Nonstop',
                'SearchEngine': 'Google',
                'SpecialCampaign': 'N/A'
            }
            self.assertDictEqual(test, expected)
        with self.subTest("CD Mexico&&Mexico"):
            campaign_name = "CD Mexico"
            adgroup_name = "Mexico"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True,
                na=True
            )
            expected = {
                'AccountName': account_name,
                'AdGroupName': adgroup_name,
                'AirlineCode': 'Y4',
                'AirlineName': 'Volaris',
                'Audience': 'N/A',
                'CampaignName': campaign_name,
                'CampaignType': 'Non-Brand',
                'Destination': 'MEX',
                'GeoTarget': 'MX',
                'KeywordGroup': 'General',
                'KeywordType': 'Destination',
                'Language': 'es',
                'LocationType': 'N/A',
                'Market': 'MX',
                'MatchType': 'N/A',
                'Network': 'N/A',
                'Origin': 'N/A',
                'MarketingNetwork': 'Search',
                'ParseRegexId': parse_regex_id,
                'ParserVersion': __version__,
                'RouteLocale': 'N/A',
                'RouteType': 'Nonstop',
                'SearchEngine': 'Google',
                'SpecialCampaign': 'N/A'
            }
            self.assertDictEqual(test, expected)
        with self.subTest("Acapulco&&Acapulco USA"):
            campaign_name = "Acapulco"
            adgroup_name = "Acapulco USA"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True,
                na=True
            )
            expected = {
                'AccountName': account_name,
                'AdGroupName': adgroup_name,
                'AirlineCode': 'Y4',
                'AirlineName': 'Volaris',
                'Audience': 'N/A',
                'CampaignName': campaign_name,
                'CampaignType': 'Non-Brand',
                'Destination': 'OAK',
                'GeoTarget': 'MX',
                'KeywordGroup': 'General',
                'KeywordType': 'Route',
                'Language': 'es',
                'LocationType': 'N/A',
                'Market': 'MX',
                'MatchType': 'N/A',
                'Network': 'N/A',
                'Origin': 'ACA',
                'MarketingNetwork': 'Search',
                'ParseRegexId': parse_regex_id,
                'ParserVersion': __version__,
                'RouteLocale': 'N/A',
                'RouteType': 'Nonstop',
                'SearchEngine': 'Google',
                'SpecialCampaign': 'N/A'
            }
            self.assertDictEqual(test, expected)
        with self.subTest("Acapulco-Target Acapulco/Tijuana&&Acapulco-Tijuana"):
            campaign_name = "Acapulco-Target Acapulco/Tijuana"
            adgroup_name = "Acapulco-Tijuana"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True,
                na=True
            )
            expected = {
                'AccountName': account_name,
                'AdGroupName': adgroup_name,
                'AirlineCode': 'Y4',
                'AirlineName': 'Volaris',
                'Audience': 'N/A',
                'CampaignName': campaign_name,
                'CampaignType': 'Non-Brand',
                'Destination': 'TIJ',
                'GeoTarget': 'MX',
                'KeywordGroup': 'General',
                'KeywordType': 'Route',
                'Language': 'es',
                'LocationType': 'N/A',
                'Market': 'MX',
                'MatchType': 'N/A',
                'Network': 'N/A',
                'Origin': 'ACA',
                'MarketingNetwork': 'Search',
                'ParseRegexId': parse_regex_id,
                'ParserVersion': __version__,
                'RouteLocale': 'N/A',
                'RouteType': 'Nonstop',
                'SearchEngine': 'Google',
                'SpecialCampaign': 'N/A'
            }
            self.assertDictEqual(test, expected)
        with self.subTest("Zacatecas LAX&&Zacatecas/LA"):
            campaign_name = "Zacatecas LAX"
            adgroup_name = "Zacatecas/LA"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True,
                na=True
            )
            expected = {
                'AccountName': account_name,
                'AdGroupName': adgroup_name,
                'AirlineCode': 'Y4',
                'AirlineName': 'Volaris',
                'Audience': 'N/A',
                'CampaignName': campaign_name,
                'CampaignType': 'Non-Brand',
                'Destination': 'LAX',
                'GeoTarget': 'MX',
                'KeywordGroup': 'General',
                'KeywordType': 'Route',
                'Language': 'es',
                'LocationType': 'N/A',
                'Market': 'MX',
                'MatchType': 'N/A',
                'Network': 'N/A',
                'Origin': 'ZCL',
                'MarketingNetwork': 'Search',
                'ParseRegexId': parse_regex_id,
                'ParserVersion': __version__,
                'RouteLocale': 'N/A',
                'RouteType': 'Nonstop',
                'SearchEngine': 'Google',
                'SpecialCampaign': 'N/A'
            }
            self.assertDictEqual(test, expected)
        with self.subTest("Morelia LAX&&Morelia/LA"):
            campaign_name = "Morelia LAX"
            adgroup_name = "Morelia/LA"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True,
                na=True
            )
            expected = {
                'AccountName': account_name,
                'AdGroupName': adgroup_name,
                'AirlineCode': 'Y4',
                'AirlineName': 'Volaris',
                'Audience': 'N/A',
                'CampaignName': campaign_name,
                'CampaignType': 'Non-Brand',
                'Destination': 'LAX',
                'GeoTarget': 'MX',
                'KeywordGroup': 'General',
                'KeywordType': 'Route',
                'Language': 'es',
                'LocationType': 'N/A',
                'Market': 'MX',
                'MatchType': 'N/A',
                'Network': 'N/A',
                'Origin': 'MLM',
                'MarketingNetwork': 'Search',
                'ParseRegexId': parse_regex_id,
                'ParserVersion': __version__,
                'RouteLocale': 'N/A',
                'RouteType': 'Nonstop',
                'SearchEngine': 'Google',
                'SpecialCampaign': 'N/A'
            }
            self.assertDictEqual(test, expected)
        with self.subTest("Mexico - DF&&Mexico - DF"):
            campaign_name = "Mexico - DF"
            adgroup_name = "Mexico - DF"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True,
                na=True
            )
            expected = {
                'AccountName': account_name,
                'AdGroupName': adgroup_name,
                'AirlineCode': 'Y4',
                'AirlineName': 'Volaris',
                'Audience': 'N/A',
                'CampaignName': campaign_name,
                'CampaignType': 'Generic',
                'Destination': 'MEX',
                'GeoTarget': 'MX',
                'KeywordGroup': 'Destination',
                'KeywordType': 'Generic',
                'Language': 'es',
                'LocationType': 'N/A',
                'Market': 'MX',
                'MatchType': 'N/A',
                'Network': 'N/A',
                'Origin': 'N/A',
                'MarketingNetwork': 'Search',
                'ParseRegexId': parse_regex_id,
                'ParserVersion': __version__,
                'RouteLocale': 'N/A',
                'RouteType': 'Nonstop',
                'SearchEngine': 'Google',
                'SpecialCampaign': 'N/A'
            }
            self.assertDictEqual(test, expected)
        with self.subTest("Pto Vallarta&&Pto Vallarta"):
            campaign_name = "Pto Vallarta"
            adgroup_name = "Pto Vallarta"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True,
                na=True
            )
            expected = {
                'AccountName': account_name,
                'AdGroupName': adgroup_name,
                'AirlineCode': 'Y4',
                'AirlineName': 'Volaris',
                'Audience': 'N/A',
                'CampaignName': campaign_name,
                'CampaignType': 'Generic',
                'Destination': 'PVR',
                'GeoTarget': 'MX',
                'KeywordGroup': 'Destination',
                'KeywordType': 'Generic',
                'Language': 'es',
                'LocationType': 'N/A',
                'Market': 'MX',
                'MatchType': 'N/A',
                'Network': 'N/A',
                'Origin': 'N/A',
                'MarketingNetwork': 'Search',
                'ParseRegexId': parse_regex_id,
                'ParserVersion': __version__,
                'RouteLocale': 'N/A',
                'RouteType': 'Nonstop',
                'SearchEngine': 'Google',
                'SpecialCampaign': 'N/A'
            }
            self.assertDictEqual(test, expected)
        with self.subTest("Pto Vallarta&&Puerto Vallarta tijuana"):
            campaign_name = "Pto Vallarta"
            adgroup_name = "Puerto Vallarta tijuana"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True,
                na=True
            )
            expected = {
                'AccountName': account_name,
                'AdGroupName': adgroup_name,
                'AirlineCode': 'Y4',
                'AirlineName': 'Volaris',
                'Audience': 'N/A',
                'CampaignName': campaign_name,
                'CampaignType': 'Non-Brand',
                'Destination': 'TIJ',
                'GeoTarget': 'MX',
                'KeywordGroup': 'General',
                'KeywordType': 'Route',
                'Language': 'es',
                'LocationType': 'N/A',
                'Market': 'MX',
                'MatchType': 'N/A',
                'Network': 'N/A',
                'Origin': 'PVR',
                'MarketingNetwork': 'Search',
                'ParseRegexId': parse_regex_id,
                'ParserVersion': __version__,
                'RouteLocale': 'N/A',
                'RouteType': 'Nonstop',
                'SearchEngine': 'Google',
                'SpecialCampaign': 'N/A'
            }
            self.assertDictEqual(test, expected)

    def test_volaris_old_brand_lang_1(self):
        """
        Tests the usual cases of parseregexid VolarisOldBrandLand.

        :return:
        """
        parse = self.parser.parse
        campaign_name = "E-English Branding"
        adgroup_name = "Volaris_US_EN"
        account_name = "Volaris USA"
        test = parse(
            campaign_name=campaign_name,
            adgroup_name=adgroup_name,
            airline_code="Y4",
            account_name=account_name,
            return_names=True
        )
        expected = {
            "AirlineCode": "Y4",
            "AirlineName": "Volaris",
            "CampaignName": campaign_name,
            "AdGroupName": adgroup_name,
            "AccountName": account_name,
            "Market": "US",
            "Language": "en",
            "CampaignType": "Brand",
            "KeywordGroup": "Core",
            "KeywordType": "Volaris",
            "ParseRegexId": "VolarisOldBrandLang",
            "ParserVersion": __version__,
            "SearchEngine": "Google",
            "MarketingNetwork": "Search"
        }
        self.assertDictEqual(
            test,
            expected
        )

    def test_volaris_usa_old_brand_lang_2(self):
        """
        Tests the spanish cases of parserregexid VolarisUSAOldBrand
        :return:
        """
        parse = self.parser.parse
        campaign_name = "E-Spanish Branding"
        account_name = "Volaris USA"
        with self.subTest("Volaris_US_ES, US Old Brand"):
            adgroup_name = "Volaris_US_ES"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                airline_code="Y4",
                account_name=account_name,
                return_names=True
            )
            expected = {
                "AirlineCode": "Y4",
                "AirlineName": "Volaris",
                "CampaignName": campaign_name,
                "AdGroupName": adgroup_name,
                "AccountName": account_name,
                "Market": "US",
                "Language": "es",
                "CampaignType": "Brand",
                "KeywordGroup": "Core",
                "KeywordType": "Volaris",
                "ParseRegexId": "VolarisOldBrandLang",
                "ParserVersion": __version__,
                "SearchEngine": "Google",
                "MarketingNetwork": "Search"
            }
            self.assertDictEqual(
                expected,
                test
            )
        with self.subTest("'Volaris Promociones', US Old Brand"):
            adgroup_name = "Volaris Promociones"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                airline_code="Y4",
                account_name=account_name,
                return_names=True
            )
            expected = {
                "AirlineCode": "Y4",
                "AirlineName": "Volaris",
                "CampaignName": campaign_name,
                "AdGroupName": adgroup_name,
                "AccountName": account_name,
                "Market": "US",
                "Language": "es",
                "CampaignType": "Brand",
                "KeywordGroup": "Modifiers",
                "ParseRegexId": "VolarisOldBrandLang",
                "ParserVersion": __version__,
                "SearchEngine": "Google",
                "MarketingNetwork": "Search"
            }
            self.assertDictEqual(
                expected,
                test
            )
        with self.subTest("'Mispeling', US Old Brand"):
            adgroup_name = "Mispeling"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                airline_code="Y4",
                account_name=account_name,
                return_names=True
            )
            expected = {
                "AirlineCode": "Y4",
                "AirlineName": "Volaris",
                "CampaignName": campaign_name,
                "AdGroupName": adgroup_name,
                "AccountName": account_name,
                "Market": "US",
                "Language": "es",
                "CampaignType": "Brand",
                "KeywordGroup": "Core",
                "KeywordType": "Mispellings",
                "ParseRegexId": "VolarisOldBrandLang",
                "ParserVersion": __version__,
                "SearchEngine": "Google",
                "MarketingNetwork": "Search"
            }
            self.assertDictEqual(
                expected,
                test
            )

    def test_volaris_old_brand_geo_target(self):
        """
        Tests that the different ways to match to the ParseRegexId VolarisOldBrandGeoTarget each return correctly.

        :return:
        """
        parse = self.parser.parse
        with self.subTest("GT Old Brand (No Geo) -'TEST S-B Branding' 'Lineas Aereas'"):
            campaign_name = "TEST S-B Branding"
            adgroup_name = "Lineas Aereas"
            account_name = "Volaris Guatemala"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                airline_code="Y4",
                account_name=account_name,
                return_names=True
            )
            expected = {
                "AirlineCode": "Y4",
                "AirlineName": "Volaris",
                "CampaignName": campaign_name,
                "AdGroupName": adgroup_name,
                "AccountName": account_name,
                "Market": "GT",
                "Language": "es",
                "CampaignType": "Brand",
                "KeywordGroup": "Modifiers",
                "ParseRegexId": "VolarisOldBrandGeoTarget",
                "ParserVersion": __version__,
                "SearchEngine": "Google",
                "MarketingNetwork": "Search"
            }
            self.assertDictEqual(
                expected,
                test
            )
        with self.subTest("PR Old Brand - 'TEST S-B Branding' 'Internacionales'"):
            campaign_name = "TEST S-B Branding"
            adgroup_name = "Internacionales"
            account_name = "Volaris Puerto Rico"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                airline_code="Y4",
                account_name=account_name,
                return_names=True
            )
            expected = {
                "AirlineCode": "Y4",
                "AirlineName": "Volaris",
                "CampaignName": campaign_name,
                "AdGroupName": adgroup_name,
                "AccountName": account_name,
                "Market": "PR",
                "Language": "es",
                "CampaignType": "Brand",
                "KeywordGroup": "Modifiers",
                "ParseRegexId": "VolarisOldBrandGeoTarget",
                "ParserVersion": __version__,
                "SearchEngine": "Google",
                "MarketingNetwork": "Search"
            }
            self.assertDictEqual(
                expected,
                test
            )
        with self.subTest("CR Old Brand - 'GUA - TEST S-B Branding' 'Boletos - Baratos'"):
            campaign_name = "GUA - TEST S-B Branding"
            adgroup_name = "Boletos - Baratos"
            account_name = "Volaris Costa Rica"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                airline_code="Y4",
                account_name=account_name,
                return_names=True
            )
            expected = {
                "AirlineCode": "Y4",
                "AirlineName": "Volaris",
                "CampaignName": campaign_name,
                "AdGroupName": adgroup_name,
                "AccountName": account_name,
                "Market": "GT",
                "Language": "es",
                "CampaignType": "Brand",
                "GeoTarget": "GT",
                "KeywordGroup": "Modifiers",
                "ParseRegexId": "VolarisOldBrandGeoTarget",
                "ParserVersion": __version__,
                "SearchEngine": "Google",
                "MarketingNetwork": "Search"
            }
            self.assertDictEqual(
                expected,
                test
            )
        with self.subTest("CR Old Brand - 'TEST S-B Branding Chicago' 'Mispeling'"):
            campaign_name = "TEST S-B Branding Chicago"
            adgroup_name = "Mispeling"
            account_name = "Volaris Costa Rica"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                airline_code="Y4",
                account_name=account_name,
                return_names=True
            )
            expected = {
                "AirlineCode": "Y4",
                "AirlineName": "Volaris",
                "CampaignName": campaign_name,
                "AdGroupName": adgroup_name,
                "AccountName": account_name,
                "Market": "US",
                "Language": "es",
                "CampaignType": "Brand",
                "GeoTarget": "ORD",
                "KeywordGroup": "Core",
                "KeywordType": "Mispellings",
                "ParseRegexId": "VolarisOldBrandGeoTarget",
                "ParserVersion": __version__,
                "SearchEngine": "Google",
                "MarketingNetwork": "Search"
            }
            self.assertDictEqual(
                expected,
                test
            )
        with self.subTest("CR Old Brand - 'TEST S-B Branding Los Angeles' 'Mispeling'"):
            campaign_name = "TEST S-B Branding Los Angeles"
            adgroup_name = "Mispeling"
            account_name = "Volaris Costa Rica"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                airline_code="Y4",
                account_name=account_name,
                return_names=True
            )
            expected = {
                "AirlineCode": "Y4",
                "AirlineName": "Volaris",
                "CampaignName": campaign_name,
                "AdGroupName": adgroup_name,
                "AccountName": account_name,
                "Market": "US",
                "Language": "es",
                "CampaignType": "Brand",
                "GeoTarget": "LAX",
                "KeywordGroup": "Core",
                "KeywordType": "Mispellings",
                "ParseRegexId": "VolarisOldBrandGeoTarget",
                "ParserVersion": __version__,
                "SearchEngine": "Google",
                "MarketingNetwork": "Search"
            }
            self.assertDictEqual(
                expected,
                test
            )
        with self.subTest("'M-B Mobile / Branding', 'Brand'"):
            campaign_name = 'M-B Mobile / Branding'
            adgroup_name = "Brand"
            test = self.parser.parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                airline_code="Y4",
                account_name="Volaris Mexico",
                return_names=True
            )
            expected = {
                "AirlineCode": "Y4",
                "AirlineName": "Volaris",
                "CampaignName": campaign_name,
                "AdGroupName": adgroup_name,
                "AccountName": "Volaris Mexico",
                "Language": "es",
                "Market": "MX",
                "CampaignType": "Brand",
                "KeywordGroup": "Core",
                "KeywordType": "Volaris",
                "ParseRegexId": "VolarisOldBrandGeoTarget",
                "ParserVersion": __version__,
                "SearchEngine": "Google",
                "MarketingNetwork": "Search"
            }
            self.assertDictEqual(
                test,
                expected
            )

    def test_volaris_old_brand_ancillary(self):
        """
        Tests matches against ParseRegexId "VolarisOldBrandAncillary"

        :return:
        """
        parse = self.parser.parse
        account_name = "Volaris Mexico"
        campaign_name = "Branding - already bought"
        adgroup_name = "Compradores"
        test = parse(
            campaign_name=campaign_name,
            adgroup_name=adgroup_name,
            account_name=account_name,
            airline_code="Y4",
            return_names=True
        )
        expected = {
            "AirlineCode": "Y4",
            "AirlineName": "Volaris",
            "CampaignName": campaign_name,
            "AdGroupName": adgroup_name,
            "AccountName": account_name,
            "Market": "MX",
            "Language": "es",
            "CampaignType": "Brand",
            "KeywordGroup": "Ancillary",
            "ParseRegexId": "VolarisOldBrandAncillary",
            "ParserVersion": __version__,
            "SearchEngine": "Google",
            "MarketingNetwork": "Search with Display select"
        }
        self.assertDictEqual(test, expected)

    def test_volaris_old_display_2(self):
        """
        Tests the display network ads of the general form: Content Blast
        :return:
        """
        parse = self.parser.parse
        with self.subTest("'Content Blast Volaris', 'Business'"):
            account_name = "Volaris Content Blast"
            campaign_name = "Content Blast Volaris"
            adgroup_name = "Business"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True
            )
            expected = {
                "AirlineCode": "Y4",
                "AirlineName": "Volaris",
                "CampaignName": campaign_name,
                "AdGroupName": adgroup_name,
                "AccountName": account_name,
                "Market": "MX",
                "Language": "es",
                "CampaignType": "Non-Brand",
                "Audience": "Business",
                "KeywordGroup": "General",
                "ParseRegexId": "VolarisOldDisplay2",
                "ParserVersion": __version__,
                "SearchEngine": "Google",
                "MarketingNetwork": "Display"
            }
            self.assertDictEqual(test, expected)
        with self.subTest("'Blast Chicago', 'Topic Targeting'"):
            campaign_name = "Blast Chicago"
            adgroup_name = "Topic Targeting"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True
            )
            expected = {
                "AirlineCode": "Y4",
                "AirlineName": "Volaris",
                "CampaignName": campaign_name,
                "AdGroupName": adgroup_name,
                "AccountName": account_name,
                "Market": "US",
                "Language": "es",
                "GeoTarget": "ORD",
                "CampaignType": "Non-Brand",
                "Audience": "Topic Targeting",
                "KeywordGroup": "General",
                "ParseRegexId": "VolarisOldDisplay2",
                "ParserVersion": __version__,
                "SearchEngine": "Google",
                "MarketingNetwork": "Display"
            }
            self.assertDictEqual(test, expected)
        with self.subTest("'D-B Blast 02.13 Feb 13 50% & Beda', 'News & Finance ICM'"):
            campaign_name = 'D-B Blast 02.13 Feb 13 50% & Beda'
            adgroup_name = 'News & Finance ICM'
            account_name = 'Volaris Mexico'
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True
            )
            expected = {
                "AirlineCode": "Y4",
                "AirlineName": "Volaris",
                "CampaignName": campaign_name,
                "AdGroupName": adgroup_name,
                "AccountName": account_name,
                "Market": "MX",
                "Language": "es",
                "CampaignType": "Brand",
                "Audience": "News & Finance ICM",
                "KeywordGroup": "General",
                "ParseRegexId": "VolarisOldDisplay2",
                "ParserVersion": __version__,
                "SearchEngine": "Google",
                "MarketingNetwork": "Display"
            }
            self.assertDictEqual(test, expected)
        with self.subTest("'Blast Main - Interests', 'Interests'"):
            campaign_name = 'Blast Main - Interests'
            adgroup_name = 'Interests'
            account_name = 'Volaris Mexico'
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True
            )
            expected = {
                "AirlineCode": "Y4",
                "AirlineName": "Volaris",
                "CampaignName": campaign_name,
                "AdGroupName": adgroup_name,
                "AccountName": account_name,
                "Market": "MX",
                "Language": "es",
                "CampaignType": "Non-Brand",
                "Audience": "Interests",
                "KeywordGroup": "General",
                "ParseRegexId": "VolarisOldDisplay2",
                "ParserVersion": __version__,
                "SearchEngine": "Google",
                "MarketingNetwork": "Display"
            }
            self.assertDictEqual(test, expected)

    def test_volaris_old_display_3(self):
        """
        Tests against the 'Smart (Display)' Campaigns that fit VolarisOldDisplay3

        :return:
        """
        parse = self.parser.parse
        with self.subTest("Smart Display Mexico&&Generica"):
            campaign_name = "Smart Display Mexico"
            adgroup_name = "Generica"
            account_name = "Volaris Mexico"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True
            )
            expected = {
                "AirlineCode": "Y4",
                "AirlineName": "Volaris",
                "CampaignName": campaign_name,
                "AdGroupName": adgroup_name,
                "AccountName": account_name,
                "Market": "MX",
                "Language": "es",
                "KeywordGroup": "Generica",
                "KeywordType": "Smart",
                "ParseRegexId": "VolarisOldDisplay3",
                "ParserVersion": __version__,
                "SearchEngine": "Google",
                "MarketingNetwork": "Display"
            }
            self.assertDictEqual(test, expected)

    def test_volaris_old_display_4(self):
        """
        Tests against the 'Smart (Display)' Campaigns that fit VolarisOldDisplay4 (2da Ola)

        :return:
        """
        parse = self.parser.parse
        with self.subTest("Smart Display Mexico&&"):
            campaign_name = "2da Ola - Quintana Roo"
            adgroup_name = "Quintana Roo"
            account_name = "Volaris Mexico"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True
            )
            expected = {
                "AirlineCode": "Y4",
                "AirlineName": "Volaris",
                "CampaignName": campaign_name,
                "AdGroupName": adgroup_name,
                "AccountName": account_name,
                "Market": "MX",
                "Language": "es",
                "KeywordGroup": "Quintana Roo",
                "KeywordType": "2DaOla",
                "GeoTarget": "Quintana Roo",
                "ParseRegexId": "VolarisOldDisplay4",
                "ParserVersion": __version__,
                "SearchEngine": "Google",
                "MarketingNetwork": "Display"
            }
            self.assertDictEqual(test, expected)

    def test_volaris_old_display_5(self):
        """
        Tests the "Other" display cases. Since these cases defy uniformity in their structures, they are to match an
        explicity series of regex OR cases, where each of these names are written explicitly into the pattern.

        Some of these have GeoTargeting data embedded in them, which should be accounted for.

        Due to their number, this method first checks that all of the applicable campaign names match the pattern and
        are assigned the correct ParseRegexId. Selected subTests afterward are to test that the airline_logic portion
        of the parsing is returned correctly.

        :return:
        """
        parse = self.parser.parse
        with self.subTest("VolarisOldDisplay5: match all campaignnames"):
            # This tests that all the campaign names that should fit this pattern do fit the pattern.
            campaigns = [
                # All of the campaign names
                "Smart Mexico Display",
                "Viaja Gratis Display",
                "Cancún 04Abril",
                "Volaris_Content",
                "Volaris-Guadalajara-Placement_USA",
                "Mkt-Test Case week3",
                "Flighted Campaigns Mexico #2",
                "Masthead 1-September",
                "Promo Negra Mayo 2014",
                "Anticamión",
                "Volaris-Guadalajara-Placement_MEX",
                "Negra 20-23 Junio",
                "Mobile Display",
                "3 Dias - Viaja en Diciembre - Abril 15",
                "499 VClub",
                "Mkt-Test Case week 2 #2",
                "Test | In-Market Interest California #2",
                "Mobile / Travel Eartlink",
                "Promo Negra MEX",
                "Volaris Ventas",
                "Display - Final Junio",
                "GDA California",
                "Test | In-Market Interest California",
                "Test | Select KW California",
                "Promo Negra Junio",
                "Buen Fin | Promodescuentos",
                "D-Campaña-Tijuana2013Junio",
                "Volaris-Guadalajara-Contextual_Mex",
                "Mexico Smart",
                "D-Campaña-Display 2013",
                "Masthead1-SEPT",
                "Mkt-Test Case week 2",
                "Flighted Campaigns Mexico",
                "Negra 20 - 23 Julio",
                "Mkt-Test Case",
                "Volaris Banners",
                "S-O Travel Eartlink",
                "Flighted Campaigns USA",
                "Volaris-Guadalajara-Contextual_USA",
                "Remarketing",
                "Campaign #2",
                "Test | Select KW California #2",
                "Volaris_Content - Promo tarifa Solo Hoy",
            ]
            for campaign_name in campaigns:
                test = {
                    parse(
                        campaign_name=campaign_name,
                        adgroup_name="AnyAdgroup#1",
                        airline_code="Y4"
                    ).get("ParseRegexId")
                }
                if "VolarisOldDisplay5" not in test:
                    raise Exception(campaign_name, "Is not VolarisOldDisplay5")
                self.assertSetEqual(
                    test,
                    {"VolarisOldDisplay5"}
                )
        with self.subTest("GDA California&&California gmail"):
            campaign_name = "GDA California"
            adgroup_name = "California gmail"
            account_name = "Display Volaris"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True
            )
            expected = {
                "AirlineCode": "Y4",
                "AirlineName": "Volaris",
                "CampaignName": campaign_name,
                "AdGroupName": adgroup_name,
                "AccountName": account_name,
                "GeoTarget": "California",
                "Market": "US",
                "Language": "es",
                "KeywordGroup": "General",
                "ParseRegexId": "VolarisOldDisplay5",
                "ParserVersion": __version__,
                "SearchEngine": "Google",
                "MarketingNetwork": "Display"
            }
            self.assertDictEqual(
                test, expected
            )
        with self.subTest("Volaris-Guadalajara-Contextual_USA&&Hotel Playa"):
            campaign_name = "Volaris-Guadalajara-Contextual_USA"
            adgroup_name = "Hotel Playa"
            account_name = "Volaris"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True
            )
            expected = {
                "AirlineCode": "Y4",
                "AirlineName": "Volaris",
                "CampaignName": campaign_name,
                "AdGroupName": adgroup_name,
                "AccountName": account_name,
                "CampaignType": "Non-Brand",
                "Destination": "GDL",
                "GeoTarget": "US",
                "Market": "US",
                "Language": "es",
                "KeywordGroup": "General",
                "KeywordType": "Destination",
                "ParseRegexId": "VolarisOldDisplay5",
                "ParserVersion": __version__,
                "RouteType": "Nonstop",
                "SearchEngine": "Google",
                "MarketingNetwork": "Display"
            }
            self.assertDictEqual(
                test, expected
            )
        with self.subTest("Volaris-Guadalajara-Contextual_Mex&&California gmail"):
            campaign_name = "Volaris-Guadalajara-Contextual_Mex"
            adgroup_name = "Playa"
            account_name = "Volaris"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True
            )
            expected = {
                "AirlineCode": "Y4",
                "AirlineName": "Volaris",
                "CampaignName": campaign_name,
                "AdGroupName": adgroup_name,
                "AccountName": account_name,
                "CampaignType": "Non-Brand",
                "Destination": "GDL",
                "GeoTarget": "MX",
                "Market": "MX",
                "Language": "es",
                "KeywordGroup": "General",
                "KeywordType": "Destination",
                "ParseRegexId": "VolarisOldDisplay5",
                "ParserVersion": __version__,
                "RouteType": "Nonstop",
                "SearchEngine": "Google",
                "MarketingNetwork": "Display"
            }
            self.assertDictEqual(
                test, expected
            )

    def test_volaris_old_display_gsp(self):
        """
        Tests against the "GSP" Campaigns case.

        :return:
        """
        parse = self.parser.parse
        with self.subTest("Prueba GSP FLL&&Ad Group #1"):
            campaign_name = "Prueba gsp FLL"
            adgroup_name = "Ad Group #1"
            account_name = "Display Volaris"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True
            )
            expected = {
                "AirlineCode": "Y4",
                "AirlineName": "Volaris",
                "CampaignName": campaign_name,
                "AdGroupName": adgroup_name,
                "AccountName": account_name,
                "Market": "US",
                "KeywordGroup": "General",
                "Language": "es",
                "MarketingNetwork": "GSP",
                "GeoTarget": "FLL",
                "ParseRegexId": "VolarisOldDisplayGSP",
                "ParserVersion": __version__,
                "SearchEngine": "Google",
            }
            self.assertDictEqual(test, expected)
        with self.subTest("GSP_prueba_Costa_Rica_tiquetes&&Ad Group #1"):
            campaign_name = "GSP_prueba_Costa_Rica_tiquetes"
            adgroup_name = "Ad Group #1"
            account_name = "Display Volaris"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True
            )
            expected = {
                "AirlineCode": "Y4",
                "AirlineName": "Volaris",
                "CampaignName": campaign_name,
                "AdGroupName": adgroup_name,
                "AccountName": account_name,
                "Market": "CR",
                "Language": "es",
                "KeywordGroup": "General",
                "KeywordType": "Tiquetes",
                "MarketingNetwork": "GSP",
                "GeoTarget": "CR",
                "ParseRegexId": "VolarisOldDisplayGSP",
                "ParserVersion": __version__,
                "SearchEngine": "Google",
            }
            self.assertDictEqual(test, expected)

    def test_volaris_old_display_6(self):
        """
        S-O Cases.

        :return:
        """
        parse = self.parser.parse
        parse_regex_id = "VolarisOldDisplay6"
        account_name = "Volaris Mexico"
        with self.subTest("S-O DSA Prueba&&All websites"):
            campaign_name = "S-O DSA Prueba"
            adgroup_name = "All websites"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True,
                na=True
            )
            expected = {
                'AccountName': account_name,
                'AdGroupName': adgroup_name,
                'AirlineCode': 'Y4',
                'AirlineName': 'Volaris',
                'Audience': 'N/A',
                'CampaignName': campaign_name,
                'CampaignType': 'Generic',
                'Destination': 'N/A',
                'GeoTarget': 'MX',
                'KeywordGroup': 'General',
                'KeywordType': 'Generic',
                'Language': 'es',
                'LocationType': 'N/A',
                'Market': 'MX',
                'MatchType': 'N/A',
                'Network': 'N/A',
                'Origin': 'N/A',
                'MarketingNetwork': 'DSA',
                'ParseRegexId': parse_regex_id,
                'ParserVersion': __version__,
                'RouteLocale': 'N/A',
                'RouteType': 'N/A',
                'SearchEngine': 'Google',
                'SpecialCampaign': 'N/A'
            }
            self.assertDictEqual(test, expected)
        with self.subTest("S-O Escápate&&Oferta"):
            campaign_name = "S-O Escápate"
            adgroup_name = "Oferta"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True,
                na=True
            )
            expected = {
                'AccountName': account_name,
                'AdGroupName': adgroup_name,
                'AirlineCode': 'Y4',
                'AirlineName': 'Volaris',
                'Audience': 'N/A',
                'CampaignName': campaign_name,
                'CampaignType': 'Generic',
                'Destination': 'N/A',
                'GeoTarget': 'MX',
                'KeywordGroup': 'General',
                'KeywordType': 'Generic',
                'Language': 'es',
                'LocationType': 'N/A',
                'Market': 'MX',
                'MatchType': 'N/A',
                'Network': 'N/A',
                'Origin': 'N/A',
                'MarketingNetwork': 'Search with Display select',
                'ParseRegexId': parse_regex_id,
                'ParserVersion': __version__,
                'RouteLocale': 'N/A',
                'RouteType': 'N/A',
                'SearchEngine': 'Google',
                'SpecialCampaign': 'N/A'
            }
            self.assertDictEqual(test, expected)
        with self.subTest("M-S-O Escápate&&Vuelo"):
            campaign_name = "M-S-O Escápate"
            adgroup_name = "Vuelo"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True,
                na=True
            )
            expected = {
                'AccountName': account_name,
                'AdGroupName': adgroup_name,
                'AirlineCode': 'Y4',
                'AirlineName': 'Volaris',
                'Audience': 'N/A',
                'CampaignName': campaign_name,
                'CampaignType': 'Generic',
                'Destination': 'N/A',
                'GeoTarget': 'MX',
                'KeywordGroup': 'General',
                'KeywordType': 'Generic',
                'Language': 'es',
                'LocationType': 'N/A',
                'Market': 'MX',
                'MatchType': 'N/A',
                'Network': 'N/A',
                'Origin': 'N/A',
                'MarketingNetwork': 'Search with Display select',
                'ParseRegexId': parse_regex_id,
                'ParserVersion': __version__,
                'RouteLocale': 'N/A',
                'RouteType': 'N/A',
                'SearchEngine': 'Google',
                'SpecialCampaign': 'N/A'
            }
            self.assertDictEqual(test, expected)

    def test_volaris_old_video_1(self):
        """
        Tests that the video network campaigns/ adgroups are parsed correctly.

        This is the more "regular" case of Volaris old video, VolarisOldVideo1.

        :return:
        """
        parse = self.parser.parse
        with self.subTest("Tarifa Limpia | OPT (12)&&Grupo de segmentación 1 (In-Display)"):
            campaign_name = "Tarifa Limpia | OPT (12)"
            adgroup_name = "Grupo de segmentación 1 (In-Display)"
            account_name = "Volaris"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True
            )
            expected = {
                'AccountName': account_name,
                'AdGroupName': adgroup_name,
                'AirlineCode': 'Y4',
                'AirlineName': 'Volaris',
                'CampaignName': campaign_name,
                'KeywordGroup': 'General',
                'Language': 'es',
                'Market': 'MX',
                'MarketingNetwork': 'Video',
                'ParseRegexId': "VolarisOldVideo1",
                'ParserVersion': __version__,
                'SearchEngine': 'Google'
            }
            self.assertDictEqual(
                test, expected
            )
        with self.subTest("YT | Tarifa Limpia | Costa Rica #2 #2 #2 #2&&Videos"):
            campaign_name = "YT | Tarifa Limpia | Costa Rica #2 #2 #2 #2"
            adgroup_name = "Videos"
            account_name = "Display Volaris"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True
            )
            expected = {
                'AccountName': account_name,
                'AdGroupName': adgroup_name,
                'AirlineCode': 'Y4',
                'AirlineName': 'Volaris',
                'CampaignName': campaign_name,
                'GeoTarget': 'CR',
                'KeywordGroup': 'General',
                'Market': 'CR',
                'MarketingNetwork': 'Video',
                'ParseRegexId': "VolarisOldVideo1",
                'ParserVersion': __version__,
                'SearchEngine': 'Google'
            }
            self.assertDictEqual(
                test, expected
            )

    def test_volaris_old_video_2(self):
        """
        Tests that the video network campaigns/ adgroups are parsed correctly.

        This is the more "regular" case of Volaris old video, VolarisOldVideo1.

        :return:
        """
        parse = self.parser.parse
        with self.subTest("US to GDL&&Grupo de segmentación 1 (In-Stream)"):
            campaign_name = "US to GDL"
            adgroup_name = "Grupo de segmentación 1 (In-Stream)"
            account_name = "Volaris"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True
            )
            expected = {
                'AccountName': account_name,
                'AdGroupName': adgroup_name,
                'AirlineCode': 'Y4',
                'AirlineName': 'Volaris',
                'CampaignName': campaign_name,
                "GeoTarget": "US",
                'KeywordGroup': 'General',
                'Language': 'es',
                'Market': 'US',
                'MarketingNetwork': 'Video',
                'ParseRegexId': 'VolarisOldVideo2',
                'ParserVersion': __version__,
                'SearchEngine': 'Google'
            }
            self.assertDictEqual(
                test, expected
            )

    def test_volaris_old_generic_1(self):
        """
        Tests that the matches associated with ParseBatchId 'VolarisOldGeneric' are processed and parsed
        correctly.

        These are conditionally generic or destination based.

        :return:
        """
        parse = self.parser.parse
        with self.subTest("Volaris_Max_Sur de CA - Promo tarifa Solo Hoy"):
            account_name = "Volaris"
            campaign_name = "Volaris_Max_Sur de CA - Promo tarifa Solo Hoy"
            with self.subTest("Volaris_Max_Sur de CA - Promo tarifa Solo Hoy&&Aerolinea"):
                adgroup_name = "Aerolinea"
                test = parse(
                    campaign_name=campaign_name,
                    adgroup_name=adgroup_name,
                    account_name=account_name,
                    airline_code="Y4",
                    return_names=True
                )
                expected = {
                    'AccountName': account_name,
                    'AdGroupName': adgroup_name,
                    'AirlineCode': 'Y4',
                    'AirlineName': 'Volaris',
                    'CampaignName': campaign_name,
                    "CampaignType": "Generic",
                    'GeoTarget': "California",
                    'KeywordGroup': 'General',
                    'KeywordType': "Generic",
                    'Language': "es",
                    'Market': "US",
                    'MarketingNetwork': 'Search with Display select',
                    'ParseRegexId': 'VolarisOldGeneric1',
                    'ParserVersion': __version__,
                    'SearchEngine': 'Google'
                }
                self.assertDictEqual(
                    test, expected
                )
            with self.subTest("Volaris_Max_Sur de CA - Promo tarifa Solo Hoy&&English"):
                adgroup_name = "English"
                test = parse(
                    campaign_name=campaign_name,
                    adgroup_name=adgroup_name,
                    account_name=account_name,
                    airline_code="Y4",
                    return_names=True
                )
                expected = {
                    'AccountName': account_name,
                    'AdGroupName': adgroup_name,
                    'AirlineCode': 'Y4',
                    'AirlineName': 'Volaris',
                    'CampaignName': campaign_name,
                    "CampaignType": "Generic",
                    'GeoTarget': "California",
                    'KeywordGroup': 'General',
                    'KeywordType': "Generic",
                    'Language': "en",
                    'Market': "US",
                    'MarketingNetwork': 'Search with Display select',
                    'ParseRegexId': 'VolarisOldGeneric1',
                    'ParserVersion': __version__,
                    'SearchEngine': 'Google'
                }
                self.assertDictEqual(
                    test, expected
                )
            with self.subTest("Volaris_Max_Sur de CA - Promo tarifa Solo Hoy&&Shuttle San Diego - Tijuana"):
                # This should show as a route campaign
                adgroup_name = "Shuttle San Diego - Tijuana"
                test = parse(
                    campaign_name=campaign_name,
                    adgroup_name=adgroup_name,
                    account_name=account_name,
                    airline_code="Y4",
                    return_names=True
                )
                expected = {
                    'AccountName': account_name,
                    'AdGroupName': adgroup_name,
                    'AirlineCode': 'Y4',
                    'AirlineName': 'Volaris',
                    'CampaignName': campaign_name,
                    "CampaignType": "Non-Brand",
                    "Destination": "TIJ",
                    'GeoTarget': "California",
                    'KeywordGroup': 'General',
                    'KeywordType': "Route",
                    'Language': "es",
                    'Market': "US",
                    'MarketingNetwork': 'Search with Display select',
                    "Origin": "SAN",
                    'ParseRegexId': 'VolarisOldGeneric1',
                    'ParserVersion': __version__,
                    'RouteType': 'Nonstop',
                    'SearchEngine': 'Google'
                }
                self.assertDictEqual(
                    test, expected
                )
            with self.subTest("Volaris_Max_Sur de CA - Promo tarifa Solo Hoy&&DF"):
                # This should show as a destination campaiggn
                adgroup_name = "DF"
                test = parse(
                    campaign_name=campaign_name,
                    adgroup_name=adgroup_name,
                    account_name=account_name,
                    airline_code="Y4",
                    return_names=True
                )
                expected = {
                    'AccountName': account_name,
                    'AdGroupName': adgroup_name,
                    'AirlineCode': 'Y4',
                    'AirlineName': 'Volaris',
                    'CampaignName': campaign_name,
                    "CampaignType": "Non-Brand",
                    "Destination": "MEX",
                    'GeoTarget': "California",
                    'KeywordGroup': 'General',
                    'KeywordType': "Destination",
                    'Language': "es",
                    'Market': "US",
                    'MarketingNetwork': 'Search with Display select',
                    'ParseRegexId': 'VolarisOldGeneric1',
                    'ParserVersion': __version__,
                    'RouteType': 'Nonstop',
                    'SearchEngine': 'Google'
                }
                self.assertDictEqual(
                    test, expected
                )
        with self.subTest("Volaris_Max_Sur de CA"):
            # NB, destination
            account_name = "Volaris"
            campaign_name = "Volaris_Max_Sur de CA"
            with self.subTest("Volaris_Max_Sur de CA&&san diego"):
                adgroup_name = "san diego"
                test = parse(
                    campaign_name=campaign_name,
                    adgroup_name=adgroup_name,
                    account_name=account_name,
                    airline_code="Y4",
                    return_names=True
                )
                expected = {
                    'AccountName': account_name,
                    'AdGroupName': adgroup_name,
                    'AirlineCode': 'Y4',
                    'AirlineName': 'Volaris',
                    'CampaignName': campaign_name,
                    "CampaignType": "Non-Brand",
                    "Destination": "SAN",
                    'GeoTarget': "California",
                    'KeywordGroup': 'General',
                    'KeywordType': "Destination",
                    'Language': "es",
                    'Market': "US",
                    'MarketingNetwork': 'Search with Display select',
                    'ParseRegexId': 'VolarisOldGeneric1',
                    'ParserVersion': __version__,
                    'RouteType': 'Nonstop',
                    'SearchEngine': 'Google'
                }
                self.assertDictEqual(
                    test, expected
                )
            with self.subTest("Volaris_Max_Sur de CA&&toluca la paz"):
                # Should be Generic, NB, en
                adgroup_name = "toluca la paz"
                account_name = "Volaris"
                test = parse(
                    campaign_name=campaign_name,
                    adgroup_name=adgroup_name,
                    account_name=account_name,
                    airline_code="Y4",
                    return_names=True
                )
                expected = {
                    'AccountName': account_name,
                    'AdGroupName': adgroup_name,
                    'AirlineCode': 'Y4',
                    'AirlineName': 'Volaris',
                    'CampaignName': campaign_name,
                    "CampaignType": "Non-Brand",
                    "Destination": "LAP",
                    'GeoTarget': "California",
                    'KeywordGroup': 'General',
                    'KeywordType': "Route",
                    'Language': "es",
                    'Market': "US",
                    'MarketingNetwork': 'Search with Display select',
                    "Origin": "TLC",
                    'ParseRegexId': 'VolarisOldGeneric1',
                    'ParserVersion': __version__,
                    'RouteType': 'Nonstop',
                    'SearchEngine': 'Google'
                }
                self.assertDictEqual(
                    test, expected
                )
            with self.subTest("Volaris_Max_Sur de CA&&Sur de California - 2"):
                # Should be Generic, NB
                adgroup_name = "Sur de California - 2"
                test = parse(
                    campaign_name=campaign_name,
                    adgroup_name=adgroup_name,
                    account_name=account_name,
                    airline_code="Y4",
                    return_names=True
                )
                expected = {
                    'AccountName': account_name,
                    'AdGroupName': adgroup_name,
                    'AirlineCode': 'Y4',
                    'AirlineName': 'Volaris',
                    'CampaignName': campaign_name,
                    "CampaignType": "Generic",
                    'GeoTarget': "California",
                    'KeywordGroup': 'General',
                    'KeywordType': "Generic",
                    'Language': "es",
                    'Market': "US",
                    'MarketingNetwork': 'Search with Display select',
                    'ParseRegexId': 'VolarisOldGeneric1',
                    'ParserVersion': __version__,
                    'SearchEngine': 'Google'
                }
                self.assertDictEqual(
                    test, expected
                )
            with self.subTest("Volaris_Max_Sur de CA&&san diego toluca la paz"):
                # Should raise an error
                adgroup_name = "san diego toluca la paz"
                account_name = "Volaris"
                with self.assertRaises(Exception):
                    test = parse(
                        campaign_name=campaign_name,
                        adgroup_name=adgroup_name,
                        account_name=account_name,
                        airline_code="Y4",
                        return_names=True
                    )
        with self.subTest("Volaris_Max"):
            # Should be Generic, NB, as above, but NOT Display
            account_name = "Volaris"
            campaign_name = "Volaris_Max"
            with self.subTest("Volaris_Max&&San Ysidro"):
                adgroup_name = "San Ysidro"
                test = parse(
                    campaign_name=campaign_name,
                    adgroup_name=adgroup_name,
                    account_name=account_name,
                    airline_code="Y4",
                    return_names=True
                )
                expected = {
                    'AccountName': account_name,
                    'AdGroupName': adgroup_name,
                    'AirlineCode': 'Y4',
                    'AirlineName': 'Volaris',
                    'CampaignName': campaign_name,
                    "CampaignType": "Non-Brand",
                    "Destination": "SAN",
                    'KeywordGroup': 'General',
                    'KeywordType': "Destination",
                    'Language': "es",
                    'Market': "MX",
                    'MarketingNetwork': 'Search',
                    'ParseRegexId': 'VolarisOldGeneric1',
                    'ParserVersion': __version__,
                    'RouteType': 'Nonstop',
                    'SearchEngine': 'Google'
                }
                self.assertDictEqual(
                    test, expected
                )
            with self.subTest("Volaris_Max&&Aeropuertos Max"):
                # Generic, kwtype Aeropuertos
                adgroup_name = "Aeropuertos Max"
                test = parse(
                    campaign_name=campaign_name,
                    adgroup_name=adgroup_name,
                    account_name=account_name,
                    airline_code="Y4",
                    return_names=True
                )
                expected = {
                    'AccountName': account_name,
                    'AdGroupName': adgroup_name,
                    'AirlineCode': 'Y4',
                    'AirlineName': 'Volaris',
                    'CampaignName': campaign_name,
                    "CampaignType": "Generic",
                    'KeywordGroup': 'General',
                    'KeywordType': "Generic",
                    'Language': "es",
                    'Market': "MX",
                    'MarketingNetwork': 'Search',
                    'ParseRegexId': 'VolarisOldGeneric1',
                    'ParserVersion': __version__,
                    'SearchEngine': 'Google'
                }
                self.assertDictEqual(
                    test, expected
                )
            with self.subTest("Volaris_Max&&Volaris Max"):
                # Brand, general
                adgroup_name = "Volaris Max"
                test = parse(
                    campaign_name=campaign_name,
                    adgroup_name=adgroup_name,
                    account_name=account_name,
                    airline_code="Y4",
                    return_names=True
                )
                expected = {
                    'AccountName': account_name,
                    'AdGroupName': adgroup_name,
                    'AirlineCode': 'Y4',
                    'AirlineName': 'Volaris',
                    'CampaignName': campaign_name,
                    "CampaignType": "Brand",
                    'KeywordGroup': 'General',
                    'KeywordType': "Modifiers",
                    'Language': "es",
                    'Market': "MX",
                    'MarketingNetwork': 'Search',
                    'ParseRegexId': 'VolarisOldGeneric1',
                    'ParserVersion': __version__,
                    'SearchEngine': 'Google'
                }
                self.assertDictEqual(
                    test, expected
                )
            with self.subTest("Volaris_Max&&ciudad juarez guadalajara"):
                # NonBrand, Route
                adgroup_name = "ciudad juarez guadalajara"
                test = parse(
                    campaign_name=campaign_name,
                    adgroup_name=adgroup_name,
                    account_name=account_name,
                    airline_code="Y4",
                    return_names=True
                )
                expected = {
                    'AccountName': account_name,
                    'AdGroupName': adgroup_name,
                    'AirlineCode': 'Y4',
                    'AirlineName': 'Volaris',
                    'CampaignName': campaign_name,
                    "CampaignType": "Non-Brand",
                    "Destination": "GDL",
                    'KeywordGroup': 'General',
                    'KeywordType': "Route",
                    'Language': "es",
                    'Market': "MX",
                    'MarketingNetwork': 'Search',
                    'Origin': 'CJS',
                    'ParseRegexId': 'VolarisOldGeneric1',
                    'ParserVersion': __version__,
                    'RouteType': 'Nonstop',
                    'SearchEngine': 'Google'
                }
                self.assertDictEqual(
                    test, expected
                )
            with self.subTest("'Volaris_Max&&' + No AdGroup"):
                # NonBrand, no marketing network (no adgroup)
                test = parse(
                    campaign_name=campaign_name,
                    account_name=account_name,
                    airline_code="Y4",
                    return_names=True
                )
                expected = {
                    'AccountName': account_name,
                    'AirlineCode': 'Y4',
                    'AirlineName': 'Volaris',
                    'CampaignName': campaign_name,
                    "CampaignType": "Non-Brand",
                    'KeywordGroup': 'General',
                    'Language': "es",
                    'Market': "MX",
                    'ParseRegexId': 'VolarisOldGeneric1-CampaignOnly',
                    'ParserV'
                    'ersion': __version__,
                    'SearchEngine': 'Google'
                }
                self.assertDictEqual(
                    test, expected
                )
        with self.subTest("Volaris_Sur de TX"):
            # Much like _Max_Sur de CA
            account_name = "Volaris"
            campaign_name = "Volaris_Sur de TX"
            with self.subTest("Volaris_Sur de CA&&san diego"):
                adgroup_name = "san diego"
                test = parse(
                    campaign_name=campaign_name,
                    adgroup_name=adgroup_name,
                    account_name=account_name,
                    airline_code="Y4",
                    return_names=True
                )
                expected = {
                    'AccountName': account_name,
                    'AdGroupName': adgroup_name,
                    'AirlineCode': 'Y4',
                    'AirlineName': 'Volaris',
                    'CampaignName': campaign_name,
                    "CampaignType": "Non-Brand",
                    "Destination": "SAN",
                    'GeoTarget': "Texas",
                    'KeywordGroup': 'General',
                    'KeywordType': "Destination",
                    'Language': "es",
                    'Market': "US",
                    'MarketingNetwork': 'Search',
                    'ParseRegexId': 'VolarisOldGeneric1',
                    'ParserVersion': __version__,
                    'RouteType': 'Nonstop',
                    'SearchEngine': 'Google'
                }
                self.assertDictEqual(
                    test, expected
                )

    def test_volaris_old_generic_2(self):
        """
        Tests that the matches associated with ParseBatchId 'VolarisOldGeneric2' are processed and parsed
        correctly.

        :return:
        """
        parse = self.parser.parse
        with self.subTest("Volaris&&Volaris"):
            # Should be Generic, NB
            account_name = "Volaris"
            campaign_name = "Volaris"
            adgroup_name = "volaris"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True
            )
            expected = {
                'AccountName': account_name,
                'AdGroupName': adgroup_name,
                'AirlineCode': 'Y4',
                'AirlineName': 'Volaris',
                'CampaignName': campaign_name,
                'CampaignType': 'Generic',
                'KeywordGroup': 'General',
                'KeywordType': 'Generic',
                'Language': 'es',
                'Market': 'MX',
                'MarketingNetwork': 'Search with Display select',
                'ParseRegexId': 'VolarisOldGeneric2',
                'ParserVersion': __version__,
                'SearchEngine': 'Google'
            }
            self.assertDictEqual(
                test, expected
            )
        with self.subTest("Volaris Chicago México&&México Boletos"):
            # Geo@ORD, Destination to Mexico, NB, Generic
            # Should be Generic, NB
            campaign_name = "Volaris Chicago Hispanos"
            adgroup_name = "Agencias Hispanos"
            account_name = "Volaris Chicago"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True
            )
            expected = {
                'AccountName': account_name,
                'AdGroupName': adgroup_name,
                'AirlineCode': 'Y4',
                'AirlineName': 'Volaris',
                'CampaignName': campaign_name,
                'CampaignType': 'Generic',
                'GeoTarget': 'ORD',
                'KeywordGroup': 'General',
                'KeywordType': 'Generic',
                'Language': "es",
                'Market': 'US',
                'MarketingNetwork': 'Search with Display select',
                'ParseRegexId': 'VolarisOldGeneric2',
                'ParserVersion': __version__,
                'SearchEngine': 'Google'
            }
            self.assertDictEqual(
                test, expected
            )
        with self.subTest("Destinos_Otros_Top&&Boletos de autobuses"):
            # Should be Generic, NB
            campaign_name = "Destinos_Otros_Top"
            adgroup_name = "Boletos de autobuses"
            account_name = "Volaris Mexico"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True
            )
            expected = {
                'AccountName': account_name,
                'AdGroupName': adgroup_name,
                'AirlineCode': 'Y4',
                'AirlineName': 'Volaris',
                'CampaignName': campaign_name,
                'CampaignType': 'Generic',
                'KeywordGroup': 'General',
                'KeywordType': 'Generic',
                'Language': 'es',
                'Market': 'MX',
                'MarketingNetwork': 'Search with Display select',
                'ParseRegexId': 'VolarisOldGeneric2',
                'ParserVersion': __version__,
                'SearchEngine': 'Google'
            }
            self.assertDictEqual(
                test, expected
            )
        with self.subTest("Volaris Chicago Hispanos&&Viajes Hispanos"):
            # Should be Generic, NB
            campaign_name = "Volaris Chicago Hispanos"
            adgroup_name = "Viajes Hispanos"
            account_name = "Volaris Chicago"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True
            )
            expected = {
                'AccountName': account_name,
                'AdGroupName': adgroup_name,
                'AirlineCode': 'Y4',
                'AirlineName': 'Volaris',
                'CampaignName': campaign_name,
                'CampaignType': 'Generic',
                'GeoTarget': 'ORD',
                'KeywordGroup': 'General',
                'KeywordType': 'Generic',
                'Language': 'es',
                'Market': 'US',
                'MarketingNetwork': 'Search with Display select',
                'ParseRegexId': 'VolarisOldGeneric2',
                'ParserVersion': __version__,
                'SearchEngine': 'Google'
            }
            self.assertDictEqual(
                test, expected
            )
        with self.subTest("Volaris Chicago Inglés&&Viajes Inglés"):
            # Should be Generic, NB, en
            campaign_name = "Volaris Chicago Inglés"
            adgroup_name = "Viajes Inglés"
            account_name = "Volaris Chicago"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True
            )
            expected = {
                'AccountName': account_name,
                'AdGroupName': adgroup_name,
                'AirlineCode': 'Y4',
                'AirlineName': 'Volaris',
                'CampaignName': campaign_name,
                'CampaignType': 'Generic',
                'GeoTarget': 'ORD',
                'KeywordGroup': 'General',
                'KeywordType': 'Generic',
                'Language': 'en',
                'Market': 'US',
                'MarketingNetwork': 'Search with Display select',
                'ParseRegexId': 'VolarisOldGeneric2',
                'ParserVersion': __version__,
                'SearchEngine': 'Google'
            }
            self.assertDictEqual(
                test, expected
            )
        with self.subTest("Aniversario&&Aniversario_2011"):
            # Should be Generic, NB. Adgroups are 'Aniversario' or 'Aniversario_2011'
            campaign_name = "Aniversario"
            adgroup_name = "Aniversario_2011"
            account_name = "Volaris"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True
            )
            expected = {
                'AccountName': account_name,
                'AdGroupName': adgroup_name,
                'AirlineCode': 'Y4',
                'AirlineName': 'Volaris',
                'CampaignName': campaign_name,
                'CampaignType': 'Generic',
                'KeywordGroup': 'General',
                'KeywordType': 'Generic',
                'Language': 'es',
                'Market': 'MX',
                'MarketingNetwork': 'Search with Display select',
                'ParseRegexId': 'VolarisOldGeneric2',
                'ParserVersion': __version__,
                'SearchEngine': 'Google'
            }
            self.assertDictEqual(
                test, expected
            )
        with self.subTest("Navidad&&regalos urgentes navidad"):
            # Should be Generic, NB, en
            campaign_name = "Navidad"
            adgroup_name = "regalos urgentes navidad"
            account_name = "Volaris"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True
            )
            expected = {
                'AccountName': account_name,
                'AdGroupName': adgroup_name,
                'AirlineCode': 'Y4',
                'AirlineName': 'Volaris',
                'CampaignName': campaign_name,
                'CampaignType': 'Generic',
                'KeywordGroup': 'General',
                'KeywordType': 'Generic',
                'Language': 'es',
                'Market': 'MX',
                'MarketingNetwork': 'Search with Display select',
                'ParseRegexId': 'VolarisOldGeneric2',
                'ParserVersion': __version__,
                'SearchEngine': 'Google'
            }
            self.assertDictEqual(
                test, expected
            )

    def test_volaris_old_generic_3(self):
        """
        Case: 'Genéricos_Futura&&Autobuses', or,
        'Genericas_Omnibus&&Venta de Boletos', or,
        'Genericas_Bus&&Boletos Bus'

        :return:
        """
        parse = self.parser.parse
        parse_regex_id = "VolarisOldGeneric3"
        with self.subTest("Genéricos_Futura&&Autobuses"):
            campaign_name = "Genéricos_Futura"
            adgroup_name = "Autobuses"
            account_name = "Volaris Mexico"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True
            )
            expected = {
                'AccountName': account_name,
                'AdGroupName': adgroup_name,
                'AirlineCode': 'Y4',
                'AirlineName': 'Volaris',
                'CampaignName': campaign_name,
                'CampaignType': 'Generic',
                'KeywordGroup': 'General',
                'KeywordType': 'Generic',
                'Language': 'es',
                'Market': 'MX',
                'MarketingNetwork': 'Search',
                'ParseRegexId': parse_regex_id,
                'ParserVersion': __version__,
                'SearchEngine': 'Google'
            }
            self.assertDictEqual(
                test, expected
            )
        with self.subTest("Genéricas_Omnibus&&Venta de Boletos"):
            campaign_name = "Genéricas_Omnibus"
            adgroup_name = "Venta de Boletos"
            account_name = "Volaris Mexico"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True
            )
            expected = {
                'AccountName': account_name,
                'AdGroupName': adgroup_name,
                'AirlineCode': 'Y4',
                'AirlineName': 'Volaris',
                'CampaignName': campaign_name,
                'CampaignType': 'Generic',
                'KeywordGroup': 'General',
                'KeywordType': 'Generic',
                'Language': 'es',
                'Market': 'MX',
                'MarketingNetwork': 'Search',
                'ParseRegexId': parse_regex_id,
                'ParserVersion': __version__,
                'SearchEngine': 'Google'
            }
            self.assertDictEqual(
                test, expected
            )
        with self.subTest("Genericas_Bus&&Boletos Bus"):
            campaign_name = "Genericas_Bus"
            adgroup_name = "Boletos Bus"
            account_name = "Volaris Mexico"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True
            )
            expected = {
                'AccountName': account_name,
                'AdGroupName': adgroup_name,
                'AirlineCode': 'Y4',
                'AirlineName': 'Volaris',
                'CampaignName': campaign_name,
                'CampaignType': 'Generic',
                'KeywordGroup': 'General',
                'KeywordType': 'Generic',
                'Language': 'es',
                'Market': 'MX',
                'MarketingNetwork': 'Search',
                'ParseRegexId': parse_regex_id,
                'ParserVersion': __version__,
                'SearchEngine': 'Google'
            }
            self.assertDictEqual(
                test, expected
            )

    def test_volaris_old_generic_4(self):
        """
        Case:

        'M-G Genérico&&Genérico - Boleto'
        'E-Generic&&Generic_US'
        etc

        :return:
        """
        parse = self.parser.parse
        parse_regex_id = "VolarisOldGeneric4"
        with self.subTest("E-Generic&&Generic_US"):
            account_name = "Volaris USA"
            campaign_name = "E-Generic"
            adgroup_name = "Generic_US"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True
            )
            expected = {
                'AccountName': account_name,
                'AdGroupName': adgroup_name,
                'AirlineCode': 'Y4',
                'AirlineName': 'Volaris',
                'CampaignName': campaign_name,
                'CampaignType': 'Generic',
                'KeywordGroup': 'General',
                'KeywordType': 'Generic',
                'Language': 'en',
                'Market': 'US',
                'MarketingNetwork': 'Search',
                'ParseRegexId': parse_regex_id,
                'ParserVersion': __version__,
                'SearchEngine': 'Google'
            }
            self.assertDictEqual(
                test, expected
            )
        with self.subTest("M-G Genérico&&Genérico - Boleto"):
            account_name = "Volaris Mexico"
            campaign_name = "M-G Genérico"
            adgroup_name = "Genérico - Boleto"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True
            )
            expected = {
                'AccountName': account_name,
                'AdGroupName': adgroup_name,
                'AirlineCode': 'Y4',
                'AirlineName': 'Volaris',
                'CampaignName': campaign_name,
                'CampaignType': 'Generic',
                'KeywordGroup': 'General',
                'KeywordType': 'Generic',
                'Language': 'es',
                'Market': 'MX',
                'MarketingNetwork': 'Search',
                'ParseRegexId': parse_regex_id,
                'ParserVersion': __version__,
                'SearchEngine': 'Google'
            }
            self.assertDictEqual(
                test, expected
            )
        with self.subTest("M-S-G-Ipod-Iphone Generic&&Generic - Brand_US"):
            account_name = "Volaris USA"
            campaign_name = "M-S-G-Ipod-Iphone Generic"
            adgroup_name = "Generic - Brand_US"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True
            )
            expected = {
                'AccountName': account_name,
                'AdGroupName': adgroup_name,
                'AirlineCode': 'Y4',
                'AirlineName': 'Volaris',
                'CampaignName': campaign_name,
                'CampaignType': 'Generic',
                'KeywordGroup': 'General',
                'KeywordType': 'Generic',
                'Language': 'en',
                'Market': 'US',
                'MarketingNetwork': 'Search',
                'ParseRegexId': parse_regex_id,
                'ParserVersion': __version__,
                'SearchEngine': 'Google'
            }
            self.assertDictEqual(
                test, expected
            )
        with self.subTest("M-S-G-Ipad Generic&&Generic - Brand_US"):
            account_name = "Volaris USA"
            campaign_name = "M-S-G-Ipad Generic"
            adgroup_name = "Generic - Brand_US"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True
            )
            expected = {
                'AccountName': account_name,
                'AdGroupName': adgroup_name,
                'AirlineCode': 'Y4',
                'AirlineName': 'Volaris',
                'CampaignName': campaign_name,
                'CampaignType': 'Generic',
                'KeywordGroup': 'General',
                'KeywordType': 'Generic',
                'Language': 'en',
                'Market': 'US',
                'MarketingNetwork': 'Search',
                'ParseRegexId': parse_regex_id,
                'ParserVersion': __version__,
                'SearchEngine': 'Google'
            }
            self.assertDictEqual(
                test, expected
            )

    def test_volaris_old_competitors(self):
        """
        Competition.

        :return:
        """
        parse = self.parser.parse
        parse_regex_id = "VolarisOldCompetitors"
        with self.subTest("Competencia&&VivaAerobus"):
            account_name = "Volaris Mexico"
            campaign_name = "Competencia"
            adgroup_name = "VivaAerobus"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True
            )
            expected = {
                'AccountName': account_name,
                'AdGroupName': adgroup_name,
                'AirlineCode': 'Y4',
                'AirlineName': 'Volaris',
                'CampaignName': campaign_name,
                'CampaignType': 'Generic',
                'KeywordGroup': 'Competitors',
                'KeywordType': 'Generic',
                'Language': 'es',
                'Market': 'MX',
                'MarketingNetwork': 'Search',
                'ParseRegexId': parse_regex_id,
                'ParserVersion': __version__,
                'SearchEngine': 'Google'
            }
            self.assertDictEqual(
                test, expected
            )

    def test_volaris_vclub(self):
        """
        Tests the one Vclub case:

        'VClub&&Volaris Club'

        :return:
        """
        parse = self.parser.parse
        parse_regex_id = "VolarisVClub"
        account_name = "VClub Volaris"
        campaign_name = "Vclub"
        adgroup_name = "Volaris Club"
        test = parse(
            campaign_name=campaign_name,
            adgroup_name=adgroup_name,
            account_name=account_name,
            airline_code="Y4",
            return_names=True
        )
        expected = {
            'AccountName': account_name,
            'AdGroupName': adgroup_name,
            'AirlineCode': 'Y4',
            'AirlineName': 'Volaris',
            'CampaignName': campaign_name,
            'CampaignType': 'Brand',
            'KeywordGroup': 'Rewards',
            'KeywordType': 'Modifiers',
            'Language': 'es',
            'Market': 'MX',
            'MarketingNetwork': 'Search',
            'ParseRegexId': parse_regex_id,
            'ParserVersion': __version__,
            'SearchEngine': 'Google'
        }
        self.assertDictEqual(test, expected)

    def test_volaris_carga(self):
        """
        Tests the limited cases for VolarisCarga

        :return:
        """
        parse = self.parser.parse
        parse_regex_id = "VolarisCarga"
        account_name = "Volaris Carga"
        with self.subTest("Volaris Encarga&&desde"):
            campaign_name = "Volaris Encarga"
            adgroup_name = "desde"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True
            )
            expected = {
                'AccountName': account_name,
                'AdGroupName': adgroup_name,
                'AirlineCode': 'Y4',
                'AirlineName': 'Volaris',
                'CampaignName': campaign_name,
                'CampaignType': 'Generic',
                'KeywordGroup': 'Encargas',
                'KeywordType': 'Generic',
                'Language': 'es',
                'Market': 'MX',
                'MarketingNetwork': 'Search',
                'ParseRegexId': parse_regex_id,
                'ParserVersion': __version__,
                'SearchEngine': 'Google'
            }
            self.assertDictEqual(test, expected)
        with self.subTest("Volaris Encarga&&Estados Unidos"):
            campaign_name = "Volaris Encarga"
            adgroup_name = "Estados Unidos"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True
            )
            expected = {
                'AccountName': account_name,
                'AdGroupName': adgroup_name,
                'AirlineCode': 'Y4',
                'AirlineName': 'Volaris',
                'CampaignName': campaign_name,
                'CampaignType': 'Generic',
                'KeywordGroup': 'Encargas',
                'KeywordType': 'Generic',
                'Language': 'es',
                'Market': 'MX',
                'MarketingNetwork': 'Search',
                'ParseRegexId': parse_regex_id,
                'ParserVersion': __version__,
                'SearchEngine': 'Google'
            }
            self.assertDictEqual(test, expected)

    def test_volaris_app(self):
        """
        Tests matches of the app-download campaigns.

        :return:
        """
        parse = self.parser.parse
        parse_regex_id = "VolarisAppDownload"
        account_name = "Aplicación Volaris"
        with self.subTest("Volaris Android App - Universal Download&&"):
            campaign_name = "Volaris Android App - Universal Download"
            adgroup_name = ""
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True
            )
            expected = {
                'AccountName': account_name,
                'AirlineCode': 'Y4',
                'AirlineName': 'Volaris',
                'CampaignName': campaign_name,
                'CampaignType': 'Generic',
                'GeoTarget': 'MX',
                'KeywordGroup': 'App Download',
                'KeywordType': "Generic",
                'Language': 'es',
                'Market': 'MX',
                'MarketingNetwork': 'Universal App Download',
                'ParseRegexId': parse_regex_id + "-CampaignOnly",
                'ParserVersion': __version__,
                'SearchEngine': 'Google'
            }
            self.assertDictEqual(test, expected)
        with self.subTest("Volaris Android App -Universal Download&&"):
            campaign_name = "Volaris Android App -Universal Download"
            adgroup_name = ""
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True
            )
            expected = {
                'AccountName': account_name,
                'AirlineCode': 'Y4',
                'AirlineName': 'Volaris',
                'CampaignName': campaign_name,
                'CampaignType': 'Generic',
                'GeoTarget': 'MX',
                'KeywordGroup': 'App Download',
                'KeywordType': "Generic",
                'Language': 'es',
                'Market': 'MX',
                'MarketingNetwork': 'Universal App Download',
                'ParseRegexId': parse_regex_id + "-CampaignOnly",
                'ParserVersion': __version__,
                'SearchEngine': 'Google'
            }
            self.assertDictEqual(test, expected)
        with self.subTest("Mobile App (Search) Ipod - Iphone&&Branding"):
            campaign_name = "Mobile App (Search) Ipod - Iphone"
            adgroup_name = "Branding"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True
            )
            expected = {
                'AccountName': account_name,
                'AdGroupName': adgroup_name,
                'AirlineCode': 'Y4',
                'AirlineName': 'Volaris',
                'CampaignName': campaign_name,
                'CampaignType': 'Brand',
                'GeoTarget': 'MX',
                'KeywordGroup': 'App Download',
                'KeywordType': 'Modifiers',
                'Language': 'es',
                'Market': 'MX',
                'MarketingNetwork': 'Search',
                'ParseRegexId': parse_regex_id,
                'ParserVersion': __version__,
                'SearchEngine': 'Google'
            }
            self.assertDictEqual(test, expected)
        with self.subTest("Mobile App (Search) Ipad&&Anuncios Ipad"):
            campaign_name = "Mobile App (Search) Ipad"
            adgroup_name = "Anuncios Ipad"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True
            )
            expected = {
                'AccountName': account_name,
                'AdGroupName': adgroup_name,
                'AirlineCode': 'Y4',
                'AirlineName': 'Volaris',
                'CampaignName': campaign_name,
                'CampaignType': 'Generic',
                'GeoTarget': 'MX',
                'KeywordGroup': 'App Download',
                'KeywordType': 'Generic',
                'Language': 'es',
                'Market': 'MX',
                'MarketingNetwork': 'Search',
                'ParseRegexId': parse_regex_id,
                'ParserVersion': __version__,
                'SearchEngine': 'Google'
            }
            self.assertDictEqual(test, expected)
        with self.subTest("Mobile App (Search) Android&&Anuncios Android"):
            campaign_name = "Mobile App (Search) Android"
            adgroup_name = "Anuncios Android"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True
            )
            expected = {
                'AccountName': account_name,
                'AdGroupName': adgroup_name,
                'AirlineCode': 'Y4',
                'AirlineName': 'Volaris',
                'CampaignName': campaign_name,
                'CampaignType': 'Generic',
                'GeoTarget': 'MX',
                'KeywordGroup': 'App Download',
                'KeywordType': 'Generic',
                'Language': 'es',
                'Market': 'MX',
                'MarketingNetwork': 'Search',
                'ParseRegexId': parse_regex_id,
                'ParserVersion': __version__,
                'SearchEngine': 'Google'
            }
            self.assertDictEqual(test, expected)
        with self.subTest("Volaris Android App - Search - Branded&&Branded"):
            campaign_name = "Volaris Android App - Search - Branded"
            adgroup_name = "Branded"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True
            )
            expected = {
                'AccountName': account_name,
                'AdGroupName': adgroup_name,
                'AirlineCode': 'Y4',
                'AirlineName': 'Volaris',
                'CampaignName': campaign_name,
                'CampaignType': 'Brand',
                'GeoTarget': 'MX',
                'KeywordGroup': 'App Download',
                'KeywordType': 'Modifiers',
                'Language': 'es',
                'Market': 'MX',
                'MarketingNetwork': 'Search',
                'ParseRegexId': parse_regex_id,
                'ParserVersion': __version__,
                'SearchEngine': 'Google'
            }
            self.assertDictEqual(test, expected)
        with self.subTest("Volaris Android App - Search - Competition Terms&&Viajes"):
            campaign_name = "Volaris Android App - Search - Competition Terms"
            adgroup_name = "Viajes"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True
            )
            expected = {
                'AccountName': account_name,
                'AdGroupName': adgroup_name,
                'AirlineCode': 'Y4',
                'AirlineName': 'Volaris',
                'CampaignName': campaign_name,
                'CampaignType': 'Non-Brand',
                'GeoTarget': 'MX',
                'KeywordGroup': 'App Download',
                'KeywordType': 'Competitors',
                'Language': 'es',
                'Market': 'MX',
                'MarketingNetwork': 'Search',
                'ParseRegexId': parse_regex_id,
                'ParserVersion': __version__,
                'SearchEngine': 'Google'
            }
            self.assertDictEqual(test, expected)
        with self.subTest("Volaris Android App - Search - Generic Terms&&Aerolineas"):
            campaign_name = "Volaris Android App - Search - Generic Terms"
            adgroup_name = "Aerolineas"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True
            )
            expected = {
                'AccountName': account_name,
                'AdGroupName': adgroup_name,
                'AirlineCode': 'Y4',
                'AirlineName': 'Volaris',
                'CampaignName': campaign_name,
                'CampaignType': 'Generic',
                'GeoTarget': 'MX',
                'KeywordGroup': 'App Download',
                'KeywordType': 'Generic',
                'Language': 'es',
                'Market': 'MX',
                'MarketingNetwork': 'Search',
                'ParseRegexId': parse_regex_id,
                'ParserVersion': __version__,
                'SearchEngine': 'Google'
            }
            self.assertDictEqual(test, expected)
        with self.subTest("Volaris Android App - Branded&&mexico city - Fort Lauderdale"):
            account_name = "Promotions Volaris"
            campaign_name = "Volaris Android App - Branded"
            adgroup_name = "mexico city - Fort Lauderdale"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True,
                na=True
            )
            expected = {
                'AccountName': account_name,
                'AdGroupName': adgroup_name,
                'AirlineCode': 'Y4',
                'AirlineName': 'Volaris',
                'Audience': 'N/A',
                'CampaignName': campaign_name,
                'CampaignType': 'Non-Brand',
                'Destination': 'FLL',
                'GeoTarget': 'MX',
                'KeywordGroup': 'App Download',
                'KeywordType': 'Route',
                'Language': 'es',
                'LocationType': 'N/A',
                'Market': 'MX',
                'MatchType': 'N/A',
                'Network': 'N/A',
                'Origin': 'MEX',
                'MarketingNetwork': 'Search',
                'ParseRegexId': parse_regex_id,
                'ParserVersion': __version__,
                'RouteLocale': 'N/A',
                'RouteType': 'Nonstop',
                'SearchEngine': 'Google',
                'SpecialCampaign': 'N/A'
            }
            self.assertDictEqual(test, expected)
        with self.subTest("Volaris App - Re Engagement&&San José (CR)"):
            account_name = "Promotions Volaris"
            campaign_name = "Volaris App - Re Engagement"
            adgroup_name = "San José (CR)"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True,
                na=True
            )
            expected = {
                'AccountName': account_name,
                'AdGroupName': adgroup_name,
                'AirlineCode': 'Y4',
                'AirlineName': 'Volaris',
                'Audience': 'N/A',
                'CampaignName': campaign_name,
                'CampaignType': 'Non-Brand',
                'Destination': 'SJO',
                'GeoTarget': 'MX',
                'KeywordGroup': 'App Download',
                'KeywordType': 'Destination',
                'Language': 'es',
                'LocationType': 'N/A',
                'Market': 'MX',
                'MatchType': 'N/A',
                'Network': 'N/A',
                'Origin': 'N/A',
                'MarketingNetwork': 'Search',
                'ParseRegexId': parse_regex_id,
                'ParserVersion': __version__,
                'RouteLocale': 'N/A',
                'RouteType': 'Nonstop',
                'SearchEngine': 'Google',
                'SpecialCampaign': 'N/A'
            }
            self.assertDictEqual(test, expected)
        with self.subTest("Volaris Android App (Opti)&&Volaris Vuelos Economicos"):
            account_name = "Promotions Volaris"
            campaign_name = "Volaris Android App (Opti)"
            adgroup_name = "Volaris Vuelos Economicos"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True,
                na=True
            )
            expected = {
                'AccountName': account_name,
                'AdGroupName': adgroup_name,
                'AirlineCode': 'Y4',
                'AirlineName': 'Volaris',
                'Audience': 'N/A',
                'CampaignName': campaign_name,
                'CampaignType': 'Brand',
                'Destination': 'N/A',
                'GeoTarget': 'MX',
                'KeywordGroup': 'App Download',
                'KeywordType': 'Modifiers',
                'Language': 'es',
                'LocationType': 'N/A',
                'Market': 'MX',
                'MatchType': 'N/A',
                'Network': 'N/A',
                'Origin': 'N/A',
                'MarketingNetwork': 'Search',
                'ParseRegexId': parse_regex_id,
                'ParserVersion': __version__,
                'RouteLocale': 'N/A',
                'RouteType': 'N/A',
                'SearchEngine': 'Google',
                'SpecialCampaign': 'N/A'
            }
            self.assertDictEqual(test, expected)
        with self.subTest("Volaris Android App - Generic Terms&&Vuelos"):
            account_name = "Promotions Volaris"
            campaign_name = "Volaris Android App - Generic Terms"
            adgroup_name = "Vuelos"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True,
                na=True
            )
            expected = {
                'AccountName': account_name,
                'AdGroupName': adgroup_name,
                'AirlineCode': 'Y4',
                'AirlineName': 'Volaris',
                'Audience': 'N/A',
                'CampaignName': campaign_name,
                'CampaignType': 'Generic',
                'Destination': 'N/A',
                'GeoTarget': 'MX',
                'KeywordGroup': 'App Download',
                'KeywordType': 'Generic',
                'Language': 'es',
                'LocationType': 'N/A',
                'Market': 'MX',
                'MatchType': 'N/A',
                'Network': 'N/A',
                'Origin': 'N/A',
                'MarketingNetwork': 'Search',
                'ParseRegexId': parse_regex_id,
                'ParserVersion': __version__,
                'RouteLocale': 'N/A',
                'RouteType': 'N/A',
                'SearchEngine': 'Google',
                'SpecialCampaign': 'N/A'
            }
            self.assertDictEqual(test, expected)
        with self.subTest("Volaris aPP 2&&Ad group #1"):
            account_name = "Promotions Volaris"
            campaign_name = "Volaris aPP 2"
            adgroup_name = "Ad group #1"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True,
                na=True
            )
            expected = {
                'AccountName': account_name,
                'AdGroupName': adgroup_name,
                'AirlineCode': 'Y4',
                'AirlineName': 'Volaris',
                'Audience': 'N/A',
                'CampaignName': campaign_name,
                'CampaignType': 'Brand',
                'Destination': 'N/A',
                'GeoTarget': 'MX',
                'KeywordGroup': 'App Download',
                'KeywordType': 'Modifiers',
                'Language': 'es',
                'LocationType': 'N/A',
                'Market': 'MX',
                'MatchType': 'N/A',
                'Network': 'N/A',
                'Origin': 'N/A',
                'MarketingNetwork': 'Search',
                'ParseRegexId': parse_regex_id,
                'ParserVersion': __version__,
                'RouteLocale': 'N/A',
                'RouteType': 'N/A',
                'SearchEngine': 'Google',
                'SpecialCampaign': 'N/A'
            }
            self.assertDictEqual(test, expected)
        with self.subTest("Volaris App&&Ad group #1"):
            account_name = "Promotions Volaris"
            campaign_name = "Volaris App"
            adgroup_name = "Ad group #1"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True,
                na=True
            )
            expected = {
                'AccountName': account_name,
                'AdGroupName': adgroup_name,
                'AirlineCode': 'Y4',
                'AirlineName': 'Volaris',
                'Audience': 'N/A',
                'CampaignName': campaign_name,
                'CampaignType': 'Brand',
                'Destination': 'N/A',
                'GeoTarget': 'MX',
                'KeywordGroup': 'App Download',
                'KeywordType': 'Modifiers',
                'Language': 'es',
                'LocationType': 'N/A',
                'Market': 'MX',
                'MatchType': 'N/A',
                'Network': 'N/A',
                'Origin': 'N/A',
                'MarketingNetwork': 'Search',
                'ParseRegexId': parse_regex_id,
                'ParserVersion': __version__,
                'RouteLocale': 'N/A',
                'RouteType': 'N/A',
                'SearchEngine': 'Google',
                'SpecialCampaign': 'N/A'
            }
            self.assertDictEqual(test, expected)

    def test_volaris_invex(self):
        """
        Single campaign case.

        'Volaris - Invex&&Mejor Tarjeta'

        :return:
        """
        parse = self.parser.parse
        parse_regex_id = "VolarisInvex"
        account_name = "Volaris - Invex"
        campaign_name = "Volaris - Invex"
        adgroup_name = "Mejor Tarjeta"
        with self.subTest("Volaris - Invex&&Mejor Tarjeta"):
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True,
                na=True
            )
            expected = {
                'AccountName': account_name,
                'AdGroupName': adgroup_name,
                'AirlineCode': 'Y4',
                'AirlineName': 'Volaris',
                'Audience': 'N/A',
                'CampaignName': campaign_name,
                'CampaignType': 'Generic',
                'Destination': 'N/A',
                'GeoTarget': 'MX',
                'KeywordGroup': 'Credit Card Application',
                'KeywordType': 'Generic',
                'Language': 'es',
                'LocationType': 'N/A',
                'Market': 'MX',
                'MatchType': 'N/A',
                'Network': 'N/A',
                'Origin': 'N/A',
                'MarketingNetwork': 'Search',
                'ParseRegexId': parse_regex_id,
                'ParserVersion': __version__,
                'RouteLocale': 'N/A',
                'RouteType': 'N/A',
                'SearchEngine': 'Google',
                'SpecialCampaign': 'N/A'
            }
            self.assertDictEqual(test, expected)

    def test_volaris_old_dsa(self):
        """
        Tests the DSA old naming convention.
        :return:
        """
        parse = self.parser.parse
        parse_regex_id = "VolarisOldDSA"
        account_name = "Volaris Mexico"
        with self.subTest("Dynamic&&Los Angeles"):
            campaign_name = "Dynamic"
            adgroup_name = "Los Angeles"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True,
                na=True
            )
            expected = {
                'AccountName': account_name,
                'AdGroupName': adgroup_name,
                'AirlineCode': 'Y4',
                'AirlineName': 'Volaris',
                'Audience': 'N/A',
                'CampaignName': campaign_name,
                'CampaignType': 'Non-Brand',
                'Destination': 'LAX',
                'GeoTarget': 'MX',
                'KeywordGroup': 'General',
                'KeywordType': 'Destination',
                'Language': 'es',
                'LocationType': 'N/A',
                'Market': 'MX',
                'MatchType': 'N/A',
                'Network': 'N/A',
                'Origin': 'N/A',
                'MarketingNetwork': 'DSA',
                'ParseRegexId': parse_regex_id,
                'ParserVersion': __version__,
                'RouteLocale': 'N/A',
                'RouteType': 'Nonstop',
                'SearchEngine': 'Google',
                'SpecialCampaign': 'N/A'
            }
            self.assertDictEqual(test, expected)
        with self.subTest("Dynamic Search Ads&&"):
            campaign_name = "Dynamic Search Ads"
            adgroup_name = ""
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True,
                na=True
            )
            expected = {
                'AccountName': account_name,
                'AdGroupName': "N/A",
                'AirlineCode': 'Y4',
                'AirlineName': 'Volaris',
                'Audience': 'N/A',
                'CampaignName': campaign_name,
                'CampaignType': 'Non-Brand',
                'Destination': 'N/A',
                'GeoTarget': 'MX',
                'KeywordGroup': 'General',
                'KeywordType': 'N/A',
                'Language': 'es',
                'LocationType': 'N/A',
                'Market': 'MX',
                'MatchType': 'N/A',
                'Network': 'N/A',
                'Origin': 'N/A',
                'MarketingNetwork': 'DSA',
                'ParseRegexId': parse_regex_id + "-CampaignOnly",
                'ParserVersion': __version__,
                'RouteLocale': 'N/A',
                'RouteType': 'N/A',
                'SearchEngine': 'Google',
                'SpecialCampaign': 'N/A'
            }
            self.assertDictEqual(test, expected)

    def test_volaris_old_vacations(self):
        """
        Tests the remaining old naming conventions vacations

        :return:
        """
        parse = self.parser.parse
        parse_regex_id = "VolarisOldVacations"
        with self.subTest("Avión + Hotel&&Cancún todo incluido"):
            account_name = "Volaris Mexico"
            campaign_name = "Avión + Hotel"
            adgroup_name = "Cancún todo incluido"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True,
                na=True
            )
            expected = {
                'AccountName': account_name,
                'AdGroupName': adgroup_name,
                'AirlineCode': 'Y4',
                'AirlineName': 'Volaris',
                'Audience': 'N/A',
                'CampaignName': campaign_name,
                'CampaignType': 'Non-Brand',
                'Destination': 'CUN',
                'GeoTarget': 'MX',
                'KeywordGroup': 'Vacations',
                'KeywordType': 'Destination',
                'Language': 'es',
                'LocationType': 'N/A',
                'Market': 'MX',
                'MatchType': 'N/A',
                'Network': 'N/A',
                'Origin': 'N/A',
                'MarketingNetwork': 'Search',
                'ParseRegexId': parse_regex_id,
                'ParserVersion': __version__,
                'RouteLocale': 'N/A',
                'RouteType': 'Nonstop',
                'SearchEngine': 'Google',
                'SpecialCampaign': 'N/A'
            }
            self.assertDictEqual(test, expected)
        with self.subTest("Avión + Hotel&&Viajes todo incluido"):
            account_name = "Volaris Mexico"
            campaign_name = "Avión + Hotel"
            adgroup_name = "Viajes todo incluido"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True,
                na=True
            )
            expected = {
                'AccountName': account_name,
                'AdGroupName': adgroup_name,
                'AirlineCode': 'Y4',
                'AirlineName': 'Volaris',
                'Audience': 'N/A',
                'CampaignName': campaign_name,
                'CampaignType': 'Generic',
                'Destination': 'N/A',
                'GeoTarget': 'MX',
                'KeywordGroup': 'Vacations',
                'KeywordType': 'Generic',
                'Language': 'es',
                'LocationType': 'N/A',
                'Market': 'MX',
                'MatchType': 'N/A',
                'Network': 'N/A',
                'Origin': 'N/A',
                'MarketingNetwork': 'Search',
                'ParseRegexId': parse_regex_id,
                'ParserVersion': __version__,
                'RouteLocale': 'N/A',
                'RouteType': 'N/A',
                'SearchEngine': 'Google',
                'SpecialCampaign': 'N/A'
            }
            self.assertDictEqual(test, expected)
        with self.subTest("Landing anticamion&&Landing"):
            account_name = "Volaris Mexico"
            campaign_name = "Landing anticamion"
            adgroup_name = "Landing"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True,
                na=True
            )
            expected = {
                'AccountName': account_name,
                'AdGroupName': adgroup_name,
                'AirlineCode': 'Y4',
                'AirlineName': 'Volaris',
                'Audience': 'N/A',
                'CampaignName': campaign_name,
                'CampaignType': 'Generic',
                'Destination': 'N/A',
                'GeoTarget': 'MX',
                'KeywordGroup': 'Vacations',
                'KeywordType': 'Generic',
                'Language': 'es',
                'LocationType': 'N/A',
                'Market': 'MX',
                'MatchType': 'N/A',
                'Network': 'N/A',
                'Origin': 'N/A',
                'MarketingNetwork': 'Search',
                'ParseRegexId': parse_regex_id,
                'ParserVersion': __version__,
                'RouteLocale': 'N/A',
                'RouteType': 'N/A',
                'SearchEngine': 'Google',
                'SpecialCampaign': 'N/A'
            }
            self.assertDictEqual(test, expected)
        with self.subTest("Test - Paquete de Viajes&&Brand"):
            account_name = "Volaris Mexico"
            campaign_name = "Test - Paquete de Viajes"
            adgroup_name = "Brand"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True,
                na=True
            )
            expected = {
                'AccountName': account_name,
                'AdGroupName': adgroup_name,
                'AirlineCode': 'Y4',
                'AirlineName': 'Volaris',
                'Audience': 'N/A',
                'CampaignName': campaign_name,
                'CampaignType': 'Brand',
                'Destination': 'N/A',
                'GeoTarget': 'MX',
                'KeywordGroup': 'Vacations',
                'KeywordType': 'Modifiers',
                'Language': 'es',
                'LocationType': 'N/A',
                'Market': 'MX',
                'MatchType': 'N/A',
                'Network': 'N/A',
                'Origin': 'N/A',
                'MarketingNetwork': 'Search',
                'ParseRegexId': parse_regex_id,
                'ParserVersion': __version__,
                'RouteLocale': 'N/A',
                'RouteType': 'N/A',
                'SearchEngine': 'Google',
                'SpecialCampaign': 'N/A'
            }
            self.assertDictEqual(test, expected)
        with self.subTest("Test - Paquete de Viajes&&General"):
            account_name = "Volaris Mexico"
            campaign_name = "Test - Paquete de Viajes"
            adgroup_name = "General"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True,
                na=True
            )
            expected = {
                'AccountName': account_name,
                'AdGroupName': adgroup_name,
                'AirlineCode': 'Y4',
                'AirlineName': 'Volaris',
                'Audience': 'N/A',
                'CampaignName': campaign_name,
                'CampaignType': 'Generic',
                'Destination': 'N/A',
                'GeoTarget': 'MX',
                'KeywordGroup': 'Vacations',
                'KeywordType': 'Generic',
                'Language': 'es',
                'LocationType': 'N/A',
                'Market': 'MX',
                'MatchType': 'N/A',
                'Network': 'N/A',
                'Origin': 'N/A',
                'MarketingNetwork': 'Search',
                'ParseRegexId': parse_regex_id,
                'ParserVersion': __version__,
                'RouteLocale': 'N/A',
                'RouteType': 'N/A',
                'SearchEngine': 'Google',
                'SpecialCampaign': 'N/A'
            }
            self.assertDictEqual(test, expected)
        with self.subTest("Test - Paquete de Viajes&&acapulco Economico"):
            account_name = "Volaris Mexico"
            campaign_name = "Test - Paquete de Viajes"
            adgroup_name = "acapulco Economico"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True,
                na=True
            )
            expected = {
                'AccountName': account_name,
                'AdGroupName': adgroup_name,
                'AirlineCode': 'Y4',
                'AirlineName': 'Volaris',
                'Audience': 'N/A',
                'CampaignName': campaign_name,
                'CampaignType': 'Non-Brand',
                'Destination': 'ACA',
                'GeoTarget': 'MX',
                'KeywordGroup': 'Vacations',
                'KeywordType': 'Destination',
                'Language': 'es',
                'LocationType': 'N/A',
                'Market': 'MX',
                'MatchType': 'N/A',
                'Network': 'N/A',
                'Origin': 'N/A',
                'MarketingNetwork': 'Search',
                'ParseRegexId': parse_regex_id,
                'ParserVersion': __version__,
                'RouteLocale': 'N/A',
                'RouteType': 'Nonstop',
                'SearchEngine': 'Google',
                'SpecialCampaign': 'N/A'
            }
            self.assertDictEqual(test, expected)

    def test_volaris_old_other(self):
        """
        Tests remaining outliers to conventions.

        :return:
        """
        parse = self.parser.parse
        with self.subTest("VOLARIS MX&&Volaris MX"):
            parse_regex_id = "VolarisOldBrandOther"
            account_name = "Volaris"
            campaign_name = "VOLARIS MX"
            adgroup_name = "Volaris MX"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True,
                na=True
            )
            expected = {
                'AccountName': account_name,
                'AdGroupName': adgroup_name,
                'AirlineCode': 'Y4',
                'AirlineName': 'Volaris',
                'Audience': 'N/A',
                'CampaignName': campaign_name,
                'CampaignType': 'Brand',
                'Destination': 'N/A',
                'GeoTarget': 'MX',
                'KeywordGroup': 'General',
                'KeywordType': 'Core',
                'Language': 'es',
                'LocationType': 'N/A',
                'Market': 'MX',
                'MatchType': 'N/A',
                'Network': 'N/A',
                'Origin': 'N/A',
                'MarketingNetwork': 'Search',
                'ParseRegexId': parse_regex_id,
                'ParserVersion': __version__,
                'RouteLocale': 'N/A',
                'RouteType': 'N/A',
                'SearchEngine': 'Google',
                'SpecialCampaign': 'N/A'
            }
            self.assertDictEqual(test, expected)
        with self.subTest("T - B Prueba Tablet&&Ad group #1"):
            parse_regex_id = "VolarisOldBrandOther"
            account_name = "Volaris Mexico"
            campaign_name = "T - B Prueba Tablet"
            adgroup_name = "Ad group #1"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True,
                na=True
            )
            expected = {
                'AccountName': account_name,
                'AdGroupName': adgroup_name,
                'AirlineCode': 'Y4',
                'AirlineName': 'Volaris',
                'Audience': 'N/A',
                'CampaignName': campaign_name,
                'CampaignType': 'Brand',
                'Destination': 'N/A',
                'GeoTarget': 'MX',
                'KeywordGroup': 'General',
                'KeywordType': 'Core',
                'Language': 'es',
                'LocationType': 'N/A',
                'Market': 'MX',
                'MatchType': 'N/A',
                'Network': 'N/A',
                'Origin': 'N/A',
                'MarketingNetwork': 'Search',
                'ParseRegexId': parse_regex_id,
                'ParserVersion': __version__,
                'RouteLocale': 'N/A',
                'RouteType': 'N/A',
                'SearchEngine': 'Google',
                'SpecialCampaign': 'N/A'
            }
            self.assertDictEqual(test, expected)
        with self.subTest("Hispanos&&Hispanos/EUA/Paquetes"):
            parse_regex_id = "VolarisOldGenericOther"
            account_name = "Volaris"
            campaign_name = "Hispanos"
            adgroup_name = "Hispanos/EUA/Paquetes"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True,
                na=True
            )
            expected = {
                'AccountName': account_name,
                'AdGroupName': adgroup_name,
                'AirlineCode': 'Y4',
                'AirlineName': 'Volaris',
                'Audience': 'N/A',
                'CampaignName': campaign_name,
                'CampaignType': 'Generic',
                'Destination': 'N/A',
                'GeoTarget': 'MX',
                'KeywordGroup': 'General',
                'KeywordType': 'Generic',
                'Language': 'es',
                'LocationType': 'N/A',
                'Market': 'MX',
                'MatchType': 'N/A',
                'Network': 'N/A',
                'Origin': 'N/A',
                'MarketingNetwork': 'Search',
                'ParseRegexId': parse_regex_id,
                'ParserVersion': __version__,
                'RouteLocale': 'N/A',
                'RouteType': 'N/A',
                'SearchEngine': 'Google',
                'SpecialCampaign': 'N/A'
            }
            self.assertDictEqual(test, expected)
        with self.subTest("VTP&&VTP"):
            parse_regex_id = "VolarisOldGenericOther"
            account_name = "Volaris"
            campaign_name = "VTP"
            adgroup_name = "VTP"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True,
                na=True
            )
            expected = {
                'AccountName': account_name,
                'AdGroupName': adgroup_name,
                'AirlineCode': 'Y4',
                'AirlineName': 'Volaris',
                'Audience': 'N/A',
                'CampaignName': campaign_name,
                'CampaignType': 'Generic',
                'Destination': 'N/A',
                'GeoTarget': 'MX',
                'KeywordGroup': 'General',
                'KeywordType': 'Generic',
                'Language': 'es',
                'LocationType': 'N/A',
                'Market': 'MX',
                'MatchType': 'N/A',
                'Network': 'N/A',
                'Origin': 'N/A',
                'MarketingNetwork': 'Search',
                'ParseRegexId': parse_regex_id,
                'ParserVersion': __version__,
                'RouteLocale': 'N/A',
                'RouteType': 'N/A',
                'SearchEngine': 'Google',
                'SpecialCampaign': 'N/A'
            }
            self.assertDictEqual(test, expected)
        with self.subTest("SJC&&SJC"):
            parse_regex_id = "VolarisOldGenericOther"
            account_name = "Volaris"
            campaign_name = "SJC"
            adgroup_name = "SJC"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True,
                na=True
            )
            expected = {
                'AccountName': account_name,
                'AdGroupName': adgroup_name,
                'AirlineCode': 'Y4',
                'AirlineName': 'Volaris',
                'Audience': 'N/A',
                'CampaignName': campaign_name,
                'CampaignType': 'Generic',
                'Destination': 'N/A',
                'GeoTarget': 'MX',
                'KeywordGroup': 'General',
                'KeywordType': 'Generic',
                'Language': 'es',
                'LocationType': 'N/A',
                'Market': 'MX',
                'MatchType': 'N/A',
                'Network': 'N/A',
                'Origin': 'N/A',
                'MarketingNetwork': 'Search',
                'ParseRegexId': parse_regex_id,
                'ParserVersion': __version__,
                'RouteLocale': 'N/A',
                'RouteType': 'N/A',
                'SearchEngine': 'Google',
                'SpecialCampaign': 'N/A'
            }
            self.assertDictEqual(test, expected)
        with self.subTest("PyMES&&PYMES"):
            parse_regex_id = "VolarisOldGenericOther"
            account_name = "Volaris"
            campaign_name = "PyMES"
            adgroup_name = "PYMES"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True,
                na=True
            )
            expected = {
                'AccountName': account_name,
                'AdGroupName': adgroup_name,
                'AirlineCode': 'Y4',
                'AirlineName': 'Volaris',
                'Audience': 'N/A',
                'CampaignName': campaign_name,
                'CampaignType': 'Generic',
                'Destination': 'N/A',
                'GeoTarget': 'MX',
                'KeywordGroup': 'General',
                'KeywordType': 'Generic',
                'Language': 'es',
                'LocationType': 'N/A',
                'Market': 'MX',
                'MatchType': 'N/A',
                'Network': 'N/A',
                'Origin': 'N/A',
                'MarketingNetwork': 'Search',
                'ParseRegexId': parse_regex_id,
                'ParserVersion': __version__,
                'RouteLocale': 'N/A',
                'RouteType': 'N/A',
                'SearchEngine': 'Google',
                'SpecialCampaign': 'N/A'
            }
            self.assertDictEqual(test, expected)
        with self.subTest("Servicios&&Servicios"):
            parse_regex_id = "VolarisOldGenericOther"
            account_name = "Volaris"
            campaign_name = "Servicios"
            adgroup_name = "Servicios"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True,
                na=True
            )
            expected = {
                'AccountName': account_name,
                'AdGroupName': adgroup_name,
                'AirlineCode': 'Y4',
                'AirlineName': 'Volaris',
                'Audience': 'N/A',
                'CampaignName': campaign_name,
                'CampaignType': 'Generic',
                'Destination': 'N/A',
                'GeoTarget': 'MX',
                'KeywordGroup': 'General',
                'KeywordType': 'Generic',
                'Language': 'es',
                'LocationType': 'N/A',
                'Market': 'MX',
                'MatchType': 'N/A',
                'Network': 'N/A',
                'Origin': 'N/A',
                'MarketingNetwork': 'Search',
                'ParseRegexId': parse_regex_id,
                'ParserVersion': __version__,
                'RouteLocale': 'N/A',
                'RouteType': 'N/A',
                'SearchEngine': 'Google',
                'SpecialCampaign': 'N/A'
            }
            self.assertDictEqual(test, expected)
        with self.subTest("VOLARIS_CONCURSO_PFL_2009&&Concurso 2009"):
            parse_regex_id = "VolarisOldGenericOther"
            account_name = "Volaris"
            campaign_name = "VOLARIS_CONCURSO_PFL_2009"
            adgroup_name = "Concurso 2009"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True,
                na=True
            )
            expected = {
                'AccountName': account_name,
                'AdGroupName': adgroup_name,
                'AirlineCode': 'Y4',
                'AirlineName': 'Volaris',
                'Audience': 'N/A',
                'CampaignName': campaign_name,
                'CampaignType': 'Generic',
                'Destination': 'N/A',
                'GeoTarget': 'MX',
                'KeywordGroup': 'General',
                'KeywordType': 'Generic',
                'Language': 'es',
                'LocationType': 'N/A',
                'Market': 'MX',
                'MatchType': 'N/A',
                'Network': 'N/A',
                'Origin': 'N/A',
                'MarketingNetwork': 'Search',
                'ParseRegexId': parse_regex_id,
                'ParserVersion': __version__,
                'RouteLocale': 'N/A',
                'RouteType': 'N/A',
                'SearchEngine': 'Google',
                'SpecialCampaign': 'N/A'
            }
            self.assertDictEqual(test, expected)
        with self.subTest("Bicentenario&&Bicentenario"):
            parse_regex_id = "VolarisOldGenericOther"
            account_name = "Volaris"
            campaign_name = "Bicentenario"
            adgroup_name = "Bicentenario"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True,
                na=True
            )
            expected = {
                'AccountName': account_name,
                'AdGroupName': adgroup_name,
                'AirlineCode': 'Y4',
                'AirlineName': 'Volaris',
                'Audience': 'N/A',
                'CampaignName': campaign_name,
                'CampaignType': 'Generic',
                'Destination': 'N/A',
                'GeoTarget': 'MX',
                'KeywordGroup': 'General',
                'KeywordType': 'Generic',
                'Language': 'es',
                'LocationType': 'N/A',
                'Market': 'MX',
                'MatchType': 'N/A',
                'Network': 'N/A',
                'Origin': 'N/A',
                'MarketingNetwork': 'Search',
                'ParseRegexId': parse_regex_id,
                'ParserVersion': __version__,
                'RouteLocale': 'N/A',
                'RouteType': 'N/A',
                'SearchEngine': 'Google',
                'SpecialCampaign': 'N/A'
            }
            self.assertDictEqual(test, expected)
        with self.subTest("Inglés&&ING/EUA"):
            parse_regex_id = "VolarisOldGenericOther"
            account_name = "Volaris"
            campaign_name = "Inglés"
            adgroup_name = "ING/EUA"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True,
                na=True
            )
            expected = {
                'AccountName': account_name,
                'AdGroupName': adgroup_name,
                'AirlineCode': 'Y4',
                'AirlineName': 'Volaris',
                'Audience': 'N/A',
                'CampaignName': campaign_name,
                'CampaignType': 'Generic',
                'Destination': 'N/A',
                'GeoTarget': 'US',
                'KeywordGroup': 'General',
                'KeywordType': 'Generic',
                'Language': 'en',
                'LocationType': 'N/A',
                'Market': 'US',
                'MatchType': 'N/A',
                'Network': 'N/A',
                'Origin': 'N/A',
                'MarketingNetwork': 'Search',
                'ParseRegexId': parse_regex_id,
                'ParserVersion': __version__,
                'RouteLocale': 'N/A',
                'RouteType': 'N/A',
                'SearchEngine': 'Google',
                'SpecialCampaign': 'N/A'
            }
            self.assertDictEqual(test, expected)
        with self.subTest("Estados&&Zacatecas/LA"):
            parse_regex_id = "VolarisOldGenericOther"
            account_name = "Volaris"
            campaign_name = "Estados"
            adgroup_name = "Zacatecas/LA"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True,
                na=True
            )
            expected = {
                'AccountName': account_name,
                'AdGroupName': adgroup_name,
                'AirlineCode': 'Y4',
                'AirlineName': 'Volaris',
                'Audience': 'N/A',
                'CampaignName': campaign_name,
                'CampaignType': 'Non-Brand',
                'Destination': 'LAX',
                'GeoTarget': 'MX',
                'KeywordGroup': 'General',
                'KeywordType': 'Route',
                'Language': 'es',
                'LocationType': 'N/A',
                'Market': 'MX',
                'MatchType': 'N/A',
                'Network': 'N/A',
                'Origin': 'ZCL',
                'MarketingNetwork': 'Search',
                'ParseRegexId': parse_regex_id,
                'ParserVersion': __version__,
                'RouteLocale': 'N/A',
                'RouteType': 'Nonstop',
                'SearchEngine': 'Google',
                'SpecialCampaign': 'N/A'
            }
            self.assertDictEqual(test, expected)
        with self.subTest("Estados&&Vuelos"):
            parse_regex_id = "VolarisOldGenericOther"
            account_name = "Volaris"
            campaign_name = "Estados"
            adgroup_name = "Vuelos"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True,
                na=True
            )
            expected = {
                'AccountName': account_name,
                'AdGroupName': adgroup_name,
                'AirlineCode': 'Y4',
                'AirlineName': 'Volaris',
                'Audience': 'N/A',
                'CampaignName': campaign_name,
                'CampaignType': 'Generic',
                'Destination': 'N/A',
                'GeoTarget': 'MX',
                'KeywordGroup': 'General',
                'KeywordType': 'Generic',
                'Language': 'es',
                'LocationType': 'N/A',
                'Market': 'MX',
                'MatchType': 'N/A',
                'Network': 'N/A',
                'Origin': 'N/A',
                'MarketingNetwork': 'Search',
                'ParseRegexId': parse_regex_id,
                'ParserVersion': __version__,
                'RouteLocale': 'N/A',
                'RouteType': 'N/A',
                'SearchEngine': 'Google',
                'SpecialCampaign': 'N/A'
            }
            self.assertDictEqual(test, expected)
        with self.subTest("Remarketing for Search&&Ad group #1"):
            parse_regex_id = "VolarisOldGenericOther"
            account_name = "Volaris Mexico"
            campaign_name = "Remarketing for Search"
            adgroup_name = "Ad group #1"
            test = parse(
                campaign_name=campaign_name,
                adgroup_name=adgroup_name,
                account_name=account_name,
                airline_code="Y4",
                return_names=True,
                na=True
            )
            expected = {
                'AccountName': account_name,
                'AdGroupName': adgroup_name,
                'AirlineCode': 'Y4',
                'AirlineName': 'Volaris',
                'Audience': 'N/A',
                'CampaignName': campaign_name,
                'CampaignType': 'Generic',
                'Destination': 'N/A',
                'GeoTarget': 'MX',
                'KeywordGroup': 'General',
                'KeywordType': 'Generic',
                'Language': 'es',
                'LocationType': 'N/A',
                'Market': 'MX',
                'MatchType': 'N/A',
                'Network': 'N/A',
                'Origin': 'N/A',
                'MarketingNetwork': 'RLSA',
                'ParseRegexId': parse_regex_id,
                'ParserVersion': __version__,
                'RouteLocale': 'N/A',
                'RouteType': 'N/A',
                'SearchEngine': 'Google',
                'SpecialCampaign': 'N/A'
            }
            self.assertDictEqual(test, expected)

    def test_volaris_adgroup_interaction(self):
        """
        Tests that an interaction does not occur with the adgroup logic used by AM.

        Any output that is returned is a pass.

        :return:
        """
        parsing = self.parser.parse(
            **{
                'campaign_name': 'Test - Paquete de Viajes', 'adgroup_name': 'Viaje Todo Incluydo - puerto vallarta',
                'airline_name': None, 'airline_code': 'Y4', 'account_name': 'Promotions Volaris',
                'search_engine': 'Google',
                'return_names': True, 'na': True
            }
        )
        # print(parsing)
        self.assertTrue(parsing)


class TestNewClientParsingUO(unittest.TestCase):
    """
    Tests that the parsing logic applied is correct.
    """

    def __init__(self, *args, **kwargs):
        """
        Declare a 'parser' attribute. (Only declared here to prevent annoying syntax highlighting; this method
        has no functionality).

        :param args:
        :param kwargs:
        :return:
        """
        self.parser = None
        super().__init__(*args, **kwargs)
        self.maxDiff = None

    def setUp(self):
        """
        Though it shouldn't be affected, set maxDiff to None (no limit to testing differences of strings in
        self.assertDictEqual).

        Instantiate the parser instance and make available.

        :return:
        """
        self.parser = Parser(cached=False)

    @unittest.skip("Need to re-create resource data")
    def test_uo_parsings_google(self):
        """
        Tests old uo_parsings
        :return:
        """
        import json
        with open("tests/test_data/uo_parsings.json") as file:
            data = json.load(file)
        data = data.values()
        for row in data:
            if row["SearchEngine"] == "Google":
                campaign_name = row["CampaignName"]
                adgroup_name = row["AdGroupName"]
                campaign_type = row["CampaignType"]
                if campaign_type == "BR":
                    campaign_type = "Brand"
                elif campaign_type == "NB":
                    campaign_type = "Non-Brand"
                elif campaign_type == "HB":
                    campaign_type = "Hybrid Brand"
                keyword_type = row["KeywordType"]
                if keyword_type == "Dest":
                    keyword_type = "Destination"
                expected = {
                    "AccountName": "HK Express",
                    "AdGroupName": adgroup_name,
                    "AirlineCode": "UO",
                    "AirlineName": "Hong Kong Express",
                    "CampaignName": campaign_name,
                    "CampaignType": campaign_type,
                    "KeywordGroup": "General",
                    "KeywordType": keyword_type,
                    "Language": row["Language"],
                    "MarketingNetwork": "Search",
                    "Market": row["Market"],
                    "MatchType": "PX",
                    "ParseRegexId": "UODictionary",
                    "ParserVersion": __version__,
                    "SearchEngine": "Google"
                }
                if campaign_type in {"Non-Brand", "Hybrid Brand"}:
                    expected["RouteType"] = "Nonstop"
                    if row["Destination"]:
                        expected["Destination"] = city_name_to_code(
                            "UO",
                            row["Destination"]
                        )
                if row.get("GeoTarget"):
                    geo = row["GeoTarget"].strip()
                    expected["GeoTarget"] = geo
                if row.get("MatchType"):
                    expected["MatchType"] = row["MatchType"]
                if "exact" in expected["AdGroupName"].lower():
                    expected["MatchType"] = "EX"
                elif "phrase" in expected["AdGroupName"].lower():
                    expected["MatchType"] = "PH"
                elif "broad" in expected["AdGroupName"].lower():
                    expected["MatchType"] = "BM"
                test = self.parser.parse(
                    campaign_name=campaign_name,
                    adgroup_name=adgroup_name,
                    airline_code="UO",
                    search_engine="Google",
                    return_names=True,
                    na=False
                )
                with self.subTest("UO Old parsings"):
                    self.assertDictEqual(
                        test, expected
                    )

    @unittest.skip("Need to re-create resource data")
    def test_uo_parsings_yahoo(self):
        """
        Tests old uo_parsings
        :return:
        """
        import json
        with open("tests/test_data/uo_parsings_yahoo.json") as file:
            data = json.load(file)
        data = data.values()
        for row in data:
            if row["SearchEngine"] == "Yahoo! Japan":
                campaign_name = row["CampaignName"]
                adgroup_name = row["AdGroupName"]
                campaign_type = row["CampaignType"]
                if campaign_type == "BR":
                    campaign_type = "Brand"
                elif campaign_type == "NB":
                    campaign_type = "Non-Brand"
                elif campaign_type == "HB":
                    campaign_type = "Hybrid Brand"
                keyword_type = row["KeywordType"]
                if keyword_type == "Dest":
                    keyword_type = "Destination"
                expected = {
                    "AdGroupName": adgroup_name,
                    "AirlineCode": "UO",
                    "AirlineName": "Hong Kong Express",
                    "CampaignName": campaign_name,
                    "CampaignType": campaign_type,
                    "KeywordGroup": "General",
                    "KeywordType": keyword_type.replace("Generics", "Generic"),
                    "Language": row["Language"],
                    "MarketingNetwork": "Search",
                    "Market": row["Market"],
                    "MatchType": "PX",
                    "ParseRegexId": "UODictionary",
                    "ParserVersion": __version__,
                    "SearchEngine": "Yahoo! Japan"
                }
                if campaign_type in {"Non-Brand", "Hybrid Brand"}:
                    if "Generic" not in expected["KeywordType"]:
                        expected["RouteType"] = "Nonstop"
                if row["Destination"]:
                    expected["Destination"] = city_name_to_code(
                        "UO",
                        row["Destination"]
                    )
                if row.get("GeoTarget"):
                    geo = row["GeoTarget"].replace(" ", "")
                    expected["GeoTarget"] = geo
                if row.get("MatchType"):
                    expected["MatchType"] = row["MatchType"]
                if "Destination" in expected.keys() and expected.get("Destination") is None:
                    expected.pop("Destination")
                test = self.parser.parse(
                    campaign_name=campaign_name,
                    adgroup_name=adgroup_name,
                    airline_code="UO",
                    search_engine="Yahoo! Japan",
                    return_names=True,
                    na=False
                )
                with self.subTest("UO Old parsings"):
                    self.assertDictEqual(
                        test, expected
                    )

    def test_uo_yahoo_j_override(self):
        """
        Testing that the search engine override works (an example when campaignnames were improperly named).

        :return:
        """
        campaign_name = "GS:ja-JP_BR\Core/Geo@JP"
        adgroup_name = "GS:ja-JP_BR\Core/Geo@JP"
        account_name = "HONG KONG EXPRESS AIRWAYS LIMITED"
        test = self.parser.parse(
            campaign_name=campaign_name,
            adgroup_name=adgroup_name,
            account_name=account_name,
            airline_code="UO",
            search_engine="Yahoo! Japan",
            return_names=True,
            na=False
        )
        self.assertEqual(
            test["SearchEngine"],
            "Yahoo! Japan"
        )


class TestNewClientParsingAM(unittest.TestCase):
    """
    Tests that the parsing logic applied is correct.
    """

    def __init__(self, *args, **kwargs):
        """
        Declare a 'parser' attribute. (Only declared here to prevent annoying syntax highlighting; this method
        has no functionality).

        :param args:
        :param kwargs:
        :return:
        """
        self.parser = None
        super().__init__(*args, **kwargs)
        self.maxDiff = None

    def setUp(self):
        """
        Though it shouldn't be affected, set maxDiff to None (no limit to testing differences of strings in
        self.assertDictEqual).

        Instantiate the parser instance and make available.

        :return:
        """
        self.parser = Parser(cached=False)

    def test_am_adgroup_item_parsing(self):
        """
        Tests that the item parsing of the wierd structure returns as expected.
        :return:
        """
        campaign_name = "GS:es-MX_NB\CC-Route=AGU>00>MEX/Geo@MX"
        adgroup_name = "Vuelos baratos"
        account_name = "Aeromexico - Mexico 02"
        airline_code = "AM"
        search_engine = "Google"
        airline_name = "Aeromexico"
        parsed = self.parser._item_parser(
            campaign_name=campaign_name,
            adgroup_name=None,
            airline_name=airline_name,
            airline_code=airline_code,
            account_name=account_name,
            search_engine=search_engine,
            return_names=True,
            na=True
        )
        expected = {
            "GeoTarget": "MX",
            "RouteLocale": "N/A",
            "CampaignName": "GS:es-MX_NB\CC-Route=AGU>00>MEX/Geo@MX",
            "AdGroupName": "N/A",
            "AirlineName": "Aeromexico",
            "AirlineCode": "AM",
            "AccountName": "Aeromexico - Mexico 02",
            "Origin": "AGU",
            "Destination": "MEX",
            "RouteType": "Nonstop",
            "SearchEngine": "Google",
            "CampaignType": "Non-Brand",
            "Market": "MX",
            "Language": "es",
            "KeywordGroup": "General",
            "KeywordType": "Route",
            "Network": "N/A",
            "Audience": "N/A",
            "SpecialCampaign": "N/A",
            "MarketingNetwork": "Search",
            "LocationType": "City>City",
            "MatchType": "PX",
            'ParseRegexId': 'EveryMundoNonBrand1-CampaignOnly',
            "ParserVersion": __version__
        }
        self.assertEqual(expected, parsed)

    def test_am_adgroup_structure(self):
        """
        Tests that the AM adgroup structure is parsed correctly.
        :return:
        """
        expected = {
            "GeoTarget": "MX",
            "RouteLocale": "N/A",
            "CampaignName": "GS:es-MX_NB\CC-Route=AGU>00>MEX/Geo@MX",
            "AdGroupName": "Vuelos baratos",
            "AirlineName": "Aeromexico",
            "AirlineCode": "AM",
            "AccountName": "Aeromexico - Mexico 02",
            "Origin": "AGU",
            "Destination": "MEX",
            "RouteType": "Nonstop",
            "SearchEngine": "Google",
            "CampaignType": "Non-Brand",
            "Market": "MX",
            "Language": "es",
            "KeywordGroup": "General",
            "KeywordType": "Route",
            "Audience": "N/A",
            "SpecialCampaign": "N/A",
            "MarketingNetwork": "Search",
            "Network": "N/A",
            "LocationType": "City>City",
            "MatchType": "PX",
            'ParseRegexId': 'EveryMundoNonBrand1-CampaignOnly',
            "ParserVersion": __version__
        }
        actual = self.parser.parse(
            account_name="Aeromexico - Mexico 02",
            campaign_name="GS:es-MX_NB\CC-Route=AGU>00>MEX/Geo@MX",
            adgroup_name="Vuelos baratos",
            airline_code="AM",
            search_engine="Google",
            return_names=True,
            na=True
        )
        self.assertEqual(actual, expected)

    def test_am_adgroup_structure_others_1(self):
        """
        Tests other cases where campaign type has returned as None.

        :return:
        """
        expected = {
            "GeoTarget": "SFO",
            "RouteLocale": "N/A",
            "CampaignName": "GS:en-US_NB\CC-Dest={SFO}>00>MEX/Geo@SFO",
            "AdGroupName": "Fly",
            "AirlineName": "Aeromexico",
            "AirlineCode": "AM",
            "AccountName": "Aeromexico - US",
            "Origin": "SFO",
            "Destination": "MEX",
            "RouteType": "Nonstop",
            "SearchEngine": "Google",
            "CampaignType": "Non-Brand",
            "Market": "US",
            "Language": "en",
            "KeywordGroup": "General",
            "KeywordType": "Destination",
            "Audience": "N/A",
            "SpecialCampaign": "N/A",
            "MarketingNetwork": "Search",
            "Network": "N/A",
            "LocationType": "City>City",
            "MatchType": "PX",
            'ParseRegexId': 'EveryMundoNonBrand1-CampaignOnly',
            "ParserVersion": __version__
        }
        actual = self.parser.parse(
            account_name="Aeromexico - US",
            campaign_name="GS:en-US_NB\CC-Dest={SFO}>00>MEX/Geo@SFO",
            adgroup_name="Fly",
            airline_code="AM",
            search_engine="Google",
            return_names=True,
            na=True
        )
        self.assertEqual(actual, expected)

    def test_am_adgroup_structure_others_2(self):
        """
        Tests other cases where campaign type has returned as None.

        :return:
        """
        expected = {
            "GeoTarget": "MX",
            "RouteLocale": "N/A",
            "CampaignName": "GS:es-MX_NB\CC-Route=MEX>00>LAS/Geo@MX",
            "AdGroupName": "Pasajes",
            "AirlineName": "Aeromexico",
            "AirlineCode": "AM",
            "AccountName": "Aeromexico - Mexico 02",
            "Origin": "MEX",
            "Destination": "LAS",
            "RouteType": "Nonstop",
            "SearchEngine": "Google",
            "CampaignType": "Non-Brand",
            "Market": "MX",
            "Language": "es",
            "KeywordGroup": "General",
            "KeywordType": "Route",
            "Audience": "N/A",
            "SpecialCampaign": "N/A",
            "MarketingNetwork": "Search",
            "Network": "N/A",
            "LocationType": "City>City",
            "MatchType": "PX",
            'ParseRegexId': 'EveryMundoNonBrand1-CampaignOnly',
            "ParserVersion": __version__
        }
        actual = self.parser.parse(
            account_name="Aeromexico - Mexico 02",
            campaign_name="GS:es-MX_NB\CC-Route=MEX>00>LAS/Geo@MX",
            adgroup_name="Pasajes",
            airline_code="AM",
            search_engine="Google",
            return_names=True,
            na=True
        )
        self.assertEqual(actual, expected)

    def test_am_adgroup_structure_others_3(self):
        """
        Tests other cases where campaign type has returned as None.

        :return:
        """
        expected = {
            "GeoTarget": "MX",
            "RouteLocale": "N/A",
            "CampaignName": "GS:es-MX_NB\CC-Route=MEX>00>MAD/Geo@MX",
            "AdGroupName": "Billetes",
            "AirlineName": "Aeromexico",
            "AirlineCode": "AM",
            "AccountName": "Aeromexico - Mexico 02",
            "Origin": "MEX",
            "Destination": "MAD",
            "RouteType": "Nonstop",
            "SearchEngine": "Google",
            "CampaignType": "Non-Brand",
            "Market": "MX",
            "Language": "es",
            "KeywordGroup": "General",
            "KeywordType": "Route",
            "Audience": "N/A",
            "SpecialCampaign": "N/A",
            "MarketingNetwork": "Search",
            "Network": "N/A",
            "LocationType": "City>City",
            "MatchType": "PX",
            'ParseRegexId': 'EveryMundoNonBrand1-CampaignOnly',
            "ParserVersion": __version__
        }
        actual = self.parser.parse(
            account_name="Aeromexico - Mexico 02",
            campaign_name="GS:es-MX_NB\CC-Route=MEX>00>MAD/Geo@MX",
            adgroup_name="Billetes",
            airline_code="AM",
            search_engine="Google",
            return_names=True,
            na=True
        )
        self.assertEqual(actual, expected)

    def test_am_adgroup_structure_others_4(self):
        """
        Tests other cases where campaign type has returned as None.

        :return:
        """
        expected = {
            "GeoTarget": "MX",
            "RouteLocale": "N/A",
            "CampaignName": "GS:es-MX_NB\CC-Route=MTY>00>QRO/Geo@MX",
            "AdGroupName": "Vuelos economicos",
            "AirlineName": "Aeromexico",
            "AirlineCode": "AM",
            "AccountName": "Aeromexico - Mexico 02",
            "Origin": "MTY",
            "Destination": "QRO",
            "RouteType": "Nonstop",
            "SearchEngine": "Google",
            "CampaignType": "Non-Brand",
            "Market": "MX",
            "Language": "es",
            "KeywordGroup": "General",
            "KeywordType": "Route",
            "Audience": "N/A",
            "SpecialCampaign": "N/A",
            "MarketingNetwork": "Search",
            "Network": "N/A",
            "LocationType": "City>City",
            "MatchType": "PX",
            'ParseRegexId': 'EveryMundoNonBrand1-CampaignOnly',
            "ParserVersion": __version__
        }
        actual = self.parser.parse(
            account_name="Aeromexico - Mexico 02",
            campaign_name="GS:es-MX_NB\CC-Route=MTY>00>QRO/Geo@MX",
            adgroup_name="Vuelos economicos",
            airline_code="AM",
            search_engine="Google",
            return_names=True,
            na=True
        )
        self.assertEqual(actual, expected)

    def test_am_adgroup_structure_others_5(self):
        """
        Tests other cases where campaign type has returned as None.

        :return:
        """
        expected = {
            "GeoTarget": "MX",
            "RouteLocale": "N/A",
            "CampaignName": "GS:es-MX_NB\CC-Route=TIJ>00>MEX/Geo@MX",
            "AdGroupName": "Viaje barato",
            "AirlineName": "Aeromexico",
            "AirlineCode": "AM",
            "AccountName": "Aeromexico - Mexico 02",
            "Origin": "TIJ",
            "Destination": "MEX",
            "RouteType": "Nonstop",
            "SearchEngine": "Google",
            "CampaignType": "Non-Brand",
            "Market": "MX",
            "Language": "es",
            "KeywordGroup": "General",
            "KeywordType": "Route",
            "Audience": "N/A",
            "SpecialCampaign": "N/A",
            "MarketingNetwork": "Search",
            "Network": "N/A",
            "LocationType": "City>City",
            "MatchType": "PX",
            'ParseRegexId': 'EveryMundoNonBrand1-CampaignOnly',
            "ParserVersion": __version__
        }
        actual = self.parser.parse(
            account_name="Aeromexico - Mexico 02",
            campaign_name="GS:es-MX_NB\CC-Route=TIJ>00>MEX/Geo@MX",
            adgroup_name="Viaje barato",
            airline_code="AM",
            search_engine="Google",
            return_names=True,
            na=True
        )
        self.assertEqual(actual, expected)


class TestAbbreviationAndTCPA(unittest.TestCase):
    """
    Tests that the Baidu abbreviation and new TCPA standards are parsed correctly as desired.
    """

    def __init__(self, *args, **kwargs):
        """
        Declare a 'parser' attribute. (Only declared here to prevent annoying syntax highlighting; this method
        has no functionality).

        :param args:
        :param kwargs:
        :return:
        """
        self.parser = None
        super().__init__(*args, **kwargs)
        self.maxDiff = None

    def setUp(self):
        """
        Though it shouldn't be affected, set maxDiff to None (no limit to testing differences of strings in
        self.assertDictEqual).

        Instantiate the parser instance and make available.

        :return:
        """
        self.parser = Parser(cached=False)

    def test_tcpa_route_type_a(self):
        """
        Tests the route type.

        :return:
        """
        expected = {
            "GeoTarget": "DE",
            "RouteLocale": "N/A",
            "CampaignName": r"GS:en-DE_NB\tCPA=Route-High/Geo@DE",
            "AdGroupName": r"GS:en-DE_NB\NN-Route=DE>00>GR/Geo@DE",
            "AirlineName": "Jet Airways",
            "AirlineCode": "9W",
            "AccountName": "9W_DE (en)",
            "Origin": "DE",
            "Destination": "GR",
            "RouteType": "Nonstop",
            "SearchEngine": "Google",
            "CampaignType": "Non-Brand",
            "Market": "DE",
            "Language": "en",
            "KeywordGroup": "tCPA",
            "KeywordType": "Route",
            "Audience": "N/A",
            "SpecialCampaign": "N/A",
            "MarketingNetwork": "Search",
            "Network": "N/A",
            "LocationType": "Nation>Nation",
            "MatchType": "High",
            'ParseRegexId': 'EveryMundo-tCPA',
            "ParserVersion": __version__
        }
        actual = self.parser.parse(
            account_name="9W_DE (en)",
            campaign_name=r"GS:en-DE_NB\tCPA=Route-High/Geo@DE",
            adgroup_name=r"GS:en-DE_NB\NN-Route=DE>00>GR/Geo@DE",
            airline_code="9W",
            search_engine="Google",
            return_names=True,
            na=True
        )
        self.assertEqual(actual, expected)

    def test_tcpa_route_type_b(self):
        """
        Tests the route type.

        :return:
        """
        expected = {
            "GeoTarget": "DE",
            "RouteLocale": "N/A",
            "CampaignName": r"GS:en-DE_NB\tCPA=Destination-Low/Geo@DE",
            "AdGroupName": r"GS:en-DE_NB\CC-Dest={000}>00>ATH/Geo@DE",
            "AirlineName": "Jet Airways",
            "AirlineCode": "9W",
            "AccountName": "9W_DE (en)",
            "Origin": "N/A",
            "Destination": "ATH",
            "RouteType": "Nonstop",
            "SearchEngine": "Google",
            "CampaignType": "Non-Brand",
            "Market": "DE",
            "Language": "en",
            "KeywordGroup": "tCPA",
            "KeywordType": "Destination",
            "Audience": "N/A",
            "SpecialCampaign": "N/A",
            "MarketingNetwork": "Search",
            "Network": "N/A",
            "LocationType": "City>City",
            "MatchType": "Low",
            'ParseRegexId': 'EveryMundo-tCPA',
            "ParserVersion": __version__
        }
        actual = self.parser.parse(
            account_name="9W_DE (en)",
            campaign_name=r"GS:en-DE_NB\tCPA=Destination-Low/Geo@DE",
            adgroup_name=r"GS:en-DE_NB\CC-Dest={000}>00>ATH/Geo@DE",
            airline_code="9W",
            search_engine="Google",
            return_names=True,
            na=True
        )
        self.assertEqual(actual, expected)

    def test_tcpa_dest_type_a(self):
        """
        Tests the route type.

        :return:
        """
        expected = {
            "GeoTarget": "DE",
            "RouteLocale": "N/A",
            "CampaignName": r"GS:en-DE_NB\tCPA=Route+Destination-Unknown/Geo@DE",
            "AdGroupName": r"GS:en-DE_NB\CC-Dest={000}>00>ATH/Geo@DE",
            "AirlineName": "Jet Airways",
            "AirlineCode": "9W",
            "AccountName": "9W_DE (en)",
            "Origin": "N/A",
            "Destination": "ATH",
            "RouteType": "Nonstop",
            "SearchEngine": "Google",
            "CampaignType": "Non-Brand",
            "Market": "DE",
            "Language": "en",
            "KeywordGroup": "tCPA",
            "KeywordType": "Destination",
            "Audience": "N/A",
            "SpecialCampaign": "N/A",
            "MarketingNetwork": "Search",
            "Network": "N/A",
            "LocationType": "City>City",
            "MatchType": "Unknown",
            'ParseRegexId': 'EveryMundo-tCPA',
            "ParserVersion": __version__
        }
        actual = self.parser.parse(
            account_name="9W_DE (en)",
            campaign_name=r"GS:en-DE_NB\tCPA=Route+Destination-Unknown/Geo@DE",
            adgroup_name=r"GS:en-DE_NB\CC-Dest={000}>00>ATH/Geo@DE",
            airline_code="9W",
            search_engine="Google",
            return_names=True,
            na=True
        )
        self.assertEqual(actual, expected)

    def test_baidu_route_type_a(self):
        """
        Tests the route type.

        :return:
        """
        expected = {
            "GeoTarget": "CN",
            "RouteLocale": "N/A",
            "CampaignName": r"Non-Brand Route",
            "AdGroupName": r"CC-Route=CJU>0>HKG",
            "AirlineName": "Hong Kong Express",
            "AirlineCode": "UO",
            "AccountName": "HKD-HKExpress-1407",
            "Origin": "CJU",
            "Destination": "HKG",
            "RouteType": "Nonstop",
            "SearchEngine": "Baidu",
            "CampaignType": "Non-Brand",
            "Market": "CN",
            "Language": "zh",
            "KeywordGroup": "General",
            "KeywordType": "Route",
            "Audience": "N/A",
            "SpecialCampaign": "N/A",
            "MarketingNetwork": "Search",
            "Network": "N/A",
            "LocationType": "City>City",
            "MatchType": "PX",
            'ParseRegexId': 'BaiduAbbreviated',
            "ParserVersion": __version__
        }
        actual = self.parser.parse(
            account_name="HKD-HKExpress-1407",
            campaign_name=r"Non-Brand Route",
            adgroup_name=r"CC-Route=CJU>0>HKG",
            airline_code="UO",
            search_engine="Baidu",
            return_names=True,
            na=True
        )
        self.assertEqual(actual, expected)

    def test_baidu_dest_type_a(self):
        """
        Tests the route type.

        :return:
        """
        expected = {
            "GeoTarget": "HKG",
            "RouteLocale": "N/A",
            "CampaignName": r"Non-Brand Dest",
            "AdGroupName": r"CC-Dest={HKG}>0>KIX",
            "AirlineName": "Hong Kong Express",
            "AirlineCode": "UO",
            "AccountName": "HKD-HKExpress-1407",
            "Origin": "HKG",
            "Destination": "KIX",
            "RouteType": "Nonstop",
            "SearchEngine": "Baidu",
            "CampaignType": "Non-Brand",
            "Market": "CN",
            "Language": "zh",
            "KeywordGroup": "General",
            "KeywordType": "Destination",
            "Audience": "N/A",
            "SpecialCampaign": "N/A",
            "MarketingNetwork": "Search",
            "Network": "N/A",
            "LocationType": "City>City",
            "MatchType": "PX",
            'ParseRegexId': 'BaiduAbbreviated',
            "ParserVersion": __version__
        }
        actual = self.parser.parse(
            account_name="HKD-HKExpress-1407",
            campaign_name=r"Non-Brand Dest",
            adgroup_name=r"CC-Dest={HKG}>0>KIX",
            airline_code="UO",
            search_engine="Baidu",
            return_names=True,
            na=True
        )
        self.assertEqual(actual, expected)


class TestAirlineCodeStability(unittest.TestCase):
    """
    Tests
    """

    def __init__(self, *args, **kwargs):
        """
        Declare a 'parser' attribute. (Only declared here to prevent annoying syntax highlighting; this method
        has no functionality).

        :param args:
        :param kwargs:
        :return:
        """
        self.parser = None
        super().__init__(*args, **kwargs)
        self.maxDiff = None

    def setUp(self):
        """
        Though it shouldn't be affected, set maxDiff to None (no limit to testing differences of strings in
        self.assertDictEqual).

        Instantiate the parser instance and make available.

        :return:
        """
        self.parser = Parser(cached=False)

    def test_airline_codes_match(self):
        """
        To address known bug as discovered by AIRSEM-1298
        :return:
        """
        expected = {
            'ParserVersion': __version__,
            'AirlineName': 'Xiamen',
            'AirlineCode': 'MF',
            'CampaignName': 'GS:en-KR_NB\\Generic=BlackFriday/Geo@KR',
            'AdGroupName': 'GS:en-KR_NB\\Generic=BlackFriday/PH',
            'AccountName': 'MF_KR (en)',
            'SearchEngine': 'Google',
            'MarketingNetwork': 'Search',
            'Language': 'en',
            'Market': 'KR',
            'CampaignType': 'Generic',
            'KeywordType': 'Generic',
            'GeoTarget': 'KR',
            'KeywordGroup': 'Blackfriday',
            'MatchType': 'PH',
            'ParseRegexId': 'EveryMundo-NewGeneric',
            'Network': 'N/A',
            'RouteLocale': 'N/A',
            'RouteType': 'N/A',
            'LocationType': 'N/A',
            'Destination': 'N/A',
            'Origin': 'N/A',
            'Audience': 'N/A',
            'SpecialCampaign': 'N/A'
        }
        actual = self.parser.parse(
            account_name='MF_KR (en)',
            campaign_name='GS:en-KR_NB\\Generic=BlackFriday/Geo@KR',
            adgroup_name='GS:en-KR_NB\\Generic=BlackFriday/PH',
            airline_code='MF',
            search_engine='Google',
            return_names=True,
            na=True
        )
        self.assertEqual(expected, actual)


class TestNewClientParsing9K(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        """
        Declare a 'parser' attribute. (Only declared here to prevent annoying syntax highlighting; this method
        has no functionality).

        :param args:
        :param kwargs:
        :return:
        """
        self.parser = None
        super().__init__(*args, **kwargs)
        self.maxDiff = None

    def setUp(self):
        """
        Though it shouldn't be affected, set maxDiff to None (no limit to testing differences of strings in
        self.assertDictEqual).

        Instantiate the parser instance and make available.

        :return:
        """
        self.parser = Parser(cached=False)

    def test_cape_generic_type_a(self):
        """
        Tests the new generic case.
        :return:
        """
        expected = {
            'ParserVersion': __version__,
            'AirlineName': 'Cape Air',
            'AirlineCode': '9K',
            'CampaignName': 'GS:en-US_NB\\Generic=Pilot/Geo@US',
            'AdGroupName': 'GS:en-US_NB\\GE=Pilot/PH',
            'AccountName': '9K_US (en)',
            'SearchEngine': 'Google',
            'MarketingNetwork': 'Search',
            'Language': 'en',
            'Market': 'US',
            'CampaignType': 'Generic',
            'SpecialCampaign': 'N/A',
            'ParseRegexId': 'EveryMundo-NewGeneric',
            'Network': 'N/A',
            'MatchType': 'PH',
            'KeywordType': 'Generic',
            'KeywordGroup': 'Pilot',
            'RouteLocale': 'N/A',
            'RouteType': 'N/A',
            'LocationType': 'N/A',
            'GeoTarget': 'US',
            'Destination': 'N/A',
            'Audience': 'N/A',
            'Origin': 'N/A'
        }
        actual = self.parser.parse(
            account_name='9K_US (en)',
            campaign_name='GS:en-US_NB\\Generic=Pilot/Geo@US',
            adgroup_name='GS:en-US_NB\\GE=Pilot/PH',
            airline_code='9K',
            search_engine='Google',
            return_names=True,
            na=True
        )
        self.assertEqual(actual, expected)


class TestBingExpansion(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        """
        Declare a 'parser' attribute. (Only declared here to prevent annoying syntax highlighting; this method
        has no functionality).

        :param args:
        :param kwargs:
        :return:
        """
        self.parser = None
        super().__init__(*args, **kwargs)
        self.maxDiff = None

    def setUp(self):
        """
        Though it shouldn't be affected, set maxDiff to None (no limit to testing differences of strings in
        self.assertDictEqual).

        Instantiate the parser instance and make available.

        :return:
        """
        self.parser = Parser(cached=False)

    def test_generic_bing_remarketing_a(self):
        campaign_name = 'BL:en-GB_NB\Search=Generic/Geo@GB'
        campaign_name = 'BL:en-GB_NB\\Generic/BM@4-30d'
        adgroup_name = 'BL:en-GB_NB\Generic/BM@Tickets'
        account_name = 'A3_GB (en)'
        expected = {
            "GeoTarget": "N/A",
            "RouteLocale": "N/A",
            "CampaignName": campaign_name,
            "AdGroupName": adgroup_name,
            "AirlineName": "Aegean Airlines",
            "AirlineCode": "A3",
            "AccountName": account_name,
            "Origin": "N/A",
            "Destination": "N/A",
            "RouteType": "N/A",
            "SearchEngine": "Bing",
            "CampaignType": "Non-Brand",
            "Market": "GB",
            "Language": "en",
            "KeywordGroup": "General",
            "KeywordType": "N/A",
            "Audience": "4-30d",
            "SpecialCampaign": "N/A",
            "MarketingNetwork": "RLSA",
            "Network": "N/A",
            "LocationType": "N/A",
            "MatchType": "PX",
            'ParseRegexId': 'LastHope-0',
            "ParserVersion": __version__
        }
        actual = self.parser.parse(
            account_name=account_name,
            campaign_name=campaign_name,
            adgroup_name=adgroup_name,
            airline_code="A3",
            search_engine="Bing",
            return_names=True,
            na=True
        )
        self.assertEqual(actual, expected)

    def test_generic_bing_remarketing_b(self):
        campaign_name = 'BL:en-GB_NB\00-Genc=Flights/Geo@GR'
        adgroup_name = 'BL:en-GB_NB\GE=Flights/PH@Converters(1-3d)'
        account_name = 'A3_GB (en)'
        expected = {
            "GeoTarget": "GR",
            "RouteLocale": "N/A",
            "CampaignName": campaign_name,
            "AdGroupName": adgroup_name,
            "AirlineName": "Aegean Airlines",
            "AirlineCode": "A3",
            "AccountName": account_name,
            "Origin": "N/A",
            "Destination": "N/A",
            "RouteType": "N/A",
            "SearchEngine": "Bing",
            "CampaignType": "Non-Brand",
            "Market": "GB",
            "Language": "en",
            "KeywordGroup": "General",
            "KeywordType": "N/A",
            "Audience": "Converters(1-3d)",
            "SpecialCampaign": "N/A",
            "MarketingNetwork": "RLSA",
            "Network": "N/A",
            "LocationType": "N/A",
            "MatchType": "PX",
            'ParseRegexId': 'LastHope-0a',
            "ParserVersion": __version__
        }
        actual = self.parser.parse(
            account_name=account_name,
            campaign_name=campaign_name,
            adgroup_name=adgroup_name,
            airline_code="A3",
            search_engine="Bing",
            return_names=True,
            na=True
        )
        self.assertEqual(actual, expected)

    def test_generic_bing_remarketing_c(self):
        campaign_name = 'BL:en-GB_NB\Search=Generic/Geo@GB'
        adgroup_name = 'BL:en-GB_NB\Generic/BM@Tickets'
        account_name = 'A3_GB (en)'
        expected = {
            "GeoTarget": "GB",
            "RouteLocale": "N/A",
            "CampaignName": campaign_name,
            "AdGroupName": adgroup_name,
            "AirlineName": "Aegean Airlines",
            "AirlineCode": "A3",
            "AccountName": account_name,
            "Origin": "N/A",
            "Destination": "N/A",
            "RouteType": "N/A",
            "SearchEngine": "Bing",
            "CampaignType": "Generic",
            "Market": "GB",
            "Language": "en",
            "KeywordGroup": "Tickets",
            "KeywordType": "Generic",
            "Audience": "N/A",
            "SpecialCampaign": "N/A",
            "MarketingNetwork": "RLSA",
            "Network": "N/A",
            "LocationType": "N/A",
            "MatchType": "BM",
            'ParseRegexId': 'CopaBrand7',
            "ParserVersion": __version__
        }
        actual = self.parser.parse(
            account_name=account_name,
            campaign_name=campaign_name,
            adgroup_name=adgroup_name,
            airline_code="A3",
            search_engine="Bing",
            return_names=True,
            na=True
        )
        self.assertEqual(actual, expected)


class TestAirlineCodeStabilityMF(unittest.TestCase):
    """
    Tests
    """

    def __init__(self, *args, **kwargs):
        """
        Declare a 'parser' attribute. (Only declared here to prevent annoying syntax highlighting; this method
        has no functionality).

        :param args:
        :param kwargs:
        :return:
        """
        self.parser = None
        super().__init__(*args, **kwargs)
        self.maxDiff = None

    def setUp(self):
        """
        Though it shouldn't be affected, set maxDiff to None (no limit to testing differences of strings in
        self.assertDictEqual).

        Instantiate the parser instance and make available.

        :return:
        """
        self.parser = Parser(cached=False)

    def test_airline_codes_match(self):
        """
        To address known bug as discovered by AIRSEM-1298
        :return:
        """
        expected = {
            'ParserVersion': __version__,
            'AirlineName': 'Xiamen',
            'AirlineCode': 'MF',  # This is the most important to have fixed
            'CampaignName': 'GD:en-TH_NB\\GDN=BlackFriday/Geo@TH',
            'AdGroupName': 'GD:en-TH_NB\\GDN=BlackFriday@Similar',
            'AccountName': 'MF - Display',
            'SearchEngine': 'Google',
            'MarketingNetwork': 'Display',
            'Language': 'en',
            'Market': 'TH',
            'CampaignType': 'Non-Brand',
            'GeoTarget': 'TH',
            'SpecialCampaign': 'N/A',
            'KeywordType': 'Similar',
            'ParseRegexId': 'CopaBrand9',  # I dont know which parseregexid it should be
            'Network': 'N/A',
            'MatchType': 'PX',
            'KeywordGroup': 'General',  # Also would accept "BlackFriday"
            'RouteLocale': 'N/A',
            'RouteType': 'N/A',
            'LocationType': 'N/A',
            'Origin': 'N/A',
            'Audience': 'N/A',
            'Destination': 'N/A'
        }
        actual = self.parser.parse(
            account_name='MF - Display',
            campaign_name='GD:en-TH_NB\\GDN=BlackFriday/Geo@TH',
            adgroup_name='GD:en-TH_NB\\GDN=BlackFriday@Similar',
            airline_code='MF',
            search_engine='Google',
            return_names=True,
            na=True
        )
        self.assertEqual(expected, actual)

    def test_airline_codes_match_GY(self):
        """
        To address known bug as discovered by AIRSEM-1298
        :return:
        """
        expected = {
            'ParserVersion': __version__,
            'AirlineName': 'Xiamen',
            'AirlineCode': 'MF',  # This is the most important to have fixed
            'CampaignName': 'GY:en-TH_NB\\GDN=BlackFriday/Geo@TH',
            'AdGroupName': 'GY:en-TH_NB\\GDN=BlackFriday@Similar',
            'AccountName': 'MF - Display',
            'SearchEngine': 'Google',
            'MarketingNetwork': 'Dynamic Remarketing',
            'Language': 'en',
            'Market': 'TH',
            'CampaignType': 'Non-Brand',
            'GeoTarget': 'TH',
            'SpecialCampaign': 'N/A',
            'KeywordType': 'Similar',
            'ParseRegexId': 'CopaBrand9',  # I dont know which parseregexid it should be
            'Network': 'N/A',
            'MatchType': 'PX',
            'KeywordGroup': 'General',  # Also would accept "BlackFriday"
            'RouteLocale': 'N/A',
            'RouteType': 'N/A',
            'LocationType': 'N/A',
            'Origin': 'N/A',
            'Audience': 'N/A',
            'Destination': 'N/A'
        }
        actual = self.parser.parse(
            account_name='MF - Display',
            campaign_name='GY:en-TH_NB\\GDN=BlackFriday/Geo@TH',
            adgroup_name='GY:en-TH_NB\\GDN=BlackFriday@Similar',
            airline_code='MF',
            search_engine='Google',
            return_names=True,
            na=True
        )
        self.assertEqual(expected, actual)




if __name__ == '__main__':
    unittest.main()
