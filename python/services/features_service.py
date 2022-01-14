from typing import List
import pandas as pd  # type: ignore
import arcpy  # type: ignore

from utils.timer_decorator import timer_decorator


class FeaturesService:
    __SR = arcpy.SpatialReference(4326)

    @timer_decorator('FeaturesService.excel_to_table')
    def excel_to_table(self, excel_path: str, workspace: str, table_name: str, excel_sheet_name: str) -> str:
        out_src: str = workspace + "/" + table_name
        self.remove_feature(out_src)

        arcpy.conversion.ExcelToTable(excel_path, out_src, excel_sheet_name, 1, '')

        return out_src

    @timer_decorator('FeaturesService.find_all')
    def find_all(self, table: str, fields: List[str]) -> pd.DataFrame:

        results: List[dict] = []
        with arcpy.da.SearchCursor(table, fields) as cursor:
            for row in cursor:
                results.append(self.read_row(row, fields))
        return pd.DataFrame(results)

    @timer_decorator('FeaturesService.convert_table_to_point')
    def convert_table_to_point(self, table, output_feature_class, x_field, y_field):

        self.remove_feature(output_feature_class)

        arcpy.management.XYTableToPoint(table, output_feature_class, x_field=x_field, y_field=y_field,
                                        coordinate_system=self.__SR)

    @timer_decorator('FeaturesService.copy_features')
    def copy_features(self, in_feature: str, out_feature: str) -> None:
        self.remove_feature(out_feature)
        arcpy.management.CopyFeatures(in_feature, out_feature, '', None, None, None)

    @staticmethod
    def get_search_cursor(table: str, fields: List[str]) -> arcpy.da.SearchCursor:
        return arcpy.da.SearchCursor(table, fields)

    @staticmethod
    @timer_decorator('FeaturesService.update_values')
    def update_values(table: str, fields: List[str]) -> arcpy.da.UpdateCursor:
        return arcpy.da.UpdateCursor(table, fields)

    @staticmethod
    @timer_decorator('FeaturesService.add_field_in_table')
    def add_field_in_table(table_name: str, field_name: str, field_type: str) -> None:
        arcpy.management.AddField(table_name, field_name, field_type)

    @staticmethod
    @timer_decorator('FeaturesService.add_computed_field')
    def add_computed_field(table: str, field_name: str, expression: str, field_type: str) -> None:
        arcpy.management.CalculateField(table, field_name, expression, field_type=field_type)

    @staticmethod
    @timer_decorator('FeaturesService.remove_feature')
    def remove_feature(feature_class: str) -> None:
        if arcpy.Exists(feature_class):
            arcpy.Delete_management(feature_class)

    @staticmethod
    def read_row(row: dict, fields: List[str]) -> dict:

        result: dict = {}

        for index, field in enumerate(fields):
            result[field] = row[index]

        return result
