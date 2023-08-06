import numpy as np

class ImpedanceData(object):
    def __init__(self, name, base_filename, *, w_data=None, f_data=None, z_real_data=None, z_imag_data=None, z_data=None):
        # self.logger = module_logger

        self.name = name
        self.base_filename = base_filename

        if f_data is not None:
            self.w_data = 2 * np.pi * f_data
        elif w_data is not None:
            self.w_data = w_data
        else:
            raise ValueError('Either w_data or f_data has to be given!')

        if z_data is not None:
            self.z_data = z_data
        elif z_real_data is not None and z_imag_data is not None:
            self.z_data = z_real_data + 1j*z_imag_data
        else:
            raise ValueError('Either z_data or z_real_data and z_imag_data have to be given!')

        if len(self.z_data) != len(self.w_data):
            raise ValueError('Data for z_data and w_data need to have same length!')            

          

