import os
import sys
import importlib
import logging
import re 

import typing

from pathlib import Path
from collections import defaultdict, OrderedDict

import numpy as np
import scipy as sp
# import pandas as pd
import lmfit

import json
from copy import deepcopy


try:
    import matplotlib.pyplot as plt
except ModuleNotFoundError:
    plt = None




# from barely_db import BarelyDBEntity, BUIDParser, FileNameAnalyzer

# from . import udr, buid_parser, serialize_to_file
# # from . import udr, buid_parser, serialize_yaml_from_cattr, serialize_to_file
# from . import patterned_input_to_dict, OLSEstimatorUnits

# from .battery_quantities import battery_attrib
# from .eq_model import EqModel

# from .utils import *
# from .material_data import *
# from .equipment import PunchCutterSpecification

# from .web import WebValidationMeasurementNeg, WebSpecificationNeg

# from .reporting import BasicReport, format_unit

# from .elan.impedance import SquidStatEISImporter, SymmetricImpedanceFitter, ComplexImpedancePlotter # formerly known as 'iman'

from .helpers import round_to_n, make_log_likelihood_function, make_complex_model_wrapper
from .impedance_data import ImpedanceData
from .plotting import ComplexImpedancePlotter, ImpedanceVsFreqPlotter


__all__ = ['FastImpedanceRawData', 'FastImpedancePrimaryAnalyzer', 'FastImpedanceSingleTrace',
            'LegacyFastImpedanceSingleTraceLoader', 'NMMeasurementView', 'NMMeasurementViewer',
           'WebRegionNMMeasurement', 'WebNMMeasurement']

# create logger
module_logger = logging.getLogger(__name__)
module_logger.setLevel(logging.DEBUG)

# general useful module components
def _reload_module():
    import sys
    import importlib
    current_module = sys.modules[__name__]
    module_logger.info('Reloading module %s' % __name__)
    importlib.reload(current_module)
   
    






# this class is structured similar to lmfit.Model
class SymmetricImpedanceFitter(object):

    _min_datapoints = 5
    result_fns = None

    assessment_min_z_lf_angle = -50 # degree
    assessment_max_z_abs_multiplier = 6 # by how much is the resistance at the transition frequency multiplied to get a good max_z_abs estimator


    @staticmethod
    def z_symmetric_impedance(w, r_sep, r_ion, gamma, q_s):
        z = ((r_ion / (q_s * (1j * w) ** gamma)) ** (1 / 2)) * \
                    1 / (np.tanh((r_ion * q_s * (1j * w) ** gamma) ** (1 / 2))) + \
                    r_sep
        return z

    @staticmethod
    def z_symmetric_impedance_w_short(w, r_sep, r_ion, gamma, q_s, r_short):
        z = 1/(1/r_short + \
               1/(((r_ion / (q_s * (1j * w) ** gamma)) ** (1 / 2)) * \
                    1 / (np.tanh((r_ion * q_s * (1j * w) ** gamma) ** (1 / 2))) + \
                    r_sep))
        return z
    
    
    # @staticmethod
    def make_params(self):
        # create a set of Parameters
        params = lmfit.Parameters()
        params.add('r_sep', value=30, min=2)
        params.add('r_ion', value=300, min=10)
        params.add('gamma', value=0.8, min=0.5, max=1.3)
        params.add('q_s', value=0.018)    
        
        if self.model == 'with_short':
            params.add('r_short', value=10000, min=0)    
            
        return params

    def __init__(self, impedance_data, 
                 model='normal', 
                 likelihood_config = dict(name='normal', scale=1)):      
        
        
        self.logger = module_logger

        self.load_data(impedance_data)

        self.show_guess_plots = False
        
        # create a model function that can be used for fitting
        self.configure_model(model)
        self.configure_likelihood(likelihood_config)
        
