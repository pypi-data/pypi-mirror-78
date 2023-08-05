'''
Command-line interface for the copuled Hydrologic-Economica Analysis (HYENA)
model. Example use:
    $ hyena.py hydro 20120901 HydroParams/precip_F2012-09-01_T2013-08-31.nc\
        HydroParams/tempmin_F2012-09-01_T2013-08-31.nc\
        HydroParams/tempmax_F2012-09-01_T2013-08-31.nc param_files_test.json\
        rivers_with_params.shp subbasins_with_params.shp
'''

from __future__ import division
import datetime
import json
import logging
import os
import pickle
import numpy as np
import tqdm
import fire
from dateutil.parser import parse
from typing import Sequence
from daWUAP import hydroengine
from daWUAP import utils

class HydroEconModel(object):
    '''
    Represents a hydrologic model run, optionally coupled with the economic
    engine for agricultural production.
    '''
    def __init__(self):
        pass

    def _run(
            self, init_date: str, precip_file: str, tmin_file: str,
            tmax_file: str, params: dict, network_file: str, basin_file: str,
            farm_json: str = None, scenario_json: str = None,
            water_user_shapes: str = None, water_user_id: str = None,
            lu_raster: str = None, lu_irr_ids: Sequence = None,
            path_kf_info: str = None, econ_results_of: str = None,
            num_time_steps: int = None, restart: bool = False,
            restart_file: str = None, hydro_maps_of: str = None,
            hydro_ts_of: str = None, verbose: bool = True):
        '''
        Main hydrologic or hydro-economic model. Not intended to be called
        directly.
        '''
        hydro_maps_of = os.curdir if hydro_maps_of is None else hydro_maps_of
        hydro_ts_of = os.curdir if hydro_ts_of is None else hydro_ts_of
        restart_file = os.curdir if restart_file is None else restart_file
        pp = utils.RasterDataset(precip_file, masked = True)
        pp_affine = pp.transform
        pp_nodata = pp.nodata
        pp_data = pp.array.clip(min=0)

        tmin = utils.RasterDataset(tmin_file, masked = True)
        tmin_affine = tmin.transform
        tmin_nodata = tmin.nodata
        tmin_data = tmin.array
        tmin_data[tmin_data != tmin_nodata] -= 273.15

        tmax = utils.RasterDataset(tmax_file, masked = True)
        tmax_affine = tmax.transform
        tmax_nodata = tmax.nodata
        tmax_data = tmax.array
        tmax_data[tmax_data != tmax_nodata] -= 273.15

        hbv_pars = {}
        with open(params) as json_file:
            pars = json.load(json_file)
            for key, value in pars.items():
                hbv_pars[key] = utils.RasterDataset(value, 1).array

        # Create base raster as template to write tiff outputs
        # base_map = utils.RasterDataset()

        # Retrieve latitude of cells
        lon, lat = tmax_affine * np.indices(tmin_data[0, :, :].shape)[[1,0],:,:]

        # Retrieve adjacency matrix
        graph = utils.NetworkParser(network_file)
        adj_net = graph.conn_matrix
        num_links = len(adj_net.index)

        # Initiate hydrologic engine with empty storages
        swe = np.zeros_like(pp_data[0, :, :])
        pond = np.zeros_like(pp_data[0, :, :])
        sm = np.zeros_like(pp_data[0, :, :])
        soils = []
        Q = np.zeros(num_links)
        qold = np.zeros(num_links)

        # If restart flag on, initiate hydrologic engine and rewrite variables using pickled states from previous run
        if restart:
            try:
                swe = pickle.load(open(os.path.join(restart_file, 'swe.pickled'), 'rb'))
                # swe = np.zeros_like(pp_data[0, :, :])
                pond = pickle.load(open(os.path.join(restart_file, 'pond.pickled'), 'rb'))
                sm = pickle.load(open(os.path.join(restart_file, 'sm.pickled'), 'rb'))
                soils = pickle.load(open(os.path.join(restart_file, 'soils.pickled'), 'rb'))
                Q = pickle.load(open(os.path.join(restart_file, 'streamflows.pickled'), 'rb'))
                qold = pickle.load(open(os.path.join(restart_file,  'lateral_inflows.pickled'), 'rb'))
            except IOError as e:
                print("Unable to find initialization file %s. Initializing variable with empty storage" % e.filename)
            except pickle.PickleError as e:
                print("Unable to read file %s. Initializing variable with empty storage" % e.filename)

        # Creates the rainfall-runoff model object, the routing object,
        #   and the model coupling objects
        rr = hydroengine.HBV(86400, swe, pond, sm, soils, pickle_dir = restart_file, **hbv_pars)
        mc = hydroengine.Routing(adj_net, rr.dt)

        # Creates mock coupler
        simulated_water_users = utils.coupling.StrawFarmCoupling(num_links)
        irr_ids = arr_land_use = 0
        if farm_json is not None and scenario_json is not None:
            print("Economic module activated, generating water users and coupling objects... ")
            # Open water user object
            with open(farm_json) as json_farms:
                farms = json.load(json_farms)

            # Open scenarios object
            with open(scenario_json) as json_scenarios:
                scenarios = json.load(json_scenarios)

            # Retrieve the list of farms in the json input
            lst_farms = farms['farms']

            # Building the model coupling object and set up the farmer users
            coupler = utils.coupling.HydroEconCoupling(mc, lst_farms, pp_data[0, :, :], pp_affine)
            coupler.setup_farmer_user(water_user_shapes, water_user_id)

            print("Simulating water users... ")
            # Simulates all users with loaded scenarios
            simulated_water_users = coupler.simulate_all_users(
                scenarios, path_kf_info)

            arr_land_use = utils.RasterDataset(lu_raster)
            arr_land_use = np.squeeze(arr_land_use.array)
            irr_ids = tuple(lu_irr_ids)

        ro_ts = []
        Q_ts = []
        up_res = []
        low_res = []
        diversions = []
        # qold = np.zeros(num_links)
        e = np.array(graph.get_parameter('e'))
        ks = np.array(graph.get_parameter('ks'))

        total_ts = pp_data.shape[0]

        if num_time_steps is not None:
            total_ts = num_time_steps

        with tqdm.tqdm(total = total_ts, unit = 'days', disable = not verbose) as pbar:
            for i in np.arange(total_ts):
                cur_date = (parse(str(init_date)) + i * datetime.timedelta(seconds = rr.dt)).strftime("%Y%m%d")
                water_diversion, water_diversion_table, water_diversion_table_rates = \
                    simulated_water_users.retrieve_water_diversion_per_node(cur_date)
                suppl_irr = simulated_water_users.retrieve_supplemental_irrigation_map(
                    arr_land_use, irr_ids, water_diversion_table)

                # Calculate potential evapotranspiration
                pet = hydroengine.hamon_pe(
                    (tmin_data[i, :, :] + tmax_data[i, :, :]) * 0.5, lat, i)
                runoff, soils = rr.run_time_step(
                    pp_data[i, :, :] + suppl_irr, tmax_data[i, :, :], tmin_data[i, :, :],
                    pet, basin_file, affine = pp_affine, nodata = pp_nodata)
                # runoff[1] = runoff[-1] = 0

                qnew = np.array(runoff)
                water_diversion = water_diversion / rr.dt

                Q = mc.muskingum_routing(Q, ks, e, qnew, qold, water_diversion)
                qold = qnew # np.array(runoff)  # np.insert(runoff, 3, 0)

                ro_ts.append(runoff)
                Q_ts.append(Q)
                # retrieve the upper and lower reservoir information from array soils objects
                upr = np.array([i[1].upper_reservoir for i in soils])
                lowr = np.array([i[1].lower_reservoir for i in soils])
                up_res.append(upr)
                low_res.append(lowr)
                try:
                    diversions.append(water_diversion.values)
                except AttributeError:
                    diversions.append([0])

                # Write to drive the states for the current time step
                latlon = np.array((lat.ravel(), lon.ravel()))
                rr.write_current_states(
                    cur_date, ".tif", pp.clone_raster, hydro_maps_of)
                if verbose:
                    pbar.update()

            rr.pickle_current_states(restart_file)
            # Pickle current streamflows
            with open(os.path.join(
                    restart_file, "streamflows.pickled"), "wb") as stream:
                pickle.dump(Q, stream)
            with open(os.path.join(
                    restart_file, "lateral_inflows.pickled"), "wb") as stream:
                pickle.dump(qold, stream)
            utils.WriteOutputTimeSeries(
                adj_net, str(init_date), fname = os.path.join(hydro_ts_of, r'streamflows.json')).write_json(Q_ts)
            utils.WriteOutputTimeSeries(
                adj_net, str(init_date), fname = os.path.join(hydro_ts_of, r'upper_soil.json')).write_json(up_res)
            utils.WriteOutputTimeSeries(
                adj_net, str(init_date), fname = os.path.join(hydro_ts_of, r'groundwater.json')).write_json(low_res)

            if farm_json is not None and scenario_json is not None:
                print("Writing water users objects to drive... ")
                utils.WriteOutputTimeSeries(
                    adj_net, str(init_date), fname = os.path.join(
                        hydro_ts_of, r'diversions.json')).write_json(diversions)
                # Open water user object
                simulated_water_users.save_farm_list_json(
                    os.path.join(econ_results_of, "Farm_data_out.json"))

    def hydro(
            self, init_date: str, precip_file: str, tmin_file: str,
            tmax_file: str, params: dict, network_file: str, basin_file: str,
            num_time_steps: int = None, restart: bool = False,
            restart_file: str = None, hydro_maps_of: str = None,
            hydro_ts_of: str = None, verbose: bool = True):
        '''
        Runs the hydrologic model, without any economic model coupling.

        Parameters
        ----------
        init_date : str
            Simulation start date (YYYYMMDD)
        precip_file : str
            Path to NetCDF file with daily precipitation (mm/day)
        tmin_file : str
            Path to NetCDF file with minimum daily temperature (K)
        tmax_file : str
            Path to file with maximum daily temperature (K)
        params : dict
            Dictionary with names of parameter files (see documentation)
        network_file : str
            Path to stream network file, Shapefile or GeoJSON format
        basin_file : str
            Path to Shapefile w/ subcatchments for each node
        num_time_steps : int or None
            Length of simulation (days); if None (Default), simulate all days
            in precipitation record
        restart : bool
            True/False to restart using pickle file with initial conditions
        restart_file : str
            Path to restart (pickle) file
        hydro_maps_of : str
            Path to output map results from hydrologic model
        hydro_ts_of : str
            Path to output time series results from hydrologic model

        Returns
        -------
        None
        '''
        return self._run(
            init_date, precip_file, tmin_file, tmax_file, params,
            network_file, basin_file, num_time_steps = num_time_steps,
            restart = restart, restart_file = restart_file,
            hydro_maps_of = hydro_maps_of, hydro_ts_of = hydro_ts_of,
            verbose = verbose)

    def hydro_econ(
            self, init_date: str, precip_file: str, tmin_file: str,
            tmax_file: str, params: dict, network_file: str, basin_file: str,
            farm_json: str, scenario_json: str,
            water_user_shapes: str, water_user_id: str, lu_raster: str,
            lu_irr_ids: Sequence, path_kf_info: str, econ_results_of: str,
            num_time_steps: int = None, restart: bool = False,
            restart_file: str = None, hydro_maps_of: str = None,
            hydro_ts_of: str = None, verbose: bool = True):
        '''
        Runs the coupled hydrologic-economic model.

        Parameters
        ----------

        init_date : str
            Simulation start date (YYYYMMDD)
        precip_file : str
            Path to NetCDF file with daily precipitation (mm/day)
        tmin_file : str
            Path to NetCDF file with minimum daily temperature (K)
        tmax_file : str
            Path to file with maximum daily temperature (K)
        params : dict
            Dictionary with names of parameter files (see documentation)
        network_file : str
            Path to stream network file, Shapefile or GeoJSON format
        basin_file : str
            Path to Shapefile w/ subcatchments for each node
        farm_json : str
            Path to farm data JSON file
        scenario_json : str
            Path to scenario data JSON file
        water_user_shapes : str
            Path to water user shapes file (Shapefile or GeoJSON)
        water_user_id : str
            Name of field to be used as user ID
        lu_raster : str
            Path to land use raster file
        lu_irr_ids : Sequence
            Sequence of integers identifying irrigation land uses in lu_raster
        path_kf_info : str
            Path to Kalman filter info (kf_info) files, for activating
            stochastic economics
        econ_results_of : str
            Path to results from economic model
        num_time_steps : int or None
            Length of simulation (days); if None (Default), simulate all days
            in precipitation record
        restart : bool
            True/False to restart using pickle file with initial conditions
        restart_file : str
            Path to restart (pickle) file
        hydro_maps_of : str
            Path to output map results from hydrologic model
        hydro_ts_of : str
            Path to output time series results from hydrologic model

        Returns
        -------
        None
        '''
        return self._run(
            init_date, precip_file, tmin_file, tmax_file, params,
            network_file, basin_file, farm_json, scenario_json,
            water_user_shapes, water_user_id, lu_raster, lu_irr_ids,
            path_kf_info, econ_results_of, num_time_steps = num_time_steps,
            restart = restart, restart_file = restart_file,
            hydro_maps_of = hydro_maps_of, hydro_ts_of = hydro_ts_of,
            verbose = verbose)


if __name__ == '__main__':
    logging.basicConfig(
        filename = 'non_standard_output.log', level = logging.WARNING)
    fire.Fire(HydroEconModel)
