import os
import pandas as pd
from datetime import datetime
import numpy as np

class LocalValidator:

    def __init__(self, store=False, history=False, united=True, identifier = None ,path="./validation_logs", file_type="pkl"):
        """
        Args:
            store (bool): Whether to store validation results.
            history (bool): Whether to store logs with historical data.
            united (bool): Whether to store all validations in one file or separately.
            path (str): Directory path where logs will be stored.
            file_type (str): The file format for storing validation results. Options are 'csv', 'xlsx', 'pkl', 'txt'.

        Raises:
            TypeError: If any of the input arguments are not of the expected type.

        """


        # Initialize attributes based on user input
        self.store = store  # Determines whether to store validation results
        self.united = united  # Determines whether to store all validations in one file
        self.history = history  # Determines whether to store logs with historical data
        self.file_type = file_type.lower()  # File type for storing validation results
        self.identifier = identifier  # Determines whether to store logs with historical data

        # Set the path for storing logs, including daily subdirectories if history is True
        if history:
            self.path = os.path.join(path, f"{datetime.now().strftime('%Y-%m-%d')}")
        else:
            self.path = path

        # Initialize an empty DataFrame for storing all validation results if united is True
        self.all_validations_df = pd.DataFrame()

        # Validate the types of the input arguments
        if not isinstance(store, bool):
            raise TypeError("The 'store' argument must be a boolean.")
        if not isinstance(united, bool):
            raise TypeError("The 'united' argument must be a boolean.")
        if not isinstance(history, bool):
            raise TypeError("The 'history' argument must be a boolean.")
        if not isinstance(file_type, str):
            raise TypeError("The 'file_type' argument must be a string.")

        # Create the directory if it doesn't exist
        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def range_check(self, *, column: str, borders: list, name: str, **kwargs):
        """
        Decorator to validate that the values in a specified column fall within given ranges.

        Args:
            column (str): The column in the DataFrame to be validated.
            borders (list): A list of tuples, each containing two numeric values representing the lower and upper bounds.
            name (str): The name of the validation for logging purposes.

        Returns:
            function: A wrapped function with the validation applied.

        Raises:
            TypeError: If input arguments are not of the expected type.
        """

        # Validate input types
        if not isinstance(column, str):
            raise TypeError("The 'column' argument must be a string.")
        if not isinstance(borders, list) or not all(isinstance(i, tuple) and len(i) == 2 for i in borders):
            raise TypeError("The 'borders' argument must be a list of tuples with two numeric values.")
        if not isinstance(name, str):
            raise TypeError("The 'name' argument must be a string.")

        def decorator(func):
            def wrapper(df, *args, **kwargs_func):
                # Check if the specified column exists in the DataFrame
                if column not in df.columns:
                    raise TypeError(f"Error: Column '{column}' not found in DataFrame.")

                # Initialize a boolean Series to track whether values are within any of the specified ranges
                in_range_mask = pd.Series([False] * len(df))

                # Iterate over the list of borders and update the mask for values within the range
                for bottom, top in borders:
                    in_range_mask |= df[column].between(bottom, top)

                # Identify rows where values are out of bounds
                out_of_bounds = df.loc[~in_range_mask].copy()

                # Save the out-of-bounds rows if any exist and storing is enabled
                if not out_of_bounds.empty and self.store:
                    self.save(out_of_bounds, name)

                # Execute the wrapped function with the original arguments
                return func(df, *args, **kwargs_func)

            return wrapper
        return decorator

    def value_check(self, *, column: str, allowed: list = None, not_allowed: list = None, name: str, **kwargs):
        """
        Decorator to validate that the values in a specified column are either allowed or not allowed.

        Args:
            column (str): The column in the DataFrame to be validated.
            allowed (list, optional): A list of allowed values for the column.
            not_allowed (list, optional): A list of not allowed values for the column.
            name (str): The name of the validation for logging purposes.

        Returns:
            function: A wrapped function with the validation applied.

        Raises:
            TypeError: If input arguments are not of the expected type.
        """

        # Validate input types
        if not isinstance(column, str):
            raise TypeError("The 'column' argument must be a string.")
        if allowed is not None and not isinstance(allowed, list):
            raise TypeError("The 'allowed' argument must be a list.")
        if not_allowed is not None and not isinstance(not_allowed, list):
            raise TypeError("The 'not_allowed' argument must be a list.")
        if not isinstance(name, str):
            raise TypeError("The 'name' argument must be a string.")

        def decorator(func):
            def wrapper(df, *args, **kwargs_func):
                # Check if the specified column exists in the DataFrame
                if column not in df.columns:
                    raise TypeError(f"Error: Column '{column}' not found in DataFrame.")

                # Initialize an empty DataFrame to store invalid rows
                invalid_rows = pd.DataFrame()

                # Validate against the allowed list, if provided
                if allowed is not None:
                    invalid_rows_allowed = df[~df[column].isin(allowed)]
                    invalid_rows = pd.concat([invalid_rows, invalid_rows_allowed])

                # Validate against the not allowed list, if provided
                if not_allowed is not None:
                    invalid_rows_not_allowed = df[df[column].isin(not_allowed)]
                    invalid_rows = pd.concat([invalid_rows, invalid_rows_not_allowed])

                # Save the invalid rows if any exist and storing is enabled
                if not invalid_rows.empty and self.store:
                    self.save(invalid_rows, name)

                # Execute the wrapped function with the original arguments
                return func(df, *args, **kwargs_func)

            return wrapper
        return decorator

    def statistical(self, *, column: str, name: str, sensitivity="medium", data_type=None, **kwargs):
        """
        Decorator to apply statistical outlier detection on a DataFrame column.
        Uses z-score for continuous data and frequency-based detection for discrete data.

        Args:
            column (str): The column in the DataFrame to be validated.
            name (str): The name of the validation for logging purposes.
            sensitivity (str): The sensitivity level of the validation. Options are 'sensitive', 'medium', 'insensitive'.
            data_type (str, optional): Specify 'continuous' or 'discrete'. If None, the type will be inferred.

        Returns:
            function: A wrapped function with the statistical validation applied.

        Raises:
            TypeError: If input arguments are not of the expected type.
            ValueError: If an invalid value is provided for 'sensitivity' or 'data_type'.
        """

        # Validate input types
        if not isinstance(column, str):
            raise TypeError("The 'column' argument must be a string.")
        if not isinstance(name, str):
            raise TypeError("The 'name' argument must be a string.")
        if not isinstance(sensitivity, str):
            raise TypeError("The 'sensitivity' argument must be a string.")
        if sensitivity.lower() not in ['sensitive', 'medium', 'insensitive']:
            raise ValueError("The 'sensitivity' argument must be one of 'sensitive', 'medium', or 'insensitive'.")
        if data_type is not None and data_type.lower() not in ['continuous', 'discrete']:
            raise ValueError("The 'data_type' argument must be 'continuous', 'discrete', or None.")

        def decorator(func):
            def wrapper(df, *args, **kwargs_func):
                # Check if the specified column exists in the DataFrame
                if column not in df.columns:
                    raise TypeError(f"Error: Column '{column}' not found in DataFrame.")

                # Infer data type if not provided
                if data_type is None:
                    num_unique_values = df[column].nunique()
                    total_values = len(df[column])
                    unique_ratio = num_unique_values / total_values

                    # Heuristic: If the number of unique values is less than 5% of total, treat as discrete
                    if unique_ratio < 0.05:
                        inferred_type = 'discrete'
                    else:
                        inferred_type = 'continuous'
                else:
                    inferred_type = data_type.lower()


                # Initialize an empty DataFrame to store outliers
                outliers = pd.DataFrame()

                if inferred_type == 'continuous':
                    # Ensure the column is numeric
                    if not pd.api.types.is_numeric_dtype(df[column]):
                        raise TypeError(f"Column '{column}' must be numeric for continuous outlier detection.")

                    # Select thresholds based on 'sensitivity'
                    if sensitivity.lower() == 'sensitive':
                        z_score_threshold = 2.0
                    elif sensitivity.lower() == 'medium':
                        z_score_threshold = 3.0
                    elif sensitivity.lower() == 'insensitive':
                        z_score_threshold = 4.0

                    # Data is continuous, use z-score method
                    mean = df[column].mean()
                    std_dev = df[column].std()
                    z_scores = np.abs((df[column] - mean) / std_dev)

                    # Identify outliers using z-score method
                    outliers = df[z_scores > z_score_threshold]

                elif inferred_type == 'discrete':
                    # Define low frequency threshold percentage based on sensitivity
                    if sensitivity.lower() == 'sensitive':
                        low_frequency_threshold_percentage = 2
                    elif sensitivity.lower() == 'medium':
                        low_frequency_threshold_percentage = 1
                    elif sensitivity.lower() == 'insensitive':
                        low_frequency_threshold_percentage = 0.5

                    # Calculate frequency counts
                    frequency_counts = df[column].value_counts()
                    total_counts = frequency_counts.sum()
                    # Determine the threshold for low-frequency values
                    low_threshold_value = total_counts * (low_frequency_threshold_percentage / 100.0)
                    # Identify values that occur less frequently than the threshold
                    outlier_values = frequency_counts[frequency_counts < low_threshold_value].index.tolist()
                    # Filter out the rows containing these outlier values
                    outliers = df[df[column].isin(outlier_values)]

                else:
                    raise ValueError("Invalid data type specified.")

                # Save the outliers if any exist and storing is enabled
                if not outliers.empty and self.store:
                    self.save(outliers, name)

                # Execute the wrapped function with the original arguments
                return func(df, *args, **kwargs_func)

            return wrapper
        return decorator

    def custom_check(self, *, custom_logic, name: str, **kwargs):
        """
        Decorator to apply custom validation logic on a DataFrame.

        Args:
            custom_logic (str or callable): The custom logic for validation, can be a query string or a function.
            name (str): The name of the validation for logging purposes.

        Returns:
            function: A wrapped function with the custom validation applied.

        Raises:
            TypeError: If input arguments are not of the expected type.
            ValueError: If the custom logic string or function fails to execute.
        """

        # Validate input types
        if not (isinstance(custom_logic, str) or callable(custom_logic)):
            raise TypeError("The 'custom_logic' argument must be a string or a callable (function).")
        if not isinstance(name, str):
            raise TypeError("The 'name' argument must be a string.")

        def decorator(func):
            def wrapper(df, *args, **kwargs_func):
                # Apply custom logic if it's a string (query)
                if isinstance(custom_logic, str):
                    try:
                        invalid_rows = df.query(custom_logic)
                    except Exception as e:
                        raise ValueError(f"Error in custom logic: {str(e)}")

                # Apply custom logic if it's a callable (function)
                elif callable(custom_logic):
                    try:
                        invalid_rows = custom_logic(df)
                    except Exception as e:
                        raise ValueError(f"Error in custom function: {str(e)}")

                    # Convert Series result to DataFrame for consistency
                    if isinstance(invalid_rows, pd.Series):
                        invalid_rows = df.loc[invalid_rows].copy()
                    elif not isinstance(invalid_rows, pd.DataFrame):
                        raise TypeError("The custom function must return a pandas Series or DataFrame.")

                # Save the invalid rows if any exist and storing is enabled
                if not invalid_rows.empty and self.store:
                    self.save(invalid_rows, name)

                # Execute the wrapped function with the original arguments
                return func(df, *args, **kwargs_func)

            return wrapper

        return decorator

    def save(self, outliers, name):
        """
        Saves the outliers to a file based on the validator settings.

        Args:
            outliers (pd.DataFrame): DataFrame containing the outliers.
            name (str): The name of the validation for logging purposes.
        """
        # Create a copy of the outliers DataFrame to avoid modifying the original
        outliers = outliers.copy()

        # Add a new column to track the name of the validation that generated the outliers
        outliers["Validation Name"] = name

        # If united is True, concatenate the outliers with the existing DataFrame of all validations
        if self.united:
            self.all_validations_df = pd.concat([self.all_validations_df, outliers], ignore_index=True)
            # Save the combined DataFrame to a file named 'log' in the specified path
            if self.identifier:
                self.all_validations_df = self.all_validations_df[[self.identifier,"Validation Name"]]
            self.save_file(self.all_validations_df, os.path.join(self.path, "log"))
        else:
            # Save the outliers DataFrame to a file named after the validation name
            if self.identifier:
                outliers = outliers[[self.identifier,"Validation Name"]]
            self.save_file(outliers, os.path.join(self.path, f"{name}"))

    def save_file(self, df, file_name):
        """
        Saves a DataFrame to a file in the specified format.

        Args:
            df (pd.DataFrame): The DataFrame to save.
            file_name (str): The path and base name of the file.

        Raises:
            ValueError: If the specified file type is not supported.
        """
        # Check the file type and save the DataFrame accordingly
        if self.file_type == "csv":
            df.to_csv(f"{file_name}.csv", index=False, encoding='utf-8')
        elif self.file_type == "xlsx":
            df.to_excel(f"{file_name}.xlsx", index=False)
        elif self.file_type == "pkl":
            df.to_pickle(f"{file_name}.pkl")
        elif self.file_type == "txt":
            with open(f"{file_name}.txt", "w") as log:
                df.to_string(log)
                log.write("\n")
        else:
            # Raise an error if the file type is not supported
            raise ValueError("Unsupported file type. Supported types are: 'csv', 'xlsx', 'pkl', 'txt'")
