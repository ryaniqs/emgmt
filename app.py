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
        tiles="https://mts.maps.openstreetmap.org/ortho/{z}/{x}/{y}.png",  # Fixed tile URL format
        attr='Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
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
        st.sidebar.download_button(
            label="Download GeoJSON",
            data=json.dumps(geojson_data),
            file_name=f'{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}_map.geojson',
            key="download_geojson",  # Added key to ensure the button updates
            help="Download GeoJSON data",
            on_click=None,  # Removed on_click, as it's not necessary in this context
            args=(),
            kwargs={},
            disabled=False,
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
        # IQSpatial's Area of Interest Application
        Follow the instructions in the sidebar on the left to draw a rectangle of your area of interest and download the resulting area as a GeoJSON. The maximum area of the rectangle is 20 km squared.
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

# Load a smaller image (25 pixels) with a clickable link
st.sidebar.markdown("[![IQSpatial Logo](https://images.squarespace-cdn.com/content/v1/5e8cc689c426331984ffa7f1/1586545924842-ZUPOCD4I7SX1OGIBHDS3/Logo_IQSpatialLogo.png?format=1500w =25x25)](https://iqspatial.com/)")
