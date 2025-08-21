import pandas as pd
from abc import ABC, abstractmethod
from .DataLoader import CSVLoader

# Classes for Data Transformation

class OverviewDataTransformer(ABC):
    @abstractmethod
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        pass

class OSMCompletenessTransformer(OverviewDataTransformer):

    def __init__(self, folder_path, areas: list):
        self.folder_path = folder_path
        self.areas = areas

    def transform(self) -> pd.DataFrame:

        # Example transformation logic

        gen_report = pd.DataFrame({
        'Area of Interest':pd.Series(dtype='str'),
        'Row Count': pd.Series(dtype='int'),
        'Name Value Count': pd.Series(dtype='int'),
        'Name Completeness': pd.Series(dtype='float'),
        'Name Value Count (eng)': pd.Series(dtype='int'),
        'Name Completeness (eng)': pd.Series(dtype='float'),
        'Address Value Count (Street)': pd.Series(dtype='int'),
        'Address Completeness (Street)': pd.Series(dtype='float'),
        })

        for area in self.areas:

            df = CSVLoader(self.folder_path, area).load_dataframes()

            row_count = len(df)
            name_count = len(df[df['name'].isnull() == False])
            name_count_eng = len(df[df['name:en'].isnull() == False])
            street_count = len(df[df['addr:street'].isnull() == False])

            data = pd.DataFrame({
            'Area of Interest': [area],
            'Row Count': [row_count],
            'Name Value Count': [name_count],
            'Name Completeness': [(name_count/row_count)],
            'Name Value Count (eng)': [name_count_eng],
            'Name Completeness (eng)': [(name_count_eng/row_count)],
            'Address Value Count (Street)': [street_count],
            'Address Completeness (Street)': [(street_count/row_count)]
            })

            if not gen_report.empty:
                gen_report = pd.concat([gen_report, data], ignore_index=True)
            elif gen_report.empty:
                gen_report = data

        return gen_report
        
class AttributeReportTransformer(OverviewDataTransformer):

    def __init__(self, folder_path: str, area: str):
        self.folder_path = folder_path
        self.area = area

    def transform(self) -> pd.DataFrame:
        
        attr_report = pd.DataFrame({
        'Attribute': pd.Series(dtype='str'),
        'Count': pd.Series(dtype='int'),
        'Name Count': pd.Series(dtype='int'),
        'Name Completeness': pd.Series(dtype='str'),
        'Name Count (eng)': pd.Series(dtype='int'),
        'Name Completeness (eng)': pd.Series(dtype='str'),
        'Address Count (Street)': pd.Series(dtype='int'),
        'Address Completeness (Street)': pd.Series(dtype='str'), 
        'Unique Values': pd.Series(dtype='int'),
        'Mode': pd.Series(dtype='int'),
        'Freq. of Mode': pd.Series(dtype='int')
        })    

        df = CSVLoader(self.folder_path, self.area).load_dataframes()  

        features = list(df['feature_type'].unique())

        for feature in features:

            if feature in list(df.columns):

                attribute = feature
                attr = df[df[attribute].isnull() == False]
                count = len(attr)
                name_count = len(attr[attr['name'].isnull() == False])
                name_count_eng = len(attr[attr['name:en'].isnull() == False])
                address_count = len(attr[attr['addr:street'].isnull() == False])
                mode_value = attr[attribute].mode()[0] if not attr[attribute].mode().empty else None
                mode_count = int((attr[attribute] == mode_value).sum())
                unique_values = len(attr[attribute].unique())       

                data = pd.DataFrame({
                    'Attribute': [attribute],
                    'Count': [count],
                    'Name Count': [name_count],
                    'Name Completeness': [(name_count/count) if count > 0 else 0],
                    'Name Count (eng)': name_count_eng,
                    'Name Completeness (eng)': [name_count_eng/count if count > 0 else 0],
                    'Address Count (Street)': [address_count],
                    'Address Completeness (Street)': [address_count/count if count > 0 else 0], 
                    'Unique Values': [unique_values],
                    'Mode': [mode_value],
                    'Freq. of Mode': [mode_count]
                })                         

                if not attr_report.empty:
                    attr_report = pd.concat([attr_report, data], ignore_index=True)
                elif attr_report.empty:
                    attr_report = data

        return attr_report


class ValuesReportTransformer(OverviewDataTransformer):

    def __init__(self, folder_path: str, area: str):
        self.folder_path = folder_path
        self.area = area

    def transform(self) -> pd.DataFrame:

        attr_value_report = pd.DataFrame({
        'attr_name': pd.Series(dtype='str'),
        'attr_values':pd.Series(dtype='str'),
        'counts':pd.Series(dtype='int'),
        'freq (excl NaN)':pd.Series(dtype='float')
        })
               
        df = CSVLoader(self.folder_path, self.area).load_dataframes()  

        features = list(df['feature_type'].unique())

        for feature in features:
            
            attribute = feature
            attr = df[df[attribute].isnull() == False]
            attr_value = attr[attribute].value_counts().rename_axis('attr_values').reset_index(name='counts')
            attr_value['attr_name'] = attribute
            attr_value = attr_value[['attr_name', 'attr_values', 'counts']]
            attr_value['freq (excl NaN)'] = attr_value['counts']/len(attr)
            attr_value_report = pd.concat([attr_value_report, attr_value], ignore_index=True)
            
        return attr_value_report 


class ChartsReportSheetTransformer(OverviewDataTransformer):

    def __init__(self, folder_path: str, area: str):
        self.folder_path = folder_path
        self.area = area

    def transform(self) -> pd.DataFrame:

        df = CSVLoader(self.folder_path, self.area).load_dataframes()

        features = list(df['feature_type'].unique())

        graph_df = pd.DataFrame({'Category': features})

        graph_df['Graph'] = 'placeholder'

        return graph_df
    
class TransformPipeline(ABC):
    @abstractmethod
    def run_transforms(self) -> dict:
        pass

class TransformPipelineReport(TransformPipeline):

    def __init__(self, folder_path: str, areas: list):
        self.folder_path = folder_path
        self.areas = areas
        
    def run_transforms(self) -> dict:

        excel_dict = {}

        gen_report = OSMCompletenessTransformer(self.folder_path, self.areas).transform()

        excel_dict['completeness_overview'] = gen_report

        for area in self.areas:
            attr_report = AttributeReportTransformer(self.folder_path, area).transform()
            values_report = ValuesReportTransformer(self.folder_path, area).transform()
            excel_dict[f'{area}_attr_report'] = attr_report
            excel_dict[f'{area}_values_report'] = values_report
            
        return excel_dict
    
class TransformPipelineCharts(TransformPipeline):

    def __init__(self, folder_path: str, areas: list):
        self.folder_path = folder_path
        self.areas = areas
        
    def run_transforms(self) -> dict:

        excel_dict = {}

        for area in self.areas:
            chart_report = ChartsReportSheetTransformer(self.folder_path, area).transform()
            excel_dict[f'{area}_charts'] = chart_report
            
        return excel_dict

