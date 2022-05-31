from tkinter import font
from turtle import bgcolor, color
import pandas as pd
import circlify
import matplotlib.pyplot as plt
import dash_bootstrap_components as dbc
import dash
from dash import html, Input, Output, callback, State
from dash import dcc
import chart_studio.plotly.plotly as py
import plotly.tools as tls
from plotly.offline import iplot
from pprint import pprint as pp


app = dash.Dash(
    __name__,
    title="KlimaDAO Tokenized Carbon Dashboard | Beta",
    suppress_callback_exceptions=True)

data = [{'id': 'World', 'datum': 25, 'children': [
    {'id': "KlimaDAO", 'datum': 18},
    {'id': "Olympus", 'datum': 2},
    {'id': "Mark Cuban", 'datum': 0.8},
    {'id': "0x23..44", 'datum': 0.3},
    {'id': "...", 'datum': 0.2},
    {'id': "...", 'datum': 0.2},
    {'id': "...", 'datum': 0.2},
    {'id': "...", 'datum': 0.2},
    {'id': "...", 'datum': 0.2},
    {'id': "...", 'datum': 0.2},
    {'id': "...", 'datum': 0.2},
    {'id': "...", 'datum': 0.2},
    {'id': "...", 'datum': 0.2},
    {'id': "...", 'datum': 0.2},
    {'id': "...", 'datum': 0.2},
    {'id': "...", 'datum': 0.2},
    {'id': "...", 'datum': 0.2},
    {'id': "...", 'datum': 0.2},
    {'id': "...", 'datum': 0.2},
]}]

data2019 = [{'id': 'World', 'datum': 10, 'children': [
    {'id': "Offchain", 'datum': 7},
    {'id': "Offchain retired", 'datum': 2},
    {'id': "Onchain", 'datum': 3},
    {'id': "Onchain retired", 'datum': 2},
]}]

data2020 = [{'id': 'World', 'datum': 12, 'children': [
    {'id': "Offchain", 'datum': 9},
    {'id': "Offchain retired", 'datum': 2},
    {'id': "Onchain", 'datum': 5},
    {'id': "Onchain retired", 'datum': 2},
]}]

style_dict = {'KlimaDAO': {'fontsize': 20, 'scale_r': 0.9, 'alpha': 1, 'color': '#00CC33'},
              'Olympus': {'fontsize': 18, 'scale_r': 0.9, 'alpha': 0.7, 'color': '#00CC33'},
              'Mark Cuban': {'fontsize': 16, 'scale_r': 0.9, 'alpha': 0.5, 'color': '#00CC33'},
              '0x23..44': {'fontsize': 12, 'scale_r': 0.9, 'alpha': 0.5, 'color': '#00CC33'},
              '...': {'fontsize': 8, 'scale_r': 0.7, 'alpha': 0.3, 'color': '#00CC33'},
              }

style_dict_offchain = {'Offchain': {'fontsize': 20, 'scale_r': 0.9, 'alpha': 1, 'color': '#0BA1FF'},
                       'Offchain retired': {'fontsize': 18, 'scale_r': 0.9, 'alpha': 0.5, 'color': '#0BA1FF'},
                       'Onchain': {'fontsize': 16, 'scale_r': 0.9, 'alpha': 1, 'color': '#00CC33'},
                       'Onchain retired': {'fontsize': 12, 'scale_r': 0.9, 'alpha': 0.5, 'color': '#00CC33'},
                       }


def create_holders_fig(data, style_dict):

    circles = circlify.circlify(
        data,
        show_enclosure=False,
        target_enclosure=circlify.Circle(x=0, y=0, r=1)
    )

    fig, ax = plt.subplots(figsize=(14, 14), facecolor='#202020')

    # Title
    # ax.set_title('Repartition of the world population', color='white')

    # Remove axes
    ax.axis('off')

    # Find axis boundaries
    lim = max(
        max(
            abs(circle.x) + circle.r,
            abs(circle.y) + circle.r,
        )
        for circle in circles
    )
    plt.xlim(-lim, lim)
    plt.ylim(-lim, lim)

    # Print circle the highest level (continents):
    for circle in circles:
        if circle.level != 2:
            continue
        x, y, r = circle
        label = circle.ex["id"]
        ax.add_patch(plt.Circle((x, y), r*style_dict[label]['scale_r'], alpha=style_dict[label]['alpha'],
                                linewidth=2, color=style_dict[label]['color']))
        plt.annotate(label, (x, y), ha='center', color="white",
                     fontsize=style_dict[label]['fontsize'], weight='bold')

    plt.savefig('src/apps/tco2_dashboard/assets/holders.svg',
                format='svg', dpi=1200)


def create_offchain_vs_onchain_fig(data, style_dict, year):

    circles = circlify.circlify(
        data,
        show_enclosure=False,
        target_enclosure=circlify.Circle(x=0, y=0, r=1)
    )

    fig, ax = plt.subplots(figsize=(14, 14), facecolor='#202020')

    # Title
    # ax.set_title('Repartition of the world population', color='white')

    # Remove axes
    ax.axis('off')

    # Find axis boundaries
    lim = max(
        max(
            abs(circle.x) + circle.r,
            abs(circle.y) + circle.r,
        )
        for circle in circles
    )
    plt.xlim(-lim, lim)
    plt.ylim(-lim, lim)

    # Print circle the highest level (continents):
    for circle in circles:
        if circle.level != 2:
            continue
        x, y, r = circle
        label = circle.ex["id"]
        ax.add_patch(plt.Circle((x, y), r*style_dict[label]['scale_r'], alpha=style_dict[label]['alpha'],
                                linewidth=2, color=style_dict[label]['color']))
        label_value = str(circle.ex["datum"])
        plt.annotate(label, (x, y), ha='center', color="white",
                     fontsize=style_dict[label]['fontsize'], weight='bold') 
        y = y - r*0.15
        plt.annotate(label_value, (x, y), ha='center', color="white",
                     fontsize=style_dict[label]['fontsize'], weight='medium')

    plt.savefig(f'src/apps/tco2_dashboard/assets/offchain_vs_onchain_{year}.svg',
                format='svg', dpi=1200)


create_holders_fig(data, style_dict)
create_offchain_vs_onchain_fig(data2020, style_dict_offchain, 2020)

off_vs_on_figs = {'2019': {'fig': create_offchain_vs_onchain_fig(data2019, style_dict_offchain, 2019)},
                  '2020': {'fig': create_offchain_vs_onchain_fig(data2020, style_dict_offchain, 2020)}}


app.layout = html.Div([
    dbc.Row(html.A([html.Img(src='assets/holders.svg',
                             style={'height': '400px', 'width': '600px%'})])),
    dbc.Row([html.A(id='output'),
             dcc.Slider(min=2019, max=2020, step=1,
                        value=2019,
                        id='year-slider')])
])

[html.Img(src='assets/offchain_vs_onchain.svg',
          style={'height': '400px', 'width': '600px%'})]


@app.callback(
    Output('output', 'children'),
    Input('year-slider', 'value'))
def update_output(value):
    return [html.Img(src=f'assets/offchain_vs_onchain_{str(value)}.svg',
                     style={'height': '400px', 'width': '600px%'})]


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')
