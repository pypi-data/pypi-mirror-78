import os
import numpy as np
import pandas as pd
import inquirer as iq


class Forecasting:
    def __unit__(self):
        """Initialises the forecasting class
        """
        self.forecasts = None

    def energy_balance_base(self, root, IEA_World_Energy_Balances_1,
                            IEA_World_Energy_Balances_2,
                            create_excel_spreadsheet, output_file):
        """ Creates the baseline energy balance for forecasting

        Args:
            root (path): Path to provide access to all the files
            IEA_World_Energy_Balances_1 (str): File name for Energy Balance A to K
            IEA_World_Energy_Balances_2 ([type]): File name for Energy Balance L to Z
            create_excel_spreadsheet (boolean): True/false on whether to create a spreadsheet
            output_file (str): Name of output energy balance spreadsheet

        Returns:
            (dict): Dictionary of energy balances and unique lists (Use these key words to access: Energy Balances, Fuel, Geography, Technology)
        """
        IEAWEBAK = root / IEA_World_Energy_Balances_1
        IEAWEBLZ = root / IEA_World_Energy_Balances_2

        # Creates dataframes from IEA World Energy Statistics and Balances CSVs from Stats.OECD.org in the OECDiLibrary
        # Note the data is from #https:s//stats.oecd.org/ and #https://www-oecd-ilibrary-org.ezproxy.auckland.ac.nz/
        column_headers = [
            'ID', 'Unit', 'Geo_Code', 'Geo_Description', 'Prod_Code',
            'Prod_Description', 'Flow_Code', 'Flow_Description', 'Year',
            'Value(TJ)'
        ]
        f1 = open(IEAWEBAK, 'r')
        df_A = pd.read_csv(f1, header=None)
        df_A.columns = column_headers
        df_A.info(verbose=True)
        f2 = open(IEAWEBLZ, 'r')
        df_B = pd.read_csv(f2, header=None)
        df_B.columns = column_headers
        df_B.info(verbose=True)
        frames = [df_A, df_B]
        df = pd.concat(frames)
        df.info(verbose=True)

        # Closes the files
        f1.close()
        f2.close()

        # Finds the unique items in each list of the energy balance sheets
        unique_fuel = df.Prod_Description.unique()
        unique_geography = df.Geo_Description.unique()
        unique_technology = df.Flow_Description.unique()
        print(unique_geography)

        # Asks for a user to select a geography using the inquirer function
        selected_geo = input(
            "Please enter the geography you wish to extract energy balances:  "
        )

        # Creates a pivot table to display the data in the way similar to the Energy Balance Sheet (cols = Energy Product, rows = Energy Flows)
        energy_balance_pivot_table = pd.pivot_table(
            df,
            index=['Geo_Description', 'Flow_Description'],
            # Converted values to PJ
            values=['Value(TJ)'],
            columns=['Prod_Description'],
            aggfunc=[np.sum],
            fill_value=0)
        # Filters to the geography the user has selected
        Input_String = 'Geo_Description == ["' + selected_geo + '"]'
        geography_energy_balance_pivot_table = energy_balance_pivot_table.query(
            Input_String)

        if create_excel_spreadsheet == True:
            # Write the filtered pivot table to an excel file
            writer = pd.ExcelWriter(root / output_file)
            geography_energy_balance_pivot_table.to_excel(writer, selected_geo)
            writer.save()

        # Returns the unique lists and filtered pivot table as a dataframe
        return {
            "Energy Balances": geography_energy_balance_pivot_table,
            "Fuel": unique_fuel,
            "Geography": unique_geography,
            "Technology": unique_technology
        }

    def calculate_constant_average_growth_rate(self, start_year, end_year,
                                               start_value, end_value):
        """ Calculates the constant average growth rate (CAGR)

        Args:
            start_year (int): Starting year
            end_year (int): Ending year
            start_value (int): Initial value
            end_value (int): Final value

        Returns:
            cagr: Constant average growth rate (1+ decimal)
        """
        if start_value == 0 or (end_year - start_year) == 0:
            cagr = 1
        else:
            cagr = np.power((end_value / start_value),
                            (1 / (end_year - start_year)))
        return cagr

    def calculate_cagr_forecasts(self, cagr_dictionary, base_year_dictionary,
                                 fuel, year):
        """ Forecasts base year fuels by a constant average growth rate for a forecast period

        Args:
            cagr_dictionary (Dict): Dictionary of constant average growth rates per fuel
            base_year_dictionary ([type]): Dictionary of base year fuel consumption in energy types
            fuel (list): List of Fuels
            year (list): List of forecast years

        Returns:
            [float, array]: 2D Array of demand forecasts per fuel
        """
        # Initialises the size of the array
        forecast = np.ones((len(fuel), len(year)))

        # Set the first forecast as the base year
        for i in range(0, len(fuel), 1):
            forecast[i, 0] = base_year_dictionary[fuel[i]]

        # Calculates the forecasting
        for i in range(0, len(fuel), 1):
            for j in range(1, len(year), 1):
                forecast[i, j] = forecast[i, j - 1] * cagr_dictionary[fuel[j]]

        return forecast