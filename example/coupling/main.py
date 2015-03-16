# -*- coding: latin-1 -*-

'''
    main
    ~~~~

    An example to show how to couple CN-Wheat and Farquhar-Wheat.

    You must first install :mod:`cnwheat` and :mod:`farquharwheat` (and add them to your PYTHONPATH)
    before running this script with the command `python`.

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
import time, datetime

import logging
import logging.config
import json

import pandas as pd

from cnwheat import simulation
from cnwheat import model as cnwheat_model
from farquharwheat import model as photosynthesis_model
from cnwheat import tools

t0 = time.time()

DATA_DIRPATH = 'data'

PLANTS_OUTPUTS_FILENAME = 'plants_outputs.csv'
AXES_OUTPUTS_FILENAME = 'axes_outputs.csv'
PHYTOMERS_OUTPUTS_FILENAME = 'phytomers_outputs.csv'
ORGANS_OUTPUTS_FILENAME = 'organs_outputs.csv'
ELEMENTS_OUTPUTS_FILENAME = 'elements_outputs.csv'

OUTPUT_PRECISION = 6

LOGGING_CONFIG_FILEPATH = os.path.join('..', 'logging.json')

LOGGING_LEVEL = logging.INFO # set to logging.DEBUG for debugging

def setup_logging(config_filepath='logging.json', level=logging.INFO,
                  log_compartments=False, log_derivatives=False, log_model=False):
    """Setup logging configuration.

    :Parameters:

        - `config_filepath` (:class:`str`) - the file path of the logging
          configuration.

        - `level` (:class:`int`) - the global level of the logging. Use either
          `logging.DEBUG`, `logging.INFO`, `logging.WARNING`, `logging.ERROR` or
          `logging.CRITICAL`.

        - `log_compartments` (:class:`bool`) - if `True`, log the values of the compartments.
          `False` otherwise.

        - `log_derivatives` (:class:`bool`) - if `True`, log the values of the derivatives.
          `False` otherwise.

        - `log_model` (:class:`bool`) - if `True`, log the messages from :mod:`cnwheat.model`.
          `False` otherwise.

    """
    if os.path.exists(config_filepath):
        with open(config_filepath, 'r') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig()
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    logging.getLogger('cnwheat.compartments').disabled = not log_compartments # set to False to log the compartments
    logging.getLogger('cnwheat.derivatives').disabled = not log_derivatives # set to False to log the derivatives
    logging.getLogger('cnwheat.model').disabled = not log_model # set to False to log the derivatives

setup_logging(LOGGING_CONFIG_FILEPATH, LOGGING_LEVEL)


def read_t_data(curr_data_dirpath, data_filename):
    data_filepath = os.path.join(curr_data_dirpath, data_filename)
    return pd.read_csv(data_filepath, sep=None, index_col='t', engine = 'python')


if __name__ == '__main__':

    population = cnwheat_model.Population()

    plant = cnwheat_model.Plant(index=1)
    population.plants.append(plant)

    axis = cnwheat_model.Axis(axis_type='MS', index=0)
    plant.axes.append(axis)

    axis.grains = cnwheat_model.Grains(starch=0, structure=10850, proteins=170)

    axis.roots = cnwheat_model.Roots(mstruct=0.504, sucrose=0, nitrates=0, amino_acids=0)

    axis.phloem = cnwheat_model.Phloem(sucrose=0, amino_acids=0)

    # Phytomer 1
    phytomer1 = cnwheat_model.Phytomer(index=1)

    phytomer1.lamina = cnwheat_model.Lamina()
    lamina_element = cnwheat_model.LaminaElement(area=0.00346, mstruct=0.14, width= 0.018, height=0.6,
                                    starch=0, sucrose=0, triosesP=0, fructan=0, nitrates=0,
                                    amino_acids=0, proteins=380)
    phytomer1.lamina.elements.append(lamina_element)

    phytomer1.sheath = cnwheat_model.Sheath()
    sheath_element = cnwheat_model.SheathElement(area=0.0006, mstruct=0.103, width=0.042, height=0.5,
                                    starch=0, sucrose=0, triosesP=0, fructan=0,
                                    nitrates=0 , amino_acids=0, proteins=130)
    phytomer1.sheath.elements.append(sheath_element)

    # Internode enclosed
    phytomer1.internode = cnwheat_model.Internode()
    internode_element1 = cnwheat_model.InternodeElement(area=0.0012, mstruct=0.148, width=0.042, height=0.3,
                                          starch=0, sucrose=0, triosesP=0, fructan=0,
                                          nitrates=0, amino_acids=0, proteins=20, index=1, exposed=False)
    phytomer1.internode.elements.append(internode_element1)

    # Internode exposed
    internode_element2 = cnwheat_model.InternodeElement(area=0.0003, mstruct=0.04, width=0.042, height=0.4,
                                          starch=0, sucrose=0, triosesP=0, fructan=0,
                                          nitrates=0, amino_acids=0, proteins=90, index=2)
    phytomer1.internode.elements.append(internode_element2)

    axis.phytomers.append(phytomer1)

    # Phytomer 2
    phytomer2 = cnwheat_model.Phytomer(index=2)

    phytomer2.lamina = cnwheat_model.Lamina()
    lamina_element = cnwheat_model.LaminaElement(area=0.0034, mstruct=0.09, width= 0.014, height=0.38,
                                    starch=0, sucrose=0, triosesP=0, fructan=0, nitrates=0,
                                    amino_acids=0, proteins=210)
    phytomer2.lamina.elements.append(lamina_element)

    phytomer2.sheath = cnwheat_model.Sheath()
    sheath_element = cnwheat_model.SheathElement(area=0.0005, mstruct=0.069, width=0.043, height=0.3,
                                    starch=0, sucrose=0, triosesP=0, fructan=0,
                                    nitrates=0 , amino_acids=0, proteins=47)
    phytomer2.sheath.elements.append(sheath_element)

    phytomer2.internode = cnwheat_model.Internode()
    internode_element = cnwheat_model.InternodeElement(area=0.0004, mstruct=0.18, width=0.043, height=0.18,
                                          starch=0, sucrose=0, triosesP=0, fructan=0,
                                          nitrates=0, amino_acids=0, proteins=20)
    phytomer2.internode.elements.append(internode_element)

    axis.phytomers.append(phytomer2)

    # Phytomer 3
    phytomer3 = cnwheat_model.Phytomer(index=3)

    phytomer3.lamina = cnwheat_model.Lamina()
    lamina_element = cnwheat_model.LaminaElement(area=0.00228, mstruct=0.05, width= 0.0125, height=0.24,
                                    starch=0, sucrose=0, triosesP=0, fructan=0, nitrates=0,
                                    amino_acids=0, proteins=85)
    phytomer3.lamina.elements.append(lamina_element)

    phytomer3.sheath = cnwheat_model.Sheath()
    sheath_element = cnwheat_model.SheathElement(area=0.0004, mstruct=0.043, width=0.04, height=0.18,
                                    starch=0, sucrose=0, triosesP=0, fructan=0,
                                    nitrates=0 , amino_acids=0, proteins=13)
    phytomer3.sheath.elements.append(sheath_element)

    phytomer3.internode = cnwheat_model.Internode()
    internode_element = cnwheat_model.InternodeElement(area=0.00025, mstruct=0.154, width=0.04, height=0.08,
                                          starch=0, sucrose=0, triosesP=0, fructan=0,
                                          nitrates=0, amino_acids=0, proteins=0)
    phytomer3.internode.elements.append(internode_element)

    axis.phytomers.append(phytomer3)

    # Phytomer 4 (reproductive)
    phytomer4 = cnwheat_model.Phytomer(index=4)

    # Enclosed peduncle
    phytomer4.peduncle = cnwheat_model.Peduncle()
    peduncle_element1 = cnwheat_model.PeduncleElement(area=0.00155, mstruct=0.168, width= 0.031, height=0.65,
                                        starch=0, sucrose=0, triosesP=0, fructan=0, nitrates=0,
                                        amino_acids=0, proteins=30, index=1, exposed=False)
    phytomer4.peduncle.elements.append(peduncle_element1)

    # Exposed peduncle
    peduncle_element2 = cnwheat_model.PeduncleElement(area=0.00085, mstruct=0.089, width= 0.031, height=0.5,
                                        starch=0, sucrose=0, triosesP=0, fructan=0, nitrates=0,
                                        amino_acids=0, proteins=180, index=2)
    phytomer4.peduncle.elements.append(peduncle_element2)
    axis.phytomers.append(phytomer4)

    # Phytomer 5 (reproductive)
    phytomer5 = cnwheat_model.Phytomer(index=5)
    phytomer5.chaff = cnwheat_model.Chaff()
    chaff_element = cnwheat_model.ChaffElement(area=0.00075, mstruct=0.21, width=0.02, height= 0.7, starch=0,
                                  sucrose=0, triosesP=0, fructan=0, nitrates=0, amino_acids=0,
                                  proteins=260)
    phytomer5.chaff.elements.append(chaff_element)
    axis.phytomers.append(phytomer5)

    # Get PAR data
    data_file_path = os.path.join(DATA_DIRPATH, 'PAR.csv')
    PAR_dF = pd.read_csv(data_file_path)
    PAR_dF_grouped = PAR_dF.groupby(['t', 'plant', 'axis', 'phytomer', 'organ', 'element'])

    # get meteo data
    meteo_df = read_t_data(DATA_DIRPATH, 'meteo.csv')

    # initialize the model of CN exchanges
    cnwheat_ = simulation.CNWheat(population=population)

    # run the models
    start_time = 0
    stop_time = 960 # 960
    photosynthesis_model_ts = 2
    cn_model_ts = 1 #241

    all_plants_df_list = []
    all_axes_df_list = []
    all_phytomers_df_list = []
    all_organs_df_list = []
    all_elements_df_list = []

    for t_photosynthesis_model in xrange(start_time, stop_time, photosynthesis_model_ts):
        # update the population
        # run the model of photosynthesis and update the population
        for plant in population.plants:
            pid = plant.index
            for axis in plant.axes:
                axid = axis.id
                for phytomer in axis.phytomers:
                    phytoid = phytomer.index
                    for organ in (phytomer.chaff, phytomer.peduncle, phytomer.lamina, phytomer.internode, phytomer.sheath):
                        if organ is not None:
                            orgid = organ.__class__.__name__
                            for element in organ.elements:
                                eltid = element.index
                                PAR = PAR_dF_grouped.get_group((t_photosynthesis_model, pid, axid, phytoid, orgid, eltid)).PAR.values[0]
                                An, Tr = photosynthesis_model.PhotosynthesisModel.calculate_An(element.width,
                                    element.height, PAR, meteo_df['air_temperature'][t_photosynthesis_model],
                                    meteo_df['ambient_CO2'][t_photosynthesis_model], meteo_df['humidity'][t_photosynthesis_model],
                                    meteo_df['Wind'][t_photosynthesis_model])
                                element.An = An
                                element.Tr = Tr

        for t_cn_model in xrange(t_photosynthesis_model, t_photosynthesis_model + photosynthesis_model_ts, cn_model_ts):
            # update the population
            # run the model of CN exchanges ; the population is internally updated by the model of CN exchanges
            all_plants_df, all_axes_df, all_phytomers_df, all_organs_df, all_elements_df = cnwheat_.run(start_time=t_cn_model, stop_time=t_cn_model+cn_model_ts, number_of_output_steps=cn_model_ts+1)
            all_plants_df_list.append(all_plants_df)
            all_axes_df_list.append(all_axes_df)
            all_phytomers_df_list.append(all_phytomers_df)
            all_organs_df_list.append(all_organs_df)
            all_elements_df_list.append(all_elements_df)

    global_plants_df = pd.concat(all_plants_df_list, ignore_index=True)
    global_plants_df.drop_duplicates(subset=simulation.CNWheat.PLANTS_INDEXES, inplace=True)
    global_plants_df.to_csv(PLANTS_OUTPUTS_FILENAME, na_rep='NA', index=False, float_format='%.{}f'.format(OUTPUT_PRECISION))

    global_axes_df = pd.concat(all_axes_df_list, ignore_index=True)
    global_axes_df.drop_duplicates(subset=simulation.CNWheat.AXES_INDEXES, inplace=True)
    global_axes_df.to_csv(AXES_OUTPUTS_FILENAME, na_rep='NA', index=False, float_format='%.{}f'.format(OUTPUT_PRECISION))

    global_phytomers_df = pd.concat(all_phytomers_df_list, ignore_index=True)
    global_phytomers_df.drop_duplicates(subset=simulation.CNWheat.PHYTOMERS_INDEXES, inplace=True)
    global_phytomers_df.to_csv(PHYTOMERS_OUTPUTS_FILENAME, na_rep='NA', index=False, float_format='%.{}f'.format(OUTPUT_PRECISION))

    global_organs_df = pd.concat(all_organs_df_list, ignore_index=True)
    global_organs_df.drop_duplicates(subset=simulation.CNWheat.ORGANS_INDEXES, inplace=True)
    global_organs_df.to_csv(ORGANS_OUTPUTS_FILENAME, na_rep='NA', index=False, float_format='%.{}f'.format(OUTPUT_PRECISION))

    global_elements_df = pd.concat(all_elements_df_list, ignore_index=True)
    global_elements_df.drop_duplicates(subset=simulation.CNWheat.ELEMENTS_INDEXES, inplace=True)
    global_elements_df.to_csv(ELEMENTS_OUTPUTS_FILENAME, na_rep='NA', index=False, float_format='%.{}f'.format(OUTPUT_PRECISION))

    execution_time = int(time.time()-t0)
    print '\n', 'Model executed in ', str(datetime.timedelta(seconds=execution_time))


####POST-PROCESSING##
import os

graphs_dirpath = 'Graphs'
x_name = 't'
x_label='Time (Hour)'

# Photosynthetic organs
ph_elements_output_df = pd.read_csv(ELEMENTS_OUTPUTS_FILENAME)

graph_variables_ph_elements = {'An': u'Net photosynthesis (�mol m$^{-2}$ s$^{-1}$)', 'Transpiration':u'Organ transpiration (mm H$_{2}$0 h$^{-1}$)',
                   'Conc_TriosesP': u'[TriosesP] (�mol g$^{-1}$ mstruct)', 'Conc_Starch':u'[Starch] (�mol g$^{-1}$ mstruct)', 'Conc_Sucrose':u'[Sucrose] (�mol g$^{-1}$ mstruct)', 'Conc_Fructan':u'[Fructan] (�mol g$^{-1}$ mstruct)',
                   'Conc_Nitrates': u'[Nitrates] (�mol g$^{-1}$ mstruct)', 'Conc_Amino_Acids': u'[Amino_Acids] (�mol g$^{-1}$ mstruct)', 'Conc_Proteins': u'[Proteins] (g g$^{-1}$ mstruct)',
                   'Nitrates_import': u'Total nitrates imported (�mol h$^{-1}$)', 'Amino_Acids_import': u'Total amino acids imported (�mol N h$^{-1}$)',
                   'S_Amino_Acids': u'[Rate of amino acids synthesis] (�mol N g$^{-1}$ mstruct h$^{-1}$)', 'S_Proteins': u'Rate of protein synthesis (�mol N g$^{-1}$ mstruct h$^{-1}$)', 'D_Proteins': u'Rate of protein degradation (�mol N g$^{-1}$ mstruct h$^{-1}$)',
                   'Loading_Sucrose': u'Loading Sucrose (�mol C sucrose g$^{-1}$ mstruct h$^{-1}$)', 'Loading_Amino_Acids': u'Loading Amino acids (�mol N amino acids g$^{-1}$ mstruct h$^{-1}$)'}


for org_ph in (['Lamina'], ['Sheath'], ['Internode'], ['Peduncle', 'Chaff']):
    for variable_name, variable_label in graph_variables_ph_elements.iteritems():
        graph_name = variable_name + '_' + '_'.join(org_ph) + '.PNG'
        tools.plot(ph_elements_output_df,
                      x_name = x_name,
                      y_name = variable_name,
                      x_label=x_label,
                      y_label=variable_label,
                      filters={'organ': org_ph},
                      plot_filepath=os.path.join(graphs_dirpath, graph_name),
                      explicit_label=False)

# Roots, grains and phloem
organs_output_df = pd.read_csv(ORGANS_OUTPUTS_FILENAME)

graph_variables_ph_elements = {'Conc_Sucrose':u'[Sucrose] (�mol g$^{-1}$ mstruct)', 'Dry_Mass':'Dry mass (g)',
                    'Conc_Nitrates_Soil':u'[Nitrates] (�mol m$^{-3}$)','Conc_Nitrates': u'[Nitrates] (�mol g$^{-1}$ mstruct)', 'Conc_Amino_Acids':u'[Amino Acids] (�mol g$^{-1}$ mstruct)', 'Proteins_N_Mass': u'[N Proteins] (g)',
                    'Uptake_Nitrates':u'Nitrates uptake (�mol h$^{-1}$)', 'Unloading_Sucrose': u'Unloaded_Sucrose (�mol C sucrose g$^{-1}$ mstruct h$^{-1}$)', 'Unloading_Amino_Acids':u'Unloaded Amino Acids (�mol N AA g$^{-1}$ mstruct h$^{-1}$)',
                    'S_Amino_Acids': u'Rate of amino acids synthesis (�mol N g$^{-1}$ mstruct h$^{-1}$)', 'S_Proteins': u'Rate of protein synthesis (�mol N g$^{-1}$ mstruct h$^{-1}$)', 'Export_Amino_Acids': u'Total export of Amino acids (�mol N AA h$^{-1}$)'}

for org in (['Roots'], ['Grains'], ['Phloem']):
    for variable_name, variable_label in graph_variables_ph_elements.iteritems():
        graph_name = variable_name + '_' + '_'.join(org) + '.PNG'
        tools.plot(organs_output_df,
                      x_name = x_name,
                      y_name = variable_name,
                      x_label=x_label,
                      y_label=variable_label,
                      filters={'organ': org},
                      plot_filepath=os.path.join(graphs_dirpath, graph_name),
                      explicit_label=False)