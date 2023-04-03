import streamlit as st
import os 
import streamlit.components.v1 as components
from streamlit import components
_RELEASE = False

if not _RELEASE:  # during development
    _component_func = components.declare_component("streamlit_info_copyable", url="http://localhost:3001")
else:  # when hosted
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    _component_func = components.declare_component("streamlit_info_copyable", path=parent_dir)

def st_info_copyable(text: str):
    _component_func(text=text)
