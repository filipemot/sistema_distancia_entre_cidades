import os
import unittest

import arcpy  # type: ignore
import pytest
from arcgisscripting import ExecuteError  # type: ignore

from services.features_service import FeaturesService
from utils.constants import TYPE_FLOAT, FIELD_CITY_LNG_STR, FIELD_CITY_LAT, TYPE_DOUBLE, FIELD_CITY_LNG, \
    FIELD_CITY_LAT_STR


class TestFeatureService(unittest.TestCase):
    TEST_GDB = 'in_memory'
    feature_service: FeaturesService = FeaturesService()
    path = os.path.dirname(os.path.realpath(__file__))
    excel_file_state = os.path.join(path, 'data', 'Estados.xlsx')
    excel_file_municipios = os.path.join(path, 'data', 'Municipios.xlsx')
    table_temp = TEST_GDB + '/estados_temp'
    table_copy = TEST_GDB + '/estados_copy_temp'
    table_temp_delete = TEST_GDB + '/estados_temp_delete'
    table_temp_convert = TEST_GDB + '/city_temp_convert'

    def setUp(self):
        arcpy.conversion.ExcelToTable(self.excel_file_state, self.table_temp, 'estados', 1, '')
        arcpy.conversion.ExcelToTable(self.excel_file_state, self.table_temp_delete, 'estados', 1, '')
        arcpy.conversion.ExcelToTable(self.excel_file_municipios, self.table_temp_convert, 'municipios', 1, '')
        self.feature_service.add_computed_field(self.table_temp_convert, f'{FIELD_CITY_LAT}',
                                                f'{TYPE_FLOAT}(!{FIELD_CITY_LNG_STR}!)', TYPE_DOUBLE)
        self.feature_service.add_computed_field(self.table_temp_convert, f'{FIELD_CITY_LNG}',
                                                f'{TYPE_FLOAT}(!{FIELD_CITY_LAT_STR}!)', TYPE_DOUBLE)
        self.feature_service.convert_table_to_point(self.table_temp_convert, self.table_copy, FIELD_CITY_LAT,
                                                    FIELD_CITY_LNG)

    def test_create_excel_to_table_with_excel_file_exists(self):
        return_excel = self.feature_service.excel_to_table(self.excel_file_state, self.TEST_GDB, 'estados', 'estados')

        assert return_excel == self.TEST_GDB + '/estados'

    def test_create_excel_to_table_with_excel_file_not_exists(self):
        with pytest.raises(ExecuteError) as e:
            self.feature_service.excel_to_table(self.excel_file_state + "_file_not_found", self.TEST_GDB, 'estados',
                                                'estados')
        assert e.value.args[0].index('Invalid file type') > -1

    def test_find_all_with_columns_exists(self):
        result = self.feature_service.find_all(self.table_temp, ['Column1', 'Column2'])

        assert len(result.index) == 27
        assert result.values[0][0] == '11'
        assert result.values[0][1] == 'RO'

    def test_find_all_with_columns_not_exists(self):
        with pytest.raises(RuntimeError) as e:
            self.feature_service.find_all(self.table_temp, ['Column85', 'Column86'])

        assert e.value.args[0] == 'A column was specified that does not exist.'

    def test_convert_table_to_point_with_feature_exists(self):
        out = self.TEST_GDB + "/point"
        self.feature_service.convert_table_to_point(self.table_temp_convert, out, FIELD_CITY_LAT, FIELD_CITY_LNG)

        exists = arcpy.Exists(out)

        return exists is True

    def test_convert_table_to_point_with_fields_lat_not_exists(self):
        with pytest.raises(ExecuteError) as e:
            out = self.TEST_GDB + "/point"
            self.feature_service.convert_table_to_point(self.table_temp_convert, out, FIELD_CITY_LAT + "_Not_Found",
                                                        FIELD_CITY_LNG)

        return e.value.args[0].index('Field X_Not_Found') > -1

    def test_convert_table_to_point_with_fields_lng_not_exists(self):
        with pytest.raises(ExecuteError) as e:
            out = self.TEST_GDB + "/point"
            self.feature_service.convert_table_to_point(self.table_temp_convert, out, FIELD_CITY_LAT,
                                                        FIELD_CITY_LNG + "_Not_Found")

        return e.value.args[0].index('Field Y_Not_Found') > -1

    def test_convert_table_to_point_with_fields_feature_not_exists(self):
        with pytest.raises(ExecuteError) as e:
            out = self.TEST_GDB + "/point"
            self.feature_service.convert_table_to_point(self.table_temp_convert + "_Not_Found", out, FIELD_CITY_LAT,
                                                        FIELD_CITY_LNG)

        return e.value.args[0].index(f'Input Table: Dataset {self.table_temp_convert + "_Not_Found"} '
                                     f'does not exist') > -1

    def test_copy_features_with_feature_exists(self):
        self.feature_service.copy_features(self.table_copy, self.TEST_GDB + "/copy_features")
        count_table_copy = arcpy.GetCount_management(self.table_copy)
        count_copy_features = arcpy.GetCount_management(self.TEST_GDB + "/copy_features")

        assert count_table_copy[0] == count_copy_features[0]

    def test_copy_features_with_feature_not_exists(self):
        with pytest.raises(ExecuteError) as e:
            self.feature_service.copy_features(self.table_copy + "_Not_Found", self.TEST_GDB + "/copy_features")

        assert e.value.args[0].index(f'Dataset {self.table_copy + "_Not_Found"} does not exist or is not supported')

    def test_get_search_cursor_with_feature_exists(self):
        result = self.feature_service.get_search_cursor(self.table_copy, [FIELD_CITY_LAT])

        assert type(result) == arcpy.da.SearchCursor

    def test_get_search_cursor_with_feature_not_exists(self):
        with pytest.raises(RuntimeError) as e:
            self.feature_service.get_search_cursor(self.table_copy + "_Not_Found", [FIELD_CITY_LAT])

        assert e.value.args[0].index(f'{self.table_copy + "_Not_Found"}') > -1 and \
               e.value.args[0].index(f'cannot open') > -1

    def test_get_search_cursor_with_field_not_exists(self):
        result = self.feature_service.get_search_cursor(self.table_copy, [FIELD_CITY_LAT + "_Not_Found"])

        try:
            with result as cursor:
                for row in cursor:
                    print(row)
            assert False
        except Exception as e:
            assert str(e.args[0]).index('A column was specified that does not exist.') > -1

    def test_update_values_with_feature_exists(self):
        result = self.feature_service.update_values(self.table_copy, [FIELD_CITY_LAT])

        assert type(result) == arcpy.da.UpdateCursor

    def test_update_values_with_feature_not_exists(self):
        with pytest.raises(RuntimeError) as e:
            self.feature_service.update_values(self.table_copy + "_Not_Found", [FIELD_CITY_LAT])

        assert e.value.args[0].index(f'{self.table_copy + "_Not_Found"}') > -1 and \
               e.value.args[0].index(f'cannot open') > -1

    def test_get_update_values_with_field_not_exists(self):
        result = self.feature_service.update_values(self.table_copy, [FIELD_CITY_LAT + "_Not_Found"])

        try:
            with result as cursor:
                for row in cursor:
                    print(row)
            assert False
        except Exception as e:
            assert str(e.args[0]).index('A column was specified that does not exist.') > -1

    def test_add_field_in_table_with_feature_exists(self):
        self.feature_service.add_field_in_table(self.table_copy, 'Temp', 'TEXT')

        lst_fields = arcpy.ListFields(self.table_copy)

        x = False

        for field in lst_fields:
            if field.name == "Temp":
                x = True

        assert x is True

    def test_add_field_in_table_with_feature_not_exists(self):
        with pytest.raises(ExecuteError) as e:
            self.feature_service.add_field_in_table(self.table_copy + "_Not_Found", 'Temp', 'TEXT')

        assert e.value.args[0].index(f'Dataset {self.table_copy + "_Not_Found"} does not exist or is not supported')

    def test_add_computed_field_with_feature_exists(self):
        self.feature_service.add_computed_field(self.table_copy, 'Temp_compute',
                                                f'{TYPE_FLOAT}(!{FIELD_CITY_LAT_STR}!)', TYPE_DOUBLE)

        lst_fields = arcpy.ListFields(self.table_copy)

        x = False

        for field in lst_fields:
            if field.name == "Temp_compute":
                x = True

        assert x is True

    def test_add_computed_field_with_feature_not_exists(self):
        with pytest.raises(ExecuteError) as e:
            self.feature_service.add_computed_field(self.table_copy + "_Not_Found", 'Temp_compute',
                                                    f'{TYPE_FLOAT}(!{FIELD_CITY_LAT_STR}!)', TYPE_DOUBLE)

        assert e.value.args[0].index(f'Dataset {self.table_copy + "_Not_Found"} does not exist or is not supported')

    def test_add_computed_field_with_expression_error(self):
        with pytest.raises(ExecuteError) as e:
            self.feature_service.add_computed_field(self.table_copy, 'Temp_compute',
                                                    f'Float(!{FIELD_CITY_LAT_STR + "_Not_Found"}!)', TYPE_DOUBLE)

        assert e.value.args[0].index(f'Invalid field {FIELD_CITY_LAT_STR + "_Not_Found"}') > -1

    def test_remove_features_with_feature_exists(self):
        exists = arcpy.Exists(self.table_temp_delete)
        self.feature_service.remove_feature(self.table_temp_delete)
        exists_before_remove = arcpy.Exists(self.table_temp_delete)

        assert exists is True
        assert exists_before_remove is False

    def test_remove_features_with_feature_not_exists(self):
        exists = arcpy.Exists(self.table_temp_delete + "_not_found")
        self.feature_service.remove_feature(self.table_temp_delete + "_not_found")
        exists_before_remove = arcpy.Exists(self.table_temp_delete + "_not_found")

        assert exists is False
        assert exists_before_remove is False

    def test_get_read_row_with_field_exists(self):
        result = self.feature_service.get_search_cursor(self.table_copy, [FIELD_CITY_LAT])

        return_result = False
        with result as cursor:
            for row in cursor:
                read_row = self.feature_service.read_row(row, [FIELD_CITY_LAT])
                if FIELD_CITY_LAT in read_row:
                    return_result = True
                    break

        assert return_result

    def tearDown(self):
        arcpy.Delete_management(self.TEST_GDB)
