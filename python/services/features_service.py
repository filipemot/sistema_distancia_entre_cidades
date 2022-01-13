from typing import List
import pandas as pd  # type: ignore
import arcpy  # type: ignore


class FeaturesService:
    __SR = arcpy.SpatialReference(4326)

    def excel_to_table(self, excel_path: str, workspace: str, table_name: str, excel_sheet_name: str) -> str:
        out_src: str = workspace + "/" + table_name
        self.remove_feature(out_src)

        arcpy.conversion.ExcelToTable(excel_path, out_src, excel_sheet_name, 1, '')

        return out_src

    def find_all(self, table: str, fields: List[str]) -> pd.DataFrame:

        results: List[dict] = []

        with arcpy.da.SearchCursor(table, fields) as cursor:
            for row in cursor:
                results.append(self.__read_row(row, fields))

        return pd.DataFrame(results)

    def convert_table_to_point(self, table, output_feature_class, x_field, y_field):

        self.remove_feature(output_feature_class)

        arcpy.management.XYTableToPoint(table, output_feature_class, x_field=x_field, y_field=y_field,
                                        coordinate_system=self.__SR)

    @staticmethod
    def copy_features(in_feature: str, out_feature: str) -> None:
        arcpy.management.CopyFeatures(in_feature, out_feature, '', None, None, None)

    @staticmethod
    def update_values(table: str, fields: List[str]) -> arcpy.da.UpdateCursor:
        return arcpy.da.UpdateCursor(table, fields)

    @staticmethod
    def add_field_in_table(table_name: str, field_name: str, field_type: str) -> None:
        arcpy.management.AddField(table_name, field_name, field_type)

    @staticmethod
    def add_computed_field(table: str, field_name: str, expression: str, field_type: str) -> None:
        arcpy.management.CalculateField(table, field_name, expression, field_type=field_type)

    @staticmethod
    def remove_feature(feature_class: str):
        if arcpy.Exists(feature_class):
            arcpy.Delete_management(feature_class)

    @staticmethod
    def __read_row(row: dict, fields: List[str]) -> dict:

        result: dict = {}

        for index, field in enumerate(fields):
            result[field] = row[index]

        return result
