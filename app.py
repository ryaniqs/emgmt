# app.py
import streamlit as st
import folium
from streamlit_folium import folium_static
import json

def main():
    st.title("Draw a Square on the Map")
    
    m = folium.Map(location=[20, 0], zoom_start=2)
    draw = folium.plugins.Draw(draw_options={
        'polygon': {'allowIntersection': False},
        'circle': False, 
        'polyline': False, 
        'circleMarker': False,
        'marker': False
    })
    draw.add_to(m)
    
    folium_static(m)
    
    geo_json_data = st.session_state.get("geo_json", None)

    if st.button("Confirm Square"):
        textarea_val = st.text_area("GeoJSON Data", value="", key="geo_data")
        if textarea_val:
            geo_json_data = json.loads(textarea_val)
            st.session_state.geo_json = geo_json_data
            
            if st.button("Is this your area of interest?"):
                st.download_button("Download GeoJSON", data=json.dumps(geo_json_data), file_name="geojson_data.geojson", mime="application/geo+json")

    if st.button("Erase and Start Again"):
        st.experimental_rerun()  # This will rerun the streamlit app

if __name__ == "__main__":
    main()
