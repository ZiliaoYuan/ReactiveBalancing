import os
import pyclbr
import shutil

from simses.commons.config.data.battery import BatteryDataConfig
from simses.commons.config.data.power_electronics import PowerElectronicsConfig
from simses.commons.config.data.energy_management import EnergyManagementDataConfig
from simses.commons.profile.technical import load_forecast
from simses.commons.utils.utilities import remove_file
from simses.logic.energy_management.strategy.basic import \
    peak_shaving_forecast_degradation_reduction
from simses.logic.energy_management.strategy.basic import \
    peak_shaving_yapsa

from simses.logic.energy_management.strategy.optimization import \
    peak_shaving_optimized_stochastic, peak_shaving_optimized
from simses.logic.energy_management.strategy.optimization.forecast_utils import \
    load_forecast_probability_density_function
from simses.logic.energy_management.strategy.optimization.forecast_utils import \
    probability_density_function
from simses.logic.energy_management.strategy.optimization.forecast_utils import \
    load_forecast_scenario_generation_function
from simses.logic.energy_management.strategy.optimization.forecast_utils import scenario_generation_function
from simses.logic.energy_management.strategy.optimization.linearized_models import \
    notton_acdc_converter_coefficients_lin_efficiency, lfp_sony_coefficients_lin_degradation, \
    coefficients_lin_degradation, coefficients_lin_efficiency, sony_lfp_cell_coefficients_lin_efficiency
from simses.logic.power_distribution import secondlife_ac, \
    secondlife_dc, regulation_based_strategy, linear_optimized_strategy, new_test_distributor
from simses.system.power_electronics.acdc_converter import aixcontrol
from simses.system.power_electronics.dcdc_converter import pgs
from simses.technology.lithium_ion.cell import nmc_samsung94Ah_labtests, nmc_akasol_akm as akm_cell, \
    nmc_akasol_oem as oem_cell, lfp_sony_gasper as sony_lfp_gasper_cell, nmc_samsung120Ah as nmc_samsung120ah_cell
from simses.technology.lithium_ion.cell import lfp_sony_multimodel as lfp_sony_multimodel
from simses.technology.lithium_ion.degradation import lfp_sony_multimodel as lfp_sony_multimodel_degradation
from simses.technology.lithium_ion.degradation.calendar import lfp_sony_multimodel as lfp_sony_multimodel_degradation_calendar
from simses.technology.lithium_ion.degradation.cyclic import lfp_sony_multimodel as lfp_sony_multimodel_degradation_cyclic
from simses.technology.lithium_ion.degradation import nrel as nrel_degradation, nmc_akasol_oem as oem_degradation, \
    nmc_akasol_akm as akm_degradation, nrel_2 as nrel_2_degradation, lfp_sony_gasper as sony_lfp_gasper_degradation, \
    nmc_samsung120ah as nmc_samsung120ah_degradation
from simses.technology.lithium_ion.degradation.calendar import nmc_akasol_akm as akm_calendar, \
    nmc_akasol_oem as oem_calendar, nrel as nrel_calendar, nrel_2 as nrel_2_calendar, lfp_sony_gasper as sony_lfp_gasper_calendar, \
    nmc_samsung120ah as nmc_samsung120ah_calendar
from simses.technology.lithium_ion.degradation.cyclic import nmc_akasol_akm as akm_cyclic, \
    nmc_akasol_oem as oem_cyclic, nrel as nrel_cyclic, nrel_2 as nrel_2_cyclic, lfp_sony_gasper as sony_lfp_gasper_cyclic, \
    nmc_samsung120ah as nmc_samsung120ah_cyclic


battery_data_config = BatteryDataConfig()
power_electronics_data_config = PowerElectronicsConfig()
energy_management_data_config = EnergyManagementDataConfig()

proprietary_modules: [str] = list()

proprietary_modules.append(aixcontrol)

proprietary_modules.append(pgs)

proprietary_modules.append(akm_cell)
proprietary_modules.append(akm_cyclic)
proprietary_modules.append(akm_degradation)
proprietary_modules.append(akm_calendar)

proprietary_modules.append(oem_cell)
proprietary_modules.append(oem_cyclic)
proprietary_modules.append(oem_degradation)
proprietary_modules.append(oem_calendar)
proprietary_modules.append(nmc_samsung94Ah_labtests)
proprietary_modules.append(lfp_sony_multimodel)
proprietary_modules.append(lfp_sony_multimodel_degradation)
proprietary_modules.append(lfp_sony_multimodel_degradation_calendar)
proprietary_modules.append(lfp_sony_multimodel_degradation_cyclic)
proprietary_modules.append(nmc_samsung120ah_cell)
proprietary_modules.append(nmc_samsung120ah_degradation)
proprietary_modules.append(nmc_samsung120ah_calendar)
proprietary_modules.append(nmc_samsung120ah_cyclic)

