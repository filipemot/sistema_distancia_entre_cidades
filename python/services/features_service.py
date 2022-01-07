import arcpy


class FeaturesService:

    def excel_to_table(self, excel_path, workspace, table_name, excel_sheet_name):
        out_src = workspace + "/" + table_name
        self.remove_feature(out_src)

        arcpy.conversion.ExcelToTable(excel_path, out_src, excel_sheet_name, 1, '')

        return out_src

    @staticmethod
    def add_field_in_table(table_name, field_name, field_type):
        arcpy.management.AddField(table_name, field_name, field_type)

    @staticmethod
    def add_computed_field(table, field_name, expression):
        arcpy.management.CalculateField(table, field_name, expression)

    @staticmethod
    def remove_feature(feature_class):
        if arcpy.Exists(feature_class):
            arcpy.Delete_management(feature_class)

    def find_all(self, table, fields):

        results = []

        with arcpy.da.SearchCursor(table, fields) as cursor:
            for row in cursor:
                results.append(self.read_row(row, fields))

        return results

    @staticmethod
    def read_row(row, fields):

        result = {}

        for index, field in enumerate(fields):
            result[field] = row[index]

        return result
