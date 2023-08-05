import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import json
import os


class EnsembleResults(object):
    def __init__(self, fn_info_json):

        with open(fn_info_json) as js:
            self.dc_info = json.load(js)

        try:
            self.xi = self.dc_info['xi']
            self.name = self.dc_info['name']
            self.id = self.dc_info['id']
            self.ens_size = self.dc_info['ensemble size']
            self.fn_inn = self.dc_info['innovation']
            self.fn_post = self.dc_info['posterior parameters']
            self.zeta = self.dc_info['zeta']
        except:
            pass

    def load_ensemble(self, header=[0, 1, 2], innovation=False):
        """return a pandas dataframe with parameter or innovation ensemble"""
        fn = self.fn_post
        if innovation:
            fn = self.fn_inn

        df = pd.read_csv(fn, header=header, index_col=0)

        return df

    def get_percentiles(self, df):
        """Returns the average, 5th, 25th, 75th and 95th percentiles of each assimilation cycle
        of the ensemble

        :param df: ensemble dataframe
        :return: 5 pandas series with mean, q5, q25, q75, q95
        """

        mean = df.median(axis=0)
        q5 = df.quantile(0.05, axis=0)
        q25 = df.quantile(0.25, axis=0)
        q40 = df.quantile(0.40, axis=0)
        q60 = df.quantile(0.60, axis=0)
        q75 = df.quantile(0.75, axis=0)
        q95 = df.quantile(0.95, axis=0)

        return mean, q5, q25, q40, q60, q75, q95

    def get_assim_cycles(self, df):
        return df.columns.get_level_values(0).unique()

    def get_parameter_names(self, df):
        return df.columns.levels[1]

    def get_crop_names(self, df):
        return df.columns.levels[2]

    def plot_parameter_ensemble(self, innovation=False, crop_lst=None, param_lst=None, show=True, **kwargs):

        df = self.load_ensemble(innovation=innovation)
        if crop_lst is None:
            crop_lst = list(self.get_crop_names(df))
            #crop_lst.remove('A')
        if param_lst is None:
            param_lst = self.get_parameter_names(df).to_list()

       # crop_lst.append('A') #append the special crop that holds farm_scale lambda

        mean, q5, q25, q40, q60, q75, q95 = self.get_percentiles(df)

        ind = self.get_assim_cycles(df)

        #plt.figure(figsize=(12, 12))
        crop_lst = set([c.rstrip('_1').rstrip('_2') for c in crop_lst])

        time_label = df.columns.unique(0)[0]

        #ax = plt.subplot(len(crop_lst), len(param_lst), 1)
        nrows, ncols = (len(crop_lst) + 1, len(param_lst) - 1) if any([x in ['first_stage_lambda', 'inn.fsl'] for x in param_lst])\
            else (len(crop_lst), len(param_lst))
        [param_lst.append(param_lst.pop(param_lst.index(x))) for x in param_lst if x in ['first_stage_lambda', 'inn.fsl']]

        fig, ax = plt.subplots(nrows, ncols, squeeze=False, sharex=True)

        axbig = None
        # prepare bottom plot for fsl if it is in the list of parmaeters
        if any([x in ['first_stage_lambda', 'inn.fsl'] for x in param_lst]):
            gs = ax[-1,0].get_gridspec()
            # remove the underlying axes
            for a in ax[-1, :]:
                a.remove()
            axbig = fig.add_subplot(gs[-1, :])


        for p, paramname in enumerate(param_lst):
            c = 0
            for i, cropname in enumerate(df[time_label, paramname].columns):

                # Special case for farm_level first_stage_lambda parameter
                if (paramname == 'first_stage_lambda' or paramname == 'inn.fsl') and len(crop_lst) > 1:
                    cropname = 'farm_level' if innovation else 'A'
                    print(paramname, cropname)
                    # ax = plt.subplot(len(crop_lst), len(param_lst), (c * len(param_lst)) + (p+1))
                    axbig.fill_between(ind, q95.loc[:, paramname, cropname], q5[:, paramname, cropname],
                                          edgecolor='w',
                                          facecolor='darkgray', alpha=0.5, **kwargs)
                    axbig.fill_between(ind, q75[:, paramname, cropname], q25[:, paramname, cropname], edgecolor='w',
                                          facecolor='dimgray', alpha=0.5, **kwargs)
                    axbig.fill_between(ind, q60[:, paramname, cropname], q40[:, paramname, cropname], edgecolor='w',
                                          facecolor='black', alpha=0.5, **kwargs)
                    axbig.plot(ind, mean[:, paramname, cropname], c=color, label=paramname, **kwargs)
                    axbig.set_ylabel(cropname, rotation=90, size='large')

                    # ax[c,p].legend()

                    if innovation:
                        axbig.axhline(c='k', alpha=0.5)
                    continue

                if not any([x in cropname for x in crop_lst]) and not (cropname == 'A' or cropname == 'farm_level'):
                    continue

                color = 'r'
                if '_' in cropname:
                    if cropname.split('_')[1] == '2':
                        color = 'b'
                        c = c -1



                print(paramname, cropname)
                #ax = plt.subplot(len(crop_lst), len(param_lst), (c * len(param_lst)) + (p+1))
                ax[c,p].fill_between(ind, q95.loc[:, paramname, cropname], q5[:, paramname, cropname], edgecolor='w',
                                facecolor='darkgray', alpha=0.5, **kwargs)
                ax[c,p].fill_between(ind, q75[:, paramname, cropname], q25[:, paramname, cropname], edgecolor='w',
                                facecolor='dimgray', alpha=0.5, **kwargs)
                ax[c, p].fill_between(ind, q60[:, paramname, cropname], q40[:, paramname, cropname], edgecolor='w',
                                      facecolor='black', alpha=0.5, **kwargs)
                ax[c,p].plot(ind, mean[:, paramname, cropname], c=color, label=paramname, **kwargs)
                ax[c,p].set_ylabel(cropname, rotation=90, size='large')

               # ax[c,p].legend()

                if innovation:
                    ax[c,p].axhline(c='k', alpha=0.5)
                c += 1


        # if fname is not None:
        if show:
            plt.tight_layout()
            plt.show()
        return fig, ax, axbig

    def plot_simulation_ensemble(self, fn_sim_ens, state_list = None, crop_list=None, **kwargs):


        df = pd.read_hdf(fn_sim_ens)

        if state_list is None:
            state_list = df.columns.tolist()
        if crop_list is None:
            crop_list = df.index.levels[1].tolist()

        fix, ax = plt.subplots(len(crop_list), len(state_list), squeeze=False)
        for p, statename in enumerate(state_list):
            for c, cropname in enumerate(crop_list):

                data = df[statename].unstack()[cropname]


                ax[c, p].hist(data, density=True, **kwargs)

                ax[c, p].set_xlabel(statename, size='large')
                #ax[c, p].set_ylabel(cropname, rotation=90, size='large')

        for ax, name in zip(ax[-1, :], state_list):
            ax.set_xlabel(name)

        for ax, name in zip(ax[:, 0], crop_list):
            ax.set_ylabel(name, rotation=90, size='large')

        plt.tight_layout()

        # if fname is not None:
        plt.savefig('test.pdf')
        plt.show()
