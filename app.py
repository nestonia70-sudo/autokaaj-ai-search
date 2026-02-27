import streamlit as st
import json

# ম্যানিফেস্ট ফাইলের তথ্য
manifest_data = {
    "name": "AutoKaaj AI",
    "short_name": "AutoKaaj",
    "start_url": "https://qljfudv.streamlit.app/",
    "display": "standalone",
    "background_color": "#ffffff",
    "theme_color": "#000000",
    "icons": [
        {
            "src": "https://raw.githubusercontent.com/your-username/your-repo/main/logo.png",
            "sizes": "512x512",
            "type": "image/png"
        }
    ]
}

# ম্যানিফেস্ট ফাইল তৈরি করার ছোট একটি ট্রিক
if st.query_params.get("manifest") == "true":
    st.write(json.dumps(manifest_data))
    st.stop()
