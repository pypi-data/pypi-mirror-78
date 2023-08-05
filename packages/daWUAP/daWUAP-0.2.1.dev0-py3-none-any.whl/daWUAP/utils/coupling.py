import datetime
import json
import logging
import os
import numpy as np
import pandas as pd
from dateutil import parser
from rasterio.features import rasterize
from daWUAP import econengine as econ
from daWUAP import utils
from daWUAP.assimilation import kalmanfilter
from daWUAP.utils.crop_coefficient import retrieve_crop_coefficient

__all__ = ['HydroEconCoupling', 'StrawFarmCoupling']

class StrawFarmCoupling(object):
    '''
    '''
    def __init__(self, size=1):
        self.size = size

    @staticmethod
    def retrieve_supplemental_irrigation_map(*args):
        return np.zeros((1,))

    def retrieve_water_diversion_per_node(self, *args):
        return np.zeros((self.size,)), \
               np.zeros((self.size,)),\
               np.zeros((self.size,))


class HydroEconCoupling(object):
    """
    Couples the hydrologic and economic models.
    """
    def __init__(self, routing_obj, water_users_lst, precip_arr, transform):
        self.nodes = routing_obj
        self.water_users = water_users_lst
        self.farms_table = self._build_water_user_matrix()
        self.farm_idx = np.where(self.farms_table)
        self.water_user_mask = np.zeros_like(precip_arr)
        self.transform = transform

    @staticmethod
    def apply_to_all_members(sequence, attrib, *args, **kwargs):
        """
        Returns a list with the results of applying attrib to a sequence
        of objects. Parameter attrib is a string with the method name and
        can be an attribute obj.attrib or a method obj.attrib(*args, **kwargs)
        """

        lst = []
        for obj in sequence:
            try:
                lst.append(getattr(obj, attrib)(*args, **kwargs))
            except TypeError:
                lst.append(getattr(obj, attrib))

        return lst

    def setup_farmer_user(
            self, water_user_shapes: str, id_field: str, **kwargs):
        """
        Sets the spatial location of farm water users. It takes a shape or
        GeoJSON polygon file with an id field to provide geographical context
        to water users.

        Parameters
        ----------
        water_user_shapes : str
            Shapefile or GeoJSON filename
        id_field : str
            Name of field in 'water_user_sapes' with farm integer farm IDs

        Returns
        -------
        HydroEconCoupling
        """
        self.water_user_mask = self._rasterize_water_user_polygons(
            water_user_shapes, id_field, **kwargs)
        return self

    def _build_water_user_matrix(self):
        """
        Returns a pandas.DataFrame in which the index are nodes in the network
        and columns are farm id's. Non-zero entries are Farm objects that
        divert water from the node indicated by the index. The function loops
        through nodes in the network, find farms diverting from it and construct
        a matrix of farms associated to each node.
        """
        nodes = []
        idx = [0]
        col_farm_id = ['node_id']

        for ids in self.nodes.conn.index:
            li = [ids]
            for i, farm in enumerate(self.water_users):
                if int(farm.get('source_id')) == ids:
                    li.append(econ.Farm(**farm))
                    col_farm_id.append(farm.get('id'))
                    idx.append(i+1) # Add one because first column of col_farm_id is ids
                else:
                    li.append(0)
            nodes.append(li)
        arr_nodes = np.array(nodes)
        nodes = np.take(arr_nodes, idx, axis=1)
        dfNodes = pd.DataFrame(nodes, index=arr_nodes[:, 0], columns=col_farm_id)
        dfNodes.set_index('node_id', inplace=True)

        return dfNodes

    def simulate_all_users(self, lst_scenarios: list, path_kf_info: str = None):
        '''
        '''
        for obs in lst_scenarios:
            for farm in self.farms_table.values[self.farm_idx]:
                if obs.get("farm_id") == farm.id:
                    if path_kf_info is None:
                        print("Simulating farm id %i with name %s using standard PMP" % (farm.id, farm.name))
                        farm.simulate(**obs)
                    if isinstance(path_kf_info, str):
                        print("Simulating farm id %s with name %s using stochastic PMP" % (str(farm.id), farm.name))
                        kf = kalmanfilter.KalmanFilter(
                            farm, fn_info_file = os.path.join(
                                path_kf_info, str(farm.id) + '_kf_info.json'))
                        kf.simulate(
                            obs, fn_write_ensemble_states = os.path.join(
                                path_kf_info, str(farm.id) + '_simul_ensemble.h5'))

        return FarmCoupling(
            self.water_users, self.farms_table, self.farm_idx,
            self.water_user_mask, self.transform)

    def _rasterize_water_user_polygons(
            self, fn_water_user_shapes: str, property_field_name: str,
            **kwargs):
        """
        Returns a 2D array with rows and cols shape like precipitation inputs
        and vector features pointed by `fn_water_user_shapes` burned in.
        Burn-in values are these provided by `property_field_name`. The
        function also updates self.array_supplemental_irrigation with the
        returned array.
        """
        fill = kwargs.get('fill_value', 0)
        shapes = utils.VectorParameterIO(fn_water_user_shapes).read_features()
        try:
            feats = ((g['geometry'], int(g['properties'][property_field_name])) for g in shapes)
        except KeyError as e:
            print("field name %s does not exist in water user polygon file" %str(property_field_name))
            print(e)
            exit(-1)
        t = self.water_user_mask = rasterize(
            feats, self.water_user_mask.shape, fill = fill,
            transform = self.transform)
        return t


