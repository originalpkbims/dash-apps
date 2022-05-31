from dash import html
from dash import dcc
import dash_bootstrap_components as dbc


def create_homepage_content(datelist):

    # app.layout = html.Div([
    #     dbc.Row(html.A([html.Img(src='assets/holders.svg',
    #                              style={'height': '400px', 'width': '600px%'})])),
    #     dbc.Row([html.A(id='output'),
    #              dcc.Slider(min=2019, max=2020, step=1,
    #                         value=2019,
    #                         id='year-slider')])
    # ])
    datelist = [str(x) for x in datelist]
    numdate = [x for x in range(len(datelist))]

    content = [
        dbc.Row(
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader(
                        html.H1("State of Tokenized Carbon", className='page-title'))
                ]), width=12, style={'textAlign': 'center'})),
        dbc.Row([html.A(id='output'),
                 dcc.Slider(min=numdate[0],  # the first date
                            max=numdate[-1],  # the last date
                            step=None,
                            value=numdate[0],  # default: the first
                            marks={numd: date for numd, date in zip(numdate, datelist)},
                            id='year-slider')
                 ])]

    return datelist, numdate, content
