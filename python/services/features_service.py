from typing import List
import pandas as pd
import arcpy  # type: ignore


class FeaturesService:

    def excel_to_table(self, excel_path: str, workspace: str, table_name: str, excel_sheet_name: str) -> str:
        out_src: str = workspace + "/" + table_name
        self.remove_feature(out_src)

        arcpy.conversion.ExcelToTable(excel_path, out_src, excel_sheet_name, 1, '')

        return out_src

    def find_all(self, table: str, fields: List[str]) -> pd.DataFrame:

        results: List[dict] = []

        with arcpy.da.SearchCursor(table, fields) as cursor:
            for row in cursor:
                results.append(self.read_row(row, fields))

        return pd.DataFrame(results)

    @staticmethod
    def update_values(table: str, fields: List[str]) -> arcpy.da.UpdateCursor:
        return arcpy.da.UpdateCursor(table, fields)

    @staticmethod
    def read_row(row: dict, fields: List[str]) -> dict:

        result: dict = {}

        for index, field in enumerate(fields):
            result[field] = row[index]

        return result

    @staticmethod
    def add_field_in_table(table_name: str, field_name: str, field_type: str) -> None:
        arcpy.management.AddField(table_name, field_name, field_type)

    @staticmethod
    def add_computed_field(table: str, field_name: str, expression: str) -> None:
        arcpy.management.CalculateField(table, field_name, expression)

    @staticmethod
    def remove_feature(feature_class: str):
        if arcpy.Exists(feature_class):
            arcpy.Delete_management(feature_class)