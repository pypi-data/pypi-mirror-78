# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class DateTimePicker(Component):
    """A DateTimePicker component.


Keyword arguments:
- id (string; optional)
- value (string; optional)
- style (dict; optional)
- timezone (string; optional)"""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, value=Component.UNDEFINED, style=Component.UNDEFINED, timezone=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'value', 'style', 'timezone']
        self._type = 'DateTimePicker'
        self._namespace = 'dash_cool_components'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'value', 'style', 'timezone']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(DateTimePicker, self).__init__(**args)