class FarmCoupling(object):
    '''
    '''
    def __init__(
            self, water_users_lst, farm_table, farm_idx, water_user_mask,
            transform):
        self.water_users = water_users_lst
        self.farms_table = farm_table
        self.farm_idx = farm_idx
        self.water_user_mask = water_user_mask
        self.applied_water_factor = np.zeros_like(self.farms_table.values)
        self.array_supplemental_irrigation = np.zeros_like(self.water_user_mask)
        # TODO: make this function initialize self.applied_water_factor as a pandas object
        self._calculate_applied_water_factor()
        self.transform = transform
        self.cell_area = self._area_lat_long()

    def _area_lat_long(self):
        """
        Returns a a 2D array with cell areas of water_user_mask map calculated
        in hectares.
        """
        lon, lat = self.transform * np.indices(self.water_user_mask.shape)[[1,0],:,:]
        r = 6371 # km, authalic radius of earth
        A = np.pi * r**2 / 180 * \
            np.abs(np.sin(lat * np.pi / 180) - np.sin((lat + self.transform.a) * np.pi / 180)) * \
            np.abs(lon - lon + self.transform.a)
        return A * 100  # km2 to ha

    def retrieve_water_diversion_per_node(self, date):
        """
        Returns a vector and two matrices with the following information:

            - vector ``num_nodes``: total daily water volume (m3/day) diverted
                from each of the n nodes from all users
            - matrix ``num_nodes x num_water_users`` daily water volume
                (m3/day) diverted from node n for user m
            - matrix ``num_nodes x num_water_users`` daily water rate (mm/day)
                diverted from node n for user m

        Parameters
        ----------
        date : str
            Date for which the diversions are required are required

        Returns
        -------
        tuple
            Tuple of (n,), (n,m), (n,m) vectors
        """

        # Obtain vector of crop coefficients
        vect_retrieve_kcs = np.vectorize(retrieve_crop_coefficient, excluded=['current_date'])

        # Obtains water simulated per crop
        s = HydroEconCoupling.apply_to_all_members(self.farms_table.values[self.farm_idx], "crop_start_date")
        c = HydroEconCoupling.apply_to_all_members(self.farms_table.values[self.farm_idx], "crop_cover_date")
        e = HydroEconCoupling.apply_to_all_members(self.farms_table.values[self.farm_idx], "crop_end_date")
        cropid = HydroEconCoupling.apply_to_all_members(self.farms_table.values[self.farm_idx], "crop_id")

        current_kcs = vect_retrieve_kcs(date, s, c, e, cropid)

        # Obtain water simulated per crop in dekasteres (10 cubic meteres)
        Xw = np.vstack(
            HydroEconCoupling.apply_to_all_members(
                self.farms_table.values[self.farm_idx], "watersim"
            )
        )

        Xlnd = np.vstack(
            HydroEconCoupling.apply_to_all_members(
                self.farms_table.values[self.farm_idx], "landsim"
            )
        )

        irr_eff = np.vstack(
            HydroEconCoupling.apply_to_all_members(
                self.farms_table.values[self.farm_idx], "irr_eff"
            )
        )

        # Obtain applied water factor
        f = np.vstack(self.applied_water_factor[self.farm_idx])

        # Transforms volume of plant water use into diversion rate by
        #   dividing by land, irrigation efficiency and applied water factor
        np.divide(Xw, Xlnd, where=f != 0, out=Xw)
        np.divide(Xw, irr_eff, where=f != 0, out=Xw)
        Xw = np.divide(Xw*current_kcs, f, where=f != 0, out=np.zeros_like(current_kcs))

        # Conversion factor to transform dekastere (10,000 liters or 10 m3)
        #   to cubic meter
        Xw_vol = Xw * Xlnd * 10.0

        # Calculated water diverted for each crop and farm
        # Water volume diversions per per farm, crop and node (m3/day)
        dvol = Xw_vol
        Dvol = self.farms_table.copy()
        Dvol.values[self.farm_idx] = tuple(dvol)

        # Water volume diversions per per farm, crop and node (mm/day)
        drate = Xw # mm/day
        Drate = self.farms_table.copy()
        Drate.values[self.farm_idx] = tuple(drate)

        # Total diversions per node
        # First sum all water diverted per crop in each farm
        dtot = [fm.sum() for fm in dvol]
        Dtot = self.farms_table.copy()
        Dtot.values[self.farm_idx] = dtot
        #Dtot = np.vstack((Dtot.values[:, 0], Dtot.values[:, 1:].sum(axis=1)))
        return Dtot.sum(axis=1), Dvol, Drate

    def retrieve_supplemental_irrigation_map(
            self, array_land_use: np.ndarray, irr_ag_ids: tuple,
            water_diversion_table: pd.DataFrame):
        """
        Returns an array with the supplemental irrigation rate on pixels in
        array ``array_land_use`` with id ``irr_ag_ids`` resulting from
        spreading evenly in space water rates diverted by water users as
        provided in ``water_diversion_table``

        Parameters
        ----------
        array_land_use : numpy.ndarray
            Array with land use codes
        irr_ag_ids : tuple
            Tuple with land use codes associated with irrigated ag
        water_diversion_table : pandas.DataFrame
            Table with water diversions in mm*ha/day (decastere/day)
        """

        if isinstance(array_land_use, np.ndarray):
            lu = array_land_use
        elif isinstance(array_land_use, str):
            lu = utils.RasterParameterIO(array_land_use).array

        else:
            raise TypeError('Incorrect type for argument array_land_use')

        if lu.shape != self.water_user_mask.shape:
            raise ValueError("Land user rasters do not line up with shapes: " +
                             str(lu.shape) + str(self.water_user_mask.shape))

        gen = (x for x in self.water_users if x.get('id') in water_diversion_table.columns)
        for i, farm in enumerate(gen):
            farm_id = int(farm.get('id'))
            ag_mask = np.isin(lu, irr_ag_ids) & (self.water_user_mask == farm_id)
            m = np.count_nonzero(ag_mask)
            area_ag = self.cell_area[ag_mask].sum()
            applied_water = np.apply_along_axis(np.sum, 0, water_diversion_table.values[:, i]).sum()

            if m == 0:
                logging.warning(
                    "WARNING: Water user with id %i is irrigating but water user mask does not contain irrigated pixels" % farm_id)

            self.array_supplemental_irrigation = np.where(
                np.isin(lu, irr_ag_ids) & (self.water_user_mask == farm_id),
                applied_water / area_ag if m > 0 else 0.0, self.array_supplemental_irrigation)

        return self.array_supplemental_irrigation

    def _calculate_applied_water_factor(self):
        """
        Sets member variable ``applied_water_factor``, a masked matrix of
        arrays with the water diversion adjustment factors per crop and farm.
        The factor takes into account the irrigation efficient as well as the
        length of the crop period expressed as the accumulation of crop
        coefficients. The factor is defined as follows:

            ::

            f:= Sum_t(Kc_t) * Ieff

        The actual daily water diverted (D) to supply water for each crop can
        then be calculated as:

            ::

            D = Wtot_t * Kc_t / f

        Factor f and the subsequent calculation of D is calculated per crop. Thus, th function yields a
        vector per farm, with one f per crop.
        """
        Kcs = np.vectorize(retrieve_crop_coefficient)
        lst_kc = []
        for i, farm in enumerate(self.farms_table.values[self.farm_idx]):
            print("Calculating applied water factors for farm %s with name %s" % (str(farm.id), str(farm.name)))
            try:
                dates = zip(farm.crop_start_date,
                            farm.crop_cover_date,
                            farm.crop_end_date,
                            farm.crop_id,
                            farm.irr_eff,
                            farm.irr)
            except TypeError as e:
                print("Water User %s does not have information on crop planting dates. Did you forget to " \
                      "simulate a scenario?" % str(farm.name))
                exit(-1)

            lst = []
            for s, c, e, cropid, i_eff, i_mask, in dates:

                date_array = [(parser.parse(s) + datetime.timedelta(days=x)).strftime("%m/%d/%Y")
                              for x in range(0, (parser.parse(e) - parser.parse(s)).days + 1)]
                lst.append(
                      Kcs(date_array, s, c, e, cropid).sum() * i_eff * i_mask
                )
            lst_kc.append(np.array(lst))

        self.applied_water_factor[self.farm_idx] = lst_kc

    def save_farm_list_json(self, fname):
        """
        Saves dictionary of farms to disk with name fname.
        """
        res = [farm.write_farm_dict() for farm in self.farms_table.values[self.farm_idx]]
        d = {"farms": res}
        with open(fname, 'w') as json_out:
            json.dump(d, json_out)
