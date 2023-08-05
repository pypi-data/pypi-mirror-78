# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class FileExplorer(Component):
    """A FileExplorer component.
ExampleComponent is an example component.
It takes a property, `label`, and
displays it.
It renders an input with the property `value`
which is editable by the user.

Keyword arguments:
- id (string; optional): The ID used to identify this component in Dash callbacks.
- selectedPath (string; optional): A selectedPath that will be printed when this component is rendered.
- value (list; optional): The value displayed in the input."""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, selectedPath=Component.UNDEFINED, value=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'selectedPath', 'value']
        self._type = 'FileExplorer'
        self._namespace = 'dash_cool_components'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'selectedPath', 'value']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(FileExplorer, self).__init__(**args)
