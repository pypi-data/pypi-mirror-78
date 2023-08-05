import numpy as np
import pandas as pd
import datetime
from dateutil.parser import parse
import json

class WriteOutputTimeSeries(object):
    """
    Handles model time series outputs.
    """
    def __init__(
            self, conn_matrix: pd.DataFrame, init_date: str,
            fname: str = r'streamflows.json', dt: int = 1):
        '''
        Initializes object with connectivity matrix, the initial date and the
        size of the simulation time step (defaults to 1 day).

        Parameters
        ----------

        conn_matrix : pandas.DataFrame
            Connectivity matrix of stream network, pandas dataframe
        init_date : str
            Date of first time step, string
        name : str
            Output filename
        dt : int
            Time step size, days
        '''
        self.conn_matrix = conn_matrix
        self.init_date = parse(init_date)
        self.fname = fname
        self.dt = datetime.timedelta(days = dt)

    def write_json(self, data: list, units: str = "m3/s"):
        """
        Writes list of model outputs at each node as a JSON file.

        Parameters
        ----------

        data : list
            List of lists of numpy array with flows
        units : str
            Description of the units to output

        Returns
        -------
        dict
            JSON dictionary in the format described above
        """
        lst_nodes = []
        data = np.array(data).T
        for row, nodeid in enumerate(self.conn_matrix.index.values):
            node = {"id": int(nodeid.tolist())}
            node["units"] = str(units)
            node["dates"] = \
                [{"date": (self.init_date + ts * self.dt).strftime("%Y/%m/%d"),
                  "flow": d.tolist()} for ts, d in enumerate(data[row])]

            lst_nodes.append(node)

        dict_nodes = {"nodes": lst_nodes}

        with open(self.fname, 'w') as buff:
            json.dump(dict_nodes, buff, indent=4)

        return dict_nodes
