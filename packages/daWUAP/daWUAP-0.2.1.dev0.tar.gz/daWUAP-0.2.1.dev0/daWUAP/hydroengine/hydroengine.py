import numpy as np


class Routing(object):
    """
    A hydrologic engine for a water management and decision support system.
    This is the central class of the hydrologic component. It is initialized
    with the connectivity matrix of the network and routes runoff generated
    at each node subcatchment through out the network. It uses outputs from
    the rainfall runoff models as water.
    """
    def __init__(self, conn, dt):
        """
        Initialization requires a connectivity matrix describing the topology
        of the water distribution network. The connectivity matrix is square
        and sparse, of size equal to the number of nodes to the network. Each
        element in the matrix represents a link (reach, channel) between nodes
        (arbitrary points in the river network, diversion points, gauges, water
        users, etc).

        Parameters
        ----------
        conn : numpy.ndarray
            N x N binary connectivity matrix, where N is the number of nodes
            in the network.
        dt : int
            Time step (seconds, scalar).
        """
        self.conn = conn
        self.dt = dt
        self.n = np.shape(conn)[0]

    def muskingum_routing(self, Qt, K, e, qnew, qold, water_diversion):
        """
        Routes water through a network graph using the Muskingum-Cunge method.
        This function takes an initial distribution of streamflows at nodes
        in the network and routes them one time step.

        Parameters
        ----------
        Qt : numpy.ndarray or Sequence
            Vector of streamflows at time t
        K : numpy.ndarray or Sequence
            Vector of reach storage parameters of size n
        e : numpy.ndarray or Sequence
            Vector of balances between inflows and outflows
        qnew : numpy.ndarray
            Vector of lateral inflows for the current time step
        qold : numpy.ndarray
            Vector of lateral inflows for the last time step
        water_diversion : numpy.ndarray
            Vector of water diversions

        Returns
        -------
        numpy.ndarray
            Vector of size n with streamflows at time t+1
        """

        # TODO Add here code to check the stability of the M-C algorithm
        # Only the upper bound this condition is necessary for stability...
        #   to lower bound for dt is to avoid possible negative flows
        dt = self.dt
        max_stab = 2 * K * (1 - e)
        # Implementation of this condition may require that K is halved
        min_stab = 2 * K * e

        # Adjust dt to maintain stability of Muskingum solution. The
        #   algorithm halves the time step until it meets the criterion
        #   for all reaches so the shortest/fastest reach will control the
        #   integration time step
        # n tracks the number of fractions that need to be computed in order
        #   to simulate the full day
        n = 1
        while np.any(np.greater(dt, max_stab)):
            dt /= 2
            n *= 2

        # Adjust Q and q to the reduced dt
        Qt = Qt/n
        qnew = qnew/n
        qold = qold/n

        # while np.any(np.greater(min_stab, self.dt)):
        #     K = K/2 # assuming K = dx/c
        #     # e = do something about e here, which is also a function of dx
        #     n *= 2
        #     min_stab = 2 * K * e

        for i in range(n):
            a = np.diag(K * (1-e) + dt)
            b = np.diag(K * e - dt)
            c = np.diag(K * (1-e))
            d = np.diag(K * e)
            lhs = (a+np.dot(self.conn, b)).T
            # rhs = np.dot((d+np.dot(self.conn, c)).T, Qt) + np.diag(a)*(qnew - qold)
            rhs = np.dot((c + np.dot(self.conn, d)).T, Qt) + np.diag(d) * (qold - qnew) + qnew * dt - water_diversion * dt
            Qt1 = np.linalg.solve(lhs, rhs)
            Qt = Qt1

        # water_diversion[:] += np.where(Qt1 < 0, Qt1, 0)
        # Qt1 = Qt1.clip(min=0)
        return Qt1
