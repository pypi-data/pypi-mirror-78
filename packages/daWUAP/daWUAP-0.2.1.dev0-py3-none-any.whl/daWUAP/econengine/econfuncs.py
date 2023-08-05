'''
    Farm
        Class representing economic behavior of farms

    rho()
        Elasticity of substitution
'''

from __future__ import division
from . import WaterUser
from daWUAP.utils.check_farms import check_farms
import numpy as np
import json
import scipy.optimize as sci


def rho(sigma):
    """returns elasticity of substitution rho

    :param sigma: substitution elasticity by crop and technology
    :return: rho parameter
    """
    return (sigma - 1) / sigma


class Farm(WaterUser):
    """Class representing economic behavior of farms"""

    def __init__(self, fname=None, **kwargs):

        if isinstance(fname, str):
            with open(fname) as json_data:
                kwargs = json.load(json_data)

        check_farms(kwargs)

        self.crop_list = kwargs.get('crop_list')
        self.input_list = kwargs.get('input_list')
        self.crop_id = np.asanyarray(kwargs.get('crop_id'), dtype=np.int)
        self.irr_eff = np.asanyarray(kwargs.get('irrigation_eff'), dtype=np.float)
        self.irr = np.asanyarray(kwargs.get('irrigation_mask'), dtype=bool)

        self.ref_et = np.asarray(kwargs['normalization_refs'].get('reference_et'))
        self.ref_prices = np.asarray(kwargs['normalization_refs'].get('reference_prices'))
        self.ref_yields = np.asarray(kwargs['normalization_refs'].get('reference_yields'))
        self.ref_land = np.asarray(kwargs['normalization_refs'].get('reference_land'))

        # makes list of constant reference quantities if single value is passed
        self.ref_et, self.ref_prices, self.ref_yields, self.ref_land = [np.repeat(ref, len(self.crop_list))
                                                                        if len(ref) == 1 else ref
                                                                          for ref in (self.ref_et,
                                                                                      self.ref_prices,
                                                                                      self.ref_yields,
                                                                                      self.ref_land)]


        # avoids div by zero if refs are not set
        self.ref_et[self.ref_et == 0] = 1
        self.ref_prices[self.ref_prices == 0] = 1
        self.ref_yields[self.ref_yields == 0] = 1
        self.ref_prices[self.ref_prices == 0] = 1
        self.ref_land[self.ref_land == 0] = 1

        self.sigmas = np.asarray(kwargs['parameters'].get('sigmas'))
        if len(self.sigmas) == 1:
            self.sigmas = np.repeat(self.sigmas, len(self.crop_list))

        self.deltas = np.asarray(kwargs['parameters'].get('deltas'))
        self.betas = np.asarray(kwargs['parameters'].get('betas'))
        self.mus = np.asarray(kwargs['parameters'].get('mus'))
        self.first_stage_lambda = np.asarray(kwargs['parameters'].get('first_stage_lambda'))
        self.lambdas_land = np.asarray(kwargs['parameters'].get('lambdas_land'))

        #self.prices = None
        #self.costs = kwargs.get('costs')  # land and water costs. Array with one row per crop. First column land second column water

        self._landsim = np.atleast_1d(kwargs['simulated_states'].get('used_land', 0)) / self.ref_land
        self._watersim = np.atleast_1d(kwargs['simulated_states'].get('used_water', 0)) / (self.ref_et * self.ref_land)
        self.etasim = np.atleast_1d(kwargs['simulated_states'].get('supply_elasticity_eta', 0))
        self._ysim = np.atleast_1d(kwargs['simulated_states'].get('yields', 0)) / self.ref_yields
        self.ysim_w = np.atleast_1d(kwargs['simulated_states'].get('yield_elasticity_water', 0))
        self._net_revs = np.atleast_1d(kwargs['simulated_states'].get('net_revenues', 0))
        self._lagrange_mults = np.atleast_1d(kwargs['simulated_states'].get('shadow_prices', [0]))

        # This to be filled with information provided during simulations
        self.crop_start_date = None
        self.crop_cover_date = None
        self.crop_end_date = None

        super(Farm, self).__init__(str(kwargs.get("id")), int(kwargs.get("source_id")), kwargs.get("name"))

    @property
    def landsim(self):
        return self._landsim * self.ref_land # land in hectares

    @landsim.setter
    def landsim(self, value):
        self._landsim = value / self.ref_land #land in hectares

    @property
    def watersim(self):
        """Returns un-normalized total simulated water use"""
        return self._watersim * (self.ref_et * self.ref_land) # water in mm

    @watersim.setter
    def watersim(self, value):
        self._watersim = value / (self.ref_et * self.ref_land) # water in mm

    @property
    def ysim(self):
        """Returns un-normalized simulated crop yields"""
        return self._ysim * self.ref_yields

    @ysim.setter
    def ysim(self, value):
        """Sets simulated yields"""
        self._ysim = value / self.ref_yields

    @property
    def net_revs(self):
        return self._net_revs * self.ref_prices # dollars?

    @net_revs.setter
    def net_revs(self, value):
        self._net_revs = value / self.ref_prices  # dollars?

    @property
    def lagrange_mults(self):
        av_scale_land = (self.ref_prices * self.ref_yields) / self.ref_land
        av_scale_water = (self.ref_prices * self.ref_yields) / (self.ref_et * self.ref_land)
        return np.multiply(self._lagrange_mults[:, np.newaxis], np.array([av_scale_land, av_scale_water]))
        # lagrange mults in $/ha and $/m3

    @lagrange_mults.setter
    def lagrange_mults(self, value):
        """

        :type lambda_land: object
        """
        av_scale_land = (self.ref_prices * self.ref_yields) / self.ref_land # $/kg * kg / ha => $/ha
        av_scale_water = (self.ref_prices * self.ref_yields) / (self.ref_et * self.ref_land) #$/kg * kg / (mm*ha) => $/(mmha)
        self._lagrange_mults = np.divide(value, np.array([av_scale_land, av_scale_water]))


    def _check_calibration_criteria(self, sigmas, eta, xbar, ybar_w, qbar, p):

        # Check calibration criteria 1
        if ((eta - ybar_w/(1 - ybar_w)) < 0).any():
            raise ValueError('calibration criteria 1'
                             'for farm %i with name %s failed' % (self.id, self.name))

        # Check calibration criteria 2
        b = xbar**2/(p * qbar)
        psi = sigmas * ybar_w / (eta * (1 - ybar_w))
        ind = np.arange(len(b))
        cc2 = b * eta * (1 - psi) - [np.sum(b[ind != i] *
                                                 eta[ind != i] * (1 + (1 / eta[ind != i]))**2 *
                                                 (1 + psi[ind != i] - ybar_w[ind != i])) for i in ind]
        if (cc2 > 0).any():
            raise ValueError('calibration criteria 2'
                             'for farm %i with name %s failed' % (self.id, self.name))

    @staticmethod
    def _eta_sim(sigmas, delta, xbar, ybar_w, qbar, p):
        """
        Simulates exogenous supply elasticities (eta) as a function
         of observed land and water allocations and parameters

        :param delta: CES production function returns-to-scale parameter, 1D array
        :param xbar: Observed resource allocations, 2D array (ncrops x nresources)
        :param ybar_w: Yield elasticity with respect to water use, 1D array
        :param qbar: Observed total production for each crop
        :param p: Observed crop prices received by farmer for each crop, 1D array
        :return: vector of simulated supply elasticities of the same shape as delta
        """

        b = xbar[:, 0]**2 / (p * qbar)
        num = b / (delta * (1 - delta))
        dem = np.sum(num + (sigmas * b * ybar_w / (delta * (delta - ybar_w))))
        return delta / (1 - delta) * (1 - (num/dem))

    @staticmethod
    def _y_bar_w_sim(sigmas, beta, delta, xbar):
        """
        Simulates yield elasticity with respect to water (ybar_w) as a function of observed
        land and water allocation and parameters.

        :param sigmas: Elasticity of substitution parameter.
        :param beta: CES shares parameter, 2D array (ncrops x nresources).
        :param delta: CES production function returns-to-scale parameter, 1D array.
        :return: Vector of simulated yield elasticities with respect to water
         of the same shape as delta
        """
        r = rho(sigmas)
        num = beta[:, -1] * xbar[:, -1]**r
        den = np.diag(np.dot(beta, xbar.T**r))
        return delta * num/den

    @staticmethod
    def production_function(sigmas, beta, delta, mu, xbar, et0=[0]):
        """
        Constant elasticity of substitution production function

        :param sigmas: Elasticity of substitution parameter.
        :param beta: CES shares parameter, 2D array (ncrops x nresources).
        :param delta: CES production function returns-to-scale parameter, 1D array.
        :param mu: CES productivity parameter, 1D array.
        :param xbar: Resource allocation, 2D array (ncrops, nresources)
        :param et0: evapotranspiration, defaults to zero
        :return: vector of crop production with same shape as delta
        """
        r = rho(sigmas)
        beta = beta.clip(min=0, max=1)
        x = xbar.copy()
        # adds evaporatranspiration to crop water if irrigation and et are dissagregated
        x[:, -1] = xbar[:, -1] + np.asarray(et0)
        x = x.clip(min=0.0000000001)
        return mu * np.diag(np.dot(beta, x.T**r))**(delta/r)

    @staticmethod
    def _first_stage_lambda_land_lhs(lambda_land, prices, costs, delta, qbar, y_bar_w, xbar):
        """
        First order optimality condition for the calibration of the land shadow value.
        Shadow value is calibrated to observed states when the function returns 0

        :param beta:
        :param delta:
        :param mu:
        :param xbar:
        :return:
        """
        #qbar  = #self.production_function(beta, delta, mu, xbar)
        #yw = #self._y_bar_w_sim(beta, delta, xbar)
        lambda_land = np.asarray(lambda_land)
        prices = np.asarray(prices)
        delta = np.asarray(delta)
        qbar = np.asarray(qbar)
        y_bar_w = np.asarray(y_bar_w)
        xbar = np.asarray(xbar)

        condition = -2. * (costs[:, 0] + lambda_land) * xbar[:, 0]**2 + 2 * xbar[:, 0] * prices * qbar * delta

        return np.sum(condition)

    @staticmethod
    def _lambda_land_water_lhs(lambda_land, first_stage_lambda, deltas, prices, costs, qbar, xbar):

        fstStgLbda = np.array([first_stage_lambda, 0])
        # this following term only applies to land, hence 0 on the water column
        p_qbar_delta = np.asarray(prices * qbar * deltas)[:, np.newaxis]
        p_qbar_delta = np.append(p_qbar_delta, np.zeros_like(p_qbar_delta), axis=1)

        lhs_lambdas = (costs + lambda_land + fstStgLbda) * xbar - p_qbar_delta

        return lhs_lambdas

    @staticmethod
    def _convex_sum_constraint(betas):
        """sum the columns of CES production function share parameters (n,m).
        The second element is a non-negativity condition.
         Betas are non-negative if the difference between the beta values and their absolute is zero

         Returns two array, the fist is the sum of the beta columns
         The second array, when zero, indicates the elements that are positive.

         :param betas: matrix of beta parameters

         :returns: (n,), (n*m,)
         """

        return betas.sum(axis=1), (betas - np.abs(betas)).flatten()

    @staticmethod
    def _observed_activity(prices, eta, ybar_w, ybar, xbar):
        """ produce the rhs of optimality equation by stacking
         the vectors of observations in a 1D vector.

          This function also also returns a mask that identifies as False the zero elements of the non-negativity
          that is not used in the stochastic assimilation scheme.
          """

        qbar = ybar * xbar[:, 0]

        seq = (eta, ybar_w, qbar, np.ones_like(prices), np.zeros(xbar.size),
               np.sum(2 * xbar[:, 0] * prices * qbar * ybar_w),
               -prices * qbar * ybar_w, prices * qbar * ybar_w)

        obs_act = np.hstack(seq)

        mask_seq = [np.zeros_like(x, dtype=bool) if i == 4 else np.ones_like(x, dtype=bool) for i, x in enumerate(seq)]
        mask_nonnegativity_condition = np.hstack(mask_seq)

        return obs_act, mask_nonnegativity_condition

    def _set_reference_observations(self, **kwargs):

        tempkwargs=kwargs.copy()
        for k in tempkwargs.keys():
            if k.startswith('mean_'):
                newkey = k[len('mean_'):]
                kwargs[newkey] = kwargs[k]
                kwargs.pop(k)

        #set calibration mask to drop crops with no land allocated
        cal_mask = np.atleast_1d(kwargs['obs_land']) != 0.0
        kwargs['obs_land'] = np.atleast_1d(kwargs['obs_land'])
        kwargs['obs_water'] = np.atleast_1d(kwargs['obs_water'])
        kwargs['ybar'] = np.atleast_1d(kwargs['ybar'])
        #kwargs['ybar_w'] = np.atleast_1d(kwargs['ybar_w'])
        kwargs['obs_land'][~cal_mask] = 1e-10
        kwargs['obs_water'][~cal_mask] = 1e-10
        kwargs['ybar'][~cal_mask] = 1e-10
        #kwargs['ybar_w'][~cal_mask] = 1e-10

        cal_mask = np.atleast_1d(kwargs['obs_land']) != 0.0

        if len(cal_mask[~cal_mask]) > 0:
            print("Getting ready to calibrate " \
                  "parameters for all crops except %s" % np.asarray(self.crop_list)[~cal_mask])

        eta = np.atleast_1d(kwargs['eta'])[cal_mask]
        ybar = (np.atleast_1d(kwargs['ybar']) / self.ref_yields)[cal_mask]
        landbar = (np.atleast_1d(kwargs['obs_land']) /self.ref_land)[cal_mask]
        waterbar = (np.atleast_1d(kwargs['obs_water']) / (self.ref_et * self.ref_land))[cal_mask]
        xbar = np.array([landbar, waterbar]).T
        ybar_w = np.atleast_1d(kwargs['ybar_w'])[cal_mask]

        prices = (np.atleast_1d(kwargs['prices']) / self.ref_prices)[cal_mask]
        costs = np.atleast_2d(kwargs['costs'])[cal_mask]

        costs[:, 0] *= 1/(self.ref_prices * self.ref_yields)[cal_mask]
        costs[:, 1] *= ((self.ref_et * self.ref_land)/(self.ref_prices * self.ref_yields))[cal_mask]

        qbar = ybar * xbar[:, 0]

        def calibrate(solve_pmp_program=True, **kwargs):

            # skip Merel's calibration conditions if not solving pmp program
            if solve_pmp_program:
                try:
                    self._check_calibration_criteria(self.sigmas[cal_mask],
                                                     eta,
                                                     xbar[:, 0],
                                                     ybar_w,
                                                     qbar,
                                                     prices
                                                     )
                except ValueError as e:
                    print("Flag raised for inconsistent observations with message: ", e)
                    print("NEW OBSERVATIONS NOT INCORPORATED INTO FARM WITH ID %s... " % self.id)
                    return type("res", (), {'success': False})

            def func(pars):

                sigmas = self.sigmas[cal_mask]

                first_stage_lambda = pars[-1]  # first stage lambda always the last parameter
                pars2 = pars[:-1].reshape(-1, prices.size).T
                deltas = pars2[:, 0]
                betas = pars2[:, 1:3]
                mus = pars2[:, 3]
                lambdas = pars2[:, 4:]
                rhs, nonneg_cond_mask = self._observed_activity(prices, eta, ybar_w, ybar, xbar)

                lhs = np.hstack((
                    self._eta_sim(sigmas, deltas, xbar, ybar_w, qbar, prices),
                    self._y_bar_w_sim(sigmas, betas, deltas, xbar),
                    self.production_function(sigmas, betas, deltas, mus, xbar),
                    np.concatenate(self._convex_sum_constraint(betas)),
                    self._first_stage_lambda_land_lhs(first_stage_lambda, prices, costs, deltas, qbar, ybar_w, xbar),
                    self._lambda_land_water_lhs(lambdas, first_stage_lambda, deltas, prices, costs, qbar,
                                                xbar).T.flatten()))

                if solve_pmp_program:
                    return lhs - rhs
                else:
                    ## remove non-negativity condition for the betas
                    return lhs[nonneg_cond_mask], rhs[nonneg_cond_mask]

            x = np.hstack((self.deltas[cal_mask], self.betas[cal_mask].T.flatten(),
                           self.mus[cal_mask],
                           self.lambdas_land[cal_mask].T.flatten(),
                           self.first_stage_lambda))
            if solve_pmp_program:
                opt_res = sci.root(func, x, method='lm', **kwargs)
                if opt_res.success:
                    print("Farm %s with id %s successfully calibrated" % (self.name, self.id))
                    self.first_stage_lambda = np.atleast_1d(opt_res.x[-1])
                    pars2 = opt_res.x[:-1].reshape(-1, prices.size).T
                    self.deltas[cal_mask] = pars2[:, 0]
                    self.betas[cal_mask] = pars2[:, 1:3]
                    self.mus[cal_mask] = pars2[:, 3]
                    self.lambdas_land[cal_mask] = pars2[:, 4:]

                return opt_res
            else:
                return func(x)

        return calibrate

    def write_farm_dict(self, fname=None):
        """Dumps farm information to a dictionary and returns it and writes it to fname"""

        farm_dic = {
            "id": str(self.id),
            "source_id": str(self.source_id),
            "name": str(self.name),
            "crop_list": self.crop_list,
            "input_list": self.input_list,
            "irrigation_mask": self.irr.tolist(),
            "crop_id": self.crop_id.tolist(),
            "irrigation_eff": self.crop_id.tolist(),
            "parameters": {
                "sigmas": self.sigmas.tolist(),
                "deltas": self.deltas.tolist(),
                "betas": self.betas.tolist(),
                "mus": self.mus.tolist(),
                "first_stage_lambda": np.atleast_1d(self.first_stage_lambda).tolist(),
                "lambdas_land": self.lambdas_land.tolist()
            },
            "constraints": {
                "land": [-1],
                "water": [-1]
            },
            "simulated_states": {
                "used_land": self.landsim.tolist(),
                "used_water": self.watersim.tolist(),
                "supply_elasticity_eta": self.etasim.tolist(),
                "yields": self.ysim.tolist(),
                "yield_elasticity_water": self.ysim_w.tolist(),
                "net_revenues": self.net_revs.tolist(),
                "shadow_price_land": self.lagrange_mults.tolist()[0],
                "shadow_price_water": self.lagrange_mults.tolist()[1]
            },
            "normalization_refs": {
                "reference_et": self.ref_et.tolist(),
                "reference_prices": self.ref_prices.tolist(),
                "reference_yields": self.ref_yields.tolist(),
                "reference_land": self.ref_land.tolist()
            }
        }

        if fname is not None:
            with open(fname, 'w') as json_file:
                json_file.write(json.dumps(farm_dic))

        return farm_dic

    def simulate(self, xinit=None, **kwargs):
        """Simulates resource allocation given given the current set of function parameters in the class.

        Parameters
        ==========

        :param kwargs:
            Dictionary with lists or arrays of prices, costs and constraints to production.

        :Example:

        ::

            observs = {
            'farm_id': 107,
            'evapotranspiration': [5., 5.]
            'prices': [5.82, 125],
            'costs': [111.56, 193.95],
            'land_constraint': 100,
            'water_constraint': 100,
            'crop_start_date': ["5/15/2014", "5/15/2014", "5/15/2014", "5/15/2014", "5/15/2014",
                                "5/15/2014", "5/15/2014", "5/15/2014"],
            'crop_cover_date': ["7/02/2014", "7/02/2014", "7/02/2014", "7/02/2014", "7/02/2014",
                                "7/02/2014", "7/02/2014", "7/02/2014"],
            'crop_end_date': ["8/25/2014", "8/25/2014", "8/25/2014", "8/25/2014", "8/25/2014",
                              "8/25/2014","8/25/2014", "8/25/2014"],
            }

            Farm_obj.simulate(**observs)

        """

        et0 = np.array(kwargs['evapotranspiration'])/self.ref_et
        prices = np.array(kwargs['prices'])/self.ref_prices
        #if prices.ndim < 2:
        #    prices = prices[:, np.newaxis]

        costs = np.array(kwargs['costs'])

        costs[:, 0] *= 1 / (self.ref_prices * self.ref_yields)
        costs[:, 1] *= (self.ref_et * self.ref_land)/(self.ref_prices * self.ref_yields)

        L = np.array(kwargs['land_constraint'])
        W = np.array(kwargs['water_constraint'])
        L = L if L >= 0 else np.inf
        W = W if W >= 0 else np.inf
        LW = np.hstack((L, W))

        self.crop_start_date = np.array(kwargs['crop_start_date'])
        self.crop_cover_date = np.array(kwargs['crop_cover_date'])
        self.crop_end_date = np.array(kwargs['crop_end_date'])

        self.mus = self.mus.clip(min=0)
        self.betas = self.betas.clip(min=0)

        # Solve maximization problem using scipy
        def netrevs(x):

            num_crops = len(self.crop_list)
            num_inputs = len(self.input_list)
            x = x.reshape(num_crops, num_inputs)
            q = self.production_function(self.sigmas, self.betas, self.deltas,
                                         self.mus, x, eta)
            lam_land = np.zeros(len(self.input_list))
            lam_land[0] = self.first_stage_lambda
            nr = prices * q - np.sum((costs + self.lambdas_land + lam_land) * x, axis=1)
            return -1 * nr.sum()

        def jac_nr(xin):
            num_crops = len(self.crop_list)
            num_inputs = len(self.input_list)
            xres = xin.reshape(num_crops, num_inputs).copy()
            x = xres #np.clip(xres, 1e-10, np.inf)

            r = rho(self.sigmas)
            q = self.production_function(self.sigmas, self.betas, self.deltas,
                                         self.mus, x, eta)
            fsl = np.zeros(len(self.input_list))
            fsl[0] = self.first_stage_lambda

            arreta = np.column_stack((np.zeros_like(eta), eta))
            bx = (self.betas.T * ((x + arreta).T**r)).sum(axis=0) #self.betas[:, 0] * x[:, 0]**r + self.betas[:, 1] * (eta + x[:, 1])**r

            dnet = (self.betas.T * prices * self.deltas * q * (x + arreta).T**(r-1) / bx).T - (costs + self.lambdas_land + fsl)

            return -dnet.flatten()

        # prepare initial guesses
        if xinit is None:
            xbar = np.array([self._landsim, self._watersim]).T
        else:
            xbar = xinit/np.array([self.ref_land, self.ref_et * self.ref_land]).T

        eta = np.ones_like(xbar[:,-1]) * et0#1 * xbar[:, -1]
        eta[self.irr] = (np.ones_like(eta) * et0)[self.irr]

        # set bounds to ensure non-negative solutions and that rainfed crops are not irrigated
        irr = np.zeros_like(xbar)
        irr[:, :-1] = np.inf
        irr[:, -1][self.irr] = np.inf
        irr = irr.flatten()
        bnds = sci.Bounds(0.0, irr)
        #bnds = sci.Bounds(0.0, np.inf)

        # set constraints that used land and water is less than available resources
        # Azeros = np.zeros_like(xbar)
        # A = []
        # for c in Azeros.T:
        #     c += 1
        #     A.append(Azeros.flatten())
        #     c -= 1
        # A = np.asarray(A)

        # set constraints that used land and water is less than available resources
        Azeros = np.ones_like(xbar)
        Azeros = Azeros * np.array([self.ref_land, (self.ref_et * self.ref_land)]).T
        Azeros = np.insert(Azeros, np.arange(1, len(self.input_list)), 0, axis=1)
        A = np.array([Azeros[:, i-2:i].flatten() for i in np.arange(2, Azeros.shape[1]+1)])

        lin_const = sci.LinearConstraint(A, 0, LW)

        res = sci.minimize(netrevs, xbar.flatten(), method='trust-constr', jac=jac_nr, hess='cs',
                           constraints=lin_const,
                           bounds=bnds, options=kwargs.get('solver_options', {}))

        if res.success:
            num_crops = len(self.crop_list)
            num_inputs = len(self.input_list)
            xbar_opt = res.x.reshape(num_crops, num_inputs)
            self._landsim = xbar_opt[:, 0]
            self._watersim = xbar_opt[:, -1]
            self._lagrange_mults = res.v[0]
            # simulate yields with optimal parameters
            self._ysim = self.production_function(self.sigmas, self.betas, self.deltas,
                                                  self.mus, xbar_opt, et0)
            self._net_revs = prices * self._ysim - np.sum((costs + self.lambdas_land) * xbar_opt, axis=1)



        # this functions shouldnt return, it should write to member variables so variables are
        # unnormalized
        return res

    def calibrate(self, solve_pmp_program=True, **kwargs):
        """Calibrates the economic model of agricultural production.

        Parameters
        ==========

        :param kwargs:
            Dictionary with lists or arrays of observed agricultural activity:

        :Example:

        ::

            observs = {
            'eta': [.35, 0.29],
            'ybar': [35, 2.2],
            'obs_land': [0.1220, 0.4.],
            'obs_water': [0.0250, 0.035],
            'ybar_w': [0.06, 0.21],
            'prices': [5.82, 125],
            'costs': [111.56, 193.95]}

            Farm_obj.calibrate(**observs)


        :return:
        """

        # set reference observations, solve nonlinear program and return results
        res = self._set_reference_observations(**kwargs)(solve_pmp_program)

        # if not solve_pmp_program:
        #     return res

        # if res.success:
        #
        #     # retrieve optimized parameters, parse them and update member parameter variables
        #     pars = res['x']
        #
        #     # Assign optimal values to Farm object
        #     self.first_stage_lambda = pars[-1]  # first stage lambda always the last parameter
        #     pars2 = pars[:-1].reshape(-1, len(self.crop_list)).T
        #     self.deltas = pars2[:, 0]
        #     self.betas = pars2[:, 1:3]
        #     self.mus = pars2[:, 3]
        #     self.lambdas_land = pars2[:, 4:]

        return res
