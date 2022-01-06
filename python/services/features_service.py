import arcpy


class FeaturesService:

    def excel_to_table(self, excel_path, workspace, table_name, excel_sheet_name):
        out_src = workspace + "/" + table_name
        self.remove_feature(out_src)

        arcpy.conversion.ExcelToTable(excel_path, out_src, excel_sheet_name, 1, '')

        return out_src

    @staticmethod
    def remove_feature(feature_class):
        if arcpy.Exists(feature_class):
            arcpy.Delete_management(feature_class)
