#################################################################
# Optimisation contains the Optimisation Class to use CPLEX
#################################################################

# Import python modules
import os
import cplex as cp
import docplex as dp


# Begin class breakdown
class Optimisation:
    """ Prepare and runs optimisation with IBM ILOG CPLEX Optimisation Studio
    """
    def __init__(self):
        """ Initialise the optimisation class
        """

    def create_linear_programme_file(self, directory, data_file, model_file,
                                     output_file):
        """ Creates the model file through executing model system commands

            Args:
                directory (str): Name of directory to put data into
                data_file (str): Name of energy system data file
                model_file (str): Name of energy system model file
                output_file (str): Name of output linear programme
            """
        # Change the working directory
        os.chdir(directory)
        # Load the custom anaconda environment
        # This assumes the conda environment has already been initialised.
        os.system('conda activate osemosys')
        # Execute the file structure to create the linear programming file
        # (glpsol -m GOCPI_OSeMOSYS_Model.txt -d GOCPI_NZ_Example_Data.txt --wlp GOCPI_NZ_Example.lp)
        command = 'glpsol -m ' + data_file + ' -d ' + model_file + '--wlp ' + output_file
        os.system(command)
