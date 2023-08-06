import os
import numpy as np
import pandas as pd


class Energy_Systems:
    """ A class of methods to initialise energy sytems and create the data/model files needed for optimisation.
    """
    def __init__(self, year, region, emission, technology, capacity_technology,
                 availability_technology, fuel, specified_fuel,
                 accumulated_fuel, timeslice, mode_of_operation, storage,
                 daytype, season, dailytimebracket):
        """ Function to create complete energy system set to prepare datafile, as per the established model.

        Args:
            Sets:
                year (list): Set of Years
                region (region): Set of Regions
                emission (list): Set of Emissions
        """
        self.year = year
        self.region = region
        self.emission = emission
        self.technology = technology
        self.capacity_technology = capacity_technology
        self.availability_technology = availability_technology
        self.fuel = fuel
        self.specified_fuel = specified_fuel
        self.accumulated_fuel = accumulated_fuel
        self.timeslice = timeslice
        self.mode_of_operation = mode_of_operation
        self.storage = storage
        self.daytype = daytype
        self.season = season
        self.dailytimebracket = dailytimebracket

        ly = len(self.year)
        lr = len(self.region)
        le = len(self.emission)
        lt = len(self.technology)
        lct = len(self.capacity_technology)
        lat = len(self.availability_technology)
        lf = len(self.fuel)
        lsf = len(self.specified_fuel)
        laf = len(self.accumulated_fuel)
        ll = len(self.timeslice)
        lm = len(self.mode_of_operation)
        ls = len(self.storage)
        lld = len(self.daytype)
        lls = len(self.season)
        llh = len(self.dailytimebracket)

        self.ly = ly
        self.lr = lr
        self.le = le
        self.lt = lt
        self.lct = lct
        self.lat = lat
        self.lf = lf
        self.lsf = lsf
        self.laf = laf
        self.ll = ll
        self.lm = lm
        self.ls = ls
        self.lld = lld
        self.lls = lls
        self.llh = llh

        self.YearSplit = np.ones((ll, ly))
        self.DiscountRate = np.ones((lr))
        self.DaySplit = np.ones((llh, ly))
        self.Conversionls = np.ones((ll, lls))
        self.Conversionld = np.ones((ll, lld))
        self.Conversionlh = np.ones((ll, llh))
        self.DaysInDayType = np.ones((lls, lld, ly))
        self.TradeRoute = np.ones((lr, lr, lf, ly))
        self.DepreciationMethod = np.ones((lr))
        self.SpecifiedAnnualDemand = np.ones((lr, lsf, ly))
        self.SpecifiedDemandProfile = np.ones((lr, lsf, ll, ly))
        self.AccumulatedAnnualDemand = np.ones((lr, laf, ly))
        self.CapacityToActivityUnit = np.ones((lr, lct))
        self.CapacityFactor = np.ones((lr, lct, ll, ly))
        self.AvailabilityFactor = np.ones((lr, lat, ly))
        self.OperationalLife = np.ones((lr, lct))
        self.ResidualCapacity = np.ones((lr, lt, ly))
        self.InputActivityRatio = np.ones((lr, lt, lf, lm, ly))
        self.OutputActivityRatio = np.ones((lr, lt, lf, lm, ly))
        self.CapitalCost = np.ones((lr, lt, ly))
        self.VariableCost = np.ones((lr, lt, lm, ly))
        self.FixedCost = np.ones((lr, lt, ly))
        self.TechnologyToStorage = np.ones((lr, lt, ls, lm))
        self.TechnologyFromStorage = np.ones((lr, lt, ls, lm))
        self.StorageLevelStart = np.ones((lr, ls))
        self.StorageMaxChargeRate = np.ones((lr, ls))
        self.StorageMaxDischargeRate = np.ones((lr, ls))
        self.MinStorageCharge = np.ones((lr, ls, ly))
        self.OperationalLifeStorage = np.ones((lr, ls))
        self.CapitalCostStorage = np.ones((lr, ls, ly))
        self.ResidualStorageCapacity = np.ones((lr, ls, ly))
        self.CapacityOfOneTechnologyUnit = np.ones((lr, lt, ly))
        self.TotalAnnualMaxCapacity = np.ones((lr, lt, ly))
        self.TotalAnnualMinCapacity = np.ones((lr, lt, ly))
        self.TotalAnnualMaxCapacityInvestment = np.ones((lr, lt, ly))
        self.TotalAnnualMinCapacityInvestment = np.ones((lr, lt, ly))
        self.TotalTechnologyAnnualActivityLowerLimit = np.ones((lr, lt, ly))
        self.TotalTechnologyAnnualActivityUpperLimit = np.ones((lr, lt, ly))
        self.TotalTechnologyModelPeriodActivityUpperLimit = np.ones((lr, lt))
        self.TotalTechnologyModelPeriodActivityLowerLimit = np.ones((lr, lt))
        self.ReserveMarginTagTechnology = np.ones((lr, lt, ly))
        self.ReserveMarginTagFuel = np.ones((lr, lf, ly))
        self.ReserveMargin = np.ones((lr, ly))
        self.RETagTechnology = np.ones((lr, lt, ly))
        self.RETagFuel = np.ones((lr, lf, ly))
        self.REMinProductionTarget = np.ones((lr, ly))
        self.EmissionActivityRatio = np.ones((lr, lt, le, lm, ly))
        self.EmissionsPenalty = np.ones((lr, le, ly))
        self.AnnualExogenousEmission = np.ones((lr, le, ly))
        self.AnnualEmissionLimit = np.ones((lr, le, ly))
        self.ModelPeriodExogenousEmission = np.ones((lr, le))
        self.ModelPeriodEmissionLimit = np.ones((lr, le))

    def load_datacase(self, case, system):
        """ Loads the data case to a correct configured and intialised energy system
            (The load status dictionary must be compatible with the data_case and system_case)

        Args:
            case (object): Energy system datacase
            system (object): Initialised energy system
            load_status (dict): Dictionary setting the required sets and parameters to load

        Returns:
            system_case (dict): Returns the updated dictionary
        """
        # Loads the sets to the energy system
        system.year = case.year
        system.region = case.region
        system.emission = case.emission
        system.capacity_technology = case.capacity_technology
        system.availability_technology = case.availability_technology
        system.technology = case.technology
        system.fuel = case.fuel
        system.specified_fuel = case.specified_fuel
        system.accumulated_fuel = case.accumulated_fuel
        system.timeslice = case.timeslice
        system.mode_of_operation = case.mode_of_operation
        system.storage = case.storage
        system.daytype = case.daytype
        system.season = case.season
        system.dailytimebracket = case.dailytimebracket
        # Loads the parameters to the energy system
        system.YearSplit = case.YearSplit
        system.DiscountRate = case.DiscountRate
        system.DaySplit = case.DaySplit
        system.Conversionls = case.Conversionls
        system.Conversionld = case.Conversionld
        system.Conversionlh = case.Conversionlh
        system.DaysInDayType = case.DaysInDayType
        system.TradeRoute = case.TradeRoute
        system.DepreciationMethod = case.DepreciationMethod
        system.SpecifiedAnnualDemand = case.SpecifiedAnnualDemand
        system.SpecifiedDemandProfile = case.SpecifiedDemandProfile
        system.AccumulatedAnnualDemand = case.AccumulatedAnnualDemand
        system.CapacityToActivityUnit = case.CapacityToActivityUnit
        system.CapacityFactor = case.CapacityFactor
        system.AvailabilityFactor = case.AvailabilityFactor
        system.OperationalLife = case.OperationalLife
        system.ResidualCapacity = case.ResidualCapacity
        system.InputActivityRatio = case.InputActivityRatio
        system.OutputActivityRatio = case.OutputActivityRatio
        system.CapitalCost = case.CapitalCost
        system.VariableCost = case.VariableCost
        system.FixedCost = case.FixedCost
        system.TechnologyToStorage = case.TechnologyToStorage
        system.TechnologyFromStorage = case.TechnologyFromStorage
        system.StorageLevelStart = case.StorageLevelStart
        system.StorageMaxChargeRate = case.StorageMaxChargeRate
        system.StorageMaxDischargeRate = case.StorageMaxDischargeRate
        system.MinStorageCharge = case.MinStorageCharge
        system.OperationalLifeStorage = case.OperationalLifeStorage
        system.CapitalCostStorage = case.CapitalCostStorage
        system.ResidualStorageCapacity = case.ResidualStorageCapacity
        system.CapacityOfOneTechnologyUnit = case.CapacityOfOneTechnologyUnit
        system.TotalAnnualMaxCapacity = case.TotalAnnualMaxCapacity
        system.TotalAnnualMinCapacity = case.TotalAnnualMinCapacity
        system.TotalAnnualMaxCapacityInvestment = case.TotalAnnualMaxCapacityInvestment
        system.TotalAnnualMinCapacityInvestment = case.TotalAnnualMinCapacityInvestment
        system.TotalTechnologyAnnualActivityLowerLimit = case.TotalTechnologyAnnualActivityLowerLimit
        system.TotalTechnologyAnnualActivityUpperLimit = case.TotalTechnologyAnnualActivityUpperLimit
        system.TotalTechnologyModelPeriodActivityUpperLimit = case.TotalTechnologyModelPeriodActivityUpperLimit
        system.TotalTechnologyModelPeriodActivityLowerLimit = case.TotalTechnologyModelPeriodActivityLowerLimit
        system.ReserveMarginTagTechnology = case.ReserveMarginTagTechnology
        system.ReserveMarginTagFuel = case.ReserveMarginTagFuel
        system.ReserveMargin = case.ReserveMargin
        system.RETagTechnology = case.RETagTechnology
        system.RETagFuel = case.RETagFuel
        system.REMinProductionTarget = case.REMinProductionTarget
        system.EmissionActivityRatio = case.EmissionActivityRatio
        system.EmissionsPenalty = case.EmissionsPenalty
        system.AnnualExogenousEmission = case.AnnualExogenousEmission
        system.AnnualEmissionLimit = case.AnnualEmissionLimit
        system.ModelPeriodExogenousEmission = case.ModelPeriodExogenousEmission
        system.ModelPeriodEmissionLimit = case.ModelPeriodEmissionLimit

    def create_model_file(self, root, file):
        """Creates the model file necessary for the project to run
        
        Args: 
            Parameters for the basic problem
        
        Returns: 
            The loaded in parameters and sets
    
        """
        # Finds the file
        # data = Find_File(data_file,model_file)
        model_location = os.path.join(root, file)
        df = pd.read_excel(model_location, sheet_name='Model')
        # Creates a new dataframe based on the variables on the Include column values
        df_Include = df[df.Include == 'Yes']
        df_model = df_Include[['Name']].copy()

        # Creates a file location and write the model to a text file
        model_txt = 'GOCPI_OseMOSYS_Model.txt'
        model_location = os.path.join(root, model_txt)

        # Saves the user defined model to a text file
        np.savetxt(model_location, df_model.values, fmt='%s')

    def create_data_file(self, file_location, defaults_dictionary,
                         toggle_defaults):
        """ Creates the osemosys datafile

        Args:
            file_location (str): String of directory to save data file
            defaults_dictionary (dict): Dictionary setting the default values for parameters
            toggle_defaults (Bool): Boolean (True/False to only print the default functions
        """
        # Opens the file for write the data
        with open(file_location, 'w') as f:
            # Sets up the preamble for the data file
            f.write('# GOCPI Energy System Data File\n')
            f.write(
                '# Insert instructions when the file is running properly\n')
            f.write('#\n')
            # Sets
            f.write('# Sets\n#\n')
            # year
            set_string = ' '.join(self.year)
            f.write('set YEAR\t:=\t{0};\n'.format(set_string))
            # region
            set_string = ' '.join(self.region)
            f.write('set REGION\t:=\t{0};\n'.format(set_string))
            # emission
            set_string = ' '.join(self.emission)
            f.write('set EMISSION\t:=\t{0};\n'.format(set_string))
            # technology
            set_string = ' '.join(self.technology)
            f.write('set TECHNOLOGY\t:=\t{0};\n'.format(set_string))
            # fuel
            set_string = ' '.join(self.fuel)
            f.write('set FUEL\t:=\t{0};\n'.format(set_string))
            # timeslice
            set_string = ' '.join(self.timeslice)
            f.write('set TIMESLICE\t:=\t{0};\n'.format(set_string))
            # mode_of_operation
            set_string = ' '.join(self.mode_of_operation)
            f.write('set MODE_OF_OPERATION\t:=\t{0};\n'.format(set_string))
            # storage
            set_string = ' '.join(self.storage)
            f.write('set STORAGE\t:=\t{0};\n'.format(set_string))
            # daytype
            set_string = ' '.join(self.daytype)
            f.write('set DAYTYPE\t:=\t{0};\n'.format(set_string))
            # season
            set_string = ' '.join(self.season)
            f.write('set SEASON\t:=\t{0};\n'.format(set_string))
            # dailytimebracket
            set_string = ' '.join(self.dailytimebracket)
            f.write('set DAILYTIMEBRACKET\t:=\t{0};\n'.format(set_string))
            f.write('#\n')
            # Parameters

            # YearSplit = np.zeros((ll,ly))
            param = 'YearSplit'
            f.write('#\n')
            columns = self.year
            column_string = ' '.join(columns)
            # Writes index specific parameter values to the text files
            if toggle_defaults[param] == True:
                f.write("param\t{0}\tdefault\t{1}:\t{2}:=\n".format(
                    param, defaults_dictionary[param], column_string))
                # Converts maxtrix rows to list
                array = np.array(self.timeslice)
                array = array.T
                lt = array.tolist()
                # Creates 2D matrix for this value
                mat = self.YearSplit[:, :]
                # Converts combined matrix to list and combines lists
                matlist = mat.tolist()
                #Combines the two lists
                combined_list = list(zip(lt, matlist))
                for line in combined_list:
                    combinedflat = ''.join(str(line))
                    combinedflat = combinedflat.replace('[', '')
                    combinedflat = combinedflat.replace(']', '')
                    combinedflat = combinedflat.replace("'", '')
                    combinedflat = combinedflat.replace(",", '')
                    combinedflat = combinedflat.replace("(", '')
                    combinedflat = combinedflat.replace(")", '')
                    f.write("{0}\n".format(combinedflat))
            else:
                f.write("param\t{0}\tdefault\t{1}:=\n".format(
                    param, defaults_dictionary[param]))
            f.write(';\n')

            # DiscountRate = np.zeros((lr))
            param = 'DiscountRate'
            f.write('#\n')
            if toggle_defaults[param] == True:
                f.write("param\t{0}\tdefault\t{1}:\t{2}:=\n".format(
                    param, defaults_dictionary[param], column_string))
                # Converts maxtrix rows to list
                array = np.array(self.region)
                array = array.T
                lt = array.tolist()
                # Creates 2D matrix for this value
                mat = self.DiscountRate[:]
                # Converts combined matrix to list and combines lists
                matlist = mat.tolist()
                #Combines the two lists
                combined_list = list(zip(lt, matlist))
                # Writes index specific parameter values to the text files
                for line in combined_list:
                    combinedflat = ''.join(str(line))
                    combinedflat = combinedflat.replace('[', '')
                    combinedflat = combinedflat.replace(']', '')
                    combinedflat = combinedflat.replace("'", '')
                    combinedflat = combinedflat.replace(",", '')
                    combinedflat = combinedflat.replace("(", '')
                    combinedflat = combinedflat.replace(")", '')
                    f.write("{0}\n".format(combinedflat))
            else:
                f.write("param\t{0}\tdefault\t{1}:=\n".format(
                    param, defaults_dictionary[param]))
            f.write(';\n')

            # DaySplit = np.zeros((llh,ly))
            param = 'DaySplit'
            f.write('#\n')
            columns = self.year
            column_string = ' '.join(columns)
            # Writes index specific parameter values to the text files
            if toggle_defaults[param] == True:
                f.write("param\t{0}\tdefault\t{1}:\t{2}:=\n".format(
                    param, defaults_dictionary[param], column_string))
                # Converts maxtrix rows to list
                array = np.array(self.dailytimebracket)
                array = array.T
                lt = array.tolist()
                # Creates 2D matrix for this value
                mat = self.DaySplit[:, :]
                # Converts combined matrix to list and combines lists
                matlist = mat.tolist()
                #Combines the two lists
                combined_list = list(zip(lt, matlist))
                # Writes index specific parameter values to the text files
                f.write("param\t{0}\t:{1}:=\n".format(param, column_string))
                for line in combined_list:
                    combinedflat = ''.join(str(line))
                    combinedflat = combinedflat.replace('[', '')
                    combinedflat = combinedflat.replace(']', '')
                    combinedflat = combinedflat.replace("'", '')
                    combinedflat = combinedflat.replace(",", '')
                    combinedflat = combinedflat.replace("(", '')
                    combinedflat = combinedflat.replace(")", '')
                    f.write("{0}\n".format(combinedflat))
            else:
                f.write("param\t{0}\tdefault\t{1}:=\n".format(
                    param, defaults_dictionary[param]))
            f.write(';\n')

            # Conversionls = np.zeros((ll,ls))
            param = 'Conversionls'  # Change this line
            f.write('#\n')
            columns = self.season  # Change this line
            column_string = ' '.join(columns)
            # Writes index specific parameter values to the text files
            if toggle_defaults[param] == True:
                f.write("param\t{0}\tdefault\t{1}:\t{2}:=\n".format(
                    param, defaults_dictionary[param], column_string))
                # Converts maxtrix rows to list
                array = np.array(self.timeslice)  # Change this line
                array = array.T
                lt = array.tolist()
                # Creates 2D matrix for this value
                mat = self.Conversionls[:, :]  # Change this line
                # Converts combined matrix to list and combines lists
                matlist = mat.tolist()
                #Combines the two lists
                combined_list = list(zip(lt, matlist))
                for line in combined_list:
                    combinedflat = ''.join(str(line))
                    combinedflat = combinedflat.replace('[', '')
                    combinedflat = combinedflat.replace(']', '')
                    combinedflat = combinedflat.replace("'", '')
                    combinedflat = combinedflat.replace(",", '')
                    combinedflat = combinedflat.replace("(", '')
                    combinedflat = combinedflat.replace(")", '')
                    f.write("{0}\n".format(combinedflat))
            else:
                f.write("param\t{0}\tdefault\t{1}:=\n".format(
                    param, defaults_dictionary[param]))
            f.write(';\n')

            # Conversionld = np.zeros((ll,lld))
            param = 'Conversionld'  # Change this line
            f.write('#\n')
            columns = self.daytype  # Change this line
            column_string = ' '.join(columns)
            if toggle_defaults[param] == True:
                f.write("param\t{0}\tdefault\t{1}:\t{2}:=\n".format(
                    param, defaults_dictionary[param], column_string))
                # Converts maxtrix rows to list
                array = np.array(self.timeslice)  # Change this line
                array = array.T
                lt = array.tolist()
                # Creates 2D matrix for this value
                mat = self.Conversionld[:, :]  # Change this line
                # Converts combined matrix to list and combines lists
                matlist = mat.tolist()
                #Combines the two lists
                combined_list = list(zip(lt, matlist))
                for line in combined_list:
                    combinedflat = ''.join(str(line))
                    combinedflat = combinedflat.replace('[', '')
                    combinedflat = combinedflat.replace(']', '')
                    combinedflat = combinedflat.replace("'", '')
                    combinedflat = combinedflat.replace(",", '')
                    combinedflat = combinedflat.replace("(", '')
                    combinedflat = combinedflat.replace(")", '')
                    f.write("{0}\n".format(combinedflat))
            else:
                f.write("param\t{0}\tdefault\t{1}:=\n".format(
                    param, defaults_dictionary[param]))
            f.write(';\n')

            # Conversionlh = np.zeros((ll,llh))
            param = 'Conversionlh'  # Change this line
            f.write('#\n')
            columns = self.dailytimebracket  # Change this line
            column_string = ' '.join(columns)
            if toggle_defaults[param] == True:
                f.write("param\t{0}\tdefault\t{1}:\t{2}:=\n".format(
                    param, defaults_dictionary[param], column_string))
                # Converts maxtrix rows to list
                array = np.array(self.timeslice)  # Change this line
                array = array.T
                lt = array.tolist()
                # Creates 2D matrix for this value
                mat = self.Conversionlh[:, :]  # Change this line
                # Converts combined matrix to list and combines lists
                matlist = mat.tolist()
                #Combines the two lists
                combined_list = list(zip(lt, matlist))
                for line in combined_list:
                    combinedflat = ''.join(str(line))
                    combinedflat = combinedflat.replace('[', '')
                    combinedflat = combinedflat.replace(']', '')
                    combinedflat = combinedflat.replace("'", '')
                    combinedflat = combinedflat.replace(",", '')
                    combinedflat = combinedflat.replace("(", '')
                    combinedflat = combinedflat.replace(")", '')
                    f.write("{0}\n".format(combinedflat))
            else:
                f.write("param\t{0}\tdefault\t{1}:=\n".format(
                    param, defaults_dictionary[param]))
            f.write(';\n')

            # DaysInDayType = np.zeros((lls,lld,ly))
            #Writes new line character at parameter metadata to the text file
            param = 'DaysInDayType'
            f.write('#\n')
            f.write("param\t{0}\tdefault\t{1}:=\n".format(
                param, defaults_dictionary[param]))
            if toggle_defaults[param] == True:
                # Writes parameter values to the text files
                for k in range(self.ly):
                    # Sets index value for format string
                    y = self.year[k]
                    # Converts matrix columns to strings columns to strings
                    columns = self.daytype
                    column_string = ' '.join(columns)
                    # Converts maxtrix rows to list
                    array = np.array(self.season)
                    array = array.T
                    lt = array.tolist()
                    # Creates 2D matrix for this value
                    mat = self.DaysInDayType[:, :, k]
                    # Converts combined matrix to list and combines lists
                    matlist = mat.tolist()
                    #Combines the two lists
                    combined_list = list(zip(lt, matlist))
                    # Writes index specific parameter values to the text files
                    f.write("\t[*,*,{0}]:\t{1}\t:=\n".format(y, column_string))
                    for line in combined_list:
                        combinedflat = ''.join(str(line))
                        combinedflat = combinedflat.replace('[', '')
                        combinedflat = combinedflat.replace(']', '')
                        combinedflat = combinedflat.replace("'", '')
                        combinedflat = combinedflat.replace(",", '')
                        combinedflat = combinedflat.replace("(", '')
                        combinedflat = combinedflat.replace(")", '')
                        f.write("{0}\n".format(combinedflat))
            f.write(';\n')

            # TradeRoute = np.zeros((lr,lr,lf,ly))
            param = 'TradeRoute'  # Change this line
            f.write('#\n')
            f.write("param\t{0}\tdefault\t{1}:=\n".format(
                param, defaults_dictionary[param]))
            if toggle_defaults[param] == True:
                # Writes parameter values to the text files
                for j in range(self.lf):
                    # Sets index value for format string
                    fl = self.fuel[j]
                    for k in range(self.ly):
                        # Sets index value for format string
                        y = self.year[k]
                        # Converts matrix columns to strings columns to strings
                        columns = self.region
                        column_string = ' '.join(columns)
                        # Converts maxtrix rows to list
                        array = np.array(self.region)
                        array = array.T
                        lt = array.tolist()
                        # Creates 2D matrix for this value
                        mat = self.TradeRoute[:, :, j, k]
                        # Converts combined matrix to list and combines lists
                        matlist = mat.tolist()
                        #Combines the two lists
                        combined_list = list(zip(lt, matlist))
                        # Writes index specific parameter values to the text files
                        f.write("\t[*,*,{0},{1}]:\t{2}\t:=\n".format(
                            fl, y, column_string))
                        for line in combined_list:
                            combinedflat = ''.join(str(line))
                            combinedflat = combinedflat.replace('[', '')
                            combinedflat = combinedflat.replace(']', '')
                            combinedflat = combinedflat.replace("'", '')
                            combinedflat = combinedflat.replace(",", '')
                            combinedflat = combinedflat.replace("(", '')
                            combinedflat = combinedflat.replace(")", '')
                            f.write("{0}\n".format(combinedflat))
            f.write(';\n')

            # DepreciationMethod = np.zeros((lr))
            param = 'DepreciationMethod'
            f.write('#\n')
            f.write("param\t{0}\tdefault\t{1}:=\n".format(
                param, defaults_dictionary[param]))
            if toggle_defaults[param] == True:
                # Converts maxtrix rows to list
                array = np.array(self.region)
                array = array.T
                lt = array.tolist()
                # Creates 2D matrix for this value
                mat = self.DepreciationMethod[:]
                # Converts combined matrix to list and combines lists
                matlist = mat.tolist()
                #Combines the two lists
                combined_list = list(zip(lt, matlist))
                # Writes index specific parameter values to the text files
                for line in combined_list:
                    combinedflat = ''.join(str(line))
                    combinedflat = combinedflat.replace('[', '')
                    combinedflat = combinedflat.replace(']', '')
                    combinedflat = combinedflat.replace("'", '')
                    combinedflat = combinedflat.replace(",", '')
                    combinedflat = combinedflat.replace("(", '')
                    combinedflat = combinedflat.replace(")", '')
                    f.write("{0}\n".format(combinedflat))
            f.write(';\n')

            # SpecifiedAnnualDemand = np.zeros((lr,lsf,ly))
            param = 'SpecifiedAnnualDemand'
            f.write('#\n')
            f.write("param\t{0}\tdefault\t{1}:=\n".format(
                param, defaults_dictionary[param]))
            if toggle_defaults[param] == True:
                # Writes parameter values to the text files
                for k in range(self.ly):
                    # Sets index value for format string
                    y = self.year[k]
                    # Converts matrix columns to strings columns to strings
                    columns = self.specified_fuel
                    column_string = ' '.join(columns)
                    # Converts maxtrix rows to list
                    array = np.array(self.region)
                    array = array.T
                    lt = array.tolist()
                    # Creates 2D matrix for this value
                    mat = self.SpecifiedAnnualDemand[:, :, k]
                    # Converts combined matrix to list and combines lists
                    matlist = mat.tolist()
                    #Combines the two lists
                    combined_list = list(zip(lt, matlist))
                    # Writes index specific parameter values to the text files
                    f.write("\t[*,*,{0}]:\t{1}\t:=\n".format(y, column_string))
                    for line in combined_list:
                        combinedflat = ''.join(str(line))
                        combinedflat = combinedflat.replace('[', '')
                        combinedflat = combinedflat.replace(']', '')
                        combinedflat = combinedflat.replace("'", '')
                        combinedflat = combinedflat.replace(",", '')
                        combinedflat = combinedflat.replace("(", '')
                        combinedflat = combinedflat.replace(")", '')
                        f.write("{0}\n".format(combinedflat))
            f.write(';\n')

            # SpecifiedDemandProfile = np.zeros((lr,lf,ll,ly))
            param = 'SpecifiedDemandProfile'  # Change this line
            f.write('#\n')
            f.write("param\t{0}\tdefault\t{1}:=\n".format(
                param, defaults_dictionary[param]))
            if toggle_defaults[param] == True:
                # Writes parameter values to the text files
                for j in range(self.ll):
                    # Sets index value for format string
                    x = self.timeslice[j]
                    for k in range(self.ly):
                        # Sets index value for format string
                        y = self.year[k]
                        # Converts matrix columns to strings columns to strings
                        columns = self.specified_fuel
                        column_string = ' '.join(columns)
                        # Converts maxtrix rows to list
                        array = np.array(self.region)
                        array = array.T
                        lt = array.tolist()
                        # Creates 2D matrix for this value
                        mat = self.SpecifiedDemandProfile[:, :, j, k]
                        # Converts combined matrix to list and combines lists
                        matlist = mat.tolist()
                        #Combines the two lists
                        combined_list = list(zip(lt, matlist))
                        # Writes index specific parameter values to the text files
                        f.write("\t[*,*,{0},{1}]:\t{2}\t:=\n".format(
                            x, y, column_string))
                        for line in combined_list:
                            combinedflat = ''.join(str(line))
                            combinedflat = combinedflat.replace('[', '')
                            combinedflat = combinedflat.replace(']', '')
                            combinedflat = combinedflat.replace("'", '')
                            combinedflat = combinedflat.replace(",", '')
                            combinedflat = combinedflat.replace("(", '')
                            combinedflat = combinedflat.replace(")", '')
                            f.write("{0}\n".format(combinedflat))
            f.write(';\n')

            # AccumulatedAnnualDemand = np.zeros((lr,lf,ly))
            param = 'AccumulatedAnnualDemand'
            f.write('#\n')
            f.write("param\t{0}\tdefault\t{1}:=\n".format(
                param, defaults_dictionary[param]))
            if toggle_defaults[param] == True:
                # Writes parameter values to the text files
                for k in range(self.ly):
                    # Sets index value for format string
                    y = self.year[k]
                    # Converts matrix columns to strings columns to strings
                    columns = self.accumulated_fuel
                    column_string = ' '.join(columns)
                    # Converts maxtrix rows to list
                    array = np.array(self.region)
                    array = array.T
                    lt = array.tolist()
                    # Creates 2D matrix for this value
                    mat = self.AccumulatedAnnualDemand[:, :, k]
                    # Converts combined matrix to list and combines lists
                    matlist = mat.tolist()
                    #Combines the two lists
                    combined_list = list(zip(lt, matlist))
                    # Writes index specific parameter values to the text files
                    f.write("\t[*,*,{0}]:\t{1}\t:=\n".format(y, column_string))
                    for line in combined_list:
                        combinedflat = ''.join(str(line))
                        combinedflat = combinedflat.replace('[', '')
                        combinedflat = combinedflat.replace(']', '')
                        combinedflat = combinedflat.replace("'", '')
                        combinedflat = combinedflat.replace(",", '')
                        combinedflat = combinedflat.replace("(", '')
                        combinedflat = combinedflat.replace(")", '')
                        f.write("{0}\n".format(combinedflat))
            f.write(';\n')

            # CapacityToActivityUnit = np.zeros((lr,lt))
            param = 'CapacityToActivityUnit'  # Change this line
            f.write('#\n')
            columns = self.capacity_technology  # Change this line
            column_string = ' '.join(columns)
            if toggle_defaults[param] == True:
                f.write("param\t{0}\tdefault\t{1}:\t{2}:=\n".format(
                    param, defaults_dictionary[param], column_string))
                # Converts maxtrix rows to list
                array = np.array(self.region)  # Change this line
                array = array.T
                lt = array.tolist()
                # Creates 2D matrix for this value
                mat = self.CapacityToActivityUnit[:, :]  # Change this line
                # Converts combined matrix to list and combines lists
                matlist = mat.tolist()
                #Combines the two lists
                combined_list = list(zip(lt, matlist))
                for line in combined_list:
                    combinedflat = ''.join(str(line))
                    combinedflat = combinedflat.replace('[', '')
                    combinedflat = combinedflat.replace(']', '')
                    combinedflat = combinedflat.replace("'", '')
                    combinedflat = combinedflat.replace(",", '')
                    combinedflat = combinedflat.replace("(", '')
                    combinedflat = combinedflat.replace(")", '')
                    f.write("{0}\n".format(combinedflat))
            else:
                f.write("param\t{0}\tdefault\t{1}:=\n".format(
                    param, defaults_dictionary[param]))
            f.write(';\n')

            # CapacityFactor = np.zeros((lr,lt,ll,ly))
            param = 'CapacityFactor'  # Change this line
            f.write('#\n')
            f.write("param\t{0}\tdefault\t{1}:=\n".format(
                param, defaults_dictionary[param]))
            if toggle_defaults[param] == True:
                # Writes parameter values to the text files
                for j in range(self.ll):
                    # Sets index value for format string
                    x = self.timeslice[j]
                    for k in range(self.ly):
                        # Sets index value for format string
                        y = self.year[k]
                        # Converts matrix columns to strings columns to strings
                        columns = self.capacity_technology
                        column_string = ' '.join(columns)
                        # Converts maxtrix rows to list
                        array = np.array(self.region)
                        array = array.T
                        lt = array.tolist()
                        # Creates 2D matrix for this value
                        mat = self.CapacityFactor[:, :, j, k]
                        # Converts combined matrix to list and combines lists
                        matlist = mat.tolist()
                        #Combines the two lists
                        combined_list = list(zip(lt, matlist))
                        # Writes index specific parameter values to the text files
                        f.write("\t[*,*,{0},{1}]:\t{2}\t:=\n".format(
                            x, y, column_string))
                        for line in combined_list:
                            combinedflat = ''.join(str(line))
                            combinedflat = combinedflat.replace('[', '')
                            combinedflat = combinedflat.replace(']', '')
                            combinedflat = combinedflat.replace("'", '')
                            combinedflat = combinedflat.replace(",", '')
                            combinedflat = combinedflat.replace("(", '')
                            combinedflat = combinedflat.replace(")", '')
                            f.write("{0}\n".format(combinedflat))
            f.write(';\n')

            # AvailabilityFactor = np.zeros((lr,lt,ly))
            param = 'AvailabilityFactor'
            f.write('#\n')
            f.write("param\t{0}\tdefault\t{1}:=\n".format(
                param, defaults_dictionary[param]))
            if toggle_defaults[param] == True:
                # Writes parameter values to the text files
                for k in range(self.ly):
                    # Sets index value for format string
                    y = self.year[k]
                    # Converts matrix columns to strings columns to strings
                    columns = self.availability_technology
                    column_string = ' '.join(columns)
                    # Converts maxtrix rows to list
                    array = np.array(self.region)
                    array = array.T
                    lt = array.tolist()
                    # Creates 2D matrix for this value
                    mat = self.AvailabilityFactor[:, :, k]
                    # Converts combined matrix to list and combines lists
                    matlist = mat.tolist()
                    #Combines the two lists
                    combined_list = list(zip(lt, matlist))
                    # Writes index specific parameter values to the text files
                    f.write("\t[*,*,{0}]:\t{1}\t:=\n".format(y, column_string))
                    for line in combined_list:
                        combinedflat = ''.join(str(line))
                        combinedflat = combinedflat.replace('[', '')
                        combinedflat = combinedflat.replace(']', '')
                        combinedflat = combinedflat.replace("'", '')
                        combinedflat = combinedflat.replace(",", '')
                        combinedflat = combinedflat.replace("(", '')
                        combinedflat = combinedflat.replace(")", '')
                        f.write("{0}\n".format(combinedflat))
            f.write(';\n')

            # OperationalLife = np.zeros((lr,lt))
            param = 'OperationalLife'  # Change this line
            f.write('#\n')
            columns = self.technology  # Change this line
            column_string = ' '.join(columns)
            if toggle_defaults[param] == True:
                f.write("param\t{0}\tdefault\t{1}:\t{2}:=\n".format(
                    param, defaults_dictionary[param], column_string))
                # Converts maxtrix rows to list
                array = np.array(self.region)  # Change this line
                array = array.T
                lt = array.tolist()
                # Creates 2D matrix for this value
                mat = self.OperationalLife[:, :]  # Change this line
                # Converts combined matrix to list and combines lists
                matlist = mat.tolist()
                #Combines the two lists
                combined_list = list(zip(lt, matlist))
                for line in combined_list:
                    combinedflat = ''.join(str(line))
                    combinedflat = combinedflat.replace('[', '')
                    combinedflat = combinedflat.replace(']', '')
                    combinedflat = combinedflat.replace("'", '')
                    combinedflat = combinedflat.replace(",", '')
                    combinedflat = combinedflat.replace("(", '')
                    combinedflat = combinedflat.replace(")", '')
                    f.write("{0}\n".format(combinedflat))
            else:
                f.write("param\t{0}\tdefault\t{1}:=\n".format(
                    param, defaults_dictionary[param]))
            f.write(';\n')

            # ResidualCapacity = np.zeros((lr,lt,ly))
            param = 'ResidualCapacity'
            f.write('#\n')
            f.write("param\t{0}\tdefault\t{1}:=\n".format(
                param, defaults_dictionary[param]))
            if toggle_defaults[param] == True:
                # Writes parameter values to the text files
                for k in range(self.ly):
                    # Sets index value for format string
                    y = self.year[k]
                    # Converts matrix columns to strings columns to strings
                    columns = self.technology
                    column_string = ' '.join(columns)
                    # Converts maxtrix rows to list
                    array = np.array(self.region)
                    array = array.T
                    lt = array.tolist()
                    # Creates 2D matrix for this value
                    mat = self.ResidualCapacity[:, :, k]
                    # Converts combined matrix to list and combines lists
                    matlist = mat.tolist()
                    #Combines the two lists
                    combined_list = list(zip(lt, matlist))
                    # Writes index specific parameter values to the text files
                    f.write("\t[*,*,{0}]:\t{1}\t:=\n".format(y, column_string))
                    for line in combined_list:
                        combinedflat = ''.join(str(line))
                        combinedflat = combinedflat.replace('[', '')
                        combinedflat = combinedflat.replace(']', '')
                        combinedflat = combinedflat.replace("'", '')
                        combinedflat = combinedflat.replace(",", '')
                        combinedflat = combinedflat.replace("(", '')
                        combinedflat = combinedflat.replace(")", '')
                        f.write("{0}\n".format(combinedflat))
            f.write(';\n')

            # InputActivityRatio = np.zeros((lr,lt,lf,lm,ly))
            param = 'InputActivityRatio'  # Change this line
            f.write('#\n')
            f.write("param\t{0}\tdefault\t{1}:=\n".format(
                param, defaults_dictionary[param]))
            if toggle_defaults[param] == True:
                # Writes parameter values to the text files
                for i in range(self.lf):  # Change loops if you need
                    # Sets index value for format string
                    x = self.fuel[i]
                    for j in range(self.lm):
                        # Sets index value for format string
                        y = self.mode_of_operation[j]
                        for k in range(self.ly):
                            # Sets index value for format string
                            z = self.year[k]
                            # Converts matrix columns to strings columns to strings
                            columns = self.technology
                            column_string = ' '.join(columns)
                            # Converts maxtrix rows to list
                            array = np.array(self.region)
                            array = array.T
                            lt = array.tolist()
                            # Creates 2D matrix for this value
                            mat = self.InputActivityRatio[:, :, i, j, k]
                            # Converts combined matrix to list and combines lists
                            matlist = mat.tolist()
                            #Combines the two lists
                            combined_list = list(zip(lt, matlist))
                            # Writes index specific parameter values to the text files
                            f.write("\t[*,*,{0},{1},{2}]:\t{3}\t:=\n".format(
                                x, y, z, column_string))
                            for line in combined_list:
                                combinedflat = ''.join(str(line))
                                combinedflat = combinedflat.replace('[', '')
                                combinedflat = combinedflat.replace(']', '')
                                combinedflat = combinedflat.replace("'", '')
                                combinedflat = combinedflat.replace(",", '')
                                combinedflat = combinedflat.replace("(", '')
                                combinedflat = combinedflat.replace(")", '')
                                f.write("{0}\n".format(combinedflat))
            f.write(';\n')

            # OutputActivityRatio = np.zeros((lr,lt,lf,lm,ly))
            param = 'OutputActivityRatio'  # Change this line
            f.write('#\n')
            f.write("param\t{0}\tdefault\t{1}:=\n".format(
                param, defaults_dictionary[param]))
            if toggle_defaults[param] == True:
                # Writes parameter values to the text files
                for i in range(self.lf):  # Change loops if you need
                    # Sets index value for format string
                    x = self.fuel[i]
                    for j in range(self.lm):
                        # Sets index value for format string
                        y = self.mode_of_operation[j]
                        for k in range(self.ly):
                            # Sets index value for format string
                            z = self.year[k]
                            # Converts matrix columns to strings columns to strings
                            columns = self.technology
                            column_string = ' '.join(columns)
                            # Converts maxtrix rows to list
                            array = np.array(self.region)
                            array = array.T
                            lt = array.tolist()
                            # Creates 2D matrix for this value
                            mat = self.OutputActivityRatio[:, :, i, j, k]
                            # Converts combined matrix to list and combines lists
                            matlist = mat.tolist()
                            #Combines the two lists
                            combined_list = list(zip(lt, matlist))
                            # Writes index specific parameter values to the text files
                            f.write("\t[*,*,{0},{1},{2}]:\t{3}\t:=\n".format(
                                x, y, z, column_string))
                            for line in combined_list:
                                combinedflat = ''.join(str(line))
                                combinedflat = combinedflat.replace('[', '')
                                combinedflat = combinedflat.replace(']', '')
                                combinedflat = combinedflat.replace("'", '')
                                combinedflat = combinedflat.replace(",", '')
                                combinedflat = combinedflat.replace("(", '')
                                combinedflat = combinedflat.replace(")", '')
                                f.write("{0}\n".format(combinedflat))
            f.write(';\n')

            # CapitalCost = np.zeros((lr,lt,ly))
            param = 'CapitalCost'
            f.write('#\n')
            f.write("param\t{0}\tdefault\t{1}:=\n".format(
                param, defaults_dictionary[param]))
            if toggle_defaults[param] == True:
                # Writes parameter values to the text files
                for k in range(self.ly):
                    # Sets index value for format string
                    y = self.year[k]
                    # Converts matrix columns to strings columns to strings
                    columns = self.technology
                    column_string = ' '.join(columns)
                    # Converts maxtrix rows to list
                    array = np.array(self.region)
                    array = array.T
                    lt = array.tolist()
                    # Creates 2D matrix for this value
                    mat = self.CapitalCost[:, :, k]
                    # Converts combined matrix to list and combines lists
                    matlist = mat.tolist()
                    #Combines the two lists
                    combined_list = list(zip(lt, matlist))
                    # Writes index specific parameter values to the text files
                    f.write("\t[*,*,{0}]:\t{1}\t:=\n".format(y, column_string))
                    for line in combined_list:
                        combinedflat = ''.join(str(line))
                        combinedflat = combinedflat.replace('[', '')
                        combinedflat = combinedflat.replace(']', '')
                        combinedflat = combinedflat.replace("'", '')
                        combinedflat = combinedflat.replace(",", '')
                        combinedflat = combinedflat.replace("(", '')
                        combinedflat = combinedflat.replace(")", '')
                        f.write("{0}\n".format(combinedflat))
            f.write(';\n')

            # VariableCost = np.zeros((lr,lt,lm,ly))
            param = 'VariableCost'  # Change this line
            f.write('#\n')
            f.write("param\t{0}\tdefault\t{1}:=\n".format(
                param, defaults_dictionary[param]))
            if toggle_defaults[param] == True:
                # Writes parameter values to the text files
                for j in range(self.lm):
                    # Sets index value for format string
                    x = self.mode_of_operation[j]
                    for k in range(self.ly):
                        # Sets index value for format string
                        y = self.year[k]
                        # Converts matrix columns to strings columns to strings
                        columns = self.technology
                        column_string = ' '.join(columns)
                        # Converts maxtrix rows to list
                        array = np.array(self.region)
                        array = array.T
                        lt = array.tolist()
                        # Creates 2D matrix for this value
                        mat = self.VariableCost[:, :, j, k]
                        # Converts combined matrix to list and combines lists
                        matlist = mat.tolist()
                        #Combines the two lists
                        combined_list = list(zip(lt, matlist))
                        # Writes index specific parameter values to the text files
                        f.write("\t[*,*,{0},{1}]:\t{2}\t:=\n".format(
                            x, y, column_string))
                        for line in combined_list:
                            combinedflat = ''.join(str(line))
                            combinedflat = combinedflat.replace('[', '')
                            combinedflat = combinedflat.replace(']', '')
                            combinedflat = combinedflat.replace("'", '')
                            combinedflat = combinedflat.replace(",", '')
                            combinedflat = combinedflat.replace("(", '')
                            combinedflat = combinedflat.replace(")", '')
                            f.write("{0}\n".format(combinedflat))
            f.write(';\n')

            # FixedCost = np.zeros((lr,lt,ly))
            param = 'FixedCost'
            f.write('#\n')
            f.write("param\t{0}\tdefault\t{1}:=\n".format(
                param, defaults_dictionary[param]))
            if toggle_defaults[param] == True:
                # Writes parameter values to the text files
                for k in range(self.ly):
                    # Sets index value for format string
                    y = self.year[k]
                    # Converts matrix columns to strings columns to strings
                    columns = self.technology
                    column_string = ' '.join(columns)
                    # Converts maxtrix rows to list
                    array = np.array(self.region)
                    array = array.T
                    lt = array.tolist()
                    # Creates 2D matrix for this value
                    mat = self.FixedCost[:, :, k]
                    # Converts combined matrix to list and combines lists
                    matlist = mat.tolist()
                    #Combines the two lists
                    combined_list = list(zip(lt, matlist))
                    # Writes index specific parameter values to the text files
                    f.write("\t[*,*,{0}]:\t{1}\t:=\n".format(y, column_string))
                    for line in combined_list:
                        combinedflat = ''.join(str(line))
                        combinedflat = combinedflat.replace('[', '')
                        combinedflat = combinedflat.replace(']', '')
                        combinedflat = combinedflat.replace("'", '')
                        combinedflat = combinedflat.replace(",", '')
                        combinedflat = combinedflat.replace("(", '')
                        combinedflat = combinedflat.replace(")", '')
                        f.write("{0}\n".format(combinedflat))
            f.write(';\n')

            # TechnologyToStorage = np.zeros((lr,lt,ls,lm))
            param = 'TechnologyToStorage'  # Change this line
            f.write('#\n')
            f.write("param\t{0}\tdefault\t{1}:=\n".format(
                param, defaults_dictionary[param]))
            if toggle_defaults[param] == True:
                # Writes parameter values to the text files
                for j in range(self.ls):
                    # Sets index value for format string
                    x = self.storage[j]
                    for k in range(self.lm):
                        # Sets index value for format string
                        y = self.mode_of_operation[k]
                        # Converts matrix columns to strings columns to strings
                        columns = self.technology
                        column_string = ' '.join(columns)
                        # Converts maxtrix rows to list
                        array = np.array(self.region)
                        array = array.T
                        lt = array.tolist()
                        # Creates 2D matrix for this value
                        mat = self.TechnologyToStorage[:, :, j, k]
                        # Converts combined matrix to list and combines lists
                        matlist = mat.tolist()
                        #Combines the two lists
                        combined_list = list(zip(lt, matlist))
                        # Writes index specific parameter values to the text files
                        f.write("\t[*,*,{0},{1}]:\t{2}\t:=\n".format(
                            x, y, column_string))
                        for line in combined_list:
                            combinedflat = ''.join(str(line))
                            combinedflat = combinedflat.replace('[', '')
                            combinedflat = combinedflat.replace(']', '')
                            combinedflat = combinedflat.replace("'", '')
                            combinedflat = combinedflat.replace(",", '')
                            combinedflat = combinedflat.replace("(", '')
                            combinedflat = combinedflat.replace(")", '')
                            f.write("{0}\n".format(combinedflat))
            f.write(';\n')

            # TechnologyFromStorage = np.zeros((lr,lt,ls,lm))
            param = 'TechnologyFromStorage'  # Change this line
            f.write('#\n')
            f.write("param\t{0}\tdefault\t{1}:=\n".format(
                param, defaults_dictionary[param]))
            if toggle_defaults[param] == True:
                # Writes parameter values to the text files
                for j in range(self.ls):
                    # Sets index value for format string
                    x = self.storage[j]
                    for k in range(self.lm):
                        # Sets index value for format string
                        y = self.mode_of_operation[k]
                        # Converts matrix columns to strings columns to strings
                        columns = self.technology
                        column_string = ' '.join(columns)
                        # Converts maxtrix rows to list
                        array = np.array(self.region)
                        array = array.T
                        lt = array.tolist()
                        # Creates 2D matrix for this value
                        mat = self.TechnologyFromStorage[:, :, j, k]
                        # Converts combined matrix to list and combines lists
                        matlist = mat.tolist()
                        #Combines the two lists
                        combined_list = list(zip(lt, matlist))
                        # Writes index specific parameter values to the text files
                        f.write("\t[*,*,{0},{1}]:\t{2}\t:=\n".format(
                            x, y, column_string))
                        for line in combined_list:
                            combinedflat = ''.join(str(line))
                            combinedflat = combinedflat.replace('[', '')
                            combinedflat = combinedflat.replace(']', '')
                            combinedflat = combinedflat.replace("'", '')
                            combinedflat = combinedflat.replace(",", '')
                            combinedflat = combinedflat.replace("(", '')
                            combinedflat = combinedflat.replace(")", '')
                            f.write("{0}\n".format(combinedflat))
            f.write(';\n')

            # StorageLevelStart = np.zeros((lr,ls))
            param = 'StorageLevelStart'  # Change this line
            f.write('#\n')
            columns = self.storage  # Change this line
            column_string = ' '.join(columns)
            if toggle_defaults[param] == True:
                f.write("param\t{0}\tdefault\t{1}:\t{2}:=\n".format(
                    param, defaults_dictionary[param], column_string))
                # Converts maxtrix rows to list
                array = np.array(self.region)  # Change this line
                array = array.T
                lt = array.tolist()
                # Creates 2D matrix for this value
                mat = self.StorageLevelStart[:, :]  # Change this line
                # Converts combined matrix to list and combines lists
                matlist = mat.tolist()
                #Combines the two lists
                combined_list = list(zip(lt, matlist))
                for line in combined_list:
                    combinedflat = ''.join(str(line))
                    combinedflat = combinedflat.replace('[', '')
                    combinedflat = combinedflat.replace(']', '')
                    combinedflat = combinedflat.replace("'", '')
                    combinedflat = combinedflat.replace(",", '')
                    combinedflat = combinedflat.replace("(", '')
                    combinedflat = combinedflat.replace(")", '')
                    f.write("{0}\n".format(combinedflat))
            else:
                f.write("param\t{0}\tdefault\t{1}:=\n".format(
                    param, defaults_dictionary[param]))
            f.write(';\n')

            # StorageMaxChargeRate = np.zeros((lr,ls))
            param = 'StorageMaxChargeRate'  # Change this line
            f.write('#\n')
            columns = self.storage  # Change this line
            column_string = ' '.join(columns)
            if toggle_defaults[param] == True:
                f.write("param\t{0}\tdefault\t{1}:\t{2}:=\n".format(
                    param, defaults_dictionary[param], column_string))
                # Converts maxtrix rows to list
                array = np.array(self.region)  # Change this line
                array = array.T
                lt = array.tolist()
                # Creates 2D matrix for this value
                mat = self.StorageMaxChargeRate[:, :]  # Change this line
                # Converts combined matrix to list and combines lists
                matlist = mat.tolist()
                #Combines the two lists
                combined_list = list(zip(lt, matlist))
                for line in combined_list:
                    combinedflat = ''.join(str(line))
                    combinedflat = combinedflat.replace('[', '')
                    combinedflat = combinedflat.replace(']', '')
                    combinedflat = combinedflat.replace("'", '')
                    combinedflat = combinedflat.replace(",", '')
                    combinedflat = combinedflat.replace("(", '')
                    combinedflat = combinedflat.replace(")", '')
                    f.write("{0}\n".format(combinedflat))
            else:
                f.write("param\t{0}\tdefault\t{1}:=\n".format(
                    param, defaults_dictionary[param]))
            f.write(';\n')

            # StorageMaxDischargeRate = np.zeros((lr,ls))
            param = 'StorageMaxDischargeRate'  # Change this line
            f.write('#\n')
            columns = self.storage  # Change this line
            column_string = ' '.join(columns)
            if toggle_defaults[param] == True:
                f.write("param\t{0}\tdefault\t{1}:\t{2}:=\n".format(
                    param, defaults_dictionary[param], column_string))
                # Converts maxtrix rows to list
                array = np.array(self.region)  # Change this line
                array = array.T
                lt = array.tolist()
                # Creates 2D matrix for this value
                mat = self.StorageMaxDischargeRate[:, :]  # Change this line
                # Converts combined matrix to list and combines lists
                matlist = mat.tolist()
                #Combines the two lists
                combined_list = list(zip(lt, matlist))
                # Writes index specific parameter values to the text files
                f.write("param\t{0}\t:{1}:=\n".format(param, column_string))
                for line in combined_list:
                    combinedflat = ''.join(str(line))
                    combinedflat = combinedflat.replace('[', '')
                    combinedflat = combinedflat.replace(']', '')
                    combinedflat = combinedflat.replace("'", '')
                    combinedflat = combinedflat.replace(",", '')
                    combinedflat = combinedflat.replace("(", '')
                    combinedflat = combinedflat.replace(")", '')
                    f.write("{0}\n".format(combinedflat))
            else:
                f.write("param\t{0}\tdefault\t{1}:=\n".format(
                    param, defaults_dictionary[param]))
            f.write(';\n')

            # MinStorageCharge = np.zeros((lr,ls,ly))
            param = 'MinStorageCharge'
            f.write('#\n')
            f.write("param\t{0}\tdefault\t{1}:=\n".format(
                param, defaults_dictionary[param]))
            if toggle_defaults[param] == True:
                # Writes parameter values to the text files
                for k in range(self.ly):
                    # Sets index value for format string
                    y = self.year[k]
                    # Converts matrix columns to strings columns to strings
                    columns = self.storage
                    column_string = ' '.join(columns)
                    # Converts maxtrix rows to list
                    array = np.array(self.region)
                    array = array.T
                    lt = array.tolist()
                    # Creates 2D matrix for this value
                    mat = self.MinStorageCharge[:, :, k]
                    # Converts combined matrix to list and combines lists
                    matlist = mat.tolist()
                    #Combines the two lists
                    combined_list = list(zip(lt, matlist))
                    # Writes index specific parameter values to the text files
                    f.write("\t[*,*,{0}]:\t{1}\t:=\n".format(y, column_string))
                    for line in combined_list:
                        combinedflat = ''.join(str(line))
                        combinedflat = combinedflat.replace('[', '')
                        combinedflat = combinedflat.replace(']', '')
                        combinedflat = combinedflat.replace("'", '')
                        combinedflat = combinedflat.replace(",", '')
                        combinedflat = combinedflat.replace("(", '')
                        combinedflat = combinedflat.replace(")", '')
                        f.write("{0}\n".format(combinedflat))
            f.write(';\n')

            # OperationalLifeStorage = np.zeros((lr,ls))
            param = 'OperationalLifeStorage'  # Change this line
            f.write('#\n')
            columns = self.storage  # Change this line
            column_string = ' '.join(columns)
            if toggle_defaults[param] == True:
                f.write("param\t{0}\tdefault\t{1}:\t{2}:=\n".format(
                    param, defaults_dictionary[param], column_string))
                # Converts maxtrix rows to list
                array = np.array(self.region)  # Change this line
                array = array.T
                lt = array.tolist()
                # Creates 2D matrix for this value
                mat = self.OperationalLifeStorage[:, :]  # Change this line
                # Converts combined matrix to list and combines lists
                matlist = mat.tolist()
                #Combines the two lists
                combined_list = list(zip(lt, matlist))
                # Writes index specific parameter values to the text files
                f.write("param\t{0}\t:{1}:=\n".format(param, column_string))
                for line in combined_list:
                    combinedflat = ''.join(str(line))
                    combinedflat = combinedflat.replace('[', '')
                    combinedflat = combinedflat.replace(']', '')
                    combinedflat = combinedflat.replace("'", '')
                    combinedflat = combinedflat.replace(",", '')
                    combinedflat = combinedflat.replace("(", '')
                    combinedflat = combinedflat.replace(")", '')
                    f.write("{0}\n".format(combinedflat))
            else:
                f.write("param\t{0}\tdefault\t{1}:=\n".format(
                    param, defaults_dictionary[param]))
            f.write(';\n')

            # CapitalCostStorage = np.zeros((lr,ls,ly))
            param = 'CapitalCostStorage'
            f.write('#\n')
            f.write("param\t{0}\tdefault\t{1}:=\n".format(
                param, defaults_dictionary[param]))
            if toggle_defaults[param] == True:
                # Writes parameter values to the text files
                for k in range(self.ly):
                    # Sets index value for format string
                    y = self.year[k]
                    # Converts matrix columns to strings columns to strings
                    columns = self.storage
                    column_string = ' '.join(columns)
                    # Converts maxtrix rows to list
                    array = np.array(self.region)
                    array = array.T
                    lt = array.tolist()
                    # Creates 2D matrix for this value
                    mat = self.CapitalCostStorage[:, :, k]
                    # Converts combined matrix to list and combines lists
                    matlist = mat.tolist()
                    #Combines the two lists
                    combined_list = list(zip(lt, matlist))
                    # Writes index specific parameter values to the text files
                    f.write("\t[*,*,{0}]:\t{1}\t:=\n".format(y, column_string))
                    for line in combined_list:
                        combinedflat = ''.join(str(line))
                        combinedflat = combinedflat.replace('[', '')
                        combinedflat = combinedflat.replace(']', '')
                        combinedflat = combinedflat.replace("'", '')
                        combinedflat = combinedflat.replace(",", '')
                        combinedflat = combinedflat.replace("(", '')
                        combinedflat = combinedflat.replace(")", '')
                        f.write("{0}\n".format(combinedflat))
            f.write(';\n')

            # ResidualStorageCapacity = np.zeros((lr,ls,ly))
            param = 'ResidualStorageCapacity'
            f.write('#\n')
            f.write("param\t{0}\tdefault\t{1}:=\n".format(
                param, defaults_dictionary[param]))
            if toggle_defaults[param] == True:
                # Writes parameter values to the text files
                for k in range(self.ly):
                    # Sets index value for format string
                    y = self.year[k]
                    # Converts matrix columns to strings columns to strings
                    columns = self.storage
                    column_string = ' '.join(columns)
                    # Converts maxtrix rows to list
                    array = np.array(self.region)
                    array = array.T
                    lt = array.tolist()
                    # Creates 2D matrix for this value
                    mat = self.ResidualStorageCapacity[:, :, k]
                    # Converts combined matrix to list and combines lists
                    matlist = mat.tolist()
                    #Combines the two lists
                    combined_list = list(zip(lt, matlist))
                    # Writes index specific parameter values to the text files
                    f.write("\t[*,*,{0}]:\t{1}\t:=\n".format(y, column_string))
                    for line in combined_list:
                        combinedflat = ''.join(str(line))
                        combinedflat = combinedflat.replace('[', '')
                        combinedflat = combinedflat.replace(']', '')
                        combinedflat = combinedflat.replace("'", '')
                        combinedflat = combinedflat.replace(",", '')
                        combinedflat = combinedflat.replace("(", '')
                        combinedflat = combinedflat.replace(")", '')
                        f.write("{0}\n".format(combinedflat))
            f.write(';\n')

            # CapacityOfOneTechnologyUnit = np.zeros((lr,lt,ly))
            param = 'CapacityOfOneTechnologyUnit'
            f.write('#\n')
            f.write("param\t{0}\tdefault\t{1}:=\n".format(
                param, defaults_dictionary[param]))
            if toggle_defaults[param] == True:
                # Writes parameter values to the text files
                for k in range(self.ly):
                    # Sets index value for format string
                    y = self.year[k]
                    # Converts matrix columns to strings columns to strings
                    columns = self.technology
                    column_string = ' '.join(columns)
                    # Converts maxtrix rows to list
                    array = np.array(self.region)
                    array = array.T
                    lt = array.tolist()
                    # Creates 2D matrix for this value
                    mat = self.CapacityOfOneTechnologyUnit[:, :, k]
                    # Converts combined matrix to list and combines lists
                    matlist = mat.tolist()
                    #Combines the two lists
                    combined_list = list(zip(lt, matlist))
                    # Writes index specific parameter values to the text files
                    f.write("\t[*,*,{0}]:\t{1}\t:=\n".format(y, column_string))
                    for line in combined_list:
                        combinedflat = ''.join(str(line))
                        combinedflat = combinedflat.replace('[', '')
                        combinedflat = combinedflat.replace(']', '')
                        combinedflat = combinedflat.replace("'", '')
                        combinedflat = combinedflat.replace(",", '')
                        combinedflat = combinedflat.replace("(", '')
                        combinedflat = combinedflat.replace(")", '')
                        f.write("{0}\n".format(combinedflat))
            f.write(';\n')

            # TotalAnnualMaxCapacity = np.zeros((lr,lt,ly))
            param = 'TotalAnnualMaxCapacity'
            f.write('#\n')
            f.write("param\t{0}\tdefault\t{1}:=\n".format(
                param, defaults_dictionary[param]))
            if toggle_defaults[param] == True:
                # Writes parameter values to the text files
                for k in range(self.ly):
                    # Sets index value for format string
                    y = self.year[k]
                    # Converts matrix columns to strings columns to strings
                    columns = self.technology
                    column_string = ' '.join(columns)
                    # Converts maxtrix rows to list
                    array = np.array(self.region)
                    array = array.T
                    lt = array.tolist()
                    # Creates 2D matrix for this value
                    mat = self.TotalAnnualMaxCapacity[:, :, k]
                    # Converts combined matrix to list and combines lists
                    matlist = mat.tolist()
                    #Combines the two lists
                    combined_list = list(zip(lt, matlist))
                    # Writes index specific parameter values to the text files
                    f.write("\t[*,*,{0}]:\t{1}\t:=\n".format(y, column_string))
                    for line in combined_list:
                        combinedflat = ''.join(str(line))
                        combinedflat = combinedflat.replace('[', '')
                        combinedflat = combinedflat.replace(']', '')
                        combinedflat = combinedflat.replace("'", '')
                        combinedflat = combinedflat.replace(",", '')
                        combinedflat = combinedflat.replace("(", '')
                        combinedflat = combinedflat.replace(")", '')
                        f.write("{0}\n".format(combinedflat))
            f.write(';\n')

            # TotalAnnualMinCapacity = np.zeros((lr,lt,ly))
            param = 'TotalAnnualMinCapacity'
            f.write('#\n')
            f.write("param\t{0}\tdefault\t{1}:=\n".format(
                param, defaults_dictionary[param]))
            if toggle_defaults[param] == True:
                # Writes parameter values to the text files
                for k in range(self.ly):
                    # Sets index value for format string
                    y = self.year[k]
                    # Converts matrix columns to strings columns to strings
                    columns = self.technology
                    column_string = ' '.join(columns)
                    # Converts maxtrix rows to list
                    array = np.array(self.region)
                    array = array.T
                    lt = array.tolist()
                    # Creates 2D matrix for this value
                    mat = self.TotalAnnualMinCapacity[:, :, k]
                    # Converts combined matrix to list and combines lists
                    matlist = mat.tolist()
                    #Combines the two lists
                    combined_list = list(zip(lt, matlist))
                    # Writes index specific parameter values to the text files
                    f.write("\t[*,*,{0}]:\t{1}\t:=\n".format(y, column_string))
                    for line in combined_list:
                        combinedflat = ''.join(str(line))
                        combinedflat = combinedflat.replace('[', '')
                        combinedflat = combinedflat.replace(']', '')
                        combinedflat = combinedflat.replace("'", '')
                        combinedflat = combinedflat.replace(",", '')
                        combinedflat = combinedflat.replace("(", '')
                        combinedflat = combinedflat.replace(")", '')
                        f.write("{0}\n".format(combinedflat))
            f.write(';\n')

            # TotalAnnualMaxCapacityInvestment = np.zeros((lr,lt,ly))
            param = 'TotalAnnualMaxCapacityInvestment'
            f.write('#\n')
            f.write("param\t{0}\tdefault\t{1}:=\n".format(
                param, defaults_dictionary[param]))
            if toggle_defaults[param] == True:
                # Writes parameter values to the text files
                for k in range(self.ly):
                    # Sets index value for format string
                    y = self.year[k]
                    # Converts matrix columns to strings columns to strings
                    columns = self.technology
                    column_string = ' '.join(columns)
                    # Converts maxtrix rows to list
                    array = np.array(self.region)
                    array = array.T
                    lt = array.tolist()
                    # Creates 2D matrix for this value
                    mat = self.TotalAnnualMaxCapacityInvestment[:, :, k]
                    # Converts combined matrix to list and combines lists
                    matlist = mat.tolist()
                    #Combines the two lists
                    combined_list = list(zip(lt, matlist))
                    # Writes index specific parameter values to the text files
                    f.write("\t[*,*,{0}]:\t{1}\t:=\n".format(y, column_string))
                    for line in combined_list:
                        combinedflat = ''.join(str(line))
                        combinedflat = combinedflat.replace('[', '')
                        combinedflat = combinedflat.replace(']', '')
                        combinedflat = combinedflat.replace("'", '')
                        combinedflat = combinedflat.replace(",", '')
                        combinedflat = combinedflat.replace("(", '')
                        combinedflat = combinedflat.replace(")", '')
                        f.write("{0}\n".format(combinedflat))
            f.write(';\n')

            # TotalAnnualMinCapacityInvestment = np.zeros((lr,lt,ly))
            param = 'TotalAnnualMinCapacityInvestment'
            f.write('#\n')
            f.write("param\t{0}\tdefault\t{1}:=\n".format(
                param, defaults_dictionary[param]))
            if toggle_defaults[param] == True:
                # Writes parameter values to the text files
                for k in range(self.ly):
                    # Sets index value for format string
                    y = self.year[k]
                    # Converts matrix columns to strings columns to strings
                    columns = self.technology
                    column_string = ' '.join(columns)
                    # Converts maxtrix rows to list
                    array = np.array(self.region)
                    array = array.T
                    lt = array.tolist()
                    # Creates 2D matrix for this value
                    mat = self.TotalAnnualMinCapacityInvestment[:, :, k]
                    # Converts combined matrix to list and combines lists
                    matlist = mat.tolist()
                    #Combines the two lists
                    combined_list = list(zip(lt, matlist))
                    # Writes index specific parameter values to the text files
                    f.write("\t[*,*,{0}]:\t{1}\t:=\n".format(y, column_string))
                    for line in combined_list:
                        combinedflat = ''.join(str(line))
                        combinedflat = combinedflat.replace('[', '')
                        combinedflat = combinedflat.replace(']', '')
                        combinedflat = combinedflat.replace("'", '')
                        combinedflat = combinedflat.replace(",", '')
                        combinedflat = combinedflat.replace("(", '')
                        combinedflat = combinedflat.replace(")", '')
                        f.write("{0}\n".format(combinedflat))
            f.write(';\n')

            # TotalTechnologyAnnualActivityLowerLimit= np.zeros((lr,lt,ly))
            param = 'TotalTechnologyAnnualActivityLowerLimit'
            f.write('#\n')
            f.write("param\t{0}\tdefault\t{1}:=\n".format(
                param, defaults_dictionary[param]))
            if toggle_defaults[param] == True:
                # Writes parameter values to the text files
                for k in range(self.ly):
                    # Sets index value for format string
                    y = self.year[k]
                    # Converts matrix columns to strings columns to strings
                    columns = self.technology
                    column_string = ' '.join(columns)
                    # Converts maxtrix rows to list
                    array = np.array(self.region)
                    array = array.T
                    lt = array.tolist()
                    # Creates 2D matrix for this value
                    mat = self.TotalTechnologyAnnualActivityLowerLimit[:, :, k]
                    # Converts combined matrix to list and combines lists
                    matlist = mat.tolist()
                    #Combines the two lists
                    combined_list = list(zip(lt, matlist))
                    # Writes index specific parameter values to the text files
                    f.write("\t[*,*,{0}]:\t{1}\t:=\n".format(y, column_string))
                    for line in combined_list:
                        combinedflat = ''.join(str(line))
                        combinedflat = combinedflat.replace('[', '')
                        combinedflat = combinedflat.replace(']', '')
                        combinedflat = combinedflat.replace("'", '')
                        combinedflat = combinedflat.replace(",", '')
                        combinedflat = combinedflat.replace("(", '')
                        combinedflat = combinedflat.replace(")", '')
                        f.write("{0}\n".format(combinedflat))
            f.write(';\n')

            # TotalTechnologyAnnualActivityUpperLimit = np.zeros((lr,lt,ly))
            param = 'TotalTechnologyAnnualActivityUpperLimit'
            f.write('#\n')
            f.write("param\t{0}\tdefault\t{1}:=\n".format(
                param, defaults_dictionary[param]))
            if toggle_defaults[param] == True:
                # Writes parameter values to the text files
                for k in range(self.ly):
                    # Sets index value for format string
                    y = self.year[k]
                    # Converts matrix columns to strings columns to strings
                    columns = self.technology
                    column_string = ' '.join(columns)
                    # Converts maxtrix rows to list
                    array = np.array(self.region)
                    array = array.T
                    lt = array.tolist()
                    # Creates 2D matrix for this value
                    mat = self.TotalTechnologyAnnualActivityUpperLimit[:, :, k]
                    # Converts combined matrix to list and combines lists
                    matlist = mat.tolist()
                    #Combines the two lists
                    combined_list = list(zip(lt, matlist))
                    # Writes index specific parameter values to the text files
                    f.write("\t[*,*,{0}]:\t{1}\t:=\n".format(y, column_string))
                    for line in combined_list:
                        combinedflat = ''.join(str(line))
                        combinedflat = combinedflat.replace('[', '')
                        combinedflat = combinedflat.replace(']', '')
                        combinedflat = combinedflat.replace("'", '')
                        combinedflat = combinedflat.replace(",", '')
                        combinedflat = combinedflat.replace("(", '')
                        combinedflat = combinedflat.replace(")", '')
                        f.write("{0}\n".format(combinedflat))
            f.write(';\n')

            # TotalTechnologyModelPeriodActivityUpperLimit = np.zeros((lr,lt))
            param = 'TotalTechnologyModelPeriodActivityUpperLimit'  # Change this line
            f.write('#\n')
            columns = self.technology  # Change this line
            column_string = ' '.join(columns)
            if toggle_defaults[param] == True:
                # Writes index specific parameter values to the text files
                f.write("param\t{0}\tdefault\t{1}:\t{2}:=\n".format(
                    param, defaults_dictionary[param], column_string))
                # Converts maxtrix rows to list
                array = np.array(self.region)  # Change this line
                array = array.T
                lt = array.tolist()
                # Creates 2D matrix for this value
                mat = self.TotalTechnologyModelPeriodActivityUpperLimit[:, :]  # Change this line
                # Converts combined matrix to list and combines lists
                matlist = mat.tolist()
                #Combines the two lists
                combined_list = list(zip(lt, matlist))
                for line in combined_list:
                    combinedflat = ''.join(str(line))
                    combinedflat = combinedflat.replace('[', '')
                    combinedflat = combinedflat.replace(']', '')
                    combinedflat = combinedflat.replace("'", '')
                    combinedflat = combinedflat.replace(",", '')
                    combinedflat = combinedflat.replace("(", '')
                    combinedflat = combinedflat.replace(")", '')
                    f.write("{0}\n".format(combinedflat))
            else:
                f.write("param\t{0}\tdefault\t{1}:=\n".format(
                    param, defaults_dictionary[param]))
            f.write(';\n')

            # TotalTechnologyModelPeriodActivityLowerLimit = np.zeros((lr,lt))
            param = 'TotalTechnologyModelPeriodActivityLowerLimit'  # Change this line
            f.write('#\n')
            columns = self.technology  # Change this line
            column_string = ' '.join(columns)
            if toggle_defaults[param] == True:
                # Writes index specific parameter values to the text files
                f.write("param\t{0}\tdefault\t{1}:\t{2}:=\n".format(
                    param, defaults_dictionary[param], column_string))
                # Converts maxtrix rows to list
                array = np.array(self.region)  # Change this line
                array = array.T
                lt = array.tolist()
                # Creates 2D matrix for this value
                mat = self.TotalTechnologyModelPeriodActivityLowerLimit[:, :]  # Change this line
                # Converts combined matrix to list and combines lists
                matlist = mat.tolist()
                #Combines the two lists
                combined_list = list(zip(lt, matlist))
                for line in combined_list:
                    combinedflat = ''.join(str(line))
                    combinedflat = combinedflat.replace('[', '')
                    combinedflat = combinedflat.replace(']', '')
                    combinedflat = combinedflat.replace("'", '')
                    combinedflat = combinedflat.replace(",", '')
                    combinedflat = combinedflat.replace("(", '')
                    combinedflat = combinedflat.replace(")", '')
                    f.write("{0}\n".format(combinedflat))
            else:
                f.write("param\t{0}\tdefault\t{1}:=\n".format(
                    param, defaults_dictionary[param]))
            f.write(';\n')

            # ReserveMarginTagTechnology = np.zeros((lr,lt,ly))
            param = 'ReserveMarginTagTechnology'
            f.write('#\n')
            f.write("param\t{0}\tdefault\t{1}:=\n".format(
                param, defaults_dictionary[param]))
            if toggle_defaults[param] == True:
                # Writes parameter values to the text files
                for k in range(self.ly):
                    # Sets index value for format string
                    y = self.year[k]
                    # Converts matrix columns to strings columns to strings
                    columns = self.technology
                    column_string = ' '.join(columns)
                    # Converts maxtrix rows to list
                    array = np.array(self.region)
                    array = array.T
                    lt = array.tolist()
                    # Creates 2D matrix for this value
                    mat = self.ReserveMarginTagTechnology[:, :, k]
                    # Converts combined matrix to list and combines lists
                    matlist = mat.tolist()
                    #Combines the two lists
                    combined_list = list(zip(lt, matlist))
                    # Writes index specific parameter values to the text files
                    f.write("\t[*,*,{0}]:\t{1}\t:=\n".format(y, column_string))
                    for line in combined_list:
                        combinedflat = ''.join(str(line))
                        combinedflat = combinedflat.replace('[', '')
                        combinedflat = combinedflat.replace(']', '')
                        combinedflat = combinedflat.replace("'", '')
                        combinedflat = combinedflat.replace(",", '')
                        combinedflat = combinedflat.replace("(", '')
                        combinedflat = combinedflat.replace(")", '')
                        f.write("{0}\n".format(combinedflat))
            f.write(';\n')

            # ReserveMarginTagFuel = np.zeros((lr,lf,ly))
            param = 'ReserveMarginTagFuel'
            f.write('#\n')
            f.write("param\t{0}\tdefault\t{1}:=\n".format(
                param, defaults_dictionary[param]))
            if toggle_defaults[param] == True:
                # Writes parameter values to the text files
                for k in range(self.ly):
                    # Sets index value for format string
                    y = self.year[k]
                    # Converts matrix columns to strings columns to strings
                    columns = self.fuel
                    column_string = ' '.join(columns)
                    # Converts maxtrix rows to list
                    array = np.array(self.region)
                    array = array.T
                    lt = array.tolist()
                    # Creates 2D matrix for this value
                    mat = self.ReserveMarginTagFuel[:, :, k]
                    # Converts combined matrix to list and combines lists
                    matlist = mat.tolist()
                    #Combines the two lists
                    combined_list = list(zip(lt, matlist))
                    # Writes index specific parameter values to the text files
                    f.write("\t[*,*,{0}]:\t{1}\t:=\n".format(y, column_string))
                    for line in combined_list:
                        combinedflat = ''.join(str(line))
                        combinedflat = combinedflat.replace('[', '')
                        combinedflat = combinedflat.replace(']', '')
                        combinedflat = combinedflat.replace("'", '')
                        combinedflat = combinedflat.replace(",", '')
                        combinedflat = combinedflat.replace("(", '')
                        combinedflat = combinedflat.replace(")", '')
                        f.write("{0}\n".format(combinedflat))
            f.write(';\n')

            # ReserveMargin = np.zeros((lr,ly))
            param = 'ReserveMargin'  # Change this line
            f.write('#\n')
            columns = self.year  # Change this line
            column_string = ' '.join(columns)
            if toggle_defaults[param] == True:
                # Writes index specific parameter values to the text files
                f.write("param\t{0}\tdefault\t{1}:\t{2}:=\n".format(
                    param, defaults_dictionary[param], column_string))
                # Converts maxtrix rows to list
                array = np.array(self.region)  # Change this line
                array = array.T
                lt = array.tolist()
                # Creates 2D matrix for this value
                mat = self.ReserveMargin[:, :]  # Change this line
                # Converts combined matrix to list and combines lists
                matlist = mat.tolist()
                #Combines the two lists
                combined_list = list(zip(lt, matlist))
                for line in combined_list:
                    combinedflat = ''.join(str(line))
                    combinedflat = combinedflat.replace('[', '')
                    combinedflat = combinedflat.replace(']', '')
                    combinedflat = combinedflat.replace("'", '')
                    combinedflat = combinedflat.replace(",", '')
                    combinedflat = combinedflat.replace("(", '')
                    combinedflat = combinedflat.replace(")", '')
                    f.write("{0}\n".format(combinedflat))
            else:
                f.write("param\t{0}\tdefault\t{1}:=\n".format(
                    param, defaults_dictionary[param]))
            f.write(';\n')

            # RETagTechnology = np.zeros((lr,lt,ly))
            param = 'RETagTechnology'
            f.write('#\n')
            f.write("param\t{0}\tdefault\t{1}:=\n".format(
                param, defaults_dictionary[param]))
            if toggle_defaults[param] == True:
                # Writes parameter values to the text files
                for k in range(self.ly):
                    # Sets index value for format string
                    y = self.year[k]
                    # Converts matrix columns to strings columns to strings
                    columns = self.technology
                    column_string = ' '.join(columns)
                    # Converts maxtrix rows to list
                    array = np.array(self.region)
                    array = array.T
                    lt = array.tolist()
                    # Creates 2D matrix for this value
                    mat = self.RETagTechnology[:, :, k]
                    # Converts combined matrix to list and combines lists
                    matlist = mat.tolist()
                    #Combines the two lists
                    combined_list = list(zip(lt, matlist))
                    # Writes index specific parameter values to the text files
                    f.write("\t[*,*,{0}]:\t{1}\t:=\n".format(y, column_string))
                    for line in combined_list:
                        combinedflat = ''.join(str(line))
                        combinedflat = combinedflat.replace('[', '')
                        combinedflat = combinedflat.replace(']', '')
                        combinedflat = combinedflat.replace("'", '')
                        combinedflat = combinedflat.replace(",", '')
                        combinedflat = combinedflat.replace("(", '')
                        combinedflat = combinedflat.replace(")", '')
                        f.write("{0}\n".format(combinedflat))
            f.write(';\n')

            # RETagFuel = np.zeros((lr,lf,ly))
            param = 'RETagFuel'
            f.write('#\n')
            f.write("param\t{0}\tdefault\t{1}:=\n".format(
                param, defaults_dictionary[param]))
            if toggle_defaults[param] == True:
                # Writes parameter values to the text files
                for k in range(self.ly):
                    # Sets index value for format string
                    y = self.year[k]
                    # Converts matrix columns to strings columns to strings
                    columns = self.fuel
                    column_string = ' '.join(columns)
                    # Converts maxtrix rows to list
                    array = np.array(self.region)
                    array = array.T
                    lt = array.tolist()
                    # Creates 2D matrix for this value
                    mat = self.RETagFuel[:, :, k]
                    # Converts combined matrix to list and combines lists
                    matlist = mat.tolist()
                    #Combines the two lists
                    combined_list = list(zip(lt, matlist))
                    # Writes index specific parameter values to the text files
                    f.write("\t[*,*,{0}]:\t{1}\t:=\n".format(y, column_string))
                    for line in combined_list:
                        combinedflat = ''.join(str(line))
                        combinedflat = combinedflat.replace('[', '')
                        combinedflat = combinedflat.replace(']', '')
                        combinedflat = combinedflat.replace("'", '')
                        combinedflat = combinedflat.replace(",", '')
                        combinedflat = combinedflat.replace("(", '')
                        combinedflat = combinedflat.replace(")", '')
                        f.write("{0}\n".format(combinedflat))
            f.write(';\n')

            # REMinProductionTarget = np.zeros((lr,ly))
            param = 'REMinProductionTarget'  # Change this line
            f.write('#\n')
            columns = self.year  # Change this line
            column_string = ' '.join(columns)
            if toggle_defaults[param] == True:
                # Writes index specific parameter values to the text files
                f.write("param\t{0}\tdefault\t{1}:\t{2}:=\n".format(
                    param, defaults_dictionary[param], column_string))
                # Converts maxtrix rows to list
                array = np.array(self.region)  # Change this line
                array = array.T
                lt = array.tolist()
                # Creates 2D matrix for this value
                mat = self.REMinProductionTarget[:, :]  # Change this line
                # Converts combined matrix to list and combines lists
                matlist = mat.tolist()
                #Combines the two lists
                combined_list = list(zip(lt, matlist))
                for line in combined_list:
                    combinedflat = ''.join(str(line))
                    combinedflat = combinedflat.replace('[', '')
                    combinedflat = combinedflat.replace(']', '')
                    combinedflat = combinedflat.replace("'", '')
                    combinedflat = combinedflat.replace(",", '')
                    combinedflat = combinedflat.replace("(", '')
                    combinedflat = combinedflat.replace(")", '')
                    f.write("{0}\n".format(combinedflat))
            else:
                f.write("param\t{0}\tdefault\t{1}:=\n".format(
                    param, defaults_dictionary[param]))
            f.write(';\n')

            # EmissionActivityRatio = np.zeros((lr,lt,le,lm,ly))
            #Writes new line character at parameter metadata to the text file
            param = 'EmissionActivityRatio'  # Change this line
            f.write('#\n')
            f.write("param\t{0}\tdefault\t{1}:=\n".format(
                param, defaults_dictionary[param]))
            if toggle_defaults[param] == True:
                # Writes parameter values to the text files
                for i in range(self.le):  # Change loops if you need
                    # Sets index value for format string
                    emission = self.emission[i]
                    for j in range(self.lm):
                        # Sets index value for format string
                        MOO = self.mode_of_operation[j]
                        for k in range(self.ly):
                            # Sets index value for format string
                            y = self.year[k]
                            # Converts matrix columns to strings columns to strings
                            columns = self.technology
                            column_string = ' '.join(columns)
                            # Converts maxtrix rows to list
                            array = np.array(self.region)
                            array = array.T
                            lt = array.tolist()
                            # Creates 2D matrix for this value
                            mat = self.EmissionActivityRatio[:, :, i, j, k]
                            # Converts combined matrix to list and combines lists
                            matlist = mat.tolist()
                            #Combines the two lists
                            combined_list = list(zip(lt, matlist))
                            # Writes index specific parameter values to the text files
                            f.write("\t[*,*,{0},{1},{2}]:\t{3}\t:=\n".format(
                                emission, MOO, y, column_string))
                            for line in combined_list:
                                combinedflat = ''.join(str(line))
                                combinedflat = combinedflat.replace('[', '')
                                combinedflat = combinedflat.replace(']', '')
                                combinedflat = combinedflat.replace("'", '')
                                combinedflat = combinedflat.replace(",", '')
                                combinedflat = combinedflat.replace("(", '')
                                combinedflat = combinedflat.replace(")", '')
                                f.write("{0}\n".format(combinedflat))
            f.write(';\n')

            # EmissionsPenalty = np.zeros((lr,le,ly))
            param = 'EmissionsPenalty'
            f.write('#\n')
            f.write("param\t{0}\tdefault\t{1}:=\n".format(
                param, defaults_dictionary[param]))
            if toggle_defaults[param] == True:
                # Writes parameter values to the text files
                for k in range(self.ly):
                    # Sets index value for format string
                    y = self.year[k]
                    # Converts matrix columns to strings columns to strings
                    columns = self.emission
                    column_string = ' '.join(columns)
                    # Converts maxtrix rows to list
                    array = np.array(self.region)
                    array = array.T
                    lt = array.tolist()
                    # Creates 2D matrix for this value
                    mat = self.EmissionsPenalty[:, :, k]
                    # Converts combined matrix to list and combines lists
                    matlist = mat.tolist()
                    #Combines the two lists
                    combined_list = list(zip(lt, matlist))
                    # Writes index specific parameter values to the text files
                    f.write("\t[*,*,{0}]:\t{1}\t:=\n".format(y, column_string))
                    for line in combined_list:
                        combinedflat = ''.join(str(line))
                        combinedflat = combinedflat.replace('[', '')
                        combinedflat = combinedflat.replace(']', '')
                        combinedflat = combinedflat.replace("'", '')
                        combinedflat = combinedflat.replace(",", '')
                        combinedflat = combinedflat.replace("(", '')
                        combinedflat = combinedflat.replace(")", '')
                        f.write("{0}\n".format(combinedflat))
            f.write(';\n')

            # AnnualExogenousEmission = np.zeros((lr,le,ly))
            param = 'AnnualExogenousEmission'
            f.write('#\n')
            f.write("param\t{0}\tdefault\t{1}:=\n".format(
                param, defaults_dictionary[param]))
            if toggle_defaults[param] == True:
                # Writes parameter values to the text files
                for k in range(self.ly):
                    # Sets index value for format string
                    y = self.year[k]
                    # Converts matrix columns to strings columns to strings
                    columns = self.emission
                    column_string = ' '.join(columns)
                    # Converts maxtrix rows to list
                    array = np.array(self.region)
                    array = array.T
                    lt = array.tolist()
                    # Creates 2D matrix for this value
                    mat = self.AnnualExogenousEmission[:, :, k]
                    # Converts combined matrix to list and combines lists
                    matlist = mat.tolist()
                    #Combines the two lists
                    combined_list = list(zip(lt, matlist))
                    # Writes index specific parameter values to the text files
                    f.write("\t[*,*,{0}]:\t{1}\t:=\n".format(y, column_string))
                    for line in combined_list:
                        combinedflat = ''.join(str(line))
                        combinedflat = combinedflat.replace('[', '')
                        combinedflat = combinedflat.replace(']', '')
                        combinedflat = combinedflat.replace("'", '')
                        combinedflat = combinedflat.replace(",", '')
                        combinedflat = combinedflat.replace("(", '')
                        combinedflat = combinedflat.replace(")", '')
                        f.write("{0}\n".format(combinedflat))
            f.write(';\n')

            # AnnualEmissionLimit = np.zeros((lr,le,ly))
            param = 'AnnualEmissionLimit'
            f.write('#\n')
            f.write("param\t{0}\tdefault\t{1}:=\n".format(
                param, defaults_dictionary[param]))
            if toggle_defaults[param] == True:
                # Writes parameter values to the text files
                for k in range(self.ly):
                    # Sets index value for format string
                    y = self.year[k]
                    # Converts matrix columns to strings columns to strings
                    columns = self.emission
                    column_string = ' '.join(columns)
                    # Converts maxtrix rows to list
                    array = np.array(self.region)
                    array = array.T
                    lt = array.tolist()
                    # Creates 2D matrix for this value
                    mat = self.AnnualExogenousEmission[:, :, k]
                    # Converts combined matrix to list and combines lists
                    matlist = mat.tolist()
                    #Combines the two lists
                    combined_list = list(zip(lt, matlist))
                    # Writes index specific parameter values to the text files
                    f.write("\t[*,*,{0}]:\t{1}\t:=\n".format(y, column_string))
                    for line in combined_list:
                        combinedflat = ''.join(str(line))
                        combinedflat = combinedflat.replace('[', '')
                        combinedflat = combinedflat.replace(']', '')
                        combinedflat = combinedflat.replace("'", '')
                        combinedflat = combinedflat.replace(",", '')
                        combinedflat = combinedflat.replace("(", '')
                        combinedflat = combinedflat.replace(")", '')
                        f.write("{0}\n".format(combinedflat))
            f.write(';\n')

            # ModelPeriodExogenousEmission = np.zeros((lr,le))
            param = 'ModelPeriodExogenousEmission'  # Change this line
            f.write('#\n')
            columns = self.emission  # Change this line
            column_string = ' '.join(columns)
            if toggle_defaults[param] == True:
                # Writes index specific parameter values to the text files
                f.write("param\t{0}\tdefault\t{1}:\t{2}:=\n".format(
                    param, defaults_dictionary[param], column_string))
                # Converts maxtrix rows to list
                array = np.array(self.region)  # Change this line
                array = array.T
                lt = array.tolist()
                # Creates 2D matrix for this value
                mat = self.ModelPeriodExogenousEmission[:, :]  # Change this line
                # Converts combined matrix to list and combines lists
                matlist = mat.tolist()
                #Combines the two lists
                combined_list = list(zip(lt, matlist))
                # Writes index specific parameter values to the text files
                f.write("param\t{0}\t:{1}:=\n".format(param, column_string))
                for line in combined_list:
                    combinedflat = ''.join(str(line))
                    combinedflat = combinedflat.replace('[', '')
                    combinedflat = combinedflat.replace(']', '')
                    combinedflat = combinedflat.replace("'", '')
                    combinedflat = combinedflat.replace(",", '')
                    combinedflat = combinedflat.replace("(", '')
                    combinedflat = combinedflat.replace(")", '')
                    f.write("{0}\n".format(combinedflat))
            else:
                f.write("param\t{0}\tdefault\t{1}:=\n".format(
                    param, defaults_dictionary[param]))
            f.write(';\n')

            # ModelPeriodEmissionLimit = np.zeros((lr,le))
            param = 'ModelPeriodEmissionLimit'  # Change this line
            f.write('#\n')
            columns = self.emission  # Change this line
            column_string = ' '.join(columns)
            if toggle_defaults[param] == True:
                # Writes index specific parameter values to the text files
                f.write("param\t{0}\tdefault\t{1}:\t{2}:=\n".format(
                    param, defaults_dictionary[param], column_string))
                # Converts maxtrix rows to list
                array = np.array(self.region)  # Change this line
                array = array.T
                lt = array.tolist()
                # Creates 2D matrix for this value
                mat = self.ModelPeriodEmissionLimit[:, :]  # Change this line
                # Converts combined matrix to list and combines lists
                matlist = mat.tolist()
                #Combines the two lists
                combined_list = list(zip(lt, matlist))
                # Writes index specific parameter values to the text files
                f.write("param\t{0}\t:{1}:=\n".format(param, column_string))
                for line in combined_list:
                    combinedflat = ''.join(str(line))
                    combinedflat = combinedflat.replace('[', '')
                    combinedflat = combinedflat.replace(']', '')
                    combinedflat = combinedflat.replace("'", '')
                    combinedflat = combinedflat.replace(",", '')
                    combinedflat = combinedflat.replace("(", '')
                    combinedflat = combinedflat.replace(")", '')
                    f.write("{0}\n".format(combinedflat))
            else:
                f.write("param\t{0}\tdefault\t{1}:=\n".format(
                    param, defaults_dictionary[param]))
            f.write(';\n')
            f.write('end;\n')
            f.write('#')
        return
