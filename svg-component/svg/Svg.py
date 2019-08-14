# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Svg(Component):
    """A Svg component.
ExampleComponent is an example component.
It takes a property, `label`, and
displays it.
It renders an input with the property `value`
which is editable by the user.

Keyword arguments:
- id (string; optional): The ID used to identify this component in Dash callbacks
- value (string; required): The value displayed in the input
- classMap (dict; required): A map of ids and the classes to be set on them for controlling
the inner svg element classes"""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, value=Component.REQUIRED, classMap=Component.REQUIRED, **kwargs):
        self._prop_names = ['id', 'value', 'classMap']
        self._type = 'Svg'
        self._namespace = 'svg'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'value', 'classMap']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in ['value', 'classMap']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Svg, self).__init__(**args)
