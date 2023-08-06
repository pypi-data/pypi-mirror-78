import os


class Navigation:
    """ Navigation is a class for navigating, manipulating and editing data in the GOCPI model.
    
    Attributes:
        Find_File(string) representing a string to the file path
    
    
    TODO: Fill out all functions below
            
    """
    def __init__(self, target_root, target_file):
        """ Initialises the navigation functions

        Args:
            target_root (str): Base directory to search from
            target_file (str): Name of file to search for
        """
        self.target_root = target_root
        self.target_file = target_file

    def Find_File(self):
        """
        Find_File searches for a target file, from a base directory, to construct
        a target directory.

        Inputs: 
        target_root = The base directory to search from (string).
        target_file = The name of the target file (string).

        Outputs: 
        f = Combinated target file location (string).
        """

        for root, dirs, files in os.walk(self.target_root):
            for name in files:
                if name == self.target_file:
                    f = os.path.abspath(os.path.join(root, name))
        return f

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