#        self.model = model
#        if model == 'normal':
#            self.m_func, self.ll_func = make_complex_model_wrapper(self.z_symmetric_impedance)
#        elif model == 'with_short':
#            self.m_func, self.ll_func = make_complex_model_wrapper(self.z_symmetric_impedance_w_short)
#        else:
#            self.logger.warning(f'Model "{model}" not supported!')

        # restricts fitting to small z values
        self.max_z_abs = None
        self.min_w = None
            
        self.last_params = self.make_params()

    def load_data(self, impedance_data):
        
        if len(impedance_data.w_data) < self._min_datapoints:
            raise ValueError(f'Impedance data has not enough data points! Need >= {self._min_datapoints}')            

        self.w_data = impedance_data.w_data
        self.z_data = impedance_data.z_data
        self.name = impedance_data.name
        self.base_file_name = impedance_data.base_filename

    def sanitize_data(self):
        self.logger.info('Removing data points with -Im(Z)<0')
        sel = self.z_data.imag < 0
        if not any(sel):
            self.logger.warning('No points would survive sanitation! Keeping all points!')
        else:
            self.w_data = np.extract(self.z_data.imag < 0, self.w_data)
            self.z_data = np.extract(self.z_data.imag < 0, self.z_data)        

    def eval(self, params=None):
        ''' Evaluates the model for a given parameter set.
        '''
        eval_w_data = self.w_data.copy()
        
        if params is None:
            params = self.last_params
        eval_z_data = self.m_func(params, x=eval_w_data)
        
        return eval_w_data, eval_z_data

    def assert_data_ok(self):
        ''' Throws an exception if the data is not ok!
        '''
        assert(len(self.w_data) == len(self.z_data))

    def configure_model(self, model):
        # create a model function that can be used for fitting
        self.model = model
        if model == 'normal':
            self.z_model = self.z_symmetric_impedance
            self.logger.info(f'Analytic model "{model}" set!')
        elif model == 'with_short':
            self.z_model = self.z_symmetric_impedance_w_short
            self.logger.info(f'Analytic model "{model}" set!')
        else:
            self.z_model = None
            self.logger.warning(f'Analytic model "{model}" not supported!')

    def configure_likelihood(self, likelihood_config = dict(name='normal', scale=1)):
        llf = make_log_likelihood_function(**likelihood_config)

        self.m_func, self.ll_func = make_complex_model_wrapper(self.z_model, 
                                                               likelihood_func = llf)
        