proprietary_modules.append(peak_shaving_forecast_degradation_reduction)
proprietary_modules.append(peak_shaving_yapsa)
proprietary_modules.append(peak_shaving_optimized)
proprietary_modules.append(peak_shaving_optimized_stochastic)
proprietary_modules.append(coefficients_lin_degradation)
proprietary_modules.append(lfp_sony_coefficients_lin_degradation)
proprietary_modules.append(coefficients_lin_efficiency)
proprietary_modules.append(notton_acdc_converter_coefficients_lin_efficiency)
proprietary_modules.append(sony_lfp_cell_coefficients_lin_efficiency)
proprietary_modules.append(probability_density_function)
proprietary_modules.append(load_forecast_probability_density_function)
proprietary_modules.append(scenario_generation_function)
proprietary_modules.append(load_forecast_scenario_generation_function)
proprietary_modules.append(nrel_degradation)
proprietary_modules.append(nrel_cyclic)
proprietary_modules.append(nrel_calendar)
proprietary_modules.append(nrel_2_degradation)
proprietary_modules.append(nrel_2_cyclic)
proprietary_modules.append(nrel_2_calendar)
proprietary_modules.append(sony_lfp_gasper_cell)
proprietary_modules.append(sony_lfp_gasper_degradation)
proprietary_modules.append(sony_lfp_gasper_calendar)
proprietary_modules.append(sony_lfp_gasper_cyclic)
proprietary_modules.append(new_test_distributor)


proprietary_modules.append(load_forecast)


proprietary_modules.append(secondlife_ac)
proprietary_modules.append(secondlife_dc)
proprietary_modules.append(regulation_based_strategy)
proprietary_modules.append(linear_optimized_strategy)


proprietary_files: [str] = list()
for module in proprietary_modules:
    proprietary_files.append(module.__file__)
proprietary_files.append(power_electronics_data_config.aixcontrol_efficiency_file)
proprietary_files.append(power_electronics_data_config.pgs_efficiency_file)
proprietary_files.append(battery_data_config.nmc_akasol_oem_current_file)
proprietary_files.append(battery_data_config.nmc_akasol_oem_ocv_file)
proprietary_files.append(battery_data_config.nmc_akasol_akm_rint_file)
proprietary_files.append(battery_data_config.nmc_akasol_akm_ocv_file)
proprietary_files.append(battery_data_config.nmc_akasol_akm_rint_file)
proprietary_files.append(battery_data_config.nmc_samsung_120ah_ocv_file)
proprietary_files.append(battery_data_config.nmc_samsung_120ah_rint_file)
proprietary_files.append(battery_data_config.nmc_samsung_120ah_capacity_cal_file)

proprietary_files.append(energy_management_data_config.linear_cyc_degradation_sony_lfp_file)
proprietary_files.append(energy_management_data_config.linear_cal_degradation_sony_lfp_file)
proprietary_files.append(energy_management_data_config.linear_efficiency_notton_acdc_file)
proprietary_files.append(energy_management_data_config.linear_efficiency_sony_lfp_file)


def contains(search_strings: [str], lines: [str]) -> bool:
    for search_string in search_strings:
        if any(search_string in line for line in lines):
            return True
    return False


def remove_occurrences_in_all_files_of_directory(directory: str, ext: str, search_strings: [str]) -> None:
    #print(directory)
    # search_string = search_string.replace(ext, '')
    for item in os.listdir(directory):
        filename = os.path.join(directory, item)
        if os.path.isfile(filename) and filename.endswith(ext):
            # print(filename, search_string)
            tmp_file: str = filename + '.tmp'
            # remove_file(tmp_file)
            file_modified: bool = False
            with open(filename, 'r') as infile:
                try:
                    lines = infile.readlines()
                    if contains(search_strings, lines):
                        file_modified = True
                        with open(tmp_file, 'w') as outfile:
                            for line in lines:
                                if not contains(search_strings, [line.split(' ')]):
                                    outfile.write(line)
                except UnicodeDecodeError as err:
                    print('Error in ' + filename + ': ' + str(err))
            if file_modified:
                print('Modifying ' + filename)
                shutil.copy(tmp_file, filename)
                remove_file(tmp_file)
        # recursive search
        if os.path.isdir(filename):
            remove_occurrences_in_all_files_of_directory(filename, ext, search_strings)


for module in proprietary_modules:
    search_strings: [str] = list()
    # print(module.__name__)
    module_info = pyclbr.readmodule(module.__name__)
    for module_cls in module_info.values():
        # print(module_cls.name)
        search_strings.append(module_cls.name)
    search_strings.append(module.__name__)
    # print(search_strings)
    # remove_occurrences_in_all_files_of_directory(os.path.dirname(simses.__file__), '.py', search_strings)

for file in proprietary_files:
    print(file)
    remove_file(file)
