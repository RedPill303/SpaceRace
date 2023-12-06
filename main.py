from bs4 import BeautifulSoup
import requests
from datetime import datetime
import pandas as pd
import plotly.express as px
from plotly.colors import n_colors
from dash import Dash, html, dcc, callback, Output, Input, State, dash_table, callback_context
import dash_bootstrap_components as dbc

#
# #  --SCRAPING--
# #
# # upcoming_url = 'https://nextspaceflight.com/launches/?page=1&search='
#
# # GET LAUNCH CODES
#
# codes = []
#
# for n in range(1, 223):
#     past_url = f'https://nextspaceflight.com/launches/past/?page={n}&search='
#     past_response = requests.get(past_url)
#     past_web = past_response.text
#     past_soup = BeautifulSoup(past_web, "html.parser")
#     launches = past_soup.find_all(class_="launch")
#     codes = codes + [launch.get("class")[1][1:] for launch in launches]
#
#     print(f'codes iteration nr {n}: ', codes)
#
#
# # GET DATA FROM EACH LAUNCH CODE
#
# data = []
#
# for code in codes:
#     print(f'obtaining info: code {code}, nr. {codes.index(code)+1} of {len(codes)}')
#     details_url = f'https://nextspaceflight.com/launches/details/{code}'
#     past_response = requests.get(details_url)
#     details_web = past_response.text
#     details_soup = BeautifulSoup(details_web, "html.parser")
#
#     name = details_soup.find_all(name="h4")[0].getText().strip()
#     outcome = details_soup.find_all(name="h6", class_='rcorners status')[0].getText().strip()
#     date = details_soup.find(id='localized').getText().strip() if details_soup.find(id='localized') else None
#     location = details_soup.find_all(class_="card section--center white mdl-grid mdl-grid--no-spacing mdl-shadow--6dp")[1].find('h4').getText()
#     country = location.split(", ")[-1]
#
#     info = [item.getText().strip().split(": ") for item in details_soup.find_all(class_="mdl-grid a")[1] if item.getText().strip() != ""]
#     info_dict = {}
#     for field in info[1:]:
#         info_dict[field[0]] = field[1]
#
#     agency = info[0][0]
#
#     status = info_dict.get('Status', None)
#     price = info_dict.get('Price', None)
#     thrust = info_dict.get('Liftoff Thrust', None)
#     payload_leo = info_dict.get('Payload to LEO', None)
#     payload_gto = info_dict.get('Payload to GTO', None)
#     stages = info_dict.get('Stages', None)
#     strap_ons = info_dict.get('Strap-ons', None)
#     rocket_height = info_dict.get('Rocket Height', None)
#     fairing_diameter = info_dict.get('Fairing Diameter', None)
#     fairing_height = info_dict.get('Fairing Height', None)
#
#     data_row = [code, name, outcome, date, location, country, agency, status, price, thrust, payload_leo, payload_gto, stages, strap_ons, rocket_height, fairing_diameter, fairing_height]
#     data.append(data_row)
#
# # INITIAL DATAFRAME
#
# print('saving initial data')
# columns = ['code', 'name', 'outcome', 'date', 'location', 'country', 'agency', 'status', 'price(MUSD)', 'thrust(kN)', 'payload_leo(kg)', 'payload_gto(kg)', 'stages', 'strap_ons', 'rocket_height(m)', 'fairing_diameter(m)', 'fairing_height(m)']
# df = pd.DataFrame(data, columns=columns)
# date = datetime.now().strftime('%d%m%Y')
# df.to_csv(f'output{date}.csv', index=False)
#
# # DATA CLEANING
#
# print('cleaning data')
#
# df['price(MUSD)'] = df['price(MUSD)'].str.replace(' million', '')
# df['price(MUSD)'] = df['price(MUSD)'].str.replace('$', '')
# df['price(MUSD)'] = df['price(MUSD)'].str.replace(',', '')
# df['price(MUSD)'].fillna(0, inplace=True)
# df['price(MUSD)'] = df['price(MUSD)'].astype(float)
#
# df['thrust(kN)'] = df['thrust(kN)'].str.replace(' kN', '')
# df['thrust(kN)'] = df['thrust(kN)'].str.replace(',', '')
# df['thrust(kN)'].fillna(0, inplace=True)
# df['thrust(kN)'] = df['thrust(kN)'].astype(float)
#
# df['payload_leo(kg)'] = df['payload_leo(kg)'].str.replace(' kg', '')
# df['payload_leo(kg)'] = df['payload_leo(kg)'].str.replace(',', '')
# df['payload_leo(kg)'].fillna(0, inplace=True)
# df['payload_leo(kg)'] = df['payload_leo(kg)'].astype(float)
#
# df['payload_gto(kg)'] = df['payload_gto(kg)'].str.replace(' kg', '')
# df['payload_gto(kg)'] = df['payload_gto(kg)'].str.replace(',', '')
# df['payload_gto(kg)'].fillna(0, inplace=True)
# df['payload_gto(kg)'] = df['payload_gto(kg)'].astype(float)
#
# df['stages'].fillna(0, inplace=True)
# df['stages'] = df['stages'].astype(int)
#
# df['strap_ons'].fillna(0, inplace=True)
# df['strap_ons'] = df['strap_ons'].astype(int)
#
# df['rocket_height(m)'] = df['rocket_height(m)'].str.replace(' m', '')
# df['rocket_height(m)'] = df['rocket_height(m)'].str.replace(',', '')
# df['rocket_height(m)'].fillna(0, inplace=True)
# df['rocket_height(m)'] = df['rocket_height(m)'].astype(float)
#
# df['fairing_diameter(m)'] = df['fairing_diameter(m)'].str.replace(' m', '')
# df['fairing_diameter(m)'] = df['fairing_diameter(m)'].str.replace(',', '')
# df['fairing_diameter(m)'].fillna(0, inplace=True)
# df['fairing_diameter(m)'] = df['fairing_diameter(m)'].astype(float)
#
# df['fairing_height(m)'] = df['fairing_height(m)'].str.replace(' m', '')
# df['fairing_height(m)'] = df['fairing_height(m)'].str.replace(',', '')
# df['fairing_height(m)'].fillna(0, inplace=True)
# df['fairing_height(m)'] = df['fairing_height(m)'].astype(float)
#
#
# # FINAL DATAFRAME
#
# print('saving final data')
# df.to_csv(f'clean_output{date}.csv', index=False)
# df = pd.read_csv(f'clean_output{date}.csv')
df = pd.read_csv('clean_output28112023.csv')

