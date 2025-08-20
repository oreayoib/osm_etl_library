from .FolderCreator import AttributionFolderCreator, ChartFolderCreator, FolderCreatorPipeline
from .DataTransformer import TransformPipelineReport, TransformPipelineCharts
from .ChartCreator import ChartBuilderPipeline
from .ExcelWriter import ExcelWriter
from .ExcelFormatter import ExcelFormatterPipeline

class Pipeline:
    def __init__(self, folder_path: str, areas: list):
        self.folder_path = folder_path
        self.areas = areas
        # self.folders = folders

    def run(self):

        # Create folders for reports and charts

        try:

            try:

                print("Creating folders for reports and charts...")

                folder_creators = [AttributionFolderCreator(self.folder_path), ChartFolderCreator(self.folder_path, self.areas)]

                FolderCreatorPipeline(folder_creators).create_folders()

                print("✅ Folders created successfully.")
            
            except Exception as e:

                print(f"❌ Error creating folders: {e}")

            # Generate reports and charts

            try:

                print("Generating dataframes for reports and charts...")

                excel_dict = TransformPipelineReport(self.folder_path, self.areas).run_transforms()

                excel_dict_charts = TransformPipelineCharts(self.folder_path, self.areas).run_transforms()

                print("✅ Dataframes generated successfully.")

            except Exception as e:

                print(f"❌ Error generating dataframes: {e}")

            try:

                print("Writing dataframes to Excel files...")
        
                ExcelWriter(excel_dict, fr"{self.folder_path}\reports\osm_data_report.xlsx").write_dataframes()

                ExcelWriter(excel_dict_charts, fr"{self.folder_path}\reports\osm_category_charts.xlsx").write_dataframes()

                print("✅ Excel files created successfully.")
            
            except Exception as e:

                print(f"❌ Error writing dataframes to Excel files: {e}")
            
            try:
                print("Formatting Excel files...")

                ChartBuilderPipeline(self.folder_path, self.areas).run_transforms()

                ExcelFormatterPipeline(fr"{self.folder_path}\reports\osm_data_report.xlsx").format_excel()

                print("✅ Excel files formatted successfully.")
   
            except Exception as e:

                print(f"❌ Error formatting Excel files: {e}")
        
            return "Pipeline completed without errors" 
    
        except Exception as e:
            print(f"❌ An error occurred in the pipeline: {e}")
            return f"❌ Pipeline failed with error: {e}"

        # Formatting the Excel files
        