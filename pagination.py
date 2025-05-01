import streamlit as st

import pandas as pd
import numpy as np
import itertools

ss = st.session_state

if "page_number" not in ss:
    ss.page_number = 0

if "page_indices" not in ss:
    ss.page_indices = []


def next_page(n_pages):
    st.session_state["page_number"] = (st.session_state["page_number"] + 1) % n_pages


def previous_page(n_pages):
    st.session_state["page_number"] = (st.session_state["page_number"] - 1) % n_pages


from streamlit_shortcuts import button, add_keyboard_shortcuts


def next_idx():
    """activate next item

    sets ss.active_idx to the index (not numeric position) of the newly active item
    """

    if len(ss.page_indices) == 0:
        return
    idx = st.session_state.active_idx
    if idx not in ss.page_indices:
        idx = ss.page_indices[0]
    position = ss.page_indices.index(idx)
    position = (position + 1) % len(ss.page_indices)
    st.session_state["active_idx"] = ss.page_indices[position]


def previous_idx():
    """activate previous item

    sets ss.active_idx to the index (not numeric position) of the newly active item
    """
    if len(ss.page_indices) == 0:
        return
    idx = st.session_state.active_idx
    if idx not in ss.page_indices:
        idx = ss.page_indices[0]
    position = ss.page_indices.index(idx)
    position = (position - 1) % len(ss.page_indices)
    st.session_state["active_idx"] = ss.page_indices[position]


def paginator(items, items_per_page=10):
    """Selects a subset of items to display based on the current page number."""
    # cycle back to first page if beyond last
    n_pages = (len(items) - 1) // items_per_page + 1
    if ss.page_number >= n_pages:
        ss.page_number = 0
    min_index = ss.page_number * items_per_page
    max_index = min(min_index + items_per_page, len(items))
    ss.page_indices = list(items[min_index:max_index])
    return ss.page_indices, n_pages
