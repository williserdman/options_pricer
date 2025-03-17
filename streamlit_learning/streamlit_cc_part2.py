import streamlit as st

st.set_page_config(page_title="super 2 duper title")

st.button("ok")
# st.button("ok") # auto generated ID on these two overlap (same type and same parameters)
st.button("ok", key="btn2")

if "slider" not in st.session_state:
    st.session_state.slider = 25

min_value = st.slider("set min value", 0, 50, 25)

# value gets reset every time because the params change, hence, the id of the slider also changes
# slider_value = st.slider("slider", min_value, 100, min_value)
st.session_state.slider = st.slider("slider", min_value, 100, st.session_state.slider)

# if a widget no longer rendered its state is destroyed
if "checkbox" not in st.session_state:
    st.session_state.checkbox = False


def toggle_input():
    st.session_state.checkbox = not st.session_state.checkbox


st.checkbox("show input field", value=st.session_state.checkbox, on_change=toggle_input)

if st.session_state.checkbox:
    user_input = st.text_input("enter something:")
    st.session_state.user_input = user_input
    # doesn't hold this value unless we put it into session state variable
else:
    user_input = st.session_state.get("user_input", "")

st.write(f"user input: {user_input}")

st.title("caching")
# a ton of different reruns of our python script, really bad if we have to reach out to api or somehting else
# THESE ARE CACHED FOR EVERY USER (on server)
# cache global for every user on every session
import time


# decorator built into streamlit ()
@st.cache_data(ttl=60)  # 60 second cache w/o ttL set lasts forever
def fetch_data():
    # unique cache for unique arguments
    time.sleep(5)
    return {"data": "this is cached data!"}


# this cached value is immutable


st.write("fetching data")
data = fetch_data()
st.write(data)

# something about cache resources, not really sure
# allows to pass mutable things out of the cache
# example was adding lines to a file in python

# manual rerun:
# st.rerun()

st.title("fragments")
# rerun only parts of the application


@st.fragment()
def toggle_and_text():
    cols = st.columns(2)
    cols[0].toggle("toggle")
    cols[1].text_area("enter text")


@st.fragment()
def filter_and_file():
    new_cols = st.columns(5)
    new_cols[0].checkbox("filter")
    new_cols[1].file_uploader("upload image")
    new_cols[2].selectbox("choose", ["option 1", "2", "3"])
    new_cols[3].slider("select value", 0, 100, 50)
    new_cols[4].text_input("enter text")


# fragment
toggle_and_text()

# global
cols = st.columns(2)
cols[0].selectbox("select", [1, 2, 3], None)
cols[1].button("update")

# fragment
filter_and_file()

# multipage apps is names of files
# see folder structure and file names

# or do page names in sidebar to functions to render (all in one page but it looks like many pages)
# look in the docs if you want to use multiple pages
