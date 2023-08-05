# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class SuperCluster(Component):
    """A SuperCluster component.
LayerGroup is a wrapper of LayerGroup in react-leaflet.
It takes similar properties to its react-leaflet counterpart.

Keyword arguments:
- data (dict | string; optional): Data (consider using url for better performance).
- url (string; optional): Url to data (use instead of data for better performance).
- format (a value equal to: "geojson", "geobuf"; default "geojson"): Data format.
- zoomToBoundsOnClick (boolean; default True): If true, zoom on cluster click.
- spiderfyOnMaxZoom (boolean; default True): If true, marker that are not resolved at max zoom level will be spiderfied on click.
- spiderfyOptions (dict; default {
    spiderfyDistanceMultiplier: 1,
    spiderLegPolylineOptions: {weight: 1.5, color: '#222', opacity: 0.5},
}): Options passed to SuperCluster, https://github.com/mapbox/supercluster. spiderfyOptions has the following type: dict containing keys 'spiderfyDistanceMultiplier', 'spiderLegPolylineOptions'.
Those keys have the following types:
  - spiderfyDistanceMultiplier (number; optional)
  - spiderLegPolylineOptions (dict; optional)
- superclusterOptions (dict; optional): Options passed to SuperCluster, https://github.com/mapbox/supercluster.
- clusterOptions (dict; default {
    iconSize: 40,
    classNames: [
        {minCount: 0, className: "marker-cluster marker-cluster-small"},
        {minCount: 100, className: "marker-cluster marker-cluster-medium"},
        {minCount: 1000, className: "marker-cluster marker-cluster-large"},
    ]
}): Option for customization of the clusters. clusterOptions has the following type: dict containing keys 'iconSize', 'classNames'.
Those keys have the following types:
  - iconSize (number; optional)
  - classNames (dict; optional): classNames has the following type: list of dicts containing keys 'minCount', 'className'.
Those keys have the following types:
  - minCount (number; optional)
  - className (string; optional)
- id (string; optional): The ID used to identify this component in Dash callbacks
- n_clicks (number; default 0): Dash callback property. Number of times the marker has been clicked
- featureClick (dict; optional): Last feature clicked.
- featureHover (dict; optional): Last feature hover."""
    @_explicitize_args
    def __init__(self, data=Component.UNDEFINED, url=Component.UNDEFINED, format=Component.UNDEFINED, zoomToBoundsOnClick=Component.UNDEFINED, spiderfyOnMaxZoom=Component.UNDEFINED, spiderfyOptions=Component.UNDEFINED, superclusterOptions=Component.UNDEFINED, clusterOptions=Component.UNDEFINED, id=Component.UNDEFINED, n_clicks=Component.UNDEFINED, featureClick=Component.UNDEFINED, featureHover=Component.UNDEFINED, **kwargs):
        self._prop_names = ['data', 'url', 'format', 'zoomToBoundsOnClick', 'spiderfyOnMaxZoom', 'spiderfyOptions', 'superclusterOptions', 'clusterOptions', 'id', 'n_clicks', 'featureClick', 'featureHover']
        self._type = 'SuperCluster'
        self._namespace = 'dash_leaflet'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['data', 'url', 'format', 'zoomToBoundsOnClick', 'spiderfyOnMaxZoom', 'spiderfyOptions', 'superclusterOptions', 'clusterOptions', 'id', 'n_clicks', 'featureClick', 'featureHover']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(SuperCluster, self).__init__(**args)
