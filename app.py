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
        tiles="https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}",
        attr='Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, ...',  # shortened for brevity
    )
    Draw(
        export=False,
        position="topleft",
        draw_options={
            "polyline": False,
            "poly": False,
            "circle": False,
            "polygon": False,
            "marker": False,
            "circlemarker": False,
            "rectangle": True,
        },
    ).add_to(m)
    return m

def download_geojson(folium_output: dict) -> None:
    geojson_data = folium_output.get("last_draw") if folium_output else None
    if geojson_data:
        st.sidebar.download_button(
            label="Download GeoJSON",
            data=json.dumps(geojson_data),
            file_name=f'{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}_map.geojson',
        )
    else:
        st.sidebar.write("Please draw a rectangle on the map to enable GeoJSON download.")

if __name__ == "__main__":
    st.set_page_config(
        page_title="mapa",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.markdown(
        """
        # Map to GeoJSON Converter
        Follow the instructions in the sidebar on the left to draw a rectangle and download the resulting GeoJSON.
        """
    )
    m = _show_map(center=[0, 0], zoom=2)  # changed to general world view
    output = st_folium(m, key="init", width=1000, height=600)

    # Instructions
    st.sidebar.markdown(
        """
        ## Instructions:
        1. Use the rectangle tool to draw an area on the map.
        2. Click the download button to get the GeoJSON.
        """,
    )
    download_geojson(output)
