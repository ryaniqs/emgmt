# app.py
import streamlit as st
import folium
from streamlit_folium import folium_static
import geopandas as gpd
from shapely.geometry import shape
import os
import shutil
import zipfile

def create_shapefile(geo_json_data, output_folder="output"):
    """Generate shapefile from GeoJSON data."""
    
    # Convert GeoJSON to Geopandas DataFrame
    gdf = gpd.GeoDataFrame({'geometry': [shape(geo_json_data['features'][0]['geometry'])]})
    
    # Export to Shapefile
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    gdf.to_file(os.path.join(output_folder, "shapefile"))

    # Zip the shapefile components for easy download
    zipf = zipfile.ZipFile('shapefile.zip', 'w', zipfile.ZIP_DEFLATED)
    zipdir(output_folder, zipf)
    zipf.close()
    shutil.rmtree(output_folder)  # Clean up the directory after zipping

def zipdir(path, ziph):
    """Zip contents of the directory."""
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), os.path.join(path, '..')))

def main():
    st.title("Draw a Square on the Map")
    
    m = folium.Map(location=[20, 0], zoom_start=2)
    draw = folium.plugins.Draw(draw_options={'polygon': {'allowIntersection': False}})
    draw.add_to(m)

    folium_static(m)

    geo_json_data = st.session_state.get("geo_json", None)

    if geo_json_data:
        create_shapefile(geo_json_data)
        st.markdown("[Download Shapefile](shapefile.zip)")
        st.session_state.geo_json = None  # Reset the session state

    draw_data = st.text_area("GeoJSON Data", value="", key="geo_data")
    if draw_data:
        st.session_state.geo_json = eval(draw_data)

        if st.button("OK"):
            create_shapefile(st.session_state.geo_json)
            st.markdown("[Download Shapefile](shapefile.zip)")
            st.session_state.geo_json = None  # Reset the session state

if __name__ == "__main__":
    main()
