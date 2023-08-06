"""
Regex parsing. Matches from the parsing patterns can be digested by match.
"""

from collections import OrderedDict

import re


_items = [
    (
        'EveryMundo',
        OrderedDict(
            [
                (
                    'EveryMundoNonBrand1',
                    re.compile(
                        r'^(?P<SearchEngine>^.)(?P<MarketingNetwork>.):(?P<Language>..)-(?P<Market>..)_(?P<CampaignType>..)\\(?P<LocationType>..)-(?P<KeywordType>[a-zA-Z]+)=[^A-Z]*?(?P<Origin>[A-Za-z0-9]+).*?>(?P<RouteType>.*)>(?P<Destination>.*)/.*@(?P<GeoTarget>[a-zA-Z]*?)&&.*?\\(?P<RouteLocale>.).*?=.*?/(?P<MatchType>PH|BM|EX|PX|PB)[@]*(?P<KeywordGroup>.*)'
                    )
                ),
                (
                     'EveryMundoBrand1C',
                     re.compile(
                        r'^(?P<SearchEngine>^.)(?P<MarketingNetwork>.):(?P<Language>..)-(?P<Market>..)_(?P<CampaignType>..)\\(?P<KeywordType>[a-zA-Z]+)/(?P<MatchType>PH|BM|EX|PX|PB|ph|bm|ex|px|pb)@(?P<GeoTarget>[a-zA-Z]*)&&$'
                     )
                ),
                (
                    'EveryMundoBrand1',
                    re.compile(
                        r'^(?P<SearchEngine>^.)(?P<MarketingNetwork>.):(?P<Language>..)-(?P<Market>..)_(?P<CampaignType>..)\\(?P<KeywordType>[a-zA-Z]+)/[a-zA-Z]+@(?P<GeoTarget>[a-zA-Z]*)&&.*/(?P<MatchType>PH|BM|EX|PX|PB)[@]*(?P<KeywordGroup>.*)'
                    )
                ),
                (
                    'EveryMundoRLSA1',
                    re.compile(
                        r'^(?P<SearchEngine>.)(?P<MarketingNetwork>.):(?P<Language>..)-(?P<Market>..)_(?P<CampaignType>..)\\(?P<LocationType>..)-(?P<KeywordType>.*?)=(?P<KeywordGroup>[^\{\}]+?)/Geo@(?P<GeoTarget>[A-Za-z\s]*?)&&..:..-.._..\\.*?/(?P<MatchType>.*?)@(?P<Audience>.*)$'
                    )
                ),
                (
                    'EveryMundoGSP1',
                    re.compile(
                        r'^(?P<SearchEngine>.)(?P<MarketingNetwork>.):(?P<Language>..)-(?P<Market>..)_(?P<CampaignType>..)\\GSP=(?P<KeywordType>[a-zA-Z\s]+)/Geo@(?P<GeoTarget>[A-Za-z]{2,3})(\[.*\])?&&..:..-.._..\\GSP=.*?@(?P<KeywordGroup>[A-Za-z\s]*)$'
                    )
                ),
                (
                    'EveryMundoDRM1',
                    re.compile(
                        r'^(?P<SearchEngine>.)(?P<MarketingNetwork>.):(?P<Language>..)-(?P<Market>..)_(?P<CampaignType>..)\\(?:[a-zA-Z\s]+?)/Geo@(?P<GeoTarget>[A-Za-z\s]+?)&&..:..-.._..\\[a-zA-Z\s]+?@(?P<Audience>.*?\)$)'
                    )
                ),
                (
                    'EveryMundo-tCPA',
                    re.compile(
                        r'^(?P<SearchEngine>^.)(?P<MarketingNetwork>.):(?P<Language>..)-(?P<Market>..)_'
                        r'(?P<CampaignType>..)\\(?P<KeywordGroup>(tCPA))=(?:[a-zA-Z\+]*)-'
                        r'(?P<MatchType>[a-zA-Z]*)/.*@(?P<GeoTarget>[a-zA-Z]*?)'
                        r'&&'
                        r'(?:.)(?:.):(?:..)-(?:..)_(?:..)\\(?P<LocationType>..)-(?P<KeywordType>[a-zA-Z]+)'
                        r'=[^A-Z]*?(?P<Origin>[A-Za-z0-9]+).*?>(?P<RouteType>.*)>(?P<Destination>.*)/.*@(?:[a-zA-Z]*?)'
                    )
                ),
                (
                    'BaiduAbbreviated',
                    re.compile(
                        r'^(?P<CampaignType>(Non-Brand)) (?:(Dest)|(Route))'
                        r'&&'
                        r'(?P<LocationType>[A-Z]{2})-(?P<KeywordType>[a-zA-Z]*)='
                        r'(?P<Origin>([a-zA-Z]*)|{(?P<GeoTarget>[a-zA-Z]*)})>(?P<RouteType>.)>'
                        r'(?P<Destination>[a-zA-Z]*)'
                    )
                ),
                (
                    'EveryMundo-NewGeneric',
                    re.compile(
                        r'^(?P<SearchEngine>.)(?P<MarketingNetwork>.):(?P<Language>..)-(?P<Market>..)_(?P<CampaignType>..)\\(?P<KeywordType>Generic)=(?:[a-zA-Z]+)/.*@(?P<GeoTarget>[a-zA-Z]*?)'
                        r'&&'
                        r'.*?\\.*?=(?P<KeywordGroup>[a-zA-Z].*)/(?P<MatchType>PH|BM|EX|PX|PB)'
                    )
                )
            ]
         )
     ),
    (
        'airberlin',
        OrderedDict(
            [
                (
                    'AirBerlinNonBrand1',
                    re.compile(
                        r'^(?P<SearchEngine>.)-(?P<Market>.*)_(?P<CampaignType>.*?)\|(?P<LocationType>NN|NC|CN)?(?:[A-Z]{2})?-?([A-Z]-)?(?P<KeywordType>[A-Za-z]*)=.*\[(?P<Language>.*?)\|.*:(?P<GeoTarget>.*?)]&&(?P<MarketingNetwork>RK)?.*?-?.{1}\|[A-Z]*_\[?(?P<Origin>[a-zA-Z\s0-9]*)\]?>(?P<RouteType>X)?>?(?P<Destination>[a-zA-Z\s0-9]+)(?:.*?-)?(?P<MatchType>(?<=\)-)[a-zA-Z]{0,2})?(?P<KeywordGroup>(?<=-)Deal)?'
                    )
                ),
                (
                    'AirBerlinBrand1',
                    re.compile(
                        r'^(?P<SearchEngine>.)-(?P<Market>.*?)_(?P<CampaignType>.*?)\|00=\[.*\]>.*?\[(?P<Language>.*?)\|.*?:(?P<GeoTarget>.*?)]&&.*-(?P<KeywordGroup>[a-zA-Z]+)'
                    )
                ),
                (
                    'AirBerlinNonBrand2',
                    re.compile(
                        r'^(?P<SearchEngine>.)-[A-Z]*\s\((?P<Language>..).*?(?P<CampaignType>[A-Za-z\s]+)'
                    )
                ),
                (
                    'AirBerlinNonBrand3',
                    re.compile(
                        r'^(?P<MarketingNetwork>..)\|\|(?P<Market>[A-Za-z]*).*?=(?P<Origin>.*?)>(?P<Destination>.*?)\s\[(?P<Language>.{2})\|.*?:(?P<GeoTarget>.*?)]'
                    )
                ),
            ]
        )
     ),
    (
        'Jet Airways',
        OrderedDict(
            [
                (
                    'JetAirwaysNonbrand1',
                    re.compile(
                        r'^(?P<SearchEngine>^.)(?P<MarketingNetwork>.):(?P<Language>..)-(?P<Market>[A-Z]{2})_(?P<CampaignType>[A-Z]{2})\\(?P<KeywordType>.*?)=.*?>(?P<RouteType>..).*?~(?P<GeoTarget>.*?)&&.*?\\(?P<LocationType>.*?)-.*?={*(?P<Origin>.*?)}*>.*?>(?P<Destination>.*)/(?P<MatchType>..)~?(?P<KeywordGroup>(?<=~)?.*)'
                    )
                ),
                (
                    'JetAirwaysNonbrand2',
                    re.compile(
                        r'^(?P<SearchEngine>^.)(?P<MarketingNetwork>.):(?P<Language>..)-(?P<Market>..)_(?P<CampaignType>..)\\(?P<LocationType>[a-zA-Z]+?)-(?P<KeywordType>[a-zA-Z]+).*?/Geo@(?P<GeoTarget>[a-zA-Z]+).*?-\s*(?P<SpecialCampaign>[a-zA-Z]+?)&&..:..-.._..\\(?P<RouteLocale>[a-zA-Z]*?)=(?P<Origin>[a-zA-Z]+).*?>(?P<RouteType>.*?)>(?P<Destination>[a-zA-Z]+)/(?P<MatchType>..)'
                    )
                ),
                (
                    'JetAirwaysBrand1',
                    re.compile(
                        r'^(?P<SearchEngine>^.)(?P<MarketingNetwork>.):(?P<Language>..)-(?P<Market>..)_(?P<CampaignType>..).*?~(?P<GeoTarget>.*?)&&.*/(?P<MatchType>..)~(?P<KeywordGroup>.*)'
                    )
                ),
                (
                    'JetAirwaysBrand2',
                    re.compile(
                        r'^(?P<SearchEngine>^.)(?P<MarketingNetwork>.):(?P<Language>..)-(?P<Market>..)_(?P<CampaignType>..)\\(?P<KeywordType>[a-zA-Z]+).*?/Geo@(?P<GeoTarget>[a-zA-Z]+)&&..:..-.._..\\(?P<RouteLocale>[A-Z]{1})[a-zA-Z]{1}=.*?(?P<Origin>[a-zA-Z]+).*?>(?P<RouteType>.*?)>(?P<Destination>[a-zA-Z]+)/(?P<MatchType>..)$'
                    )
                ),
                (
                    'JetAirways_tCPA1',
                    re.compile(
                        r'^tCPA_New_(?P<SearchEngine>.)(?P<MarketingNetwork>.):(?P<Language>..)-(?P<Market>..)_'
                        r'(?P<CampaignType>..)\\(?P<LocationType>..)-(?P<KeywordType>[a-zA-Z]+)=[^A-Z]*?'
                        r'(?P<Origin>[A-Z]+).*?>(?P<RouteType>.*?)>(?P<Destination>.*)/.*@(?P<GeoTarget>[a-zA-Z]*?)'
                        r'&&'
                        r'.*?\\(?P<RouteLocale>.).*?=.*?/(?P<MatchType>PH|BM|EX|PX|PB)[@]*(?P<KeywordGroup>.*)'
                    )
                ),
                (
                    'JetAirways_tCPA2',
                    re.compile(
                        # 'tCPA_GL:en-AE_'
                        r'^(?:(tCPA_)+)+(?P<SearchEngine>.)(?P<MarketingNetwork>.):(?P<Language>..)-(?P<Market>..)_'
                        # 'NB\\00-Genc='
                        r'(?P<CampaignType>..)\\(?P<RouteType>..)-(?P<KeywordType>[a-zA-Z]+)='
                        # 'Deals/Geo@AE'
                        r'[^A-Z]*?(?P<KeywordGroup>[A-Z]+).*?/.*@(?P<GeoTarget>[a-zA-Z]*?)'
                        r'&&'
                        r'.*?\\.*?=.*?/(?P<MatchType>PH|BM|EX|PX|PB)[@](?P<Audience>.*)$'
                    )
                ),
                (
                    'JetAirways_DispRem',
                    re.compile(
                        r'^(?P<SearchEngine>[A-Za-z])(?P<MarketingNetwork>[A-Za-z]):(?P<Language>[a-z]{2})-(?P<Market>[A-Z]{2})_.+?/Geo~(?P<GeoTarget>[a-zA-Z]+?)&&[A-Z]{2}:[a-z]{2}-[A-Z]{2}_.+?=(?P<KeywordGroup>[A-Za-z]+)'
                    )
                ),
                (
                    'JetAirways_DSA_OutOfConvention',
                    re.compile(
                        # corresponds to the out of convention style of one type of campaign
                        r'^(?P<MarketingNetwork>(DSA))+(?:( campaign based on Feed)+)+'
                        r'&&'
                        r'(?P<KeywordGroup>(.*))$'
                    )
                )
            ]
        )
    ),
    (
        'Copa Airlines',
        OrderedDict(
            [
                (
                    'CopaNonbrand1M',
                    re.compile(
                        r'^(?P<SearchEngine>^.)(?P<MarketingNetwork>.):(?P<Language>..)-(?P<Market>..)_(?P<CampaignType>..)\\(?P<LocationType>[a-zA-Z]*)-(?P<KeywordType>[a-zA-Z]+)=(?P<Origin>.+?)>(?P<RouteType>.+?)>(?P<Destination>.+?)/Geo@(?P<GeoTarget>[a-zA-Z]+)(:?\[(?P<SpecialCampaign>.+?)\])?&&$'
                    )
                ),
                (
                    'CopaNonbrand1',
                    re.compile(
                        r'^(?P<SearchEngine>^.)(?P<MarketingNetwork>.):(?P<Language>..)-(?P<Market>..)_(?P<CampaignType>..)\\(?P<LocationType>[a-zA-Z]*)-(?P<KeywordType>[a-zA-Z]+).*?/Geo@(?P<GeoTarget>[a-zA-Z]+)(:?\[(?P<SpecialCampaign>.+?)\])?&&..:..-.._..\\(?P<RouteLocale>[A-Z]{1})[a-zA-Z]{1}=.*?(?P<Origin>[a-zA-Z]+).*?>(?P<RouteType>.*?)>(?P<Destination>[a-zA-Z]+)/(?P<MatchType>..)'
                    )
                ),
                (
                    'CopaBrand1',
                    re.compile(
                        r'^(?P<SearchEngine>.)(?P<MarketingNetwork>.):(?P<Language>..)-(?P<Market>..)_(?P<CampaignType>BR)\\(?P<KeywordType>[a-zA-Z\s]+)/(?:..?)?@(?P<GeoTarget>[A-Z]..?).*?&&..:..-.._..\\[a-zA-Z\s]+/.*?@(?P<MatchType>BMM|BM|PH|EX|PX)\+?(?P<KeywordGroup>[A-Za-z\s]+)?$'
                    )
                ),
                (
                    'CopaBrand4',
                    re.compile(
                        r'^(?P<SearchEngine>.)(?P<MarketingNetwork>.):(?P<Language>..)-(?P<Market>.+)_(?P<CampaignType>..)\\OLD-(?P<KeywordType>[a-zA-Z]+)/(?P<MatchType>..)?@(?P<GeoTarget>..)&&(?P<KeywordGroup>.*$)'
                    )
                ),
                (
                    'CopaNonbrand7',
                    re.compile(
                        r'^(?P<SearchEngine>.)(?P<MarketingNetwork>.):(?P<Language>..)-(?P<Market>..)_(?P<CampaignType>..)\\(?P<Destination>[a-zA-Z\.]+)/@?(?P<GeoTarget>..)&&(?P<KeywordGroup>[a-zA-Z]+)/(?P<MatchType>[a-zA-Z0-9]+)$'
                    )
                ),
                (
                    'CopaBrand2',
                    re.compile(
                        r'^(?P<SearchEngine>.)(?P<MarketingNetwork>.):(?P<Language>..)-(?P<Market>..)_(?P<CampaignType>BR)\\(?P<KeywordType>[a-zA-Z\s]+)/(?P<MatchType>BMM|BM|PH|EX|PX)?@(?P<GeoTarget>[A-Z]..?).*?&&..:..-.._..\\[a-zA-Z\s]+/.*?@(?P<KeywordGroup>[A-Za-z\s]+)?$'
                    )
                ),
                (
                    'CopaNonbrand10',
                    re.compile(
                        r'^(?P<SearchEngine>.)(?P<MarketingNetwork>.):(?P<Language>..)-(?P<Market>..)_(?P<CampaignType>NB)\\(?P<KeywordType>MODIFIERS|Generic|SeasonalityGeneric)/@(?P<GeoTarget>[A-Z]..?).*?&&..:..-.._..\\[a-zA-Z\s\.]+/.*?@(?P<MatchType>BM|PX|BMM)$'
                    )
                ),
                (
                    'CopaNonbrand12',
                    re.compile(
                        r'^(?P<SearchEngine>.).:(?P<Language>..)-(?P<Market>.+)_(?P<CampaignType>RM|RMK)\\Rmkt-Keywords/@(?P<GeoTarget>[A-Za-z]+?)&&..:..-.+?_(?:RMK|RM)\\(?P<Destination>[A-Za-z\s\-]+)/(?:.*?)@[a-zA-Z0-9]*$'
                    )
                ),
                (
                    'CopaNonbrand11',
                    re.compile(
                        r'^(?P<SearchEngine>.)(?P<MarketingNetwork>.):(?P<Language>..)-(?P<Market>..)_(?P<CampaignType>NB)\\(?P<KeywordType>MODIFIERS|Generic|SeasonalityGeneric)/@(?P<GeoTarget>[A-Z]..?).*?&&..:..-.._..\\[a-zA-Z\s\.]+/.*?@(?P<KeywordGroup>[A-Za-z\s\+0-9]*)$'
                    )
                ),
                (
                    'CopaNonbrand3',
                    re.compile(
                        r'^(?P<SearchEngine>.)(?P<MarketingNetwork>.):(?P<Language>..)-(?P<Market>..)_(?P<CampaignType>NB)\\(?P<Destination>[a-zA-Z\s\.]+)/(?P<MatchType>[A-Z ]..?)@(?P<GeoTarget>[A-Z]{2}?).*?&&..:..-.._..\\[a-zA-Z\s\.]+/.*?@.*?\+?(?P<KeywordGroup>[A-Za-z\s\+0-9]*)$'
                    )
                ),
                (
                    'CopaNonbrand8',
                    re.compile(
                        r'^(?P<SearchEngine>.)(?P<MarketingNetwork>.):(?P<Language>..)-(?P<Market>..)_(?P<CampaignType>..)\\ND-(?P<Destination>[a-zA-Z\.]+)/@?(?P<GeoTarget>..)&&..:..-.._..\\.*-(?P<KeywordGroup>.[a-zA-Z]+)/..@(?P<MatchType>[A-Za-z0-9]+)$'
                    )
                ),
                (
                    'CopaNonbrand13',
                    re.compile(
                        r'^(?P<SearchEngine>.)(?P<MarketingNetwork>.):(?P<Language>..)-(?P<Market>..)_(?P<CampaignType>..)\\ND={(?P<Origin>[a-zA-Z\.]+)}>(?P<RouteType>[A-Z0-9]+)>(?P<Destination>[A-Z]+?)/Geo@(?P<GeoTarget>..)&&..:..-.._..\\(?P<KeywordGroup>.[a-zA-Z]+?)={..}>..>.../(?P<MatchType>[A-Z]{2})$'
                    )
                ),
                (
                    'CopaNonbrand2',
                    re.compile(
                        r'^(?P<SearchEngine>.)(?P<MarketingNetwork>.):(?P<Language>..)-(?P<Market>..)_(?P<CampaignType>NB)\\(?P<Destination>[a-zA-Z\s\.]+)/@(?P<GeoTarget>[A-Z]{2})(-)?(?P<SpecialCampaign>[A-Za-z]+?)&&..:..-.._..\\[a-zA-Z\s\.]+/.*?@(?P<MatchType>BMM|BM|PH|EX|PX[0-9]+)?$'
                    )
                ),
                (
                    'CopaGeneric1',
                    re.compile(
                        r'^(?P<SearchEngine>.)(?P<MarketingNetwork>.):(?P<Language>..)-(?P<Market>..)_(?P<CampaignType>..)\\(?P<KeywordType>[a-zA-Z\s]+)/Geo@(?P<GeoTarget>[A-Z]..?)&&..:..-.._..\\[a-zA-Z\s]+/(?P<MatchType>[A-Z]*)$'
                    )
                ),
                (
                    'CopaNonbrand6',
                    re.compile(
                        r'^(?P<SearchEngine>.)(?P<MarketingNetwork>.):(?P<Language>..)_(?P<CampaignType>..)\\(?P<KeywordType>[a-zA-Z]+)/-(?P<SpecialCampaign>.+?)&&[a-zA-Z]+/(?P<MatchType>[a-zA-Z0-9]+)$'
                    )
                ),
                (
                    'CopaNonbrand5',
                    re.compile(
                        r'^(?P<SearchEngine>.).:(?P<Language>..)-(?P<Market>.+)_(?P<CampaignType>RM|RMK)\\(?P<MarketingNetwork>.*-)?(?P<KeywordType>[a-zA-Z-]+)/@(?P<GeoTarget>[A-Za-z]+?)&&..:..-.+?_(?:RMK|RM)\\(?P<KeywordGroup>[A-Za-z\s\-]+)/(?:.*?)@[a-zA-Z0-9]*$'
                    )
                ),
                (
                    'CopaNonbrand9',
                    re.compile(
                        r'^(?P<SearchEngine>.)(?P<MarketingNetwork>.):(?P<Language>..)-(?P<Market>..)\\(?P<SpecialCampaign>[A-Za-z0-9]+)/@(?P<GeoTarget>[A-Z]+)&&..:..-.._..\\[A-Z]+?-(?P<Destination>[A-Z]+)/$'
                    )
                ),
                (
                    'CopaNonbrand4',
                    re.compile(
                        r'^(?P<SearchEngine>.)(?P<MarketingNetwork>.):(?P<Language>..)-(?P<Market>..)_(?P<CampaignType>NB)\\(?:[a-zA-Z\s]+)/@(?P<GeoTarget>[A-Z]+?)-(?P<SpecialCampaign>[A-Z]+?)&&..:..-.._NB\\(?:[A-Za-z\s\-]+)/$'
                    )
                ),
                (
                    'CopaBrand3',
                    re.compile(
                        r'^(?P<SearchEngine>.)(?P<MarketingNetwork>.):(?P<Language>..)-(?P<Market>..)_(?P<CampaignType>BR)\\(?P<KeywordType>[a-zA-Z\s]+)/(?:..?)?@(?P<GeoTarget>[A-Z]..?).*?&&..:..-..\\(?P<KeywordGroup>[A-Za-z\s]+)/.*?@..$'
                    )
                ),
                (
                    'CopaBrand5',
                    re.compile(
                        r'^(?P<SearchEngine>.)(?P<MarketingNetwork>.):(?P<Language>..)-(?P<Market>..)_(?P<CampaignType>.+?)\\(?P<KeywordType>[a-zA-Z]+)/@?(?P<GeoTarget>..)&&..:..-.._.+?\\.*?/..@(?P<MatchType>[A-Z]+)[0-9]$'
                    )
                ),
                (
                    'CopaRLSA1',
                    re.compile(
                        r'^(?P<SearchEngine>.)(?P<MarketingNetwork>.):(?P<Language>..)-(?P<Market>..)_(?P<CampaignType>..)\\(?:..)-(?P<KeywordType>.*?)=(?P<KeywordGroup>.*?)/Geo@(?P<GeoTarget>[A-Za-z\s]*?)&&..:..-.._..\\Match=(?P<Audience>.*?)$'
                    )
                ),
                (
                    'CopaBrand6',
                    re.compile(
                        r'^(?P<SearchEngine>.)(?P<MarketingNetwork>.):(?P<Language>..)-(?P<Market>..)_(?P<CampaignType>..)\\(?P<KeywordType>[a-zA-Z\s]+)/Geo@(?P<GeoTarget>[A-Z]..?)\[(?P<SpecialCampaign>.*?)\]&&..:..-.._..\\.*?=.+?/(?P<MatchType>[a-zA-Z]+?)@(?P<KeywordGroup>.+)$'
                    )
                ),
                (
                    'CopaNonBrand16',
                    re.compile(
                        r'^(?P<SearchEngine>.)(?P<MarketingNetwork>.):(?P<Language>..)-(?P<Market>..)_(?P<CampaignType>..)\\(?P<KeywordType>[^\{\}>]+?)={(?P<Origin>[a-zA-Z\.]+)}>(?P<RouteType>[A-Z0-9]+)>(?P<Destination>[A-Z]+?)/Geo@(?P<GeoTarget>[A-Z]+)(?:-)?(?P<SpecialCampaign>.+?)?&&$'
                    )
                ),
                (
                    'CopaNonBrand14',
                    re.compile(
                        r'^(?P<SearchEngine>.)(?P<MarketingNetwork>.):(?P<Language>..)-(?P<Market>..)_(?P<CampaignType>..)\\(?P<KeywordType>[^\{\}>]+?)={(?:[a-zA-Z\.]+)}>(?:[A-Z0-9]+)>(?:[A-Z]+?)/Geo@(?P<GeoTarget>[A-Z]+)(?:-)?(?P<SpecialCampaign>.+?)?&&..:..-.._..\\.*?=\{(?P<Origin>[a-zA-Z]+?)\}>(?P<RouteType>.+?)>(?P<Destination>.+?)/(?P<MatchType>.{2})$'
                    )
                ),
                (
                    'CopaNonBrand15C1',
                    re.compile(
                        r'^(?P<SearchEngine>.)(?P<MarketingNetwork>.):(?P<Language>..)-(?P<Market>..)_(?P<CampaignType>..)\\(?:.+?)={(?P<Origin>[a-zA-Z\.]+)}>(?P<RouteType>[A-Z0-9]+)>(?P<Destination>[A-Z]+?)/(?P<MatchType>..)-(?P<SpecialCampaign>.+?)&&$'
                    )
                ),
                (
                    'CopaNonBrand15C2',
                    re.compile(
                        r'^(?P<SearchEngine>.)(?P<MarketingNetwork>.):(?P<Language>..)-(?P<Market>..)_(?P<CampaignType>..)\\(?:.+?)={(?P<Origin>[a-zA-Z\.]+)}>(?P<RouteType>[A-Z0-9]+)>(?P<Destination>[A-Z]+?)/(?P<MatchType>..)&&$'
                    )
                ),
                (
                    'CopaBrand7',
                    re.compile(
                        r'^(?P<SearchEngine>.)(?P<MarketingNetwork>.):(?P<Language>..)-(?P<Market>..)_(?P<CampaignType>..)\\[0A-Za-z-]+?=(?P<KeywordType>[^\{\}>]+?)/Geo@(?P<GeoTarget>[A-Za-z]+)(\[(?P<SpecialCampaign>[A-Z]{3})\])?&&..:..-.._..\\.+?/(?P<MatchType>[A-Z]+?)@(?P<KeywordGroup>.+?)$'
                    )
                ),
                (
                    'CopaBrand8',
                    re.compile(
                        r'^(?P<SearchEngine>.)(?P<MarketingNetwork>.):(?P<Language>..)-(?P<Market>..)_(?P<CampaignType>..)\\.+?=(?:[^\{\}>+?)/Geo@(?P<GeoTarget>[A-Za-z]+)(?:\[(?P<SpecialCampaign>[A-Z]{3})\])?&&..:..-.._..\\.+?@(?P<KeywordType>.+?)/(?P<MatchType>[A-Z]{2})'
                    )
                ),
                (
                    'CopaBrand9',
                    re.compile(
                        r'^(?P<SearchEngine>.)(?P<MarketingNetwork>.):(?P<Language>..)-(?P<Market>..)_(?P<CampaignType>..)\\.+?=(?:[^\{\}>]+?)/Geo@(?P<GeoTarget>[A-Za-z]+)(?:\[(?P<SpecialCampaign>[A-Z]{3})\])?&&..:..-.._..\\.+?@(?P<KeywordType>[^/]+)$'
                    )
                ),
                (
                    'CopaBrand10',
                    re.compile(
                        r'^(?P<SearchEngine>.)(?P<MarketingNetwork>.):(?P<Language>..)-(?P<Market>..)\\(?P<KeywordType>.+?)/Geo@(?P<GeoTarget>.+)&&$'
                    )
                ),
                (
                    'CopaBrand11',
                    re.compile(
                        r'^(?P<SearchEngine>.)(?P<MarketingNetwork>.):(?P<Language>..)-(?P<Market>..)\\(?P<KeywordType>.+?)/geo@(?P<GeoTarget>[a-zA-Z]+)&&$'
                    )
                ),
            ]
        )
     ),
    (
        'Aegean Airlines',
        OrderedDict(
            [
                (
                    'AegeanNonBrand3',
                    re.compile(
                        r'^(?P<Market>..)_(?P<KeywordType>.*?)\|(?P<CampaignType>.*?)\|(?P<Language>.*?)\|\|(?P<RouteLocale>[a-zA-Z\s]*? - [a-zA-Z\s]*?)&&.?\|(?P<Origin>[a-zA-Z\s]*?) - (?P<Destination>[a-zA-Z\s]*?)\|\|(?P<KeywordGroup>[a-zA-Z]*$)'
                    )
                ),
                (
                    'AegeanNonBrand5',
                    re.compile(
                        r'^(?P<Market>..)_(?P<KeywordType>.*?)\|(?P<CampaignType>.*?)\|(?P<Language>.*?)\|\|(?P<KeywordGroup>[a-zA-Z\s]*?)&&'
                    )
                ),
                (
                    'AegeanNonBrand1',
                    re.compile(
                        r'^(?P<Market>..)_(?P<KeywordType>.*?)\|(?P<CampaignType>[A-Za-z]+)\|(?P<Language>[A-Za-z]+)\|\|GEO:(?P<GeoTarget>[A-Za-z]*)(?P<RouteLocale>).*&&.?\|(?P<Origin>[a-zA-Z\s]*?) - (?P<Destination>[a-zA-Z\s]*?)\|\|.*?\|(?P<KeywordGroup>[a-zA-Z]*$)'
                    )
                ),
                (
                    'AegeanNonBrand4',
                    re.compile(
                        r'(?P<Market>.*?)_.*?\|(?P<CampaignType>.*?)\|(?P<Language>[A-Za-z]+)\|(?P<KeywordGroup>[a-zA-Z\s]+)&&.*?\|\|(?P<MatchType>.{2})'
                    )
                ),
                (
                    'AegeanNonBrand2',
                    re.compile(
                        r'^(?P<Market>..)_(?P<KeywordType>.*?)\|(?P<CampaignType>[A-Za-z]+)\|(?P<Language>[A-Za-z]+)\|\|GEO:(?P<GeoTarget>[A-Za-z]*)(?P<RouteLocale>).*&&.?\|(?P<Origin>[a-zA-Z\s]*?) - (?P<Destination>[a-zA-Z\s]*?)\|\|.*?\|(?P<KeywordGroup>[a-zA-Z]*$)'
                    )
                ),
                (
                    'AegeanBrand1',
                    re.compile(
                        r'^(?P<Market>.*?)_.*?\|(?P<CampaignType>.*?)\|(?P<Language>.*?)\|\|.*&&.*\|*?\|\|(?P<KeywordGroup>.*)'
                    )
                ),
            ]
        )
    ),
    (
        'Interjet',
        OrderedDict(
            [
                (
                    'InterjetNonbrand1',
                    re.compile(
                        r'^(?P<SearchEngine>.)-(?P<Market>..)_(?P<CampaignType>.*?)\|(?P<KeywordType>[a-zA-Z]+?)=.*\[(?P<Language>[a-zA-Z]*?)\|Geo:(?P<GeoTarget>[A-Za-z]*?)\]&&.\|.*?_(?P<Origin>[a-zA-Z\s]*?)>.+?>(?P<Destination>[a-zA-Z\s]+).*$'
                    )
                ),
                (
                    'InterjetIntertours1',
                    re.compile(
                        r'^(?P<SearchEngine>.)-(?P<Market>.{2})_(?P<CampaignType>.{2})\|(?P<KeywordType>.{2})=..>...\[(?P<Language>.{2})\|Geo:(?P<GeoTarget>.{2})\]&&O\|.._(?P<Origin>.+?)>(?P<Destination>.+?)\(..\)[^a-zA-Z]+(?P<KeywordGroup>[a-zA-Z\s]*)$'
                    )
                ),
                (
                    'InterjetDest1',
                    re.compile(
                        r'^(?P<SearchEngine>.)-(?P<Market>.*)_(?P<CampaignType>.*?)\|(?P<LocationType>NN|NC|CN)?(?:[A-Z]{2})?-?([A-Z]-)?(?P<KeywordType>Dest)=.*>.*?\[(?P<Language>.*?)\|.*:(?P<GeoTarget>.*?)]&&(?P<MarketingNetwork>RK)?.*?-?.{1}\|[A-Z]*_\[?(?P<Origin>[a-zA-Z\s0-9]*)\]?>(?P<RouteType>X)?>?(?P<Destination>[a-zA-Z\s0-9]+)(?:.*?-)?(?P<MatchType>(?<=\)-)[a-zA-Z]{0,2})?(?P<KeywordGroup>(?<=-)Deal)?'
                    )
                ),
                (
                    'InterjetHybrid1',
                    re.compile(
                        r'^(?P<SearchEngine>.)-(?P<Market>.*)_(?P<CampaignType>.*?)\|(?P<LocationType>NN|NC|CN)?(?:[A-Z]{2})?-?(?P<KeywordType>[A-Za-z]*)=.*\[(?P<Language>.*?)\|.*:(?P<GeoTarget>.*?)]&&(?P<MarketingNetwork>RK)?.*?-?.{1}\|[A-Z]*_\[?(?P<Origin>[a-zA-Z\s0-9]*)\]?>(?P<RouteType>X)?>?(?P<Destination>[a-zA-Z\s0-9]+).*?-\s*?(?P<KeywordGroup>[A-Za-z\s_]+)$'
                    )
                ),
                (
                    'InterjetNonBrand2',
                    re.compile(
                        r'^(?P<SearchEngine>.)-(?P<Market>..?)_(?P<CampaignType>..?)\|(?P<KeywordType>.+?)=.*?\[(?P<Language>..?)\|Geo:(?P<GeoTarget>.*?)\]&&.?\|..?_.*?>.*-(?P<MatchType>BM)?(?(MatchType)|(?P<KeywordGroup>[a-zA-Z]*))'
                    )
                ),
                (
                    'InterjetBrand1',
                    re.compile(
                        r'^(?P<SearchEngine>.)-(?P<Market>..?)_(?P<CampaignType>..?)\|.*?\[(?P<Language>..?)\|Geo:(?P<GeoTarget>.*?)\]&&.?\|..?_.*?>.*-(?P<MatchType>BM)?(?(MatchType)|(?P<KeywordGroup>[a-zA-Z]*))'
                    )
                ),
                (
                    'InterjetDDR1',
                    re.compile(
                        r'^(?P<SearchEngine>.)-(?P<Market>..)_(?P<CampaignType>.*?)\|(?P<KeywordType>[a-zA-Z]+?)=.*\[(?P<Language>[a-zA-Z]*?)\|Geo:(?P<GeoTarget>[A-Za-z]*?)\]&&.\|.*?_(?P<Origin>[a-zA-Z\s]*?)>(?P<Destination>[a-zA-Z\s]+).*$'
                    )
                ),
                (
                    'InterjetDDR2',
                    re.compile(
                        r'^(?P<SearchEngine>.)-(?P<Market>..)_(?P<CampaignType>.*?)\|[A-Za-z>\s]+\[(?P<Language>[a-zA-Z]*?)\|Geo:(?P<GeoTarget>[A-Za-z]*?)\]&&(?P<Network>DSA)\|.{2}_(?P<Destination>[A-Za-z\s]+?)\([A-Za-z]+?\)'
                    )
                ),
                (
                    'InterjetGSP1',
                    re.compile(
                        r'^(?P<SearchEngine>.)-(?P<Market>..)_(?P<MarketingNetwork>.*?)\|.*?=(?P<Origin>..)>(?P<Destination>..).*?\[(?P<Language>..)\|Geo:(?P<GeoTarget>..)\]&&[A-Z\|]*?_.*?\s(?P<KeywordType>[a-zA-Z\s]*)$'
                    )
                ),
                (
                    'InterjetRLSA1',
                    re.compile(
                        r'^(?P<SearchEngine>.)-(?P<Market>..)_(?P<CampaignType>.*?)\|.+?(?P<Origin>[A-Z]+?)>(?P<Destination>..).*?\[(?P<Language>..)\|Geo:(?P<GeoTarget>..)\]&&.*?-\s?(?P<Audience>[a-zA-Z\s]*$)'
                    )
                ),
                (
                    'InterjetBrand2',
                    re.compile(
                        r'^(?P<SearchEngine>^.)-(?P<Market>[A-Z]{2})_(?P<CampaignType>[A-Z]{2})(?P<MarketingNetwork>[A-Z]+)\|..=[A-Z\s]+?\[(?P<Language>[a-z]+?)\|[A-Za-z]+?:(?P<GeoTarget>[A-Z]+?)\]&&[A-Z]\|[A-Z]+?\s>\s[A-Za-z\s&]+$'
                    )
                ),
                (
                    'InterjetBrandDisp1',
                    re.compile(
                        r'^(?P<SearchEngine>.)-(?P<Market>..)_(?P<MarketingNetwork>[A-Z]+)\|..=.+?\[(?P<Language>..)\|Geo:(?P<GeoTarget>.+?)\]&&.\|.+$'
                    )
                ),
                (
                    'InterjetBrandDisp2',
                    re.compile(
                        r'^(?P<SearchEngine>.)-(?P<Market>..)_(?P<MarketingNetwork>[A-Z]+)\|..=.+?\[(?P<Language>..)\|Geo:(?P<GeoTarget>.+?)\]&&4O.+$'
                    )
                ),
                (
                    'InterjetRMK1',
                    re.compile(
                        r'^(?P<SearchEngine>.)-(?P<Market>..)_(?P<CampaignType>[A-Z]+?)\|.+?>.+?\[(?P<Language>..)\|Geo:(?P<GeoTarget>.+?)\]&&.+?>\s?(?P<Audience>[\w\s-]+)$'
                    )
                ),
                (
                    'InterjetNBDisp',
                    re.compile(
                        r'^(?P<SearchEngine>.)-(?P<Market>..)_(?P<CampaignType>[A-Z]{2}?)(?P<MarketingNetwork>D).+?\|(?P<KeywordType>.+?)=..>.+?\[(?P<Language>..)\|Geo:(?P<GeoTarget>.+?)\]&&.+$'
                    )
                ),
            ]
        )
    ),
    (
        'Volaris',
        OrderedDict(
            [
                (
                    "VolarisOldGeneric1",
                    re.compile(
                        r'^(?:(Volaris_)(Max)?_?)+(?P<MarketingNetwork>(Sur de )((CA)|(TX)))?'
                        r'(?:( - Promo tarifa Solo Hoy))?'
                        r'&&'
                        r'(?:(.*)?)?$'
                    )
                ),
                (
                    "VolarisOldGeneric2",
                    re.compile(
                        r'^(?:'
                            # These are explicitly listed.
                            r'(Volaris)|(Destinos_Otros_Top)|(Aniversario)|(Navidad)|(Campaign #1)|'
                            r'(San Diego)|(Carrera Volaris 5k & 10k)|(Volaris Chicago México)|'
                            r'(Volaris Chicago México Banners)|(Volaris Chicago Hispanos)|(Volaris Chicago Inglés)'
                        r')'
                        r'&&'
                        r'(?:(.*))$'
                    )
                ),
                (
                    'VolarisOldGeneric3',
                    re.compile(
                        r'^(?:(Genéricos)|(Genéricas)|(Genericas))_'
                        r'(?:([a-zA-Záéíóúñü _]+))'
                        r'&&'
                        r'(?:(.*))$'
                    )
                ),
                (
                    'VolarisOldGeneric4',
                    re.compile(
                        r'^(?:(E-)|(M-G)|(M-S-G)|(S-G))'
                        r'(?:((-Ipod-Iphone)|(-Ipad)))?'
                        r' ?'
                        r'(?:(Generic)|(Genérico))'
                        r'&&'
                        r'(?:(.*))'
                    )
                ),
                (
                    'VolarisOldGenericOther',
                    re.compile(
                        r'^(?:(Hispanos)|(VTP)|(SJC)|(PyMES)|(Servicios)|(VOLARIS_CONCURSO_PFL_2009)|'
                        r'(Bicentenario)|(Inglés)|(Estados)|(Remarketing for Search))'
                        r'&&'
                        r'(?:(.*))$'
                    )
                ),
                (
                    'VolarisOldNonBrand2',
                    re.compile(
                        # GUA - SF <airplane to:>|<route:> ...
                        r'^(?P<Market>(GUA))+(?:( - SF - ))+'
                        r'(?P<KeywordType>((Route)|(Airplane to))+)+:?'
                        # Ensure origin comes together with the ' - ' string. 
                        # Origin/ destination come as 
                        r'((?P<Origin>[a-zA-Záéíóúñü ]+)(?= - ))?(?:( - ))?(?P<Destination>[a-zA-Záéíóúñü ]+)'
                        # Delimit to adgroup
                        r'&&'
                        # Adgroups are generally irrelavant, and have the same information as the campaign name
                        r'(?:(.*))$'
                    )
                ),
                (
                    'VolarisOldNonBrand1',
                    re.compile(
                        # SF Airplane to: <Destination>, or SF Route: <origin> - <destination>. Include Typo case cSF
                        r'^(?:c?(SF - ))+(?P<KeywordType>((Route)|(Airplane to))+)+:?'
                        # Ensure origin comes together with the ' - ' string.
                        r'((?P<Origin>[a-zA-Záéíóúñü ]+)(?= - )(?! - To mexico))?(?:( - ))?'
                        r'(?P<Destination>[a-zA-Záéíóúñü ]+)(\(?(?P<Market>(USA)|(GUA)|(PR)|(CR))\)?)?'
                        # Ignore the device specific bits
                        r' ?(?:(\((Mobile)|(Desktop)|(mobile)|(desktop)|(New)|(new)\)))?'
                        # Ignore the wierd numbers
                        r'(?:[0-9. ()]+)?'
                        # Though they say 'from guatemala' that doesn't actually geotarget guatemala, nor do the 
                        # keywords reflect this. Therefore, ignore.
                        r'(?:((from)|(From)|(to)|(To)) ((Guatemala)|(guatemala)|(mexico)|(Mexico)))?'
                        # Delimit to adgroup
                        r'&&'
                        # Adgroups are generally irrelavant, and have the same information as the campaign name
                        r'(?:(.*))$'
                    )
                ),
                (
                    'VolarisOldNonBrand3',
                    re.compile(
                        # Example: 'S-R SAN&&MEX', 'S-R SAN&&CUU (conexión)'
                        r'^(?:(S-R )+)'
                        r'(?P<Origin>('
                            r'[a-zA-Z]+)|(San Luis Potosi)|(Ciudad Juarez)|(Ciudad Obregon)|'
                            r'(Los Cabos)|(Puerto Vallarta)|(Los Mochis)|(La Paz)'
                        r')+'
                        r'(?:( NOT))?'
                        r'&&'
                        r'(?P<Destination>[a-zA-Záéíóúñü ]+)+'
                        r'(\((?P<RouteType>[a-zA-Záéíóúñü ]+)\))?$'
                    )
                ),
                (
                    'VolarisOldNonBrand5',
                    re.compile(
                        # Exception to VolarisOldNonBrand4 that must be checked before OldNonBrand4
                        r'^(?:(S-D-OAnti-camión))+'
                        r'&&'
                        r'(?P<Destination>.*)?$'
                    )
                ),
                (
                    'VolarisOldNonBrand4',
                    re.compile(
                        # Case: TEST S-D México DF&&Distrito Federal - Ofertas
                        r'^(?:(TEST ))?(?:(M-))?(?:(S-D))+(?:(-Iphone))?(?:(-Ipod))?(?:(-Ipad))?'
                        r' (?P<Destination>[a-zA-Záéíóúñü .]+)'
                        r'&&'
                        r'(?:.*)$'
                    )
                ),
                (
                    'VolarisOldNonBrand6',
                    re.compile(
                        # Case: Destino_DF&&Autobuses
                        r'^(?:(Destino)+s?_+)+'
                        r'(?P<Destination>([a-zA-Záéíóúñü _]+))'
                        r'&&'
                        r'(?:.*)$'
                    )
                ),
                (
                    'VolarisOldNonBrand7',
                    re.compile(
                        # Case: 'SEM | Destinos: Multiples | GEO: Monterrey&&Chihuahua | Pasajes - Económico'
                        # Note: this generally leaves whitespace characters in with the destination, be sure to strip()
                        # that out
                        r'^(?:(SEM \| Destinos: [a-zA-Záéíóúñü ]+\| GEO: ))'
                        r'(?P<GeoTarget>([a-zA-Záéíóúñü ]+))'
                        r'&&'
                        r'(?P<Destination>([a-zA-Záéíóúñü ]+))'
                        r'(?:( \| ))+(?P<KeywordGroup>[a-zA-Záéíóúñü -]+)$'
                    )
                ),
                (
                    'VolarisOldNonBrand8',
                    re.compile(
                        # Case: 'SEM | Rutas | GEO: MX&&Veracruz-Df | Viajes'
                        # Note: Only 1 campaign, but many adgroup variations
                        r'^(SEM \| Rutas \| GEO: (?P<GeoTarget>(MX)))+'
                        r'&&'
                        r'((?P<Origin>[a-zA-Záéíóúñü ]+)-(?P<Destination>([a-zA-Záéíóúñü ]+)))'
                        r'(?:( \| ))(?P<KeywordGroup>([a-zA-Záéíóúñü -]+))$'
                    )
                ),
                (
                    'VolarisOldNonBrand9',
                    re.compile(
                        # Case: 'D-FAT&&GDL'
                        r'^(?:(D-))+'
                        r'(?P<Origin>[A-Z]+)+'
                        r'&&'
                        r'((?P<Destination>[A-Z]+)$|(?:(Ad group #1))$)'
                    )
                ),
                (
                    'VolarisOldNonBrand12',
                    re.compile(
                        # Case: SanFrancisco-Mexicalli&&SanFrancisco-Mexicalli
                        # Case: LosAngeles-Los Cabos&&LosAngeles-Los Cabos
                        r'^(?P<Origin>(LosAngeles)|(SanFrancisco))'
                        r'\-'
                        # More options here. Limit damage by excplicitly identifying each possible destiantion
                        r'(?P<Destination>((cancun)|(culiacan)|(Guadalajara)|(La Paz)|(los cabos)|(mazatlan)|'
                        r'(Mexicalli)|(Merida)|(merida)|(tijuana)|(Toluca)))'
                        r'&&'
                        r'(?:(.*))?$'
                    )
                ),
                (
                    'VolarisOldNonBrand13',
                    re.compile(
                        # Case: Los Angeles-Cancun-SP&&Pasajes
                        # Case: Los Angeles-Cancun-SP&&Spring Break
                        # Case: Los Angeles-Cancun-EN&&
                        # Case: Los Angeles-Cancun-EN&&
                        # The EN vs SP has LITERALLY nothing to do with the language
                        r'^((?P<Origin>(Los Angeles))-(?P<Destination>(Cancun))-)(?:(SP)|(EN))'
                        r'&&'
                        r'(?:(.*))$'
                    )
                ),
                (
                    'VolarisOldNonBrand14',
                    re.compile(
                        # Leftover cases, explicitly names.
                        r'^(?:((Los Cabos)|(Tijuana)|(Urupan)|(Mérida)|(Hermosillo)|'
                        r'(Acapulco-Target Acapulco/Tijuana)|(La Paz)|(CD Mexico)|(Zacatecas LAX)|(Aguascalientes)|'
                        r'(Leon Bajio)|(Merida)|(Guadalajara)|(Morelia LAX)|(Morelia)|(Toluca)|(Oaxaca)|(Mazatlan)|'
                        r'(Puebla)|(Chihuahua)|(Oakland)|(Mexico - DF)|(Cancun)|(Monterrey)|(Mexicalli)|(Pto Vallarta)|'
                        r'(Culiacan)|(Mexicali - Mèxico)|(Acapulco)))'
                        r'&&'
                        r'(?:(.*))$'
                    )
                ),
                (
                    'VolarisOldBrandGeoTarget',
                    # 'TEST S-B Branding', 'GUA - TEST S-B Branding', 'S-B Branding (Chicago)'
                    re.compile(
                        # Campaign name
                        # Optional - market will be GT if prefixed with GUA
                        r'^((?P<Market>(GUA))?(?:( \- )))?(?:(TEST ))?'
                        # Sometimes present (but not always) S-B Branding, or M-B Mobile / Branding, or TEST
                        r'(?:((M\-B Mobile \/ )|(S\-B )))+'
                        # Really the only standard for these campaigns
                        r'(?P<CampaignType>(Branding))+'
                        # Geo target OR useless information
                        r'((?P<GeoTarget>[a-zA-Z \(\)].*)|(\(49k\)))?'
                        # Adgroup delimiter
                        r'&&'
                        # Adgroup value
                        r'(?P<KeywordGroup>.*)?$'
                    )
                ),
                (
                    'VolarisMexicoOldBrand',
                    # 'Branding Campaign - June 28 (in) (was 65)&&...'
                    re.compile(
                        # Campaign name
                        r'^(?P<CampaignType>(Brand))+(?:(ing Campaign \- June 28 \(in\) \(was 65\)))+' 
                        # Adgroup delimiter
                        r'&&' 
                        # Adgroup value
                        r'(?P<KeywordGroup>.*)$'
                    )
                ),
                (
                    "VolarisOldBrandLang",
                    re.compile(
                        # Campaign name 'E-English Branding' or 'E-Spanish Branding'
                        r'^(?:E-)+(?P<Language>(English)|(Spanish))+(?: )+(?P<CampaignType>(Brand))+(?:ing)+' 
                        # Adgroup delimiter
                        r'&&' 
                        # Adgroup value
                        r'(?P<KeywordGroup>.*)$'
                    )
                ),
                (
                    "VolarisOldBrandAncillary",
                    re.compile(
                        # Branding - Already bought
                        r"(?P<CampaignType>Branding)+"
                        r"(?P<KeywordType>(.*already bought))+"
                        # Adgroup value
                        r"&&"
                        r"(?P<KeywordGroup>.*)$"
                    )
                ),
                (
                    "VolarisOldBrandOther",
                    re.compile(
                        # T - B Prueba Tablet&&Ad group #1
                        r'^(?:(T - B Prueba Tablet)|(VOLARIS MX))'
                        r'&&'
                        r'(?:(Ad group #1)|(Volaris Tablet)|(Volaris MX))$'
                    )
                ),
                (
                    "VolarisOldDSA",
                    re.compile(
                        # Dynamic&&Cancun
                        # Dynamic Search Ads&&
                        r'^(?P<MarketingNetwork>(Dynamic))+(?:( Search Ads))?'
                        r'&&'
                        # Since the campaign names here are so generic, we must list out the adgroups to prevent false 
                        # positives on matching to this pattern
                        r'(?P<Destination>(Cancun)|(Guadalajara)|(Tijuana)|(Mexicali)|(Mexico)|(Monterrey)|(Hermosillo)'
                        r'|(Chicago)|(Los Angeles))$'

                    )
                ),
                (
                    "VolarisOldDisplay2",
                    re.compile(
                        # Campaign name
                        # Content Blast, Content Blast Agosto, Blast Julio, D-B Blast Feb 2012
                        r'^((?:(Content ))|((?P<MarketingNetwork>D)+?-+(?P<CampaignType>B)+?) )?' 
                        r'((?:(Blast))+.)' 
                        r'((?P<GeoTarget>(Chicago)+)|(?:.+))?' 
                        # Delimiter
                        r'&&' 
                        # Adgroup value
                        r'(?P<Audience>(.*))$'
                    )
                ),
                (
                    "VolarisOldDisplay3",
                    re.compile(
                        # Smart Display Mexico
                        r'^(?P<KeywordType>(Smart))+.(?P<MarketingNetwork>(Display))?.?' 
                        r'(?P<Market>(US)|(Mexico)|(mexico))?.?(?P<Language>(En)|(Es))?' 
                        r'&&' 
                        r'(?P<KeywordGroup>.*)$'
                    )
                ),
                (
                    "VolarisOldDisplay4",
                    re.compile(
                        r'(?P<KeywordType>(2da Ola))+(?:[ -]+)?'
                        r'(?P<GeoTarget>[a-zA-Z ]+)?'
                        r'&&'
                        r'(?P<KeywordGroup>.*)$'
                    )
                ),
                (
                    "VolarisOldDisplay5",
                    re.compile(
                        r'('
                        r'(?:(Smart Mexico Display)+)|'
                        r'(?:(Viaja Gratis Display)+)|'
                        r'(?:(Cancún 04Abril)+)|'
                        r'(?:(Volaris_Content)+)|'
                        r'(?:(Volaris\-Guadalajara\-Placement_USA)+)|'
                        r'(?:(Mkt-Test Case week3)+)|'
                        r'(?:(Flighted Campaigns Mexico #2)+)|'
                        r'(?:(Masthead 1-September)+)|'
                        r'(?:(Promo Negra Mayo 2014)+)|'
                        r'(?:(Anticamión)+)|'
                        r'(?:(Volaris\-Guadalajara\-Placement_MEX)+)|'
                        r'(?:(Negra 20-23 Junio)+)|'
                        r'(?:(Mobile Display)+)|'
                        r'(?:(3 Dias - Viaja en Diciembre - Abril 15)+)|'
                        r'(?:(499 VClub)+)|'
                        r'(?:(Mkt-Test Case week 2 #2)+)|'
                        r'(?:(Test \| In-Market Interest California #2)+)|'
                        r'(?:(Mobile / Travel Eartlink)+)|'
                        r'(?:(Promo Negra MEX)+)|'
                        r'(?:(Volaris Ventas)+)|'
                        r'(?:(Display - Final Junio)+)|'
                        r'(?:(GDA California)+)|'
                        r'(?:(Test \| In-Market Interest California)+)|'
                        r'(?:(Test \| Select KW California)+)|'
                        r'(?:(Promo Negra Junio)+)|'
                        r'(?:(Buen Fin \| Promodescuentos)+)|'
                        r'(?:(D-Campaña-Tijuana2013Junio)+)|'
                        r'(?:(Volaris-Guadalajara-Contextual_Mex)+)|'
                        r'(?:(Mexico Smart)+)|'
                        r'(?:(D-Campaña-Display 2013)+)|'
                        r'(?:(Masthead1-SEPT)+)|'
                        r'(?:(Mkt-Test Case week 2)+)|'
                        r'(?:(Flighted Campaigns Mexico)+)|'
                        r'(?:(Negra 20 - 23 Julio)+)|'
                        r'(?:(Mkt-Test Case)+)|'
                        r'(?:(Volaris Banners)+)|'
                        r'(?:(S-O Travel Eartlink)+)|'
                        r'(?:(Flighted Campaigns USA)+)|'
                        r'(?:(Volaris-Guadalajara-Contextual_USA)+)|'
                        r'(?:(Remarketing)+)+(?![a-zA-Z0-9,_|=/\\;\[\](){}+:!@#$%^*=\'"\-])|'
                        r'(?:(Campaign #2)+)|'
                        r'(?:(Test \| Select KW California #2)+)|'
                        r'(?:(Volaris_Content - Promo tarifa Solo Hoy)+)'
                        r')'
                        r'&&'
                        r'(?:(.*))?$'
                    )
                ),
                (
                    "VolarisOldDisplay6",
                    re.compile(
                        # S-O DSA Prueba&&All websites
                        # S-O Escápate&&Oferta
                        # M-S-O Escápate&&Vuelo
                        r'^(?:(M-)?(S-O )+)'
                        r'(?:(Escápate)|(DSA Prueba))'
                        r'&&'
                        r'(?:(.*))'
                    )
                ),
                (
                    "VolarisOldDisplayGSP",
                    re.compile(
                        # GSP is an important distinction to make with the marketing network
                        r'(?:(Prueba)+)?.?-?.?(?P<MarketingNetwork>((gsp)|(GSP))+)+.?_?'
                        # Campaign is either trying to pull bus customers, or is geo targeted accordingly
                        r'((?P<KeywordType>(Bus Switching ))|'
                        r'((?:prueba_)(?P<GeoTarget>(Costa_Rica))(?P<KeywordType1>(_tiquetes)))|'
                        r'(?P<GeoTarget1>[a-zA-Z _]+))'
                        r'&&'
                        # In this case, we get nothing informative out of the adgroup name
                        r'(?:.*)$'
                    )
                ),
                (
                    "VolarisOldVideo1",
                    re.compile(
                        #########################
                        # Examples:
                        # "YT | Tarifa Limpia | Costa Rica #3 #2 #2 #2&&Videos"
                        # "Tarifa Limpia | OPT (12)&&Grupo de segmentación 1 (In-Display)"
                        #########################
                        # Optional 'YT |' prefix
                        r'^(?:(YT \| ))?' 
                        # We are guarenteed the 'Tarifa Limpia'
                        r'(?P<MarketingNetwork>(Tarifa Limpia))+'
                        # About half of this pattern have this  OPT (<number>) suffix or the OPT (FUN) suffix
                        r'(?:( \| ))(?:(OPT ))?(?:[a-zA-Z0-9\(\)]+)?'
                        # Many have the market of focus, (CR only)
                        r'(?P<Market>(Costa Rica))?(?:[0-9 #]+)?'
                        # Delimiter
                        r'&&'
                        # Adgroup value
                        r'(?:.*)$'
                    )
                ),
                (
                    "VolarisOldVideo2",
                    re.compile(
                        # Absolutely a brute-force matching. Patterns are non-existant or too diverse.
                        r'^(?:(10mo Aniversario adstream))|(?:(10mo aniversario in-display))|(?:(7mo Aniversario))|' 
                        r'(?:(7mo Aniversario OK))|(?:(Alex Lora (Completo)))|(?:(Alex Lora Volars))|' 
                        r'(?:(Algo de ti es mexicano))|(?:(Aniversario 9))|(?:(Anticamión & Escápate))|' 
                        r'(?:(App Volaris))|(?:(Bus switching: camion vs avión))|(?:(Criaturas misteriosas))|' 
                        r'(?:(D-V Volaris Aniversario TrueView))|(?:(Educación temporada alta))|' 
                        r'(?:(Enamorados de Ponle tu Nombre))|(?:(Escápate 2013))|(?:(Escápate 2013 promo))|' 
                        r'(?:(Escápate Godinez))|(?:(Guatemala #desdeelaire))|(?:(Hablemos Claro))|' 
                        r'(?:(Inaugural TLC TIJ))|(?:(Juanes))|(?:(Juntos contra el cáncer de mama))|(?:(Mundial #1))|' 
                        r'(?:(Mundial Godinez))|(?:(Navidad))|(?:(No más camión))|(?:(Opcionales))|' 
                        r'(?:(Promo - Mama En 12 horas))|(?:(Promo aniversario (Customer Match)))|' 
                        r'(?:(Promocion aniversario))|(?:(Prueba))|(?:(Prueba migración))|' 
                        r'(?:(Sala Remates - Mayo 2014))|(?:(Sigue tu pasión))|(?:(Sky writing))|' 
                        r'(?:(Tarjeta Volaris Invex))|(?:(TLC TIJ))|' 
                        r'(?:(Tu Decides))|(?:(US to GDL))|(?:(Viajemos Todos por México))|(?:(Vuela fácil Mobile))|' 
                        r'(?:(Vuela Fácil views))|(?:(Vuela Fácil views Customer Match))|(?:(Vuelo Inaugural))|' 
                        r'(?:(Vuelo inaugural TLC-TIJ))|(?:(Xolos))' 
                        r'&&' 
                        r'(?:.*)$'
                    )
                ),
                (
                    "VolarisCarga",
                    re.compile(
                        r'^(?:(Volaris ))?(?:(Encarga))+'
                        r'&&'
                        r'(?:(.*))$'
                    )
                ),
                (
                    "VolarisVClub",
                    re.compile(
                        r'(?:(Vclub))+'
                        r'&&'
                        r'(?:(Volaris Club))+$'
                    )
                ),
                (
                    "VolarisOldVacations",
                    re.compile(
                        # Explicitly named. Matched together due to similar general attributes and intended parsing.
                        r'^((Avión \+ Hotel)|(Test - Paquete de Viajes)|(Landing anticamion))+'
                        r'&&'
                        r'(?:.*)$'
                    )
                ),
                (
                    "VolarisAppDownload",
                    re.compile(
                        # Volaris Android App - Universal Download
                        # Volaris Android App - Search - GenericTerms&&Aerolineas
                        # Mobile App (Search) Ipod - Iphone&&Branding
                        r'(?:(Volaris ))?'
                        r'(?:(Android )|(Mobile ))?'
                        r'(?:(App)|(aPP 2))+.?'
                        r'(?:(\(Search\) )|(- ?Universal Download)|(- Search - ))?'
                        r'(?:(Ipod - Iphone)|(Ipad)|(Android))?'
                        r'([ -]+)?((?:(Re Engagement))|(?P<KeywordType>(Competition)|(Generic))( Terms))?'
                        r'(?:(Branded)|(\(Opti\)))?'
                        r'&&'
                        r'('
                        # Adgroup cases: Brand
                        r'((?P<CampaignType>(Brand))((ed)|(ing)))'
                        # Origin - Destination NB
                        r'|((?P<Origin>[a-zA-Záéíóúñü ]+)+( - )+(?P<Destination>[a-zA-Záéíóúñü ]+)+)'
                        # Anything else
                        r'|(?:(.*))'
                        r')$'
                    )
                ),
                (
                    "VolarisOldCompetitors",
                    re.compile(
                        # Competencia&&
                        r'(?:(Competencia))'
                        r'&&'
                        r'(?:(.*))$'
                    )
                ),
                (
                    "VolarisInvex",
                    re.compile(
                        # Volaris - Invex&&
                        r'^(?:(Volaris - Invex))+'
                        r'&&'
                        r'(?:(.*))$'
                    )
                ),
                # These last Non Brand campaigns are numerous, but require exhausting the other patterns before
                # attempting to match; They are incredibly vague and risks matching too broadly.
                (
                    "VolarisOldNonBrand10",
                    re.compile(
                        r'^(?!RMK)((SF-)(?P<Origin>(Oakland))-(?P<Destination>(Cancun))-(?P<Language>(EN)|(SP)))'
                        r'&&'
                        r'(?:(.*))$'
                    )
                ),
                (
                    "VolarisOldNonBrand11",
                    re.compile(
                        r'^(?:(Mobile / ))?(?P<Origin>([a-zA-Záéíóúñü ]+))+(?:(_US))+'
                        r'&&'
                        r'(?:(.*))$'
                    )
                ),
            ]
        )
    ),
    (
        'LastHope',
        OrderedDict(
            [
                (
                    'LastHope-0',
                    re.compile(
                        r'^(?P<SearchEngine>.)(?P<MarketingNetwork>.):(?P<Language>..)-(?P<Market>..)_(?P<CampaignType>..).+@(?P<Audience>.{4,})&&.*?'
                    )
                ),
                (
                    'LastHope-0a',
                    re.compile(
                        r'^(?P<SearchEngine>.)(?P<MarketingNetwork>.):(?P<Language>..)-(?P<Market>..)_(?P<CampaignType>..).+@(?P<GeoTarget>.{2})&&.*?@(?P<Audience>.*)',
                    )
                ),
                (
                    'LastHope-1',
                    re.compile(
                        r'^(?P<SearchEngine>.)(?P<MarketingNetwork>.):(?P<Language>..)-(?P<Market>..)_(?P<CampaignType>..).+(?<=\[(?P<SpecialCampaign>[A-Z]{3})\])?.*(@(?P<Audience>.*))?'
                    )
                ),
                (
                    'LastHope-2',
                    re.compile(
                        r'^(?P<SearchEngine>.)(?P<MarketingNetwork>.):(?P<Language>..)_(?P<CampaignType>..).+(?<=\[(?P<SpecialCampaign>[A-Z]{3})\])?.*'
                    )
                ),
            ]
        )
    ),
]


########################################################################################################################
# REGEXES are as defined above (case: campaignname + adgroup name)
########################################################################################################################
REGEXES = OrderedDict(_items)

########################################################################################################################
# CAMP_REGEXES are as defined above, up to the delimiter '&&' (case: campaignname only))
########################################################################################################################
# Create them from the compiled regex patterns
CAMP_REGEXES = OrderedDict()
for airline in REGEXES.keys():
    # Recompile the campaignname only substring of the pattern string
    for regex in REGEXES[airline].keys():
        # The ParseRegexId should be the same as the original, but with -CampaignOnly appended
        try:
            # Case 1: (Alex's regexes) Pattern is delimited with "&&" directly
            CAMP_REGEXES[airline][regex + '-CampaignOnly'] = re.compile(
                REGEXES[airline][regex].pattern.split('&&')[0] + '&&'
            )
        except KeyError:
            # If the airline's codes havent yet been added, create the ordered dict instance
            CAMP_REGEXES[airline] = OrderedDict()
            CAMP_REGEXES[airline][regex + '-CampaignOnly'] = re.compile(
                REGEXES[airline][regex].pattern.split('&&')[0] + '&&'
            )
