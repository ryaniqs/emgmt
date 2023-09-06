# app.py
import streamlit as st

def main():
    st.title("Streamlit app with geojson.io")

    # Create an iframe that embeds geojson.io
    iframe_code = '<iframe src="http://geojson.io" width="100%" height="600px"></iframe>'
    st.markdown(iframe_code, unsafe_allow_html=True)

    st.write("""
    Above is an embedded version of geojson.io. You can draw, edit, and export GeoJSON directly from this interface.
    """)

if __name__ == "__main__":
    main()
