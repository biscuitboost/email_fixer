import streamlit as st
import os 
from streamlit import file_util
from streamlit import components
_RELEASE = False

if not _RELEASE:  # during development
    _component_func = components.declare_component("streamlit_info_copyable", url="https://email-fixer.streamlit.app")
else:  # when hosted
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    _component_func = components.declare_component("streamlit_info_copyable", path=parent_dir)

def st_info_copyable(text: str):
    _component_func(text=text)