df["date"] = pd.to_datetime(df["date"])
df['year'] = df['date'].dt.year
df['count'] = 1

year_country_df = df.groupby(['country', 'year']).agg({'name': pd.Series.count}).reset_index()
year_agency_df = df.groupby(['agency', 'year']).agg({'name': pd.Series.count}).reset_index()

top_10 = df.groupby('agency').count().sort_values('code', ascending=False).head(10).index.values
agency_list = df.groupby('agency').count().sort_values('agency').index.values.tolist()
country_list = df.groupby('country').count().sort_values('country').index.values.tolist()
outcome_list = df.groupby('outcome').count().sort_values('country').index.values.tolist()
status_list = df.groupby('status').count().sort_values('country').index.values.tolist()

agency_options = [{"label": item, "value": (agency_list.index(item) + 1)} for item in agency_list]
country_options = [{"label": item, "value": (country_list.index(item) + 1)} for item in country_list]
outcome_options = [{"label": item, "value": (outcome_list.index(item) + 1)} for item in outcome_list]
status_options = [{"label": item, "value": (status_list.index(item) + 1)} for item in status_list]

# --DASHBOARD--


dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY, dbc_css], prevent_initial_callbacks=True)
server = app.server
app.title = "Space Race"

q_colors = int(len(agency_list)/6)+1

agency_colors = n_colors('rgb(220, 30, 30)', 'rgb(220, 30, 220)', q_colors, colortype='rgb')
agency_colors.extend(n_colors('rgb(220, 30, 220)', 'rgb(30, 30, 220)', q_colors, colortype='rgb'))
agency_colors.extend(n_colors('rgb(30, 30, 220)', 'rgb(30, 220, 220)', q_colors, colortype='rgb'))
agency_colors.extend(n_colors('rgb(30, 220, 220)', 'rgb(30, 220, 30)', q_colors, colortype='rgb'))
agency_colors.extend(n_colors('rgb(30, 220, 30)', 'rgb(220, 220, 30)', q_colors, colortype='rgb'))
agency_colors.extend(n_colors('rgb(220, 220, 30)', 'rgb(220, 30, 30)', q_colors, colortype='rgb'))

