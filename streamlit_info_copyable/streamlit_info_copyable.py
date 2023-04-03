import os
import streamlit.components.v1 as components

_RELEASE = True
print (_RELEASE)

if not _RELEASE:  # during development
    _component_func = components.declare_component("streamlit_info_copyable", url="http://localhost:3001")
    print ("Dev")
else:  # when hosted
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    _component_func = components.declare_component("streamlit_info_copyable", path=parent_dir)
    print ("PROD")

def st_info_copyable(text: str):
    _component_func(text=text)