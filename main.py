from osm_etl_library import Pipeline

if __name__ == "__main__":

    # specifiy the areas to be processed. These can be changed depending on the OSM CSV files you have exported from FME.

    areas = ["buckinghamshire", "hertfordshire"]

    # specify the folder path - make sure its the same folder as the OSM CSV files exported from FME 

    folder_path = fr"C:\Users\Oreayo.bolarinwa\OneDrive - Envitia Ltd\Documents\osm_workflow"

    # run ETL 

    Pipeline(folder_path, areas).run()

