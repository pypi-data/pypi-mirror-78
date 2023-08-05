# -*- coding: utf-8 -*-
"""
Classes to manipulate vector datasets used in daWUAP. The VectorDataset base
class reads and writes fiona geometry objects. This class is inherited by the
other three classes in this module.

Contents
--------
VectorDataset
    Base class for classes that read and write vector data files
NetworkParser
    Parses a network vector file and represents a hydrology network
VectorParameterIO
    Class for updating sub-shed and network vector datasets
ModelVectorDatasets
    Class to write specific model parameters to vector datasets
"""

from __future__ import division
import itertools
import pandas as pd
import fiona
from shapely.geometry import mapping, shape
from daWUAP import NETWORK_ID, SUBSHED_ID

class VectorDataset(object):
    '''
    Base class to read vector datasets using Fiona. Reads and stores metadata
    from fiona objects, and facilitates the writing of vector files.
    '''

    def __init__(self, fn_vector):
        """
        The constructors requires a path to a file such as 'data/map_spain.shp'.
        An internal call to the private ``_read_fiona_object()`` method opens
        the file and populates the metadata variables.

        Parameters
        ----------
        fn_vector : str
            File path for the input vector dataset (e.g., "myfile.shp")
        """
        self.fn_vector = fn_vector
        # Next three variables are updated after the call to _read_fiona_object()
        self.crs = None
        self.schema = None
        self.driver = None
        self._read_fiona_object()

    def _read_fiona_object(self):
        """Returns an iterator over records in the vector file"""
        # test it as fiona data source
        features_iter = None
        try:
            with fiona.open(self.fn_vector, 'r') as src:
                assert len(src) > 0
                self.crs = src.crs
                self.schema = src.schema.copy()
                self.driver = src.driver

            def fiona_generator(obj):
                with fiona.open(obj, 'r') as src2:
                    for feature in src2:
                        yield feature

            features_iter = fiona_generator(self.fn_vector)

        except (AssertionError, TypeError, IOError, OSError):
            print("fn_vector does not point to a fiona object", error)

        return features_iter

    def _write_fiona_object(
            self, fn, crs = None, driver = None, schema = None, params = None):
        """
        Writes a vector file using the original input vector file as a
        template. TODO: Solve problem writing projection info in shp and geojson.
        Also overwriting geojson files.

        Parameters
        ----------
        fn : str
            Output file name
        crs : str
            Coordinate reference system code (EPSG code)
        driver : str
            Name of the file driver (e.g., "ESRI Shapefile", "GeoJSON")
        schema : str
            Schema for the output attribute table
        params : dict
        """
        if crs is None:
            crs = self.crs
        if driver is None:
            driver = self.driver
        if schema is None:
            schema = self.schema

        # TODO: solve problems writing projection information in shapefiles and geojson
        feature_iter = self._read_fiona_object()
        with fiona.open(fn, 'w', crs=crs, driver=driver, schema=schema) as sink:

            for i, feats in enumerate(feature_iter):
                geom = shape(feats['geometry'])
                if params is not None:
                    props = params[i]['properties']
                else:
                    props = feats['properties']
                sink.write({'properties': props, 'geometry': mapping(geom)})


class NetworkParser(VectorDataset):
    """
    Parses the model stream network. It calculates the connectivity matrix
    during the initialization and makes it available as a class variable.
    """

    def __init__(self, fn_vector):
        super(NetworkParser, self).__init__(fn_vector)
        self.conn_matrix = self._calc_connectivity_matrix()

    def _calc_connectivity_matrix(self):
        feature_iter = self._read_fiona_object()
        lst_node_connections = []
        for i, feats in enumerate(feature_iter):
            geom = shape(feats['geometry'])
            props = feats['properties']
            lst_node_connections.append((props["FROM_NODE"], props["TO_NODE"]))

        # Compare all unique node IDs to IDs of nodes flowing out;
        missing_nodes = set(itertools.chain(*lst_node_connections))\
            .difference((c[0] for c in lst_node_connections))\
            .difference((0,)) # "0" is the ID that signals no outflow
        if len(missing_nodes) > 0:
            raise ValueError('At least one node is flowing into a missing catchment; check ARCID(s): %s' % ', '.join(map(lambda x: str(x), missing_nodes)))

        lstNodes = sorted(set(list(zip(*lst_node_connections))[0]))
        df = pd.DataFrame(0, index=lstNodes, columns=lstNodes)
        # drop the connections that go out of the basin to node 0
        lst_node_connections = [i for i in lst_node_connections if i[1]>0]
        for link in lst_node_connections:
            df.loc[link] = 1

        return df

    def get_parameter(self, param):
        """
        Retrieves a list of values associated with the named parameter.

        Parameters
        ----------
        param : str
            Name of the parameter to retrieve

        Returns
        -------
        pandas.Series
            Series with parameter values. The key is the SUBSHED_ID in
            ascending order.
        """
        feature_iter = self._read_fiona_object()

        lst_param = []
        lst_ids = []

        for i, feats in enumerate(feature_iter):
            lst_param.append(
                feats['properties'][param]
            )
            lst_ids.append(
                feats['properties'][SUBSHED_ID]
            )

        return pd.Series(lst_param, index=lst_ids).sort_index()