agency_color_map = {agency: agency_colors[agency_list.index(agency)] for agency in agency_list}


#  Components

jumbotron = html.Div(
    dbc.Container(
        [
            html.H2("Space Race", className="display-3"),
            html.P(
                ["A graphical visualization of space launches from 1957 to the date."],
                className="lead",
            ),
            html.P(
                ["All rocket and launch info was scraped from ",
                 html.A("NextSpaceFlight", href="https://nextspaceflight.com/")],
            ),
            html.Hr(className="my-2"),
        ],
        fluid=True,
        className="my-3",
    ),
    className="p-3 rounded-3")

offcanvas = html.Div(
    [
        html.Div(
            dbc.Button("Filters", id="open-offcanvas", n_clicks=0),
            style={"position": "fixed", "top": "20px", "right": "20px", "z-index": "999"}
        ),

        dbc.Offcanvas(
            html.P([

                dbc.Container([
                    dbc.Row([
                        dbc.Label("Time Range"),
                        dcc.RangeSlider(1957, 2023, 1, tooltip={"placement": "top", "always_visible": True},
                                        allowCross=False, value=[1957, 2023],
                                        marks={i: str(i) for i in range(1957, 2023, 10)},
                                        id='year-range', className='mt-3 mb-2')
                    ], className='my-2'),

                    html.Hr(),

                    dbc.Row([
                        dbc.Label("Agencies Selection"),
                        dbc.RadioItems(
                            id="agency-group",
                            className="btn-group my-2",
                            inputClassName="btn-check",
                            labelClassName="btn btn-outline-primary",
                            labelCheckedClassName="active",
                            options=[
                                {"label": "Top 10", "value": 1},
                                {"label": "All", "value": 2},
                            ],
                            value=1)
                    ], className="my-2"),

                    html.Hr(),

                    dbc.Row([

                        dbc.Accordion([
                            dbc.AccordionItem([
                                dbc.Checklist(
                                    options=status_options,
                                    value=[status_list.index(item) + 1 for item in status_list],
                                    id="status-checklist-input")
                            ],
                                title="Status"),
                            dbc.AccordionItem([
                                dbc.Checklist(
                                    options=outcome_options,
                                    value=[outcome_list.index(item) + 1 for item in outcome_list],
                                    id="outcome-checklist-input")
                            ],
                                title="Outcome"),
                            dbc.AccordionItem([
                                dbc.Checklist(
                                    options=agency_options,
                                    value=[agency_list.index(item) + 1 for item in agency_list],
                                    id="agency-checklist-input")
                            ],
                                title="Agencies"),
                            dbc.AccordionItem([
                                dbc.Checklist(
                                    options=country_options,
                                    value=[country_list.index(item) + 1 for item in country_list],
                                    id="country-checklist-input")
                            ],
                                title="Launch Country"),
                        ], start_collapsed=True, className='my-2'),
                    ]),

                    html.Hr()

                ])
            ]),
            id="offcanvas",
            title="Filters",
            is_open=False,
        ),
    ]
)

# App layout

app.layout = dbc.Container([jumbotron, offcanvas,

                            dbc.Row([
                                dbc.Col(dcc.Graph(figure={}, id='line'), xl=6, width=12, className='my-2'),
                                dbc.Col(dcc.Graph(figure={}, id='success_line'), xl=6, width=12, className='my-2')
                            ]),

                            dbc.Row([
                                dbc.Col(dcc.Graph(figure={}, id='scatter2'), xl=6, width=12, className='my-2'),
                                dbc.Col(dcc.Graph(figure={}, id='histogram'), xl=6, width=12, className='my-2')
                            ]),


                            dbc.Row([
                                dbc.Col(dcc.Graph(figure={}, id='scatter'), xl=6, width=12, className='my-2'),
                                dbc.Col(dcc.Graph(figure={}, id='box'), xl=6, width=12, className='my-2'),
                            ]),

                            dbc.Row([
                                dbc.Col(dcc.Graph(figure={}, id='sunburst'), xl=4, width=12, className='my-2'),
                                dbc.Col([
                                        dbc.Row(dbc.Label("Underlying Data", className="text-center pt-2"),
                                                style={'background-color': '#111111'}, className='mx-0'),
                                        dbc.Row(dash_table.DataTable(data=None, id='table',
                                                                 page_size=10,
                                                                 style_table={'overflowX': 'auto',
                                                                              'border': '5px solid #111111'},
                                                                 style_header={
                                                                        'backgroundColor': 'rgb(40, 40, 40)',
                                                                        'color': 'white',
                                                                        'textAlign': 'center'
                                                                    },
                                                                 style_data={
                                                                        'backgroundColor': 'rgb(60, 60, 60)',
                                                                        'color': 'white',
                                                                        'textAlign': 'left'},
                                                                 ))], xl=8, width=12, className='my-2')
                            ]),

                            ], fluid=True)


