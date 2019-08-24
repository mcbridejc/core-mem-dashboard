import click
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_dangerously_set_inner_html
from dash.dependencies import Input, Output, State
import itertools
import flask
import random
from svg import Svg
import os 
import time

from driver import CoreMemDriver
from mockdriver import MockCoreMemDriver


memory_content = [0] * 8


def svg_data():
    with open('array_diagram.svg') as f:
        data = f.read().splitlines(True)
    # Drop the first line, containing the <? xml...?> header
    return "".join(data[1:])

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

def location_to_bit(row, col):
    """Convert the location of a core in the array to and word and bit offset
    """
    assert(row < 8 and col < 8)
    bit = int(row / 2 + int(col / 4) * 4)
    # Tables define which XSEL line drives each physical row/col
    XROWS = [0, 1, 1, 0, 0, 1, 1, 0]
    YCOLS = [0, 3, 1, 2, 2, 1, 3, 0]
    
    addr = XROWS[row] + (YCOLS[col]<<1)
    return addr, bit

def get_class_map(highlight_addr=None):
    classMap = {}
    for row, col in itertools.product(range(8), repeat=2):
        addr, bit = location_to_bit(row, col)
        className = ''
        if memory_content[addr] & (1<<bit):
            className = 'active'
        classMap['core_%d%d' % (row, col)] = className
    
    for y in range(4): 
        classMap['Y%d' % y] = ''

    for x in range(2):
        classMap['X%d' % x] = ''

    if highlight_addr is not None:
        xsel = highlight_addr & (1<<0)
        ysel = highlight_addr >> 1
        classMap['Y%d' % ysel] = 'active'
        classMap['X%d' % xsel] = 'active'

    return classMap

app = dash.Dash("Core Mem")

app.layout = html.Div([
    html.H1('Magnetic Core Memory Dashboard'),
    html.Div([
        html.Div([
            Svg(id='diagram', value=svg_data(), classMap=get_class_map())
        ], className='box diagram-box'),
        html.Div([memory_value_table()], id='mem-table-div', className='box mem-table-box'),
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
            html.Button('Read', id='readButton'),
        ], className='box read-box'),
        html.Fieldset([
            html.Legend('Digital Pot Control'),
            html.Div([
                "VDRIVE: ",
                dcc.Slider(id='vdriveInput', value=1000, updatemode='drag', min=0, max=30000),
                html.Span(id='vdriveDisplay'),
            ]),
            html.Div([
                "VTHRESH: ",
                dcc.Slider(id='vthreshInput', value=0, updatemode='drag', min=0, max=20000),
                html.Span(id='vthreshDisplay'),
            ]),
            html.Button('Write pot settings', id='writePotButton'),
            html.Button('Read', id='readPotButton'),
        ], className='box pot-box'),
        html.Fieldset([
            html.Legend('Sense Delay'),
            html.Div([
                "Sense Delay: ",
                dcc.Input(id='senseDelayInput', value=0, min=0, max=255, type='number', placeholder='SENSE DELAY'),
                html.Span(id='senseDelayDisplay')
            ]),
            html.Button('Write Sense Delay', id='writeSenseDelayButton'),
            html.Button('Read', id='readSenseDelayButton'),
        ], className='box sense-delay-box'),

    ], className='wrapper'),
    html.P("", id="dummy"),
    html.Div(id='read-signal', style={'display': 'none'}),
    
    #html.Div(id='my-div')
], id='layout')

@app.callback(
    Output(component_id='diagram', component_property='classMap'),
    [
        Input(component_id='addrInput', component_property='value'), 
        Input(component_id='read-signal', component_property='children')
    ]
)
def diagram_update(address, signal):
    try:
        return get_class_map(int(address))
    except TypeError:
        return get_class_map()

@app.callback(
    Output(component_id='writeButton', component_property='value'),
    [Input(component_id='writeButton', component_property='n_clicks')],
    [
        State(component_id='addrInput', component_property='value'),
        State(component_id='wrValInput', component_property='value'),
    ]
)
def writeMemCallback(n_clicks, addr, val):
    spi_driver.mem_write(int(addr), int(val))
    return ""

@app.callback(
    [
        Output(component_id='readButton', component_property='value'),
        Output(component_id='mem-table-div', component_property='children'),
        Output(component_id='read-signal', component_property='children'),
    ],
    [Input(component_id='readButton', component_property='n_clicks')],
    [State(component_id='addrInput', component_property='value')]
)
def readMemCallback(n_clicks, addr):
    for addr in range(8):
        #memory_content[addr] = random.randint(0, 255)# TODO: read value
        read_value = spi_driver.mem_read(addr)
        print("Read %x" % read_value)
        memory_content[addr] = read_value
    return "", memory_value_table(), ""

@app.callback(
    Output(component_id='vdriveDisplay', component_property='children'),
    [Input(component_id='vdriveInput', component_property='value')]
)
def vdriveChangeCallback(input_value):
    val = int(input_value)
    volts = 1.25 * (1 + val / 4.7e3)
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
    try:
        val = int(input_value)
        delay_us = CLK_PERIOD_US * val
        return "%.2fus" % (delay_us)
    except TypeError:
        return ""

@app.callback(
    Output(component_id='writeSenseDelayButton', component_property='value'),
    [Input(component_id='senseDelayInput', component_property='value')]
)
def writeSenseDelay(value):
    spi_driver.set_sensedelay(int(value))

@app.callback(
    Output(component_id='senseDelayInput', component_property='value'),
    [Input(component_id='readSenseDelayButton', component_property='n_clicks')]
)
def readSenseDelay(n_clicks):
    value = spi_driver.read_sensedelay()
    return value

@app.callback(
    [
        Output(component_id='vthreshInput', component_property='value'),
        Output(component_id='vdriveInput', component_property='value'),
    ],
    [Input(component_id='readPotButton', component_property='n_clicks')]
)
def readPot(n_clicks):
    vdrive = spi_driver.read_vdrive()
    vthresh = spi_driver.read_vthresh()
    return vthresh, vdrive

def run_server(driver):
    global spi_driver
    spi_driver = driver
    app.run_server(debug=False)

