import streamlit as st

st.write("hello world 12356")  # magic command in streamlit
st.write(
    {"key": "value"}
)  # streamlit will automatically figure out how to write this based on its type
st.write(123)
st.write(True)

3 + 4  # thi is auto written to the screen,, kind of like jupyter

"hello world" if False else "bye bye"

# every time something changes streamlit reruns the entire python file

pressed = st.button("press me")
print(pressed)  # when something changes state we rerun the ENTIRE python file

btn2 = st.button("2nd button")
print("second", btn2)  # every interaction reruns the entire script
# so cannot get these two buttons true in the same run

# sometimes you might have to rerun the terminal command

st.title("this is a title")
st.header("this is a header")  # no h1 h2 though
st.subheader("this is a subheader")
st.markdown(" this is **markdown**!")
st.caption("small text")
code_example = """
def greet(name):
    print("hello", name)
"""

st.code(code_example, language="python")

st.divider()  # creates a grey line

# to add images create a folder in the directory called "static"

import os  # to define path to image

st.image(os.path.join(os.getcwd(), "static", "headshot.png"))

import pandas as pd

st.title("streamlit elements demo")

st.subheader("dataframe")
df = pd.DataFrame(
    {
        "Name": ["Alice", "Bob", "Charlie", "David"],
        "Age": [20, 32, 33, 45],
        "Occupation": ["Engineer", "Doctor", "Student", "Unemployed"],
    }
)
st.dataframe(df)  # specific for pandas dataframe gives a lot of cool features

st.subheader("data editor")
edit_tabledf = st.data_editor(df)  # same as before but we can edit it in the frontend
print(edit_tabledf)

st.subheader("static table")  # simple table
st.table(df)

st.subheader("metrics")
st.metric(label="total rows", value=len(df))
st.metric(label="average age", value=round(df["Age"].mean(), 1))

st.subheader("JSON and dictionary")
sample_dict = {
    "name": "Alice",
    "age": 25,
    "skills": ["python", "data science", "machine learning"],
}
st.json(sample_dict)
st.write(sample_dict)

st.title("streamlit charts")

import numpy as np

chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["A", "B", "C"])

st.subheader("area chart")
st.area_chart(chart_data)

st.subheader("bar chart")
st.bar_chart(chart_data)

st.subheader("line chart")
st.line_chart(chart_data)

st.subheader("scatter plot")
scatter_data = pd.DataFrame({"x": np.random.randn(100), "y": np.random.randn(100)})
st.scatter_chart(scatter_data)

st.subheader("map")
map_data = pd.DataFrame(
    np.random.randn(100, 2) / [50, 50] + [37.76, -122.4],  # coords around sf i guess
    columns=["lat", "lon"],  # must be these names
)
st.map(map_data)

import matplotlib.pyplot as plt

st.subheader("pyplot chart")
fig, ax = plt.subplots()
ax.plot(chart_data["A"], label="A")
ax.plot(chart_data["B"], label="B")
ax.plot(chart_data["C"], label="C")
ax.set_title("pyplot line chart")
ax.legend()
st.pyplot(fig)


st.title("trying out making some forms")
st.header("these prevent the entire app from rerunning when we change one thing")

bname = st.text_input("Enter your name:")  # will update immediately every letter typed
print(bname)

from datetime import datetime

min_date = datetime(1990, 1, 1)
max_date = datetime.now()

form_values = {
    "name": None,
    "height": None,
    "gender": None,
    "dob": None,
}
with st.form(key="user_info_form", clear_on_submit=False):
    form_values["name"] = st.text_input("Enter your name:")
    form_values["height"] = st.number_input("enter height (cm)")
    form_values["gender"] = st.selectbox("gender", ["male", "female"])
    form_values["dob"] = st.date_input(
        "date of birth", max_value=max_date, min_value=min_date
    )

    bday = form_values["dob"]
    if bday:
        age = max_date.year - bday.year
        if bday.month > max_date.month or (
            bday.month == max_date.month and bday.day > max_date.day
        ):
            age -= 1

    st.write(f"your calculated age is {age} years")

    # when we run the form the rerun is deffered until later
    print(form_values)

    submit_button = st.form_submit_button(label="submit")

    if submit_button:  # True when submit button is pressed
        if not all(form_values.values()):
            print(1)
            st.warning("Please fill in all the fields")
        else:
            print(2)
            st.balloons()
            st.write("### Info")
            for key, value in form_values.items():
                st.write(f"{key}: {value}")


st.title("session state")
st.write(
    "something that we can use to store values in one user session (one tab they have open)"
)

if "count" not in st.session_state:
    st.session_state.count = 0

st.write(
    f"counter value: {st.session_state.count}"
)  # run top to bottom, this happens before rewrite

if st.button("increment counter"):
    st.session_state.count += 1
    st.write(f"counter incremented to {st.session_state.count}")

if st.button("reset"):
    st.session_state.count = 0

st.write("callbacks")

if "step" not in st.session_state:
    st.session_state.step = 1
if "info" not in st.session_state:
    st.session_state.info = {}


def goto_step2(name):
    print("callback, value:", name)
    st.session_state.info["name"] = (
        name  # info is a dict that stores user information in session_state
    )
    st.session_state.step = 2

    print(st.session_state.info, st.session_state.step)


if st.session_state.step == 1:
    st.header("part 1")

    st.write("making this equal to whatever is in session state")
    name = st.text_input("name", value=st.session_state.info.get("name", ""))
    st.caption("you must hit the enter button to apply this")

    print(name)
    st.button(
        "next", on_click=goto_step2, args=(name,)
    )  # we get into this is on button click one, SEE BELOW

    # callback run before any other code on the next rerun

# SEE ABOVE, we have to click it a second time to rerun the code befor e getting to this if statement
elif st.session_state.step == 2:
    st.header("part 2: review")
    st.subheader("please review this")
    print("name:", st.session_state.info.get("name", ""))
    st.write(f"**Name**: {st.session_state.info.get("name", "")}")

print(st.session_state.info)

st.sidebar.title("this is a title in the sidebar")
st.sidebar.write("this is writing in the sidebar")
sidebar_input = st.sidebar.text_input("enter something in the sidebar")


tabs = st.tabs(["tab 1", "tab2", "tab 3"])

with tabs[0]:
    st.write("you are in tab 1")
with tabs[1]:
    st.write("you are in tab 2")
with tabs[2]:
    st.write("you are in tab 3")

columns = st.columns(2)

with columns[0]:
    st.header("col 1")
with columns[1]:
    st.header("col 2")

with st.container(border=True):
    st.write("in a container")

placeholder = st.empty()
placeholder.write("this is an empty placeholder, useful for dynamic content")

if st.button("update placeholder"):
    placeholder.write("the content of placeholder has been overwritten")

with st.expander("expand for more details"):
    st.write("more details")

st.write("hover over this for a tooltip")

st.button("button w/ tooltip", help="this shows on hover")  # bug in this version

if sidebar_input:
    st.write(f"you entered in the sidebar: {sidebar_input}")
