from __future__ import division
import pandas as pd
from dateutil import parser
import math
from scipy.interpolate import interp1d
import pkg_resources

DATA_PATH = pkg_resources.resource_filename('daWUAP.utils', '/')

def retrieve_crop_coefficient(
        current_date: str, start_date: str, cover_date: str, end_date: str,
        crop_id: int, kc_table: str = "crop_coefficients.txt"):
    """
    Returns crop coefficient for current_date interpolated from agMet lookup
    table. Dates are strings with m/d/YYYY format if they are ambiguous
    (e.g. 06/03/12 is June, 3 2012)

    Parameters
    ----------
    current_date: str
        Date for crop coefficient, m/d/YYYY string if dates are ambiguous
    start_date : str
        Crop planting date, m/d/YYYY string if dates are ambiguous
    cover_date : str
        Date at which crop is fully matured and has reached maximum coverage
    end_date : str
        Date at which crop ends, either harvested or dead
    crop_id : int
        Integer with crop id from AgMet crop coefficient lookup table
    kc_table : str
        Optional. File path to text-format lookup table with crop coefficient
        curves. See default table for format.

    Returns
    -------
    float
        Crop coefficient of crop_id for corresponding current_date
    """

    df_kc = pd.read_csv(DATA_PATH + '/' + kc_table, index_col="crop_id", sep='\t')
    current_date = parser.parse(current_date).timetuple().tm_yday
    start_date = parser.parse(start_date).timetuple().tm_yday
    cover_date = parser.parse(cover_date).timetuple().tm_yday
    end_date = parser.parse(end_date).timetuple().tm_yday
    crop_id = int(crop_id)

    if (current_date > start_date) & (current_date < cover_date):
        frac_growing_season = (current_date - start_date) / (cover_date - start_date) * 100
        f = interp1d(range(0, 110, 10), df_kc.loc[crop_id][:11])
    elif (current_date >= cover_date) & (current_date <= end_date):
        frac_growing_season = (current_date - cover_date) / (end_date - cover_date) * 100
        f = interp1d(range(0, 110, 10), df_kc.loc[crop_id][10:-2])
    else:
        return 0.0

    return f(frac_growing_season)
