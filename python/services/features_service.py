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
    def add_computed_field(city, state, table, table_geodocde, workspace):
        arcpy.conversion.TableToTable(table, workspace, "table_geocode")
        arcpy.management.CalculateField(table_geodocde, "endereco_completo",
                                        f"concatenarEndereco(!Endereco!, \"{city}\",\"{state}\")",
                                        "PYTHON3", codeblockaddress, "TEXT")

    @staticmethod
    def remove_feature(feature_class):
        if arcpy.Exists(feature_class):
            arcpy.Delete_management(feature_class)
