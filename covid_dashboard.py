import pandas as pd
import numpy as np
from datetime import datetime, timedelta

import plotly.graph_objects as go

import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
csv_url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/ecdc/full_data.csv"
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

raw_data = None
smaller_frame = None
unique = None
obj = None
table_data = None
unique_entity = None
data_table_array = None
datelist = None
max_range_for_deaths = None
max_range_for_fatality = None


# # # # # <---- START of reading and wrangling data ---->
# # # reading online csv file
# raw_data = pd.read_csv(csv_url)

# # # renaming the columns because I had already prebuilt the application and these were the column names I already had
# raw_data = raw_data.rename(
#     columns={
#         "date":"Date",
#         "location":"Entity",
#         "total_cases":"Total_Cases",
#         "total_deaths":"Deaths"
#     }
# )

# # # dropping stuff I dont need
# raw_data = raw_data.drop(["new_cases","new_deaths"], axis = 1)

# # # new data set did not come with fatality rate so I had to calculate it myself
# def calculate_Fatality(argument1):
#     if(argument1["Total_Cases"] != 0):
#         percent = (argument1["Deaths"]/argument1["Total_Cases"])*100
#         return round(percent,3)

# raw_data["Fatality"] = raw_data.apply(calculate_Fatality, axis = 1)

# # # # # <---- END of reading and wrangling data ---->

# # # # # <---- START of time range slider ---->
# smaller_frame = raw_data[raw_data["Entity"] == "China"]
# # print(smaller_frame.head(30))

# # create unique list of dates to use for our graph
# unique = raw_data["Date"].unique().tolist()

# def sort_datetime(element):
#     # return datetime.strptime(element,'%b %d, %Y')
#     return datetime.strptime(element,'%Y-%m-%d')

# unique.sort(key=sort_datetime, reverse= False)

# obj = dict()
# for index,uniq in enumerate(unique):
#     obj[index] = uniq

# # difference_in_days = datetime.strptime(obj[131],'%Y-%m-%d') - datetime.strptime(obj[0],'%Y-%m-%d')
# # base = datetime.today()
# # date_list = [base - timedelta(weeks=x) for x in range(10)]

# datelist = pd.date_range(start=datetime.strptime(obj[0],'%Y-%m-%d') - timedelta(days=10),end=datetime.today(), freq="4D").tolist()

# max_range_for_deaths = raw_data["Deaths"].max()
# max_range_for_fatality = raw_data["Fatality"].max()

# # strftime seems to format the date a lot better than .date() method
# for d in range(len(datelist)):
#     datelist[d] = datelist[d].strftime("%Y-%m-%d")

# # # # # <---- END of time range slider ---->

# # # # # <---- START of creating data for data table ---->
# table_data = raw_data.copy()
# table_data = table_data.drop(["Date"],axis=1)
# unique_entity = table_data["Entity"].unique()

# data_table_array = []
# for entity in unique_entity:
#     temp_obj = {}
#     temp_obj["Entity"] = entity
#     temp_obj["Fatality"] = temp_fatality = table_data[table_data["Entity"] == entity]["Fatality"].mean()
#     temp_obj["Deaths"] = temp_deaths = table_data[table_data["Entity"] == entity]["Deaths"].max()
#     temp_obj["Total_Cases"] = temp_deaths = table_data[table_data["Entity"] == entity]["Total_Cases"].max()
#     data_table_array.append(temp_obj)
    
# # print(unique_entity)
# raw_data["Date"] = raw_data["Date"].astype("datetime64[ns]")
# # print(raw_data.iloc[1:4,:])
# # # # # <---- END of creating data for data table ---->

# # # # <---- START of layout for the dash app ---->


