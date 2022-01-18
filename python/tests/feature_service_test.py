import os
import unittest

import arcpy

from services.features_service import FeaturesService


class TestFeatureService(unittest.TestCase):
    TEST_GDB = 'in_memory'
    feature_service: FeaturesService = FeaturesService()
    path = os.path.dirname(os.path.realpath(__file__))
    excel_file = os.path.join(path, 'data', 'Estados.xlsx')
    table_temp = TEST_GDB + '/estados_temp'
    table_temp_delete = TEST_GDB + '/estados_temp_delete'

    def setUp(self):
        arcpy.conversion.ExcelToTable(self.excel_file, self.table_temp, 'estados', 1, '')
        arcpy.conversion.ExcelToTable(self.excel_file, self.table_temp_delete, 'estados', 1, '')

    def test_create_excel_to_table(self):
        return_excel = self.feature_service.excel_to_table(self.excel_file, self.TEST_GDB, 'estados', 'estados')

        assert return_excel == self.TEST_GDB + '/estados'

    def test_find_all(self):
        result = self.feature_service.find_all(self.table_temp, ['Column1', 'Column2'])

        assert len(result.index) == 27
        assert result.values[0][0] == '11'
        assert result.values[0][1] == 'RO'

    def test_remove_features(self):
        exists = arcpy.Exists(self.table_temp_delete)
        self.feature_service.remove_feature(self.table_temp_delete)
        exists_before_remove = arcpy.Exists(self.table_temp_delete)

        assert exists == True
        assert exists_before_remove == False

    def tearDown(self):
        arcpy.Delete_management(self.TEST_GDB)
