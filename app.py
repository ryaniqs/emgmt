import datetime
import os
import json
import logging
import folium
import streamlit as st
from folium.plugins import Draw
from streamlit_folium import st_folium
from typing import List

log = logging.getLogger(__name__)
log.setLevel(os.getenv("LOG_LEVEL", "DEBUG"))

def _show_map(center: List[float], zoom: int) -> folium.Map:
    m = folium.Map(
        location=center,
        zoom_start=zoom,
        control_scale=True,
        tiles="https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}",  # Use Google Maps hybrid imagery
        attr='Map data: &copy; <a href="https://www.google.com">Google</a>',
    )
    Draw(
        export=True,
        position="topleft",
        draw_options={
            "polyline": False,
            "poly": False,
            "circle": False,
            "polygon": False,
            "marker": False,
            "circlemarker": False,
            "rectangle": True,
            "max_width": 20000,
            "max_height": 20000,
        },
    ).add_to(m)
    return m

def download_geojson(folium_output: dict) -> None:
    geojson_data = folium_output.get("last_draw") if folium_output else None
    if geojson_data:
        crs_options = [
            {"name": "WGS84", "code": "EPSG:4326"},
            {"name": "Web Mercator", "code": "EPSG:3857"},
            {"name": "UTM Zone 38N", "code": "EPSG:32638"},
        ]
        crs = st.selectbox(
            "Select the CRS of the GeoJSON:",
            crs_options,
            index=0,
        )
        st.write(f"The selected CRS is: {crs}")
        st.sidebar.download_button(
            label="Download GeoJSON",
            data=json.dumps(geojson_data),
            file_name=f'{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}_map.geojson',
            key="download_geojson",
            help="Download GeoJSON data",
            on_click=None,
            args=(),
            kwargs={"crs": crs},
            disabled=False,
        )
    else:
        st.sidebar.write("Please zoom to your AOI and draw a rectangle on the map to enable GeoJSON download.")

if __name__ == "__main__":
    st.set_page_config(
        page_title="mapa",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.markdown(
        """
        # Area of Interest  Selection
        Follow the instructions in the sidebar on the left to draw a rectangle of your area of interest and download the resulting area as a GeoJSON. The maximum area of the rectangle is 20 km2/ 7.7 mi2.
        """
    )
    m = _show_map(center=[0, 0], zoom=2)
    output = st_folium(m, key="init", width=1000, height=600)

    # Instructions
    st.sidebar.markdown(
        """
        ## Instructions:
        1. Use the rectangle tool to draw an area on the map.
        2. Click the blue "Export" link below the map to download the GeoJSON File.
        3. Rename the file as needed and email it to IQSpatial for feature extraction. 
        """,
    )
    download_geojson(output)

# Load a smaller image (25 pixels) with a clickable link
st.sidebar.markdown("[![IQSpatial Logo](https://images.squarespace-cdn.com/content/v1/5e8cc689c426331984ffa7f1/1586545924842-ZUPOCD4I7SX1OGIBHDS3/Logo_IQSpatialLogo.png?format=25x25)](https://iqspatial.com/)")
