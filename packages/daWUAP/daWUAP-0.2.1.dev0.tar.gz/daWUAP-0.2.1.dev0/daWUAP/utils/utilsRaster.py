'''
Contents
--------
RasterDataset
ModelRasterDatasetHBV
'''

from __future__ import division
import rasterio as rio
import numpy as np
import json

class RasterDataset(object):
    """
    Base class to read raster datasets, retrieve and keep metadata, and write
    GeoTIFFs.
    """
    def __init__(
            self, fn_base_raster: str, band: int = None,
            masked: bool = False):
        self.fn_base_raster = fn_base_raster
        # Profile and shape are updated with call to _read_base_raster()
        self.profile = None
        self.shape = None
        self.affine = None
        self.nodata = -9999
        self.array = None
        self._read_base_raster(band, masked=masked)

    def _read_base_raster(self, band: int, masked: bool = False):
        'Read in a raster that serves as a template (base) for new rasters'
        with rio.open(self.fn_base_raster, 'r') as src:
            self.profile = src.profile
            self.shape = src.shape
            self.transform = src.transform
            if src.nodata is not None:
                self.nodata = int(src.nodata)

            self.array = src.read(band, masked=masked)
            no_data_mask = self.array == src.nodata
            scale = (np.ones_like(self.array).T * np.array(src.scales)).T
            offset = (np.ones_like(self.array).T * np.array(src.offsets)).T
            self.array = \
                self.array * scale + offset
                #self.array * np.array(src.scales)[:, np.newaxis, np.newaxis] + np.array(src.offsets)[:, np.newaxis, np.newaxis]
            self.array[no_data_mask] = self.nodata

    def _write_to_geotiff(self, fn_out: str, array: np.ndarray):
        """
        Writes numpy arrays as tiff file using metadata from a template GeoTiff map.

        Parameters
        ----------
        fn_out : str
            Path to output raster file
        array : numpy.ndarray
            Array to be written to output GeoTIFF
        """
        if not isinstance(array, np.ndarray) or array.shape != self.shape:
            raise ValueError("Shape mismatch!. Template shape is %s. Arrays shape is %s" % (src.shape, array.shape))
        self.profile.update(driver='GTiff', count=1, dtype='float64')
        try:
            with rio.open(fn_out, 'w', **self.profile) as dst:
                dst.write(array.astype('float64'), 1)
        except IOError as e:
            raise e

    def clone_raster(self, fn_out: str, array: np.ndarray):
        '''
        Based on a source raster, write an array to a GeoTIFF file with
        similar characteristics.

        Parameters
        ----------
        fn_out : str
            Path to output raster file
        array : numpy.ndarray
            Array to write to the raster file
        '''
        self._write_to_geotiff(fn_out, array)

    def update_raster(self, fn_new_raster: str, band: int = None):
        """
        Updates the array of an existing Raster object with the array of
        fn_new_raster. The shape of the file pointed to by fn_new_raster needs
        to be identical to the existing raster.

        Parameters
        ----------
        fn_new_raster : str
            Filename of the new raster file to update existing raster
        band : int
            Band of fn_new_raster to use for the update
        """
        try:
            with rio.open(fn_new_raster, 'r') as src:
                shape = src.shape
                nodata = int(src.nodata)
                array = src.read(band)
        except IOError as e:
            raise e

        if shape != self.shape:
            raise ValueError("Shape mismatch!. Template shape is %s. Arrays shape is %s" % (src.shape, array.shape))

        self.array = array
        self.nodata = int(nodata)


class ModelRasterDatasetHBV(object):

    def __init__(
            self, fn_base_raster: str, fn_temp_thresh: str = None,
            fn_ddf: str = None, fn_soil_max_water: str = None,
            fn_soil_beta: str = None, fn_aet_lp_param: str = None):
        """
        Initializes a class to write raster parameters for the HBV model. A
        base map, typically a climate input map, is required to obtain the
        geometry of the domain. Optional parameter maps can be used to
        initialize the object to specified parameter values. If the maps do
        not exist it initializes the maps with a default value.

        Parameters
        ----------
        fn_base_map : str
            Filename to map to obtain the geometry and projection of the domain
        fn_temp_thresh : str
            Filename to map with snow-rain temperature threshold
        fn_ddf : str
            Filename to map with degree-day factor
        fn_soil_max_water : str
            Filename to map with soil maximum storage parameter
        fn_soil_beta : str
            Filename to map with...
        fn_aet_lp_param : str
            Filename...

        Methods
        -------
        write_parameter_input_file
            Writes a JSON dictionary with values pointing to input parameter
            file paths
        write_parameter_to_geotiff
            Writes a parameter value (constant) or array to an output GeoTIFF
        """
        self.fn_base_raster = fn_base_raster
        self.fn_temp_thresh = fn_temp_thresh
        self.fn_ddf = fn_ddf
        self.fn_soil_max_water = fn_soil_max_water
        self.fn_soil_beta = fn_soil_beta
        self.fn_aet_lp_param = fn_aet_lp_param

    def write_parameter_to_geotiff(self, fn_out: str, value):
        '''
        Write an array to an output GeoTIFF with the input value(s); will
        attempt to broadcast the value(s) to a grid of the reference raster
        shape. A common application is that users have a single, constant
        value for a parameter that otherwise is spatially varying. This method
        creates a GeoTIFF, based on the input dataset's shape, with that
        constant value.

        Parameters
        ----------
        fn_out : str
            Path for output raster file
        value : float or int or numpy.ndarray
            Value(s) to be written to GeoTIFF
        '''
        base = RasterDataset(self.fn_base_raster)
        shp = base.shape[:2] # Guard against too many axes
        if hasattr(value, 'dim') and hasattr(value, 'shape'):
            assert value.shape == shp,\
            'Vector-valued "value" must have the same shape as the base raster'
        base.clone_raster(fn_out, np.multiply(np.ones(shp), value))

    def write_parameter_input_file(self, fn_out: str):
        '''
        Writes a JSON dictionary with the parameter name keys and the path to files
        holding the parameter map. This file is needed to run the hydrovehicle.

        Parameters
        ----------
        fn_out : str
            Filename to write the json dictionary
        '''
        self.filenamedic = {
            'pp_temp_thresh': self.fn_temp_thresh,
            'ddf': self.fn_ddf,
            'soil_max_water': self.fn_soil_max_water,
            'soil_beta': self.fn_soil_beta,
            'aet_lp_param': self.fn_aet_lp_param
        }
        with open(fn_out, 'w') as src:
            json.dump(self.filenamedic, src)