#        if model == 'normal':
#            self.m_func, self.ll_func = make_complex_model_wrapper(self.z_symmetric_impedance)
#        elif model == 'with_short':
#            self.m_func, self.ll_func = make_complex_model_wrapper(self.z_symmetric_impedance_w_short)
#        else:
#            self.logger.warning(f'Model "{model}" not supported!')
        
    def estimate_transition_frequency(self, w_data, z_data, make_plots=None):
        ''' This function estimates the transition frequency 
        that corresponds to the kink in the symmetric impedance
        plot.
        '''
        if make_plots is None:
            make_plots = self.show_guess_plots
        
        z_data_diff = np.diff(z_data)
        
        # look at angle vs Re(Z)
        z_angle = np.angle(z_data_diff)/np.pi*180
        z_angle_pos = z_data.real[:-1]
        z_angle_weight = np.diff(z_data.real)
        angle_mean = np.mean(z_angle_pos * z_angle)/np.mean(z_data.real[:-1])
        
        if make_plots:
            f, ax = plt.subplots()
            ax.plot(z_angle_pos, z_angle, 'o')
            print('angle_mean: %f' % angle_mean)

        # determine the position of the step in angle
        # by the maximum of angle integral (with 0 mean!)
        z_angle_int = np.cumsum((z_angle-angle_mean)*z_angle_weight)
        z_angle_max_i = np.argmax(z_angle_int)
        w_trans = w_data[z_angle_max_i]
        
        module_logger.info('z_angle_max_i: %d' % z_angle_max_i)
        module_logger.info('w_trans: %f' % w_trans)

        if make_plots:
            f, ax = plt.subplots()
            # ax.plot(z_data_diff.real, -z_data_diff.imag)
            ax.plot(z_angle_pos, z_angle_int, 'o')        
            
        if z_angle_max_i == 0 or z_angle_max_i == len(z_angle_int):
            module_logger.warning('transition frequeny could not be determined!')
            w_trans = None

        return w_trans


    def assess_data(self, w_data=None, z_data=None, make_plots=None):

        if z_data is None:
            z_data = self.z_data    
        
        if w_data is None:
            w_data = self.w_data    

        if make_plots is None:
            make_plots = self.show_guess_plots

        if plt is None and make_plots:
            self.logger.error(f'Matplotlib not available. Cannot make plots!')
            make_plots = False

        # determine transition frequency, where the kink happens
        w_trans = self.estimate_transition_frequency(w_data, z_data, make_plots=make_plots)

        # determine if there is a short in the measurement
        w_min_i = np.argmin(w_data)
        z_lf_angle = np.angle(z_data[w_min_i])
        z_angle_min = np.min(np.angle(z_data))

        has_short = False
        # has_short |=  z_lf_angle > z_angle_min          # if angle goes up at low frequencies, probably shorted
        has_short |=  (z_lf_angle * 180 / np.pi) > self.assessment_min_z_lf_angle  # if the sample is not capacitive enough, probably shorted!


        if w_trans is not None:
            w_trans_i = np.argmin(np.abs(w_data-w_trans))
            z_w_trans = np.abs(z_data)[w_trans_i]
            max_z_abs = self.assessment_max_z_abs_multiplier*z_w_trans,
        else:
            z_w_trans = None
            max_z_abs = None 


        assessment = dict(w_trans=w_trans, 
                          z_w_trans=z_w_trans,
                          max_z_abs=max_z_abs,
                          has_w_trans = w_trans is not None,
                          has_short=has_short, )

        self.logger.info(f'Data assessment: {assessment}')

        return assessment


    def guess(self, w_data=None, z_data=None, make_plots=None):
        if z_data is None:
            z_data = self.z_data    
        
        if w_data is None:
            w_data = self.w_data    

        if make_plots is None:
            make_plots = self.show_guess_plots

        if plt is None and make_plots:
            self.logger.error(f'Matplotlib not available. Cannot make plots!')
            make_plots = False

        # setup parameters
        params  = self.make_params()
        params['r_sep'].set(value = 2*np.min(np.abs(z_data.real)))
        params['r_ion'].set(value = 10*2*np.min(np.abs(z_data.real)))
        params['gamma'].set(value = 0.8)
        params['q_s'].set(value = 0.002)

        if self.model == 'with_short':
            params['r_short'].set(value = 10*np.max(z_data.real))
        

        # improve estimation
        w_trans = self.estimate_transition_frequency(w_data, z_data, make_plots=make_plots)
        if w_trans is None:
            self.logger.error(f'Could not determine transition frequency! Might not be a valid dataset!')
        else:
            w_factor = 1.4
            w_low_top = w_trans / w_factor
            w_high_bottom = w_trans * w_factor

            z_data_high = np.extract(w_data > w_high_bottom, z_data)
            z_data_low = np.extract(w_data < w_low_top, z_data)
            
            high_slope,high_intercept, high_r_value, high_p_value, high_std_err = \
                sp.stats.linregress(z_data_high.real, -z_data_high.imag)
            
            low_slope, low_intercept, low_r_value, low_p_value, low_std_err = \
                sp.stats.linregress(z_data_low.real, -z_data_low.imag)

            if make_plots:
                fit_high_imag = z_data_high.real * high_slope + high_intercept
                fit_low_imag = z_data_low.real * low_slope + low_intercept

                f, ax = plt.subplots()
                # ax.plot(z_data.real, -z_data.imag, marker = 'o', label = 'data')
                ax.plot(z_data_high.real, -z_data_high.imag,  marker = 'o', label = 'high ω data')
                ax.plot(z_data_low.real, -z_data_low.imag,  marker = 'o',  label = 'low ω data')
                ax.plot(z_data_high.real, fit_high_imag,  label = 'high ω fit')
                ax.plot(z_data_low.real, fit_low_imag,  label = 'low ω fit')
                ax.set_aspect('equal')
                ax.set_adjustable('datalim')

                ax.set_title('Two part linear fit estimation')
                ax.set_xlabel('Re(Z) (Ω)', fontsize = 18)
                ax.set_ylabel('-Im(Z) (Ω)', fontsize = 18)
                ax.legend()
                f.tight_layout()
                

            params['r_sep'].set(value = - high_intercept / high_slope)
            # params['r_low'].set(value = - low_intercept / low_slope)
            r_low = - low_intercept / low_slope
            params['r_ion'].set(value = (r_low - params['r_sep']) * 3)
            params['gamma'].set(value = np.arctan(low_slope)/(np.pi/2))
            


        self.last_params = params        

        return params

       
    def set_max_z_abs(self, value):
        self.max_z_abs = value
        self.logger.warning(f'Data is restricted to <{self.max_z_abs}Ohm. Reset with set_max_z_abs(None)')

    def set_min_w(self, value):
        self.min_w = value
        self.logger.warning(f'Data is restricted to <{self.min_w}Ohm. Reset with set_min_w(None)')
                
    def _get_current_fit_data(self, do_crop=True):
        w_data = self.w_data.copy()
        z_data = self.z_data.copy()
        
        if do_crop and (self.max_z_abs is not None):
            self.logger.info(f'Data is restricted to |Z| < {self.max_z_abs} Ohm')
            data_sel = np.abs(z_data) < self.max_z_abs
            z_data = z_data[data_sel]
            w_data = w_data[data_sel]

        if do_crop and (self.min_w is not None):
            self.logger.info(f'Data is restricted to >{self.min_w} rad/s')            
            data_sel = w_data > self.min_w
            z_data = z_data[data_sel]
            w_data = w_data[data_sel]            
            
        return {'x': w_data, 'data': z_data, 'eps': 1}
        
    def fit_auto(self, start_params=None, crop_data = True, crop_multiple = 6, 
                       max_z_abs = None, save_results = True, display_results=False,
                       auto_model = True,
                       export_folder=None, plot_save_kwds = {}, 
                       likelihood_config = dict(name='t', scale=1, df=1),
                       debug=False):
            
        self.sanitize_data()


        # assess dataset 
        assessment = self.assess_data(make_plots=debug)

        if auto_model:
            # choose right model
            if assessment['has_short']:
                self.configure_model('with_short')

        # restrict data range
        self.set_min_w(None)

        max_z_abs = max_z_abs or assessment['max_z_abs']
        self.set_max_z_abs(max_z_abs)

        # use student t likelihood function
        self.configure_likelihood(likelihood_config=likelihood_config)


        # guess start parameters
        start_params_1 = self.guess(make_plots=debug)

        # apply manual overrides
        if start_params:
            for key, val in start_params.items():
                start_params_1[key].set(value=val)

        result = self.fit()        
        
        if save_results or display_results:
            fit_report_str = lmfit.fit_report(result, show_correl=False)
            f, ax = self.plot_fit(start_params = start_params_1);
        
        if display_results:
            self.logger.info(fit_report_str)
            f.show()

        if save_results:
            self.result_fns = self.save_results(export_folder=export_folder, plot_save_kwds=plot_save_kwds,plot_figure=f)
        else:
            self.result_fns = None

        
        return result        
        
    def fit(self, start_params=None):
        if start_params is None:
            start_params = self.last_params

