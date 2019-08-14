import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_dangerously_set_inner_html
from dash.dependencies import Input, Output, State
import flask
from svg import Svg
import os 
import time

def svg_data():
    with open('array_diagram.svg') as f:
        data = f.read().splitlines(True)
    # Drop the first line, containing the <? xml...?> header
    return "".join(data[1:])

memory_content = [0] * 8

def memory_value_table():
    return html.Table([
        html.Tbody(
            [ 
                html.Tr([
                    html.Th('Address'),
                    html.Th('Val (dec)'),
                    html.Th('Val (hex)')
                ])
            ] + [
                html.Tr([
                    html.Td('%d' % addr),
                    html.Td('%d' % val),
                    html.Td('0x%x' % val),
                ])
                for addr, val in enumerate(memory_content)
            ])
    ], id='mem-table')


app = dash.Dash("Core Mem")


classMap = {'core_00': 'active'}
app.layout = html.Div([
    html.H1('Magnetic Core Memory Dashboard'),
    html.Div([
        html.Div([
            Svg(id='diagram', value=svg_data(), classMap=classMap),
        ], className='box diagram-box'),
        html.Div([memory_value_table()], className='box mem-table-box'),
        html.Fieldset([
            html.Legend(['Write to Memory']),
            html.Span([
                'Addr: ',
                dcc.Input(id='addrInput', value='0', type='number', min=0, max=7, placeholder="Write Addr"),
            ]),
            html.Span([
                'Value: ',
                dcc.Input(id='wrValInput', value='0', type='number', min=0, max=255, placeholder="Value"),
            ]),
            html.Button('Write', id='writeButton'),
        ], className='box write-box'),
        html.Fieldset([
            html.Legend('Read memory'),
            html.Button('Read full array', id='readButton'),
        ], className='box read-box'),
        html.Fieldset([
            html.Legend('Digital Pot Control'),
            html.Div([
                "VDRIVE: ",
                dcc.Slider(id='vdriveInput', value=1000, updatemode='drag', min=1000, max=30000),
                html.Span(id='vdriveDisplay'),
            ]),
            html.Div([
                "VTHRESH: ",
                dcc.Slider(id='vthreshInput', value=0, updatemode='drag', min=0, max=20000),
                html.Span(id='vthreshDisplay'),
            ]),
            html.Button('Write pot settings', id='writePotButton'),
        ], className='box pot-box'),
        html.Fieldset([
            html.Legend('Sense Delay'),
            html.Div([
                "Sense Delay: ",
                dcc.Input(id='senseDelayInput', value=0, min=0, max=255, type='number', placeholder='SENSE DELAY'),
                html.Span(id='senseDelayDisplay')
            ]),
            html.Button('Write Sense Delay', id='writeSenseDelayButton'),
        ], className='box sense-delay-box'),

    ], className='wrapper'),
    html.P("", id="dummy"),
    
    #html.Div(id='my-div')
])

@app.callback(
    Output(component_id='diagram', component_property='classMap'),
    [Input(component_id='addrInput', component_property='value'), ]
)
def active_callback(input_value):
    ysel = int(input_value) >> 1
    xsel = int(input_value) & 1
    for y in range(4): 
        className = ''
        if y == ysel:
            className = 'active'
        classMap['Y%d' % y] = className

    for x in range(2):
        className = ''
        if x == xsel:
            className = 'active'
        
        classMap['X%d' % x] = className

    return classMap

@app.callback(
    Output(component_id='writeButton', component_property='value'),
    [Input(component_id='writeButton', component_property='n_clicks')],
    [
        State(component_id='addrInput', component_property='value'),
        State(component_id='wrValInput', component_property='value'),
    ]
)
def writeMemCallback(n_clicks, addr, val):
    time.sleep(2)
    return ""

@app.callback(
    Output(component_id='readButton', component_property='value'),
    [Input(component_id='readButton', component_property='n_clicks')]
)
def readMemCallback(n_clicks):
    time.sleep(2)
    return ""

@app.callback(
    Output(component_id='vdriveDisplay', component_property='children'),
    [Input(component_id='vdriveInput', component_property='value')]
)
def vdriveChangeCallback(input_value):
    val = int(input_value)
    volts = 1.21 * (10e3 + val) / val
    return "%.2fV (%d)" % (volts, val)

@app.callback(
    Output(component_id='vthreshDisplay', component_property='children'),
    [Input(component_id='vthreshInput', component_property='value')]
)
def vthreshChangeCallback(input_value):
    val = int(input_value)
    volts = 3.3 * val / 65356.
    return "%.3fV (%d)" % (volts, val)

@app.callback(
    Output(component_id='writePotButton', component_property='value'),
    [Input(component_id='writePotButton', component_property='n_clicks')],
    [
        State(component_id='vdriveInput', component_property='value'),
        State(component_id='vthreshInput', component_property='value')
    ]
)
def writePotCallback(n_clocks, vdrive, vthresh):
    # the for moment, we dont do anything, but make sure the UX is good
    # in terms of indicating when write is completed
    time.sleep(2)
    return ""

@app.callback(
    Output(component_id='senseDelayDisplay', component_property='children'),
    [Input(component_id='senseDelayInput', component_property='value')]
)
def senseDelayChangeCallback(input_value):
    CLK_PERIOD_US = 1e6 / 20e6
    val = int(input_value)
    delay_us = CLK_PERIOD_US * val
    return "%.2fus" % (delay_us)

if __name__ == '__main__':
    app.run_server(debug=True)