# Add controls to build the interaction

@callback(
    [
        Output('line', 'figure'),
        Output('success_line', 'figure'),
        Output('scatter2', 'figure'),
        Output('table', 'data'),
        Output('histogram', 'figure'),
        Output('scatter', 'figure'),
        Output('box', 'figure'),
        Output('sunburst', 'figure'),
    ],
    [Input('year-range', 'value'),
     Input('agency-group', 'value'),
     Input('agency-checklist-input', 'value'),
     Input('country-checklist-input', 'value'),
     Input('outcome-checklist-input', 'value'),
     Input('status-checklist-input', 'value'),
     ]
)
def update_years(year_range_value,
                 agency_group_value,
                 agency_checklist_input_value,
                 country_checklist_input_value,
                 outcome_checklist_input_value,
                 status_checklist_input_value
                 ):
    filtered_df = df[(df['date'].dt.year >= year_range_value[0]) & (df['date'].dt.year <= year_range_value[1])]
    if agency_group_value == 1:
        filtered_df = filtered_df[filtered_df['agency'].isin(top_10)]

    filtered_agency_list = [agency_list[i - 1] for i in agency_checklist_input_value]
    filtered_country_list = [country_list[i - 1] for i in country_checklist_input_value]
    filtered_outcome_list = [outcome_list[i - 1] for i in outcome_checklist_input_value]
    filtered_status_list = [status_list[i - 1] for i in status_checklist_input_value]

    filtered_df = filtered_df[filtered_df['agency'].isin(filtered_agency_list)]
    filtered_df = filtered_df[filtered_df['country'].isin(filtered_country_list)]
    filtered_df = filtered_df[filtered_df['outcome'].isin(filtered_outcome_list)]
    filtered_df = filtered_df[filtered_df['status'].isin(filtered_status_list)]

    filtered_outcome_df = filtered_df.pivot_table(index=['year', 'agency'], columns='outcome', values='count',
                                                  aggfunc='sum', fill_value=0).reset_index()
    required_keys = ['Success', 'Failure', 'Partial Failure', 'Prelaunch Failure']
    existing_keys = [key for key in required_keys if key in filtered_outcome_df.columns]

    if 'Success' in filtered_outcome_df.columns:
        filtered_outcome_df['success_ratio'] = (filtered_outcome_df['Success'] / filtered_outcome_df[existing_keys].sum(
            axis=1)) * 100
    else:
        filtered_outcome_df['success_ratio'] = 0

    filtered_outcome_df['roll'] = filtered_outcome_df['success_ratio'].rolling(window=5).mean()

    filtered_agg_df = filtered_df.groupby(['year', 'agency']).agg(
        count=pd.NamedAgg(column='name', aggfunc='count'),
        total_price_MUSD=pd.NamedAgg(column='price(MUSD)', aggfunc='sum'),
        avg_thrust_kN=pd.NamedAgg(column='thrust(kN)', aggfunc='mean'),
        total_payload_leo_kg=pd.NamedAgg(column='payload_leo(kg)', aggfunc='sum'),
        total_payload_gto_kg=pd.NamedAgg(column='payload_gto(kg)', aggfunc='sum'),
        avg_rocket_height=pd.NamedAgg(column='rocket_height(m)', aggfunc='mean'),
        avg_fairing_diameter_m=pd.NamedAgg(column='fairing_diameter(m)', aggfunc='mean'),
        avg_fairing_height_m=pd.NamedAgg(column='fairing_height(m)', aggfunc='mean'),
    ).reset_index()

    line = (px.line(filtered_agg_df, x='year', y='count', color='agency',
                    color_discrete_map=agency_color_map, template="plotly_dark")
            .update_layout(legend=dict(traceorder='normal'),
                           title={'text': 'Launches per year by agency', 'x': 0.5}
                           )
            .update_traces(hovertemplate='<b>Year</b>: %{x}'
                                         '<br><b>Launches</b>: %{y}')
            )

    success_line = (px.line(filtered_outcome_df, x='year', y='roll', color='agency',
                            color_discrete_map=agency_color_map, template="plotly_dark")
                    .update_layout(legend=dict(traceorder='normal'),
                                   title={'text': 'Success ratio (5 year rolling average)', 'x': 0.5})
                    .update_traces(hovertemplate='<b>Year</b>: %{x}<br><b>Success ratio</b>: %{y:.1f}%'))

    scat2_filtered_df = filtered_df[(filtered_df['price(MUSD)'] > 0)]
    scat2 = (px.scatter(scat2_filtered_df, x='date',
                        y='price(MUSD)',
                        hover_name='name',
                        color='agency', color_discrete_map=agency_color_map, template="plotly_dark")
             .update_layout(xaxis_title="Time",
                            yaxis_title="Price (in USD Millions)",
                            legend=dict(traceorder='normal'),
                            yaxis={'type': 'log'},
                            title={'text': 'Price distribution over time', 'x': 0.5}
                            )
             .update_traces(hovertemplate='<b>Year</b>: %{x}'
                                          '<br><b>Price (MUSD)</b>: %{y}'
                                          '<br><b>Name</b>: %{hovertext}')
             )

    tab = filtered_df.to_dict('records')

    hist = (px.histogram(filtered_df, x='agency', color='outcome', histfunc='count',
                         hover_name='outcome', template="plotly_dark")
            .update_layout(xaxis={'categoryorder': 'total descending'},
                           title={'text': 'Total number of launches', 'x': 0.5})
            .update_traces(hovertemplate='<b>Agency</b>: %{x}'
                                         '<br><b>Launches</b>: %{y}')
            )

    scat_filtered_df = filtered_df[(filtered_df['price(MUSD)'] > 0) & (filtered_df['payload_leo(kg)'] > 0)]
    scat = (px.scatter(scat_filtered_df, x='price(MUSD)',
                       y='payload_leo(kg)',
                       size='thrust(kN)',
                       hover_name='name',
                       color='agency', color_discrete_map=agency_color_map, template="plotly_dark")
            .update_layout(xaxis_title="Price (in USD Millions)",
                           yaxis_title="Payload to LEO (kg)",
                           xaxis={'type': 'log'},
                           legend=dict(traceorder='normal'),
                           title={'text': 'Price and payload to LEO', 'x': 0.5}
                           )
            .update_traces(hovertemplate='<b>Name</b>: %{hovertext}' +
                                         '<br><b>Price</b>: %{x:.2f} MUSD' +
                                         '<br><b>Payload</b>: %{y} kg' +
                                         '<br><b>Thrust</b>: %{marker.size} kN'
                           )
            )

    box = px.box(filtered_df[filtered_df['thrust(kN)'] > 0],
                 y='thrust(kN)',
                 x='agency',
                 color='agency',
                 color_discrete_map=agency_color_map,
                 template="plotly_dark",
                 points=False,
                 notched=True).update_layout(xaxis_title="Agency",
                                             yaxis_title="Thrust (kN)",
                                             yaxis=dict(type='log'),
                                             legend=dict(traceorder='normal'),
                                             title={'text': 'Thrust distribution', 'x': 0.5})

    sunburst = (px.sunburst(filtered_df, path=['country', 'location'], values='count', template="plotly_dark")
                .update_layout(title={'text': 'Launch sites by country', 'x': 0.5})
                .update_traces(
                    hovertemplate='<b>Location</b>: %{label}<br>' +
                                  '<b>Count</b>: %{value}'
                )
    )

    return (line,
            success_line,
            scat2,
            tab,
            hist,
            scat,
            box,
            sunburst,
            )


@app.callback(
    Output("offcanvas", "is_open"),
    Input("open-offcanvas", "n_clicks"),
    [State("offcanvas", "is_open")],
)
def toggle_offcanvas(n1, is_open):
    if n1:
        return not is_open
    return is_open


# Run the app
if __name__ == '__main__':
    app.run(debug=False)
