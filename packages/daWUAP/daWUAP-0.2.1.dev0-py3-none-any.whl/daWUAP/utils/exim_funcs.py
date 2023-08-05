import pandas as pd
import json

def import_obs_from_csv(
        fn_input_csv: str, fn_out_json: str = None, year = None,
        sep: str = ',', crops = None):
    """
    Produces a JSON file with a list of observation dictionaries.
    """
    lst_dict = []
    d = {}
    df_in = pd.read_csv(fn_input_csv, sep=sep, index_col=["id", "year", "crop"])

    if crops is not None:
        df_in = df_in[df_in.index.get_level_values(2).isin(crops)]

    for id, df_farm in df_in.groupby(level=(0,1)):
        if year is None or id[1] == year:
            print("Processing farm %s with id %i, year %i" % (df_farm["name"][0], id[0], id[1]))

        # Make NaNs zero
        df_farm = df_farm.fillna(0)
        # Get list of crops and year from index level 1 and 2
        d["crop_list"] = list(df_farm.index.get_level_values(2))
        d["year"] = id[1].tolist()
        d["id"] = id[0].tolist()
        d["name"] = df_farm["name"][0]
        d["mean_eta"] = list(df_farm["supply_elasticity"])
        d["mean_ybar"] = list(df_farm["production"])
        d["mean_obs_land"] = list(df_farm["area_planted"])
        d["mean_obs_water"] = list(df_farm["crop_water_observation"])
        d["mean_ybar_w"] = list(df_farm["yield_elasticity"])
        d["mean_prices"] = list(df_farm["crop_prices"])
        d["mean_costs"] = list(zip(list(df_farm["cost_land"]), list(df_farm["cost_water"])))
        d["std_eta"] = list(df_farm["supply_elasticity_sd"])
        d["std_ybar"] = list(df_farm["production_sd"])
        d["std_obs_land"] = list(df_farm["area_planted_sd"])
        d["std_obs_water"] = list(df_farm["crop_water_observation_sd"])
        d["std_ybar_w"] = list(df_farm["yield_elasticity_sd"])
        d["std_prices"] = list(df_farm["crop_prices_sd"])
        d["std_costs"] = list(zip(list(df_farm["cost_land_sd"]), list(df_farm["cost_water_sd"])))
        if year is None or id[1] == year:
            lst_dict.append(d.copy())

    if fn_out_json is not None:
        with open(fn_out_json, 'w') as json_file:
            json.dump(lst_dict, json_file)

    return lst_dict
