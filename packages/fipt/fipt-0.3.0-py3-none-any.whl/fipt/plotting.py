import logging
import textwrap

import numpy as np
# import scipy as sp
# import pandas as pd


__all__ = ['ComplexImpedancePlotter', 'ImpedanceVsFreqPlotter']

# create logger
module_logger = logging.getLogger(__name__)
module_logger.setLevel(logging.DEBUG)


class ComplexImpedancePlotter(object):
    
    def __init__(self, ax, title):
        self.ax = ax

        ax.set_aspect('equal')
        ax.set_adjustable('datalim')
      
        ax.set_xlabel('Re(Z) (Ω)', fontsize = 18)
        ax.set_ylabel('-Im(Z) (Ω)', fontsize = 18)

        self.set_title(title)
        pass  
    
    def set_title(self, title, title_wrap = 25):
        self.ax.set_title("\n".join(textwrap.wrap(title, title_wrap)))
            
    def plot_complex(self, z_data, **kwds):
        ''' Plots impedance data. Passes all keywords to plt.plot.
        '''
        self.ax.plot(z_data.real, -z_data.imag, **kwds)
    
    def finalize(self):
        self.ax.legend()
        # ax.figure.tight_layout()
        
    def get_axis(self):
        return self.ax
        
        

class ImpedanceVsFreqPlotter(object):
    
    def __init__(self, ax, title):
        self.ax = ax
#         ax.set_aspect('equal')
#         ax.set_adjustable('datalim')

        ax.set_xlabel('Frequency (Hz)', fontsize = 18)
        ax.set_xlim([0.01, 1000000])
                
        self.set_title(title)
        pass  
    
    def set_title(self, title, title_wrap = 25):
        self.ax.set_title("\n".join(textwrap.wrap(title, title_wrap)))
                
    def plot_abs(self, w_data, z_data, **kwds):
        ''' Plots impedance data. Passes all keywords to plt.loglog.
        '''
        z_data_abs = np.absolute(z_data)
        self.ax.loglog(w_data, z_data_abs, **kwds)
        self.ax.set_ylabel('|Z| (Ω)', fontsize = 18)
        self.ax.set_ylim([10, 10000])

    def plot_angle(self, w_data, z_data, **kwds):
        ''' Plots impedance data. Passes all keywords to plt.semilogx.
        '''
        z_data_angle = np.angle(z_data) / np.pi * 180
        self.ax.semilogx(w_data, z_data_angle, **kwds)
        self.ax.set_ylabel(r'$\varphi$(Z)', fontsize = 18)
        self.ax.set_ylim([-80, 70])
        
    def finalize(self):
        self.ax.legend(loc = 'upper right')
        self.ax.figure.tight_layout()
        
    def get_axis(self):
        return self.ax    