class VectorParameterIO(VectorDataset):
    """
    Class to provide model parameter fields and values to network and basin
    vector datasets.
    """
    def __init__(self, fn_vector):
        """
        Initializes the object with a polygon (basin) or multiline (network)
        vector dataset.

        Parameters
        ----------
        fn_vector : str
            File path to vector dataset
        """
        super(VectorParameterIO, self).__init__(fn_vector)

    def read_features(self):
        """
        Return a generator of features in the dataset

        Returns
        -------
        generator
        """
        return self._read_fiona_object()

    def write_dataset(
            self, fn, crs = None, driver = None, schema = None,
            params = None):
        """
        Writes a vector file using fn_vector as template

        Parameters
        ----------
        fn : str
            Output file name
        crs : str
            Coordinate reference system code (EPSG code)
        driver : str
            Name of the file driver (e.g., "ESRI Shapefile", "GeoJSON")
        schema : str
            Schema for the output attribute table
        params : dict
        """
        return self._write_fiona_object(fn, crs, driver, schema, params)


class ModelVectorDatasets(object):
    """
    Class to handle the the manipulation of all vector dataset in the model.
    """
    def __init__(
            self, fn_network: str = None, fn_subsheds: str = None,
            verbose: bool = True):
        self._verbose = verbose
        self.network = None
        self.subsheds = None
        if fn_network is not None:
            self.network = VectorParameterIO(fn_network)
        if fn_subsheds is not None:
            self.subsheds = VectorParameterIO(fn_subsheds)

    def write_muskingum_parameters(self, outfn: str, params: list = None):
        """
        Adds or updates the vector network file with the Muskingum-Cunge
        parameters. If params is not provided, the dataset is updated with
        default parameter values.

        Parameters
        ----------
        outfn : str
            Filename for output, updated network vector file
        params : list
            List of parameter dictionaries, e.g.:
                [{'ARCID': ID, 'e': value, 'ks': value}, {...}, ...]
        """
        # Check if network dataset is present
        if self.network is None:
            return

        schema = self.network.schema.copy()
        schema['properties']['e'] = 'float'
        schema['properties']['ks'] = 'float'

        lstDicts = []
        feature_iter = self.network.read_features()
        for i, feats in enumerate(feature_iter):
            arc_id = feats['properties'][NETWORK_ID]
            if self._verbose:
                print("Processing reach feature id %i" % arc_id)
            try:
                val = next(item for item in params if item[NETWORK_ID] == arc_id)
            except:
                val = {}
            feats['properties']['e'] = val.get('e', 0.35)
            feats['properties']['ks'] = val.get('ks', 82400)
            lstDicts.append(feats)

        self.network.write_dataset(outfn, schema=schema, params=lstDicts)

    def write_hbv_parameters(self, outfn: str, params: list = None):
        """
        Adds or updates the vector file of model subwatersheds with the hbv RR model parameters.
        If params is not provided, the dataset is updatd with default parameter values

        Parameters
        ----------
        outfn : str
            Filename for updated vector network
        params: str
            List of parameter dictionaries with format []
        """
        if self.subsheds is None:
            return

        schema = self.subsheds.schema.copy()
        schema['properties']['hbv_ck0'] = 'float'
        schema['properties']['hbv_ck1'] = 'float'
        schema['properties']['hbv_ck2'] = 'float'
        schema['properties']['hbv_hl1'] = 'float'
        schema['properties']['hbv_perc'] = 'float'
        schema['properties']['hbv_pbase'] = 'int'

        lstDicts = []
        feature_iter = self.subsheds.read_features()
        for i, feats in enumerate(feature_iter):
            arc_id = feats['properties'][SUBSHED_ID]
            if self._verbose:
                print("Processing subwatershed feature id %i" %arc_id)
            try:
                val = next(item for item in params if item[SUBSHED_ID] == arc_id)
            except:
                val = {}

            feats['properties']['hbv_ck0'] = val.get('hbv_ck0', 10.)
            feats['properties']['hbv_ck1'] = val.get('hbv_ck1', 50.)
            feats['properties']['hbv_ck2'] = val.get('hbv_ck2', 10000)
            feats['properties']['hbv_hl1'] = val.get('hbv_hl1', 50)
            feats['properties']['hbv_perc'] = val.get('hbv_perc', 50)
            feats['properties']['hbv_pbase'] = val.get('hbv_pbase', 5)
            lstDicts.append(feats)

        self.subsheds.write_dataset(outfn, schema=schema, params=lstDicts)
