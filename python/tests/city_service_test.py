import unittest

from unittest import mock
from unittest.mock import Mock, patch, call

from services.base_service import BaseService
from services.city_service import CityService
from utils.constants import FEATURE_CITY


class TestCityService(unittest.TestCase):

    @patch("services.city_service.CityService.__init__")
    def test_city_service_prepare_data(self, spy_city_service_init):
        spy_city_service_init.return_value = None

        with mock.patch.object(CityService, "_CityService__create_table") as spy_create_table:
            with mock.patch.object(CityService, "_CityService__add_fields_in_table") as spy_add_fields_in_table:
                with mock.patch.object(CityService, "_CityService__save_field_state") as spy_save_field_state:
                    with mock.patch.object(CityService, "_CityService__convert_feature_to_cities") \
                            as spy_convert_feature_to_cities:
                        spy_convert_feature_to_cities.return_value = None
                        spy_add_fields_in_table.return_value = None
                        spy_save_field_state.return_value = None
                        spy_create_table.return_value = None
                        city_service = CityService()
                        city_service.features_service = Mock()
                        city_service.table_city_geo = 'table_city_geo'
                        city_service.features_service.update_values.return_value = []
                        city_service.table_city = "table_city"
                        city_service.city_db_services = Mock()
                        city_service.prepare_data()

        assert city_service.table_city == 'table_city'
        city_service.city_db_services.delete_all_cities.assert_called_once()
        city_service.city_db_services.insert_cities.assert_called_once()

    @patch("services.city_service.CityService.__init__")
    def test_city_service_remove_feature(self, spy_city_service_init):
        with mock.patch.object(BaseService, "configs", {'workspace': 'workspace'}) as spy_config_service:
            spy_city_service_init.return_value = None

            city_service = CityService()
            city_service.features_service = Mock()
            city_service.table_city_geo = 'table_city_geo'
            city_service.table_city = 'table_city'
            city_service.state = Mock()
            city_service.remove_feature()

            assert city_service.table_city == 'table_city'
            expected_calls_remove_feature = [call('table_city_geo'), call("workspace//" + FEATURE_CITY)]
            city_service.features_service.remove_feature.assert_has_calls(expected_calls_remove_feature)
            city_service.state.remove_feature.assert_called_once()
