# -*- coding: latin-1 -*-

'''
    simu
    ~~~~

    An example to show how to initialize and run a simulation using CN-Wheat.

    :copyright: Copyright 2014 INRA-EGC, see AUTHORS.
    :license: TODO, see LICENSE for details.
    
    .. seealso:: Barillot et al. 2014.
'''

'''
    Information about this versioned file:
        $LastChangedBy$
        $LastChangedDate$
        $LastChangedRevision$
        $URL$
        $Id$
'''

import os

import pandas as pd

from cnwheat import simulation
from cnwheat import model

DATA_DIRPATH = 'data'

OUTPUT_FILEPATH = 'cnwheat_output.csv'

OUTPUT_PRECISION = 2

def setup_logging():
    '''Setup logging configuration
    '''
    import logging
    import logging.config
    ROOT_LOGGING_LEVEL = 'DEBUG'
    LOGGING_CONFIG = \
    {
        'version': 1,
        'formatters': {
            'verbose': {
                'format': '%(levelname)s - %(name)s - %(lineno)d - %(message)s'
            },
            'simple': {
                'format': '%(message)s'
            }
        },
        'handlers': {
            'console': {
                'level': 'WARNING',
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stdout',
                'formatter': 'verbose'
            },
            'file': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': 'debug.log',
                'maxBytes': 10485760,
                'backupCount': 100,
                'mode': 'w',
                'formatter': 'verbose'
            },
            'compartments_file': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': 'compartments.log',
                'maxBytes': 10485760,
                'backupCount': 100,
                'mode': 'w',
                'formatter': 'simple'
            },
            'derivatives_file': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': 'derivatives.log',
                'maxBytes': 10485760,
                'backupCount': 100,
                'mode': 'w',
                'formatter': 'simple'
            }
        },
        'loggers': {
            'cnwheat_compartments': {
                'level': 'DEBUG',
                'handlers': ['compartments_file'],
                'propagate': False
            },
            'cnwheat_derivatives': {
                'level': 'DEBUG',
                'handlers': ['derivatives_file'],
                'propagate': False
            }
        },
        'root': {
            'level': ROOT_LOGGING_LEVEL,
            'handlers': ['console', 'file']
        }
    }
    logging.config.dictConfig(LOGGING_CONFIG)
    
# setup logging
setup_logging()

def read_t_data(curr_data_dirpath, data_filename):
    data_filepath = os.path.join(curr_data_dirpath, data_filename)
    return pd.read_csv(data_filepath, sep=None, index_col='t', engine = 'python')


if __name__ == '__main__':
    organs = []
    # create the chaff
    name='Chaff'
    PAR_df = read_t_data(DATA_DIRPATH, 'PAR_%s.csv' % name)
    chaff = model.Chaff(area=0.00075, mstruct=0.21, width=0.02, height= 0.7, PAR=PAR_df.PAR,
                        starch_0=0, sucrose_0=0, triosesP_0=0, fructan_0=0, nitrates_0=0, amino_acids_0=0, proteins_0=0, name=name)
    organs.append(chaff)

    # create the internodes
    name='Internode'
    PAR_df = read_t_data(DATA_DIRPATH, 'PAR_%s.csv' % name)
    internode = model.Internode(area=0.0012, mstruct=0.148, width=0.042, height=0.4, PAR=PAR_df.PAR,
                                      starch_0=0, sucrose_0=0, triosesP_0=0, fructan_0=0, nitrates_0=0, amino_acids_0=0, proteins_0=0, name=name)
    organs.append(internode)

    # create the laminae
    name='Lamina'
    PAR_df = read_t_data(DATA_DIRPATH, 'PAR_%s.csv' % name)
    lamina = model.Lamina(area=0.00346, mstruct=0.14, width= 0.018, height=0.6, PAR=PAR_df.PAR,
                                    starch_0=0, sucrose_0=0, triosesP_0=0, fructan_0=0, nitrates_0=0, amino_acids_0=0, proteins_0=0, name=name)
    organs.append(lamina)

    # create the peduncles
    name = 'Peduncle'
    PAR_df = read_t_data(DATA_DIRPATH, 'PAR_%s.csv' % name)
    peduncle = model.Peduncle(area=0.00155, mstruct=0.168, width= 0.031, height=0.65, PAR=PAR_df.PAR,
                                        starch_0=0, sucrose_0=0, triosesP_0=0, fructan_0=0, nitrates_0=0, amino_acids_0=0, proteins_0=0, name=name)
    organs.append(peduncle)

    # create the sheaths
    name = 'Sheath'
    PAR_df = read_t_data(DATA_DIRPATH, 'PAR_%s.csv' % name)
    sheath = model.Sheath(area=0.0006, mstruct=0.103, width=0.042, height=0.5, PAR=PAR_df.PAR,
                                    starch_0=0, sucrose_0=0, triosesP_0=0, fructan_0=0, nitrates_0=0 , amino_acids_0=0, proteins_0=0, name=name)
    organs.append(sheath)

    # create the grains
    grains = model.Grains(starch_0=0, structure_0=10850, proteins_0=0, name='grains')
    organs.append(grains)

    # create the roots
    roots = model.Roots(mstruct=0.504, sucrose_0=0, nitrates_0=250, amino_acids_0=0, name='roots')
    organs.append(roots)

    # create the phloem
    phloem = model.Phloem(sucrose_0=0, amino_acids_0=0, name='phloem')
    organs.append(phloem)

    # get meteo data
    meteo_df = read_t_data(DATA_DIRPATH, 'meteo.csv')

    # initialize the simulator
    cnwheat_ = simulation.CNWheat(organs=organs, meteo=meteo_df)

    # run the model
    output_df = cnwheat_.run(start_time=0, stop_time=48, number_of_output_steps=7,
                             photosynthesis_computation_interval=4)
    
    output_df.to_csv(OUTPUT_FILEPATH, na_rep='NA', index=False, float_format='%.{}f'.format(OUTPUT_PRECISION))

    