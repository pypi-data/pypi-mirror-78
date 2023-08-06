import pytest
from em_parser import Parser

competitor_test_sample_cases = [
    # (campaign_name, expected campaign type),
    # -----------------------------------------------------------------------------
    # Competitor.
    # -----------------------------------------------------------------------------
    (r'GS:en-US_CO=SteamshipAuthority/Geo@US', 'Competitor'),
    (r'GS:en-US_CO=HylineCruises/Geo@US', 'Competitor'),
    (r'GS:en-US_CO=SeastreakFerryNewBedford/Geo@US', 'Competitor'),
    (r'GS:en-US_CO=SteamshipAuthority/Geo@US', 'Competitor'),
    (r'GS:en-US_CO=IslandQueen/Geo@US', 'Competitor'),
    (r'GS:en-US_CO=DartmouthCoach/Geo@US-Bus', 'Competitor')
]

DRMKT_test_sample_cases = [
    # (campaign_name, expected campaign type),
    # -----------------------------------------------------------------------------
    # Competitor.
    # -----------------------------------------------------------------------------
    (r'GY:en-CY_NB\DynRmk/Geo@CY[GDRMKT]', 'DRMKT'),
    (r'GY:el-CY_NB\DynRmk/Geo@CY[GDRMKT]', 'DRMKT'),
    (r'GY:es-WW_NB\DynRmk/Geo@WW[GDRMKT]', 'DRMKT'),
    (r'GY:en-DE_NB\DynRmk/Geo@DE[GDRMKT]', 'DRMKT'),
    (r'GY:en-AU_NB\DynRmk/Geo@AU[GDRMKT]', 'DRMKT'),
    (r'GY:en-ES_NB\DynRmk/Geo@ES[GDRMKT]', 'DRMKT'),
    (r'GY:es-ES_NB\DynRmk/Geo@ES[GDRMKT]', 'DRMKT'),
    (r'GY:en-GB_NB\DynRmk/Geo@GB[GDRMKT]', 'DRMKT'),
    (r'GY:en-WW_NB\DynRmk/Geo@WW[GDRMKT]', 'DRMKT'),
    (r'GY:de-DE_NB\DynRmk/Geo@DE[GDRMKT]', 'DRMKT')
]


class TestCampaignTypes:
    """ Tests for campaign types. """

    @pytest.mark.parametrize('campaign_name,campaign_type', competitor_test_sample_cases)
    def test_competitor(self, campaign_name, campaign_type):
        """ Test for examples on type COMPETITOR """
        result = Parser(cached=False).parse(campaign_name)
        assert result['CampaignType'] == campaign_type

    @pytest.mark.parametrize('campaign_name,campaign_type', DRMKT_test_sample_cases)
    def test_drmkt(self, campaign_name, campaign_type):
        """ Test for examples on type DRMKT """
        result = Parser(cached=False).parse(campaign_name)
        assert result['CampaignType'] == campaign_type
