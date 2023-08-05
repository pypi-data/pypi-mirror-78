import streamlit as st
import pandas as pd
from enum import Enum

class Section(Enum):
    INTRO = "Introduction"
    
    BAR_CHART = "Static Embed: Bar Chart"
    PENGUINS =  "Static Embed: Scatterplot Matrix Penguins"
    SPIKE = "Static Embed: Spike Map"
    FORCE_GRAPH = "Static Embed: Force Graph"

    FORM = "Bi-Directional Embed: HTML Form"
    DRAW = "Bi-Directional Embed: Drawing Canvas"
    COUNTIES = "Bi-Directional Embed: Selecting Counties"
    

@st.cache
def get_penguins():
    return pd.read_csv("https://raw.githubusercontent.com/allisonhorst/palmerpenguins/master/inst/extdata/penguins.csv")
        
def showcase(observable):
    sections = list(map(lambda d: d.value, Section))
    section_i = 0
    section_param = st.experimental_get_query_params().get("section")
    if section_param and section_param[0] in sections:
        section_i = sections.index(section_param[0])

    section = st.sidebar.radio(
        "Section",
        sections,
        index=section_i
    )
    if section == Section.INTRO.value:
        st.experimental_set_query_params(section=Section.INTRO.value)
        st.write("""
# Introduction to `streamlit-observable`

👋🏼 Hello! This Streamlit app is an introduction to the `streamlit-observable` 
library - a Streamlit custom component for embeding [Observable notebooks](https://observablehq.com)
into Streamlit apps. You can render, re-use, and recycle any Observable notebook
found on observablehq.com! Which means, you get access to hundreds of data visualizations,
maps, charts, and animations that you can embed into any Streamlit app.

👈🏼Check out the sidebar for a deep-dive into different ways you can use 
`streamlit-observable` in your apps. Or, just scroll down to check out 
quick examples below!
         """)
        with st.echo():
            observable("Intro to Observable", "@observablehq/five-minute-introduction")

        with st.echo():
            observable("The Trusted Line Chart", "@d3/line-chart", ["chart"])

        with st.echo():
            observers = observable("World Tour!", 
                notebook="@d3/world-tour", 
                targets=["canvas"], 
                observe=["name"]
            )
            st.write(observers.get("name"))
        
        with st.echo():
            observable("Eyes", 
                notebook="@mbostock/eyes",
                targets=["canvas", "mouse"], 
                hide=["mouse"]
            )

    if section == Section.SPIKE.value:
        st.experimental_set_query_params(section=Section.SPIKE.value)

        st.write("""
## Static Embed: U.S. Spike Map of Births in 2010

Here, we re-use the [Spike Map](https://observablehq.com/@d3/spike-map) Observable notebook, 
with on own data on births per month in each county. [The dataset](https://github.com/the-pudding/data/tree/master/births) 
was cleaned and offered  by the folks over at [The Pudding](https://pudding.cool/2017/05/births/),
with the original dataset offered by the US National Vital Statistics System.

Just like with penguin scatterplot matrix, we need to [fork the orginal D3 notebook](https://observablehq.com/d/1f434ef3b0569a00), 
for three reasons:

1. We want to choose the color of the spikes based off of `st.color_picker`, but the color of the spikes
weren't exposed in a separate cell in the original notebook. 
2. We want to pass in a JSON serializable list into the notebook, and re-use the data processing 
logic found in the original `"data"` cell.

Let's take a look at what the data looks like, and make a `st.slider` widget to select a specific 
month in 2010 to look at:
""")
        with st.echo():
            @st.cache
            def get_birth_csv():
                df = pd.read_csv("https://raw.githubusercontent.com/the-pudding/data/master/births/allBirthData.csv",
                                    dtype={"State": str, "County": str})
                df["State"] = df["State"].str.zfill(2)
                df["County"] = df["County"].str[-3:]
                return df
            
            df = get_birth_csv()

            year = 2010
            month = st.slider("Month", min(df["Month"]), max(df["Month"]))
            
            df_map = df[(df["Year"] == year) & (df["Month"] == month)]

            st.dataframe(df_map)
        
        st.write("""
Now, let's make a color_picker widget, to choose what color the spikes should be.
We will pass that into the `redefine` param of `observable()`, as well as the value 
of `df_map` (which we will filter + tranform before passing it in, to match the schema
the underlying notebook is expecting).
""")

        with st.echo():
            color = st.beta_color_picker("Spike Color", "#ff0000")
        
            observable("Spike Chart of Births by County", 
                notebook="d/1f434ef3b0569a00", 
                targets=["chart"], 
                redefine={
                    "rawData": df_map[["countyBirths", "State", "County"]].to_numpy().tolist(),
                    "color": color
                }
            )
        
        st.write('Now try changing the "Month" slider and the "Spike Color" color picker, and see how the map responds!')

    elif section == Section.BAR_CHART.value:
        st.experimental_set_query_params(section=Section.BAR_CHART.value)
        st.write("""## Static Embed: Bar Chart
Let's start with a humble bar chart!

Let's define 3 different sliders, one for each person: Alex, Brian, and Craig. 
These sliders are normal Streamlit [`st.slider`](https://docs.streamlit.io/en/stable/api.html#streamlit.slider) 
widgets, defined in Python. With these 3 values, let's make a bar chart, with 1 bar per person. We could use the 
standard [D3 Bar Chart](https://observablehq.com/@d3/bar-chart) Observable notebook, 
but let's instead use Julien Barnier's [Updatable Bar Chart](https://observablehq.com/@juba/updatable-bar-chart) 
notebook, which gives nice transitions when the bar values change.

So we have our 3 Streamlit sliders, and we know what Observable notebook we want to use. How do we embed it?

        """)
        with st.echo():
            a = st.slider("Alex", value=30)
            b = st.slider("Brian", value=20)
            c = st.slider("Craig", value=50)

            observable("Example Updatable Bar Chart", 
                notebook="@juba/updatable-bar-chart", 
                targets=["chart", "draw"], 
                redefine={
                    "data": [
                        {"name": "Alex", "value": a},
                        {"name": "Brian", "value": b},
                        {"name": "Craig", "value": c}
                    ],
                },
                hide=["draw"]
            )
        st.write(""" 
And that's it! Try changing the `a`, `b`, or `c` sliders above, and watch how the new values automatically 
get propogated down into the notebook.

Let's quickly explain the parameters to the `observable()` function. You can find the full API Reference for 
`streamlit-observable` [here](TODO):

The first parameter, `"Example Updatable Bar Chart"`, is the `key` parameter, used to uniquely identify every `streamlit-observable` embed. 

`notebook` is the id of the notebook at observablehq.com. You can find this at the end of the notebook's URL: https://observablehq.com/@juba/updatable-bar-chart

`targets` are the cells of the notebook we want to be render in the embed. In this case, we just want to 
render the SVG chart found in the `chart` cell, as well as the `draw` cell that contains the logic to 
dynmically update the chart with new data.

`redefine` is a dict with key/values of the cells of the notebook we want to redefine, or "inject" into. 
In this case, we want to redefine the `"data"` cell, which in the original notebook is an array of JS objects,
each with `"name"` and `"value"` keys. So, we can simply hardcode the 3 names we have, pass in the `a`, `b`, and `c` 
variables we defined with `st.slider` calls, and we're good to go!

`hide` is a list of cells that we want to the ran in the embed, but not displayed. In this case, since the `"draw"` 
cell only performs logic for updating the `"chart"` SVG (and does not embed anything of interest in itself), we can 
just hide it to make our embed cleaner. Normally, unless you are dealing with animations or transitions, you don't need 
to work with the `hide` parameter much! 
        """)

        
    elif section == Section.FORM.value:
        st.experimental_set_query_params(section=Section.FORM.value)

        st.write(""" 
## Bi-Directional Component: HTML Form

`streamlit-observable` can not only embed an Observable notebook from Python -> JavaScript, but
we can also pass values back from an Observable notebook, from Javascript -> Python!

Let's use Mike Bostock's [Form Input](https://observablehq.com/@mbostock/form-input) notebook as an example.
The notebook offers a cool utility in the `form` cell, which can be used to turn any HTML form into an 
Observable "view" (See ["Introduction to Views"](https://observablehq.com/@observablehq/introduction-to-views) 
for an explanation). It also has an example, found in the `viewof object` cell. 
Let's embed that example into Streamlit, then pass that value back into Python!
        """)
        with st.echo():
            observers = observable("Example form", 
                notebook="@mbostock/form-input",
                targets=["viewof object"],
                observe=["object"]
            )

            o = observers.get("object")

            st.write("message: **'{message}'**, hue: '{hue}', size: '{size}', emojis: '{emojis}'".format(
                message=o.get("message"),
                hue=o.get("hue"),
                size=o.get("size"),
                emojis=str(o.get("emojis"))
            ))
        st.write(""" 
Let's take a closer look to see how this example is working:

First part, rendering the actual notebook. We pass in the key, `"Example form"`. 
The `notebook` param passes in the observablehq.com notebook ID for the notebook, `"@mbostock/form-input"`.
In `targets`, we only want to render the `viewof object` cell, which is the cell that is the HTML form 
that we want to interact with. The `observe` parameter is a list of cells that we want to observe.
Meaning, whenever the value of the `"object"` cell changes, we want to pass that new value 
back into the Streamlit app/Python-land. """)

        if st.button('❓Whats the difference between the "viewof object" cell and the "object" cell?'):
            st.info("""The `"viewof object"` cell and the `"object"` cell are two different cells, 
even though they are defined on the same line in observablehq.com. The `"viewof object"` cell is
the HTML form that we want to embed and see in the browser, and the `"object"` cell is underlying 
*value* of that HTML form. See ["https://observablehq.com/@observablehq/a-brief-introduction-to-viewof"](https://observablehq.com/@observablehq/a-brief-introduction-to-viewof)
for details.
""")
        st.write(""" 
Now, when you pass in any cell into `observe`, then the `observable()` call will return a dict,
where the keys are the names of the cells, and the values are the value of those cells as they 
exist in the notebook. In this case, the entire `"observers"` object looks like this:
""")
        with st.echo():
            st.json(observers)
        
    elif section == Section.FORCE_GRAPH.value:
        st.experimental_set_query_params(section=Section.FORCE_GRAPH.value)
        @st.cache
        def get_force():
            df_characters = pd.read_json(
                'https://raw.githubusercontent.com/sxywu/hamilton/master/src/data/char_list.json')
            df_links = pd.read_csv(
                'https://raw.githubusercontent.com/sxywu/hamilton/master/data/meta/characters.csv')
            return (df_characters, df_links)
        df_characters, df_links = get_force()
        characters = df_characters.transpose().rename(
            columns={0: "id", 1: "group"}).to_dict('records')

        character_index_to_name = {}
        for index, character in enumerate(characters):
            character_index_to_name[index] = character.get("id")

        df_links_directed = df_links[~df_links["directed_to"].isna()]
        df_links_directed = df_links_directed[
            (df_links_directed["characters"].str.isnumeric())
            & (df_links_directed["directed_to"].str.isnumeric())]
        d = df_links_directed.groupby(
            ["characters", "directed_to"])["lines"].count().rename_axis(["from", "to"]).reset_index(level=[0, 1])
        st.write(character_index_to_name)
        d["from"] = d["from"].apply(lambda x: character_index_to_name[(x)])
        d["to"] = d["to"].apply(lambda x: character_index_to_name[(x)])
        st.write(d)

        observable("Example Force Directed Graph", notebook="@d3/disjoint-force-directed-graph", targets=["chart"],
                   redefine={
            "data": {
                "nodes": characters,
                "links": [],
            }
        })

    elif section == Section.DRAW.value:
        st.experimental_set_query_params(section=Section.DRAW.value)

        st.write("""
## 

""")

        observers = observable("Example Drawing Canvas", 
            notebook="@d3/draw-me", 
            targets=["viewof strokes", "viewof lineWidth", "viewof strokeStyle", "undo"], 
            observe=["strokes"]
        )

        strokes = observers.get("strokes")

        st.json(strokes)


    elif section == Section.COUNTIES.value:
        st.experimental_set_query_params(section=Section.COUNTIES.value)
        
        @st.cache
        def get_county_pop():
            df = pd.read_json("https://api.census.gov/data/2016/acs/acs5?get=B01001_001E&for=county:*", 
                orient="records",
                dtype=False)
            df.drop(df.head(1).index, inplace=True)
            df = df.rename(columns={0:"population", 1:"state", 2:"county"})
            df.population = df.population.astype('int')
            df["county_fips"] = df["state"] + df["county"]
            return df

        st.write("""

## 

""")    
        df = get_county_pop()
        
        observers = observable("County Brush", 
            notebook="d/4f9aa5feff9761c9",
            targets=["viewof countyCodes"], 
            observe=["selectedCounties"]
        )

        selectedCounties = observers.get("selectedCounties")
        
        df_selected = df[df["county_fips"].isin(selectedCounties)]
        df_not_selected = df[~df["county_fips"].isin(selectedCounties)]

        sel_sum = df_selected.population.sum()
        not_sel_sum = df_not_selected.population.sum()

        st.write("""
**{:,}** people live in the **{:,}** counties that are selected above. 
That's **{:.2%}** of the total US population.""".format(
    sel_sum, len(df_selected), sel_sum / not_sel_sum
))

    elif section == Section.PENGUINS.value:
        st.experimental_set_query_params(section=Section.PENGUINS.value)
        
        st.write(""" 
## Static Embed: Scatterplot Matrix with Penguins

Allison Horst [published a dataset](https://github.com/allisonhorst/palmerpenguins) about 
penguins! Using Streamlit, we can use `pd.read_csv` to read in the dataset into a pandas 
DataFrame, which looks like this:
        """)
        penguins = get_penguins()

        st.dataframe(penguins)

        st.write("""

Now, what if we want to visualize this data in a really cool way - say, with a 
[Brushable Scatterplot Matrix](https://observablehq.com/@d3/brushable-scatterplot-matrix)? 
It's possible! however, instead of using that D3 notebook directly, we're going to 
[fork the notebook](https://observablehq.com/@observablehq/fork-share-merge), in order to make 
these two changes:

1. In the D3 notebook, the color legend of the is rendered, but the cell doesn't have a name,
making embeding hard. So, we'll just add a `legend =` to that cell to give it a name.
2. We want to be able to inject our own CSV string using a new cell, so we'll add a `rawData` 
cell that we can redefine to pass in our own CSV.

Now, we'll enable link sharing to that fork, and pass in the notebook's id into `observable()`!
""")

        with st.echo():
            observable("Palmer Penguin Scatterplot Matrix", 
                notebook="d/1bba1cb4219a9df5",
                targets=["chart", "legend"], 
                redefine={
                    "rawData":penguins.to_csv(),
                    "columns": ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"]
                }
            )
        st.write("Try dragging a box around some of the points!")
