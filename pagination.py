import streamlit as st

import pandas as pd
import numpy as np
import itertools

ss = st.session_state

if "page_number" not in ss:
    ss.page_number = 0


def next_page(n_pages):
    st.session_state["page_number"] = (st.session_state["page_number"] + 1) % n_pages


def previous_page(n_pages):
    st.session_state["page_number"] = (st.session_state["page_number"] - 1) % n_pages


from streamlit_shortcuts import button, add_keyboard_shortcuts


def next_idx(page_indices):
    """activate next item"""
    page_indices
    if len(page_indices) == 0:
        return
    idx = st.session_state.active_idx
    if idx not in page_indices:
        idx = page_indices[0]
    position = page_indices.index(idx)
    position = (position + 1) % len(page_indices)
    st.session_state["active_idx"] = page_indices[position]


def previous_idx(page_indices):
    """activate previous item"""
    if len(page_indices) == 0:
        return
    idx = st.session_state.active_idx
    if idx not in page_indices:
        idx = page_indices[0]
    position = page_indices.index(idx)
    position = (position - 1) % len(page_indices)
    st.session_state["active_idx"] = page_indices[position]


def paginator(label, items, items_per_page=10, on_sidebar=True):
    """Lets the user paginate a set of items.
    Parameters
    ----------
    label : str
        The label to display over the pagination widget.
    items : Iterator[Any]
        The items to display in the paginator.
    items_per_page: int
        The number of items to display per page.
    on_sidebar: bool
        Whether to display the paginator widget on the sidebar.

    Returns
    -------
    Iterator[Tuple[int, Any]]
        An iterator over *only the items on that page*, including
        the item's index.
    Example
    -------
    This shows how to display a few pages of fruit.
    >>> fruit_list = [
    ...     'Kiwifruit', 'Honeydew', 'Cherry', 'Honeyberry', 'Pear',
    ...     'Apple', 'Nectarine', 'Soursop', 'Pineapple', 'Satsuma',
    ...     'Fig', 'Huckleberry', 'Coconut', 'Plantain', 'Jujube',
    ...     'Guava', 'Clementine', 'Grape', 'Tayberry', 'Salak',
    ...     'Raspberry', 'Loquat', 'Nance', 'Peach', 'Akee'
    ... ]
    ...
    ... for i, fruit in paginator("Select a fruit page", fruit_list):
    ...     st.write('%s. **%s**' % (i, fruit))
    """

    # Figure out where to display the paginator
    if on_sidebar:
        location = st.sidebar  # .empty()
    else:
        location = st  # .empty()

    # Display a pagination selectbox in the specified location.
    items = list(items)
    n_pages = len(items)
    n_pages = (len(items) - 1) // items_per_page + 1
    page_format_func = lambda i: "Page %s" % i

    # if st.button("Next"):
    #     next_page(n_pages)

    # Iterate over the items in the page to let the user display them.
    min_index = st.session_state.page_number * items_per_page
    max_index = min(min_index + items_per_page, len(items))
    page_indices = list(np.arange(min_index, max_index))

    if ss.page_number >= n_pages:
        ss.page_number = 0

    with location:

        ss.page_number = st.selectbox(
            label,
            range(n_pages),
            format_func=page_format_func,
            index=ss.page_number,
        )
        cols = st.columns(2)
        with cols[0]:
            # next/previous item buttons
            button(
                "Prev. Page",
                "p",
                on_click=previous_page,
                args=(n_pages,),
                hint=True,
            )

        with cols[1]:
            button("Next Page", "n", on_click=next_page, args=(n_pages,), hint=True)
        # with cols[2]:
        #     button(
        #         "\<",
        #         "j",
        #         on_click=previous_idx,
        #         args=(page_indices,),
        #         hint=True,
        #     )

        # with cols[3]:
        #     button(">", "k", on_click=next_idx, args=(page_indices,), hint=False)

        #     previous_page(n_pages)

    return page_indices
    # itertools.islice(enumerate(items), min_index, max_index)
