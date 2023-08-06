import sys
from pathlib import Path


# create logger
import os
import logging
from .main_logging import configure_colored_logger

os.system('COLOR 08')

logging.basicConfig(level=logging.INFO)
configure_colored_logger(remove_existing_handlers=True, level=logging.INFO)

module_logger = logging.getLogger('fipt')
module_logger.setLevel(logging.DEBUG)


# Load fipt analysis
import pandas as pd
import fipt


fn = sys.argv[1]
fn = str(Path(fn).resolve().absolute())

if not Path(fn).exists():
    raise FileNotFoundError(fn)

module_logger.info(f'Loading {fn}')



df = pd.read_csv(fn)
ipdata =  fipt.ImpedanceData(fn, fn, 
                   f_data = df.iloc[:, 0].values,  
                   z_real_data = df.iloc[:, 1].values, 
                   z_imag_data = df.iloc[:, 2].values)


symimfit = fipt.SymmetricImpedanceFitter(impedance_data=ipdata)        

result = symimfit.fit_auto(debug=True)

if symimfit.result_fns:
    for result_fn in symimfit.result_fns:
        if result_fn:
            module_logger.info(f'Result written to {result_fn}')