def serve():
    # # # # <---- START of reading and wrangling data ---->
    global raw_data
    global smaller_frame
    global unique
    global obj
    global table_data
    global unique_entity
    global data_table_array
    global datelist
    global max_range_for_deaths
    global max_range_for_fatality

   # # # # <---- START of reading and wrangling data ---->
    # # reading online csv file
    raw_data = pd.read_csv(csv_url)

    # # renaming the columns because I had already prebuilt the application and these were the column names I already had
    raw_data = raw_data.rename(
        columns={
            "date":"Date",
            "location":"Entity",
            "total_cases":"Total_Cases",
            "total_deaths":"Deaths"
        }
    )

    # # dropping stuff I dont need
    raw_data = raw_data.drop(["new_cases","new_deaths"], axis = 1)
    # # new data set did not come with fatality rate so I had to calculate it myself
    def calculate_Fatality(argument1):
        if(argument1["Total_Cases"] != 0):
            percent = (argument1["Deaths"]/argument1["Total_Cases"])*100
            return round(percent,3)

    raw_data["Fatality"] = raw_data.apply(calculate_Fatality, axis = 1)

    # # # # <---- END of reading and wrangling data ---->

    # # # # <---- START of time range slider ---->
    smaller_frame = raw_data[raw_data["Entity"] == "China"]
    # print(smaller_frame.head(30))

    # create unique list of dates to use for our graph
    unique = raw_data["Date"].unique().tolist()

    def sort_datetime(element):
        # return datetime.strptime(element,'%b %d, %Y')
        return datetime.strptime(element,'%Y-%m-%d')

    unique.sort(key=sort_datetime, reverse= False)

    obj = dict()
    for index,uniq in enumerate(unique):
        obj[index] = uniq

    # difference_in_days = datetime.strptime(obj[131],'%Y-%m-%d') - datetime.strptime(obj[0],'%Y-%m-%d')
    # base = datetime.today()
    # date_list = [base - timedelta(weeks=x) for x in range(10)]

    datelist = pd.date_range(start=datetime.strptime(obj[0],'%Y-%m-%d') - timedelta(days=10),end=datetime.today(), freq="4D").tolist()

    max_range_for_deaths = raw_data["Deaths"].max()
    max_range_for_fatality = raw_data["Fatality"].max()

    # strftime seems to format the date a lot better than .date() method
    for d in range(len(datelist)):
        datelist[d] = datelist[d].strftime("%Y-%m-%d")

    # # # # <---- END of time range slider ---->

    # # # # <---- START of creating data for data table ---->
    table_data = raw_data.copy()
    table_data = table_data.drop(["Date"],axis=1)
    unique_entity = table_data["Entity"].unique()

    data_table_array = []
    for entity in unique_entity:
        temp_obj = {}
        temp_obj["Entity"] = entity
        temp_obj["Fatality"] = table_data[table_data["Entity"] == entity]["Fatality"].mean()
        temp_obj["Deaths"] = table_data[table_data["Entity"] == entity]["Deaths"].max()
        temp_obj["Total_Cases"] = table_data[table_data["Entity"] == entity]["Total_Cases"].max()
        data_table_array.append(temp_obj)
        
    # print(unique_entity)
    raw_data["Date"] = raw_data["Date"].astype("datetime64[ns]")
    # print(raw_data.iloc[1:4,:])
    # # # # <---- END of creating data for data table ---->

    return(
        html.Div([
            html.Div(
                # html.Div(
            #    dcc,Graph(id="table")
                dash_table.DataTable(
                    id="editable_table",
                    columns=(
                        # [{'id': 'Model', 'name': 'Model'}] +
                        [{'id': p, 'name': p} for p in ['Entity','Total_Cases','Fatality','Deaths']]
                    ),
                    data=data_table_array,
                    # [
                        
                        # dict(Entity=[1,2], Fatality=1), #for i in range(1,5)
                        # dict(Entity="South Africa", Deaths=1),
                        # dict(Entity=2, Deaths=1),
                    # ],
                    # editable=True,
                    row_selectable="multi",
                    selected_rows=[10,41,97,198,199],
                    style_as_list_view=True,
                    fixed_rows={"headers": True, "data": 0},
                    style_table={
                        "maxHeight": "1000px",
                        "height": "1000px",
                        # "overflowY": "scroll",
                    },
                    style_cell={"font_family": "Helvetica Neue"},
                    style_cell_conditional=[
                        {"if": {"column_id": "Entity"}, "width": "23%"},
                        {"if": {"column_id": "Fatality"}, "width": "23%"},
                        {"if": {"column_id": "Total_Cases"}, "width": "23%"},
                        {"if": {"column_id": "Deaths"}, "width": "23%"},
                        {"if": {"column_id": "Fatality"}, "color": "#d7191c"},
                        {"if": {"column_id": "Total_Cases"}, "color": "#1a9622"},
                        {"if": {"column_id": "Deaths"}, "color": "#6c6c6c"},
                        {"textAlign": "left"},
                    ],
                    style_header={
                        "backgroundColor": "#f4f4f2",
                        "fontWeight": "bold",
                        "padding": "0.4rem",
                    },
                    sort_action="native",
                    filter_action="native",
                    virtualization=True,
                ),
            # ),
                style={"width":"30%","height":"100%","float":"left","padding":"30px","background-color": "lightyellow"}
            ),

            html.Div([
                html.Div([
                    html.Div([
                        dcc.Dropdown(
                            id='xaxis-column',
                            options=[{'label': i, 'value': i} for i in ["Fatality Rate vs Total Confirmed", "(Testing) Animate Fatality Rate vs Total Confirmed WO Slider", "option3"]],
                            value='Fatality Rate vs Total Confirmed'
                        ),
                    ],
                    style={'width': '48%', 'display': 'inline-block'}),
                    # # # # the value property is for default value property. this is used when you first load the chart in
                    # # # # there is no enter button for when you input the number in...it will auto change after sometime
                    html.Div([
                        dcc.Input(
                            id='num-multi',
                            type='number',
                            value="This done nothing at the moment"
                        ),
                    ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),
                    html.Div([
                        dcc.RadioItems(
                            id='yaxis-type',
                            options=[{'label': i, 'value': i} for i in ['log', 'linear']],  # # # # list comprehension # options = [{"value": i} for i in [1,2,5,9,7,5]] print(options[0]) can use generator expressions also
                            value='log',
                            labelStyle={'display': 'inline-block'}
                        ) 
                    ])
                    # # html.Div(id="outt")
                ]),
                html.Div(
                    dcc.Graph(id='indicator-graphic')
                ),
                
                html.Div([
                    dcc.RangeSlider(
                        id= "range_slide",
                        # updatemode="drag",
                        min=0,
                        max=len(datelist) - 1,
                        step=1,
                        value=[0,len(datelist) - 1],
                        dots=True,
                        updatemode='mouseup',
                        # marks={
                        #     0:"Start",
                        #     5:"Middle",
                        #     10:"End",
                        # } # # # check how obj is set up. needs a dictionary with keys as indexed numbers
                    )
                ]),
                html.Div(id='output-container-range-slider'),
                html.Div(dcc.Graph(id="tables")),
            ],style={"width":"60%","height":"100%","float":"left","padding":"30px"}) #, "background-color": "lightblue"
        ])
    )

app.layout = serve
# # # # <---- END of layout for the dash app ---->

@app.callback(
     Output('indicator-graphic', 'figure'),
    [
        # Input("editable_table","derived_virtual_selected_rows"),
        Input("editable_table", "derived_virtual_data"),
        Input("editable_table", "derived_virtual_selected_rows"),
        Input('range_slide', 'value'),
        Input('xaxis-column','value'),
        Input('yaxis-type','value')
    ],
)
def make_graph_based_on_input(derived_virtual_data , derived_virtual_selected_rows , range_slider_date , drop_down, yaxis_type):
    graphing_array = []
    if derived_virtual_data is not None:
        for i in derived_virtual_selected_rows:
            graphing_array.append(derived_virtual_data[i]["Entity"])
    else:
        pass
        # print("its None")

    if len(graphing_array) == 0:
            graphing_array = ["Australia"]

    # if range_slider_date is not None or len(range_slider_date) != 0:
        # print("You are looking at data from the start date {start} to the end date of {end}"
        # .format(start=datelist[range_slider_date[0]], end=datelist[range_slider_date[1]]))

    fig=go.Figure()
    # fig.update_layout(xaxis={"range":[0,300000]}) # zzzzz
    fig.update_layout(xaxis_type=yaxis_type) # ,plot_bgcolor="white",paper_bgcolor="rgb(18, 22, 37)"

    # updatemenus = list([
    #     dict(active=1,
    #         buttons=list([
    #             dict(label='Linear Scale',
    #                 method='relayout',
    #                 args=[
    #                     { # 'title': 'Linear scale',
    #                         'xaxis': {'type': 'linear'}
    #                     }
    #                 ]
    #             ),
    #             dict(label='Log Scale',
    #                 method='relayout',
    #                 args=[
    #                     { # 'title': 'Log scale',
    #                         'xaxis': {'type': 'log'}
    #                     }
    #                 ]
    #             )
    #         ]),
    #     )
    # ])

    # fig.update_layout(updatemenus=updatemenus, title="Fatality Rate vs Total Confirmed",xaxis_title="Total Confirmed Deaths",yaxis_title="Fatality Rate",)
    fig.update_layout(title="Fatality Rate vs Total Confirmed",xaxis_title="Total Confirmed Deaths",yaxis_title="Fatality Rate")


    for entity in graphing_array:
        temp_frame = raw_data[raw_data["Entity"] == entity]

        temp_frame = temp_frame[(temp_frame["Date"] > datelist[range_slider_date[0]]) & (temp_frame["Date"] < datelist[range_slider_date[1]])]

        temp_trace = go.Scattergl(
            x=temp_frame.Deaths,
            y=temp_frame.Fatality,
            mode="markers+lines",
            name=entity,
            hovertemplate =
            '<b>Fatality</b>: %{y:.2f}%'+
            '<br><b>Death</b>: %{x}'+
            '<br><b>Date</b>: %{text}',
            text=temp_frame.Date,
            customdata=temp_frame.Entity,
        )
        fig.add_trace(temp_trace)
    

# # # <---- ---->

    fig_dict = {
        "data": [],
        "layout": {},
        "frames": []
    }
    
    for ent in ["World"]:
        master_data = raw_data[raw_data["Entity"] == ent]
        first_data = master_data[master_data["Date"] == unique[50]]
        
        temp_trace = go.Scattergl(
            x=first_data.Deaths,
            y=first_data.Fatality,
            mode="lines",
            name=ent,
            hovertemplate =
            '<b>Fatality</b>: %{y:.2f}%'+
            '<br><b>Death</b>: %{x}'+
            '<br><b>Date</b>: %{text}',
            text=first_data.Date,
            customdata=first_data.Entity,
        )
        temp_trace2 = go.Scattergl(
            x=first_data.Deaths,
            y=first_data.Fatality,
            mode="markers",
            name=ent,
            hovertemplate =
            '<b>Fatality</b>: %{y:.2f}%'+
            '<br><b>Death</b>: %{x}'+
            '<br><b>Date</b>: %{text}',
            text=first_data.Date,
            customdata=first_data.Entity,
        )

        fig_dict["data"].append(temp_trace)
        fig_dict["data"].append(temp_trace2)


        # country_array = []

        # for i in range(50, len(unique)):
        #     frame_data = master_data[master_data["Date"] < unique[i]]
            
        #     frame = go.Frame(
        #         data=[
        #             go.Scatter(
        #                 x=frame_data.Deaths,
        #                 y=frame_data.Fatality,
        #                 mode="lines",
        #             ),
        #             go.Scatter(
        #                 x=frame_data.Deaths,
        #                 y=frame_data.Fatality,
        #                 mode="markers",
        #             ),
        #         ],
        #         traces=[0,1]
        #     )
            

        #     fig_dict["frames"].append(frame)


#     # updatemenuss=[
#     #     dict(
#     #         type="buttons",
#     #         buttons=[
#     #             dict(
#     #                 label="Play",
#     #                 method="animate",
#     #                 args=[
#     #                     None
#     #                 ]
#     #             )
#     #         ]
#     #     )
#     # ]


    fig_dict["layout"] = go.Layout(
        # width=1050,
        # height=600,

        # xaxis_type="log",
        xaxis=dict(
            range=[0,max_range_for_deaths]
        ),
        yaxis=dict(
            range=[0,9]
        ),


        # showlegend=False,
        hovermode='closest',
        updatemenus= [
            dict(
                type='buttons',
                showactive=False,
                # y=1.05,
                # x=1.15,
                xanchor='right',
                yanchor='top',
                # pad=dict(
                #     t=0, 
                #     r=10
                # ),
                buttons=[
                    dict(
                        label='Play',
                        method='animate',
                        args=[None, 
                            dict(
                                frame=dict(
                                    duration=100, 
                                    redraw=False
                                ),
                                transition=dict(
                                    duration=0
                                ),
                                fromcurrent=True,
                                mode='immediate'
                            )
                        ]
                    )
                ]
            )
        ]
    )

    figg = go.Figure(fig_dict)

        # figg.update_layout(updatemenus=updatemenuss)
        # figg.update_layout(layout=layout)

            # figg.add_trace(temp_trace)

            # figg["frame"] = ["fake frame"]

    if drop_down == "Fatality Rate vs Total Confirmed":
        return fig

    elif drop_down == "(Testing) Animate Fatality Rate vs Total Confirmed WO Slider":
        # figg = go.Figure()
        return figg



@app.callback(
    Output("tables","figure"),
    [
        Input('indicator-graphic','selectedData'),
    ]
)
def selectData2(selected):
    if selected is not None:
        # print(selected["points"])
        entity_arr = []
        date_arr = []
        fatality_arr = []
        deaths_arr = []
        for point in selected["points"]:
           entity_arr.append(point["customdata"])
           date_arr.append(point["text"])
           fatality_arr.append(point["y"])
           deaths_arr.append(point["x"])
    
        table = go.Figure(
            go.Table(
                header=dict(values=['Entity','Date','Fatality','Total_Deaths'],
                    fill = dict(color='#C2D4FF'),
                    align = ['left'] * 5),
                cells=dict(values=[
                    entity_arr,
                    date_arr,
                    fatality_arr,
                    deaths_arr,
                ],
                fill = dict(color='#F5F8FF'),
                align = ['left'] * 5)
            ),
            layout={
                "title":"Display Selected data points from Graph",
            }
        )
        return table
    else:
        return go.Figure(
            go.Table(
        header=dict(values=['Entity','Date','Fatality','Total_Deaths'],
                    fill = dict(color='#C2D4FF'),
                    align = ['left'] * 5),
        cells=dict(values=[

        ],
            fill = dict(color='#F5F8FF'),
            align = ['left'] * 5)
        ),
        layout={
            "title":"Display Selected data points from Graph",
        }
        )


@app.callback(
    Output('output-container-range-slider', 'children'),
    [
        Input('range_slide', 'value'),
    ]
)

def update_output(value):
    # return 'You have selected "{}"'.format(value)
    return 'Start date: {v} \n End date: {z}'.format(v=str(datelist[value[0]]), z=str(datelist[value[1]]))



if __name__ == "__main__":
    app.run_server()
