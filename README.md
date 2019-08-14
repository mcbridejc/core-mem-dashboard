# core-mem-dashboard

Provides a dashboard in a browser to interact with the core memory SPI slave using an
FTDI 2232H breakout board. 

The dashboard is created with dash, and FTDI control is done via PyFtdi. 

## Custom Svg dash component

The `svg-component` directory contains a fairly simply custom dash component which allows an SVG file to be inlined into the DOM, while applying a certain classes to certain elements in the SVG based on their IDs. What I wanted was to be able to create an SVG diagram representing the array, with each element identified -- e.g. Core_00 for the core at the top left corner -- so that I could adjust the display with CSS selectors. This turned out to be a bit more complex than I'd hoped, but it works well enough this way. 

The svg component can be build and installed by running this in the `svg-component` directory:

`npm run build && python setup.py sdist && pip install dist/svg-0.0.1.tar.gz`

## Running the app

`python app.py`
