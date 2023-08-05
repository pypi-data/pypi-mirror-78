import numpy as np
import pandas as pd

def _generate_crop_list(varshape: tuple):
    """
    Generates a generic list to be used as column names in pandas dataframe.

    Parameters
    ----------
    varshape : tuple
        Tuple with shape of variable (i.e. beta is 2D, delta is 1D)

    Returns
    -------
    list
        An alphabetical list for generic crop naming
    """

    if len(varshape) == 1:
        clist = [chr(i) for i in range(ord('A'), ord('A') + varshape[0])]
    elif len(varshape) == 2:
        abclist = [chr(i) for i in range(ord('A'), ord('A') + varshape[0])]
        pair1 = [i + '1' for i in abclist]
        pair2 = [i + '2' for i in abclist]
        pair_zip = [list(a) for a in zip(pair1, pair2)]
        clist = [item for sublist in pair_zip for item in sublist]
    return clist


def _generate_param_list(params: list):
    """
    Generates a list of parameter values in the correct format.

    Parameters
    ----------
    params : list
        All parameters, indexed from pandas df[key]

    Returns
    -------
    list
        Parameter values for ingestion into dict2pandas multi index dataframe
    """

    paramshape = np.asarray(params[0]).shape
    if len(paramshape) == 1:
        param_list = params.values.tolist()
    elif len(paramshape) == 2:
        param_list = [[i for j in sublist for i in j] for sublist in params.values.tolist()]
    return param_list


def dict2pandas(lst_par_dcts: dict, crop_names: list = None):
    """
    Converts parameter ensemble to a multi-index pandas dataframe where
    crops are labeled alphabetically. The input ensemble is a list of
    dictionaries.

    Parameters
    ----------
    lst_par_dcts : dict
        Dictionary with list of parameters to be converted to
        multi-index pandas dataframe
    crop_names:
        List of crop names in the order given in dictionary, default is
        generic alphabetical list

    Returns
    -------
    pandas.DataFrame
    """

    # Convert lst_par_dcts to DF
    df = pd.DataFrame(lst_par_dcts)
    df = df.drop('sigmas', axis=1)

    df_list = []
    label_list = []
    if crop_names:
        for key in df.keys():
            varshape = np.asarray(df[key][0]).shape
            if varshape[0] != len(crop_names):
                colnm = _generate_crop_list(varshape)
                param_list = _generate_param_list(df[key])
            else:
                if len(varshape) == 1:
                    colnm = crop_names
                elif len(varshape) == 2:
                    pair1 = [i + '_1' for i in crop_names]
                    pair2 = [i + '_2' for i in crop_names]
                    pair_zip = [list(a) for a in zip(pair1, pair2)]
                    colnm = [item for sublist in pair_zip for item in sublist]
                param_list = _generate_param_list(df[key])
            param = pd.DataFrame(param_list, columns=colnm)
            df_list.append(param)
            label_list.append(key)

    # If crop name list not given
    else:
        for key in df.keys():
            varshape = np.asarray(df[key][0]).shape
            colnm = _generate_crop_list(varshape)
            param_list = _generate_param_list(df[key])
            param = pd.DataFrame(param_list, columns=colnm)
            df_list.append(param)
            label_list.append(key)
    return pd.concat(df_list, axis=1, keys=label_list)


def write_pandas(df: pd.DataFrame, fname: str):
    '''
    Writes a pandas.DataFrame to a CSV file.

    Parameters
    ----------
    df : pandas.DataFrame
    fname : str
    '''
    df.reset_index().to_csv(fname, index=False)


def read_pandas(fname: str, results: bool = False, retrieve_assimilation_step = None):
    '''
    Reads in a CSV file and returns pandas.DataFrame instance.

    Parameters
    ----------
    fname : str
        File path of the CSV to read
    results : bool
    retrieve_assimilation_step: int or str or None
    '''
    df = pd.read_csv(fname, header=[0, 1, 2], index_col=0)
    if results:
        return df
    else:
        if retrieve_assimilation_step is None:
            return df[df.columns[-1][0]]
        if isinstance(retrieve_assimilation_step, str):
            return df[retrieve_assimilation_step]
        if isinstance(retrieve_assimilation_step, int):
            return df[df.columns[retrieve_assimilation_step][0]]
