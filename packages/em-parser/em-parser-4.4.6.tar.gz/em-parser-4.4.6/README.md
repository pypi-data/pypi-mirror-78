
# EveryMundo Campaign and Adgroup Parser

Python module to parse campaigns and adgroup names into a human readable
format for accounts managed by EveryMundo.

## Table of Contents

- [Installation](#installation)

- [Usage](#usage)

- [Examples](#examples)

- [Versioning](#versioning)

- [Issue Reporting](#issue-reporting)

### Installation:

   ~~pip install em_parser~~
   
   Install from source:
   
    pip install git+https://github.com/EveryMundo/CampaignAdgroupParser.git
   
   **or**
   
    git clone https://github.com/EveryMundo/CampaignAdgroupParser.git  
    cd CampaignAdgroupParser
    python setup.py install 
    
### Usage:
    from em_parser import Parser
    Parser().parse(campaign, adgroup='', airline_name=None, airline_code=None, search_engine=None,
              cache=False, return_names=False)
    
or 

    from em_parser import parse
    parse(campaign=campaign, adgroup=adgroup, airline_name=None, 
        airline_code=iata_code, search_engine=se, cache=False, return_names=False, 
        na=False)
    
The function returns a Python dictionary containing human readable keys
and values.

The only required argument is campaign. All others are optional. adgroup
and airline_name or airline_code are highly recommended in order to
improve parsing accuracy.

If the airline or search engine aren’t provided, the program will try to
figure out the airline and search engine. However, because the same
naming convention is used across multiple clients and the convention
doesn’t contain any reference to the client then the program may not be
able to return the airline name and code. If you input a campaign
and ad group that uses a convention specific to one client, then the
program will be able to return the airline and airline code.


### Examples:

In: 
    
    from em_parser import Parser
    Parser().parse(r'GS:en-BD_NB\NC-Route=CA>XX>DAC/Geo@BD', r'GS:en-BD_NB\IR=CA>XX>DAC/BM',
                                      airline_name='Jet Airways', search_engine='Google')
Out:

    {'Airline': 'Jet Airways',
     'AirlineCode': '9W',
     'CampaignType': 'Non-Brand',
     'Destination': 'DAC',
     'GeoTarget': 'BD',
     'KeywordGroup': '',
     'KeywordType': 'Route',
     'Language': 'en',
     'LocationType': 'Nation>City',
     'Market': 'BD',
     'MatchType': 'BM',
     'MarketingNetwork': 'Search',
     'Origin': 'CA',
     'ParseRegexId': 'EveryMundoNonBrand1',
     'ParserVersion': '1.0.17,
     'RouteLocale': 'International',
     'RouteType': 'Connecting',
     'SearchEngine': 'Google'}
 In:
    
    Parser.parse('G-DE_NB|Route=DE>DE[de|Geo:DE]', 'R|NB_Cologne>Munich (de)')

Out:

    {'ParseRegexId': 'AirBerlinNonBrand1',
     'GeoTarget': 'DE',
     'AirlineCode': 'AB',
     'MarketingNetwork': 'Search',
     'Destination': 'Munich',
     'LocationType': 'City>City',
     'RouteType': 'Nonstop',
     'CampaignType': 'Non-Brand',
     'Airline': 'airberlin',
     'Language': 'de',
     'KeywordType': 'Route',
     'ParserVersion': '1.0.17',
     'KeywordGroup': 'General',
     'MatchType': 'PX',
     'SearchEngine': 'Google',
     'Market': 'DE',
     'Origin': 'Cologne'}

Future revisions will include additional fields like: Origin Airport,
Destination Airport, Origin City, Destination City,
Origin Nation, Destination Nation, etc…


### Versioning:
X.Y.Z

X - major release: added or changed classes and/or function calls,
changed return type of field (integer to string, etc)

Y - minor release: added new return field(s), updated how certain fields
return data i.e., RouteLocale now returns “International" instead of “I”,
added more regexes, fixed incorrect
parsing, etc

Z - negligible code change: internal code fix, optimization, etc

### New in 4.4.4

1. Fixed campaign type categorization for Generic campaigns. Everywhere the `KeywordType` is set to generic for Non-Brand
campaigns, the campaign type will be set to `Generic`

2. Added test for parsing KU (Kuwait) campaign names. 

### New in 4.3.17

Expanded format options for GSP campaigns.

### New in 4.3.16

Added coverage for some new RLSA cases outside the Google platform

### New in 4.3.15

New regexes added to conform to slightly updated generic structure

### New in 4.3.13

New regexes added corresponding to the new tCPA naming convention
standard, and the related pattern for the necessary abbreviation of the
UO campaign and adgroup names. Of notice, new values can be attributed
to the "MatchType" field. The new values, "High", "Medium", "Low", and,
"Unknown", correspond to the target CPA buckets assigned to each for
tCPA campaigns.

### New in 4.3.10

Handling the hybrid-cases where campaign names are provided by the EM
structure but the adgroup names are not compliant.


### New in 4.3.8

Added Aeromexico as another recognizable airline. 


### New in 4.3.3

Inclusion of new airline old parsings.


#### New in 4.2.0

Cached entries are now saved to disk and operate at the Parser class
instantiation level instead of the Parser.parse() level. This improves
performances greatly for the worst case scenario parsings, in
particular, for those that have no match in future executions.


#### New in 4.0.2 - 4.1.9

Bugfixes, increased verbosity, performance improvements and better
handling of outlier cases.


#### New in 4.0.1:

Now supporting Y4 old style naming conventions.


#### New in 4.0.0:

Major refactoring to allow for better modularization of parsing process
and easier integration of new parsing patterns. Important, calls of the
form:
    
    Parser.parse()
    
should be replaced with 

    Parser().parse() 

calls, or with a call to 

    em_parser.parse(),

which instantiates the object Parser(). This is to allow for better
memory and CPU optimization in further updates.

Support for Python versions < Python3.2 is now discontinued. 

##### Performance improvements 

 - (using timeit, 100 loops over 4000 rows to parse, repeated 3 times):
 - "Persistant" refers to parsing while keeping the Parser instance;
 "individual" refers to a new parser instance each iteration (4.0.0) or
 the classmethod call to Parser.parse() (3.5.5)


| Version | Persistant    | Individual    | 
|---------|---------------|---------------| 
| 3.5.5   | 648 msec/loop | 715 msec/loop | 
| 4.0.0   | 399 msec/loop | 404 msec/loop | 
| % Diff  | -38%          | -43%          | 



### Issue Reporting:

**PLEASE!!! PLEASE!!! Use this formatting when reporting issues. If you
can, provide more details.**

##### Example:

>Cc --> Route
>Added routelocale, locationtype, specialcampaign

>Wrong:
``` python
>{'AdGroupName': 'GS:en-IN_NB\\DR=BOM>00>GOI/PH',
 'Airline': 'Jet Airways',
 'AirlineCode': '9W',
 'CampaignName': 'GS:en-IN_NB\\CC-Route=BOM>00>GOI/Geo@IN - CPA',
 'CampaignType': 'Non-Brand',
 'Destination': 'GOI',
 'GeoTarget': 'IN',
 'KeywordType': 'Cc',
 'Language': 'en',
 'Market': 'IN',
 'MarketingNetwork': 'Search',
 'MatchType': 'PH',
 'Origin': 'BOM',
 'ParseRegexId': 'CopaNonbrand1',
 'ParserVersion': '2.0.0',
 'SearchEngine': 'Google'}
```
>Correct:
``` python
{'AdGroupName': 'GS:en-IN_NB\\DR=BOM>00>GOI/PH',
 'Airline': 'Jet Airways',
 'AirlineCode': '9W',
 'CampaignName': 'GS:en-IN_NB\\CC-Route=BOM>00>GOI/Geo@IN - CPA',
 'CampaignType': 'Non-Brand',
 'Destination': 'GOI',
 'GeoTarget': 'IN',
 'KeywordType': 'Route',
 'Language': 'en',
 'Market': 'IN',
 'MarketingNetwork': 'Search',
 'MatchType': 'PH',
 'Origin': 'BOM',
'Locationtype': 'City-City',
'RouteLocale': 'Domestic',
'SpecialCampaign': 'CPA'
 'ParseRegexId': 'CopaNonbrand1',
 'ParserVersion': '2.0.0',
 'SearchEngine': 'Google'}
```
