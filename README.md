# core-mem-dashboard

Provides a dashboard in a browser to interact with the core memory SPI slave using an
FTDI 2232H breakout board. 

The dashboard is created with dash, and FTDI control is done via PyFtdi. 

## Custom Svg dash component

The `svg-component` directory contains a fairly simply custom dash component which allows an SVG file to be inlined into the DOM, while applying a certain classes to certain elements in the SVG based on their IDs. What I wanted was to be able to create an SVG diagram representing the array, with each element identified -- e.g. Core_00 for the core at the top left corner -- so that I could adjust the display with CSS selectors. This turned out to be a bit more complex than I'd hoped, but it works well enough this way. 

The svg component can be build and installed by running this in the `svg-component` directory:

`npm run build && python setup.py sdist && pip install dist/svg-0.0.1.tar.gz`

## Running the app

`python main.py`

## Notes

I think dash is great, but after trying it out I think it's philosophy is not symphathetic with an embedded device dashboard app. It generally assumes there's no state in the server, so that multiple user sessions can run concurrently, and perhaps even load-balanced amongst back-end instances. You can't run this applicaiton in debug mode, or the hot-reloading will constantly be trying to re-create the FTDI driver. I've made this application work, with the only big compromise being the lack of hot-reloading. However, I don't think there's any mechanism for pushing updates to the client, and in the general embedded device dashboard use-case I need support for events originating from python (e.g. because they originate from the device). 