#         if z_data is None:
#             z_data = self.z_data

        self.assert_data_ok()

        # do fit, here with leastsq model
        minner = lmfit.Minimizer(self.m_func, start_params, fcn_kws=self._get_current_fit_data())
        self.result = minner.minimize()

        if self.result.success:
            self.last_params = self.result.params

        return self.result


    def plot_fit(self, w_data = None, z_data=None, z_data_fit=None, params=None, start_params=None, data_only=False, plot_params=True):             
        if plt is None:
            self.logger.error(f'Matplotlib not available. Cannot make plots!')
            return None, None


        plot_title = self.name

        if w_data is None:
            w_data = self.w_data            

        if z_data is None:
            z_data = self.z_data

        if not data_only:
            if start_params is None:
                w_data_fit_start, z_data_fit_start = None, None
            else:    
                w_data_fit_start, z_data_fit_start = self.eval(start_params)

            if z_data_fit is None:
                if params is None:
                    params = self.last_params
                w_data_fit, z_data_fit = self.eval(params)

        else:
            plot_params = False


        if self.max_z_abs is not None:
            data_limited = self._get_current_fit_data()             
            z_data_limited = data_limited['data']
            w_data_limited = data_limited['x']


        f, axes = plt.subplots(nrows=1, ncols=3, figsize=(18, 6))

        plot_opts_data = dict( marker = 'o', label='data')
        plot_opts_data_selected = dict( marker = 'o', color='green', label='data selected')
        plot_opts_fit = dict(color='red',  label='fit')
        plot_opts_fit_start = dict(color='lightgray', label='fit start')

        impax = ComplexImpedancePlotter(axes[0], plot_title)
        impax.plot_complex(z_data, **plot_opts_data)
        if self.max_z_abs is not None:
            impax.plot_complex(z_data_limited, **plot_opts_data_selected)
        
        if not data_only:
            impax.plot_complex(z_data_fit, **plot_opts_fit)
            if z_data_fit_start is not None:
                impax.plot_complex(z_data_fit_start, **plot_opts_fit_start)
        impax.finalize()

        impax = ImpedanceVsFreqPlotter(axes[1], plot_title)
        impax.plot_abs(w_data, z_data, **plot_opts_data)
        if self.max_z_abs is not None:
            impax.plot_abs(w_data_limited, z_data_limited, **plot_opts_data_selected)

        if not data_only:
            impax.plot_abs(w_data, z_data_fit, **plot_opts_fit)
            if z_data_fit_start is not None:
                impax.plot_abs(w_data, z_data_fit_start, **plot_opts_fit_start)
        impax.finalize()

        impax = ImpedanceVsFreqPlotter(axes[2], plot_title)
        impax.plot_angle(w_data, z_data, **plot_opts_data)
        if self.max_z_abs is not None:
            impax.plot_angle(w_data_limited, z_data_limited, **plot_opts_data_selected)

        if not data_only:
            impax.plot_angle(w_data, z_data_fit, **plot_opts_fit)
            if z_data_fit_start is not None:
                impax.plot_angle(w_data, z_data_fit_start, **plot_opts_fit_start)
        impax.finalize()

        if plot_params:
            props = dict(boxstyle='square', facecolor='wheat', alpha=0.65)
            param_report_text = self.make_params_text()

            # place a text box in upper left in axes coords
            ax = axes[0]
            ax.text(0.05, 0.95, param_report_text[0], transform=ax.transAxes, fontsize=10,
                    verticalalignment='top', bbox=props)        
            
            if param_report_text[1] is not None:
                ax = axes[1]
                ax.text(0.15, 0.95, param_report_text[1], transform=ax.transAxes, fontsize=7,
                        verticalalignment='top', zorder=-2, bbox=props)        

        
        if params: 
            plot_scale = 2*params['r_ion'].value

            axes[0].set_xlim(0, plot_scale)
            axes[0].set_ylim(0, plot_scale)


        f.tight_layout()
        
        return f, axes

    
    def make_params_text(self):
        params_text = 'No parameters available!'
        report_text = None
        
        try:
            result =  self.result
            report_text = lmfit.fit_report(result)            
        except AttributeError as e:
            pass

        # try last parameters as fall back
        try:
            params =  self.last_params.valuesdict()
            for k in params:
                params[k] = round_to_n(params[k], 4)            
            
            params_text = json.dumps(dict(params), indent=2)
            params_text = 'Used parameters: ' + params_text
        except AttributeError as e:
            pass

        # fail graciously
        return (params_text, report_text)

            

    def fit_result_to_json(self, result=None):
        if result is None:
            result = self.result
        
        class ParametersEncoder(json.JSONEncoder):
            def default(self, obj):
                if isinstance(obj, lmfit.parameter.Parameters):
                    return obj.dumps()
                    # Let the base class default method raise the TypeError
                if isinstance(obj, np.ndarray):
                    return obj.tolist()
                if isinstance(obj, np.bool_):
                    return bool(obj)        

                return json.JSONEncoder.default(self, obj)

        result_json = result.__dict__.copy()
        result_json['params_table'] = result_json['params'].pretty_print()
        result_json['params_repr'] = result_json['params'].pretty_repr()
        result_json['params'] = json.loads(result_json['params'].dumps())  
        result_json = json.dumps(result_json, cls=ParametersEncoder, sort_keys=True, indent=4)
        
        return result_json


    def save_results(self, base_file_name=None, title=None, export_folder=None, plot_save_kwds = {}, plot_figure = None):
        if title is None:
            title = self.name

        if base_file_name is None:
            base_file_name = self.base_file_name
            self.logger.info('Using base file name: %s' % base_file_name)

        if export_folder is not None:
            export_folder = Path(export_folder)
            export_folder.mkdir(parents=True, exist_ok=True)
            base_file_name = export_folder.joinpath(Path(base_file_name).name)
            self.logger.info('Using export folder: %s' % export_folder)

        base_file_name = str(base_file_name)
    
        raw_data_fn = None
        # sorry this is a mess...: 
        # df = pd.DataFrame(self._get_current_fit_data(do_crop=False))
        # df = df.rename(columns={'x': 'w_data', 'data': 'z_data'}).drop(columns='eps') 
        # params = self.last_params
        # w_data_fit, z_data_fit = self.eval(params)
        # df['z_data_fit'] = pd.Series(z_data_fit, index=df.index)      
        # df.to_hdf(raw_data_fn, key='EISdata')
                
        try:
            result =  self.result
            do_export_result = True
        except AttributeError as e:
            self.logger.warning('No fitting results to export!')
            do_export_result = False

        report_fn, result_fn, params_fn, params_simp_fn, fitplot_fn = None, None, None, None, None

        if do_export_result:
            report_fn = base_file_name + '.fit.report.txt'
            report_text = lmfit.fit_report(result)
            with open(report_fn, 'w') as f:
                f.write(report_text)
            
            result_fn = base_file_name + '.fit.result_full.json'
            result_json  = self.fit_result_to_json(result)
            with open(result_fn, 'w') as f:
                f.write(result_json )

            json_params = dict(indent=4)
            params_fn = base_file_name + '.fit.result_params.json'
            params_json  = result.params.dumps(**json_params)
            with open(params_fn, 'w') as f:
                f.write(params_json )

            params_simp_fn = base_file_name + '.fit.result_simple.json'
            params_simp = result.params.valuesdict()
            params_simp['chisqr'] = result.chisqr
            params_simp_json  = json.dumps(dict(params_simp), **json_params)
            with open(params_simp_fn, 'w') as f:
                f.write(params_simp_json )

        if plt is None:
            self.logger.error(f'Matplotlib not available. Cannot make plots!')
            make_plots = False
            fitplot_fn = None
        else:
            fitplot_fn = base_file_name + '.fit.plot.png'
            if plot_figure is None:        
                plot_figure, axes = self.plot_fit();
            plot_figure.savefig(fitplot_fn, **plot_save_kwds)
            plt.close(plot_figure)

        return raw_data_fn, report_fn, result_fn, params_fn, params_simp_fn, fitplot_fn



class TortuosityCalculator(object):
    def __init__(self, data):
        self.data = data
        
    # checked on 180613
    def calc_tortuosity(self, data=None):
        df = self.data if data is None else data
        
        if 'area' not in df:
            df['area'] = np.pi * (df['diameter']/2) ** 2

        df['n_m'] = (df['r_ion'] *  df['area'] * df['el_conductivity']) / (2 * df['thickness'])
            
        if 'density' not in df:
            df['density'] = df['loading']/df['thickness']           
        
        df['porosity'] = 1 - df['density']/df['density_solid']

        df['tau'] = df['n_m'] * df['porosity']
        df['alpha'] = -(np.log10(df['n_m']) / np.log10(df['porosity'])) - 1   

        # df['alpha2'] = -(np.log10(df['tau']) / np.log10(df['porosity'])) samesame
        return df