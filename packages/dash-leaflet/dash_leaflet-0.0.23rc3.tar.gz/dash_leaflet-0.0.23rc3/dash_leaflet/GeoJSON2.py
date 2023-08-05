# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class GeoJSON2(Component):
    """A GeoJSON2 component.
LayerGroup is a wrapper of LayerGroup in react-leaflet.
It takes similar properties to its react-leaflet counterpart.

Keyword arguments:
- children (a list of or a singular dash component, string or number; optional): Children
- data (dict | string; optional): Data (consider using url for better performance).
- url (string; optional): Url to data (use instead of data for better performance).
- format (a value equal to: "geojson", "geobuf"; default "geojson"): Data format.
- options (dict; optional): Options for the GeoJSON object (see https://leafletjs.com/reference-1.6.0.html#geojson-option for details).
- hoverStyle (string; optional): Style function applied on hover.
- id (string; optional): The ID used to identify this component in Dash callbacks
- n_clicks (number; default 0): Dash callback property. Number of times the object has been clicked.
- featureClick (dict; optional): Last feature clicked.
- featureClickBounds (dict; optional): Bounds of last feature clicked.
- featureHover (dict; optional): Last feature hovered.
- featureHoverBounds (dict; optional): Bounds of last feature hovered."""
    @_explicitize_args
    def __init__(self, children=None, data=Component.UNDEFINED, url=Component.UNDEFINED, format=Component.UNDEFINED, options=Component.UNDEFINED, hoverStyle=Component.UNDEFINED, id=Component.UNDEFINED, n_clicks=Component.UNDEFINED, featureClick=Component.UNDEFINED, featureClickBounds=Component.UNDEFINED, featureHover=Component.UNDEFINED, featureHoverBounds=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'data', 'url', 'format', 'options', 'hoverStyle', 'id', 'n_clicks', 'featureClick', 'featureClickBounds', 'featureHover', 'featureHoverBounds']
        self._type = 'GeoJSON2'
        self._namespace = 'dash_leaflet'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'data', 'url', 'format', 'options', 'hoverStyle', 'id', 'n_clicks', 'featureClick', 'featureClickBounds', 'featureHover', 'featureHoverBounds']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(GeoJSON2, self).__init__(children=children, **args)
