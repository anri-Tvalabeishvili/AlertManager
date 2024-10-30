# AlertManager

## Overview

AlertManager is an open-source Python library designed to streamline and enhance data validation processes for both local Pandas DataFrames and database tables. It provides a suite of decorators that seamlessly integrate data validation checks into your data processing functions. By automating common validation tasks such as range checks, value checks, statistical outlier detection, and custom logic application, AlertManager helps maintain data integrity and quality throughout your data pipeline.

The library consists of two main components:

- **LocalValidator**: For validating data within Pandas DataFrames.
- **DatabaseValidator**: For validating data directly within database tables using SQLAlchemy.

With AlertManager, you can configure flexible alerting and logging options, ensuring that data anomalies are caught and handled appropriately before they impact your system.
# Table of Contents

- [Features](#features)
- [Installation](#installation)
  - [Using pip](#using-pip)
  - [Using conda](#using-conda)
- [Usage](#usage)
  - [1. LocalValidator](#1-localvalidator)
    - [Initialization](#initialization)
    - [Decorators](#decorators)
      - [1. range_check](#1-range_check)
      - [2. value_check](#2-value_check)
      - [3. statistical](#3-statistical)
      - [4. custom_check](#4-custom_check)
    - [Examples for Each Decorator](#examples-for-each-decorator)
      - [Example 1: range_check](#example-1-range_check)
      - [Example 2: value_check](#example-2-value_check)
      - [Example 3: statistical](#example-3-statistical)
      - [Example 4: custom_check](#example-4-custom_check)
  - [2. DatabaseValidator](#2-databasevalidator)
    - [Initialization](#initialization-1)
    - [Decorators](#decorators-1)
      - [1. range_check](#1-range_check-1)
      - [2. value_check](#2-value_check-1)
      - [3. statistical](#3-statistical-1)
      - [4. custom_check](#4-custom_check-1)
    - [Examples for Each Decorator](#examples-for-each-decorator-1)
      - [Example 1: range_check](#example-1-range_check-1)
      - [Example 2: value_check](#example-2-value_check-1)
      - [Example 3: statistical](#example-3-statistical-1)
      - [Example 4: custom_check](#example-4-custom_check-1)
- [Configuration Options](#configuration-options)
  - [Example Initialization with Custom Configuration](#example-initialization-with-custom-configuration)
    - [LocalValidator](#localvalidator)
    - [DatabaseValidator](#databasevalidator)
- [Best Practices and Detailed Explanations](#best-practices-and-detailed-explanations)
  - [Decorator Usage](#decorator-usage)
  - [Statistical Outlier Detection Sensitivity](#statistical-outlier-detection-sensitivity)
  - [Custom Validation Logic](#custom-validation-logic)
- [Alert Management](#alert-management)
- [Error Handling](#error-handling)
- [Conclusion](#conclusion)
- [Contribution and Support](#contribution-and-support)
- [License](#license)

## Features

- **Seamless Integration with Decorators**: Apply validations directly to your data processing functions using decorators, making data checks an integral part of your workflow.
- **Range Checks**: Validate that numeric values fall within specified ranges in DataFrames or database tables.
- **Value Checks**: Ensure that values in a column are within an allowed set or not within a disallowed set.
- **Statistical Outlier Detection**: Detect outliers in both continuous and discrete data using appropriate statistical methods, with customizable sensitivity levels.
- **Custom Validation Logic**: Implement custom validation rules using query strings or callable functions for specialized data checks.
- **Database Support**: Validate data directly in your databases using SQLAlchemy, supporting various database backends.
- **Flexible Alerting and Logging**: Store validation results with options for historical logging, unified or separate files, and multiple file formats (csv, xlsx, pkl, txt).
- **Configurable Alert Management**: Control how and where alerts are stored, and specify identifiers for easy tracking of validation issues.

By incorporating AlertManager into your data processing pipeline, you can proactively manage data quality issues, reduce the risk of errors, and maintain high standards of data integrity.

## Installation

You can install AlertManager using either pip or conda.

### Using pip

If AlertManager is available on PyPI, you can install it directly:

```bash
pip install AlertManager
```

### Using conda

If you prefer using `conda`, you can create a new environment and install AlertManager:

```bash
conda install -c conda-forge AlertManager
```


## Usage

AlertManager provides two main classes:

- **LocalValidator**: For validating Pandas DataFrames.
- **DatabaseValidator**: For validating data in database tables.

Each class offers the same set of validation decorators:

- **range_check**
- **value_check**
- **statistical**
- **custom_check**

### 1. LocalValidator

#### Initialization

To use `LocalValidator`, import the class and initialize it:

```python
import pandas as pd
from AlertManager import LocalValidator  # Replace with the correct import path

# Initialize the LocalValidator
AlertManager = LocalValidator(
store=True,
history=False,
united=True,
identifier='id',
path='./validation_logs',
file_type='csv'
)
```

**Parameters**:
- `store` (bool, default False): Whether to store validation results.
- `history` (bool, default False): Whether to store logs with historical data (creates subdirectories based on date).
- `united` (bool, default True): Whether to store all validations in one file (True) or separately (False).
- `identifier` (str, optional): Column name to identify rows (e.g., primary key).
- `path` (str, default './validation logs'): Directory path where logs will be stored.
- `file_type` (str, default 'pkl'): The file format for storing validation results. Options are 'csv', 'xlsx', 'pkl', 'txt'.

#### Decorators

##### 1. range_check  
   Validates that the values in a specified column fall within given ranges.

```python
@AlertManager.range_check(column='column_name', borders=[(lower_bound, upper_bound)], name='Validation Name')
def your_function(df):
    # Your data processing logic
    return df
```

**Parameters**:
- `column` (str): The column in the DataFrame to be validated.
- `borders` (list of tuple): A list of tuples, each containing two numeric values representing the lower and upper bounds.
- `name` (str): A name for the validation, used in logging.

##### 2. value_check
   Validates that the values in a specified column are either allowed or not allowed.

```python
@AlertManager.value_check(column='column_name', allowed=['value1', 'value2'], not_allowed=['value3'], name='Validation Name')
def your_function(df):
  # Your data processing logic
  return df
```

**Parameters**:
- `column` (str): The column in the DataFrame to be validated.
- `allowed` (list, optional): A list of allowed values for the column.
- `not_allowed` (list, optional): A list of not allowed values for the column.
- `name` (str): A name for the validation, used in logging.

##### 3. statistical  
   Applies statistical outlier detection on a DataFrame column.

```python
@AlertManager.statistical(column='column_name', name='Validation Name', sensitivity='medium', data_type='continuous')
def your_function(df):
  # Your data processing logic
  return df
```

**Parameters**:
- `column` (str): The column in the DataFrame to be validated.
- `name` (str): A name for the validation, used in logging.
- `sensitivity` (str, default 'medium'): Adjusts the strictness of outlier detection. Options are 'sensitive', 'medium', 'insensitive'.
- `data_type` (str, optional): Specify 'continuous' or 'discrete'. If None, the type will be inferred.

##### 4. custom_check
   Applies custom validation logic on a DataFrame.

```python
@AlertManager.custom_check(custom_logic='column_name > value', name='Validation Name')
def your_function(df):
  # Your data processing logic
  return df
```

**Parameters**:
- `custom_logic` (str or callable): The custom logic for validation, can be a query string or a function.
- `name` (str): A name for the validation, used in logging.

### Examples for Each Decorator

Assuming you have the following sample DataFrame:

```python
import pandas as pd

data = {
'id': range(1, 11),
'age': [25, 38, 17, 120, 29, 41, -5, 30, 22, 300],
'status': ['active', 'inactive', 'active', 'pending', 'active', 'inactive', 'unknown', 'active', 'active', 'inactive'],
'salary': [50000, 60000, 55000, 70000, 65000, 52000, 48000, 1000000, 59000, 61000],
'gender_id': [1, 2, 1, 2, 1, 3, 1, 2, 2, 2]
}

df = pd.DataFrame(data)
```

#### Example 1: range_check

Validate that the `age` column values are between 0 and 120.

```python
@AlertManager.range_check(column='age', borders=[(0, 120)], name='Age Range Check')
def process_data(df):
  # Data processing logic
  return df

df = process_data(df)
```

Explanation: Any records where age is less than 0 or greater than 120 will be flagged and stored according to the AlertManager configuration.

#### Example 2: value_check

Ensure that `status` is either 'active' or 'inactive'.

```python
@AlertManager.value_check(column='status', allowed=['active', 'inactive'], name='Status Value Check')
def process_data(df):
  # Data processing logic
  return df

df = process_data(df)
```

Explanation: Records with a status of 'pending' or 'unknown' will be flagged.

#### Example 3: statistical

Detect outliers in the `salary` column, which is continuous data.

```python
@AlertManager.statistical(column='salary', name='Salary Outlier Check', sensitivity='medium', data_type='continuous')
def process_data(df):
  # Data processing logic
  return df

df = process_data(df)
```

Explanation: Uses the z-score method to detect outliers based on the sensitivity level.

For discrete data:

```python
@AlertManager.statistical(column='gender_id', name='Gender ID Outlier Check', sensitivity='medium', data_type='discrete')
def process_data(df):
  # Data processing logic
  return df

df = process_data(df)
```

Explanation: Identifies rarely occurring `gender_id` values as outliers using frequency-based detection.

#### Example 4: custom_check

Using a query string:

```python
@AlertManager.custom_check(custom_logic='age < 0 or age > 100', name='Custom Age Check')
def process_data(df):
  # Data processing logic
  return df

df = process_data(df)
```

Explanation: Flags records where age is less than 0 or greater than 100.

Using a callable function:

```python
def custom_logic(df):
    return df[(df['salary'] < 30000) | (df['salary'] > 200000)]

@AlertManager.custom_check(custom_logic=custom_logic, name='Custom Salary Check')
def process_data(df):
  # Data processing logic
  return df

df = process_data(df)
```

Explanation: Flags records where salary is less than 30,000 or greater than 200,000.

### 2. DatabaseValidator

#### Initialization

To use `DatabaseValidator`, import the class and initialize it with a database connection string:

```python
from AlertManager import DatabaseValidator  # Replace with the correct import path

# Database connection string
connection_string = 'sqlite:///my_database.db'  # Replace with your actual connection string

# Initialize the DatabaseValidator
alert_manager_db = DatabaseValidator(
connection_string=connection_string,
table_name='users',  # Replace with your actual table name
schema=None,  # Replace with your schema if necessary
store=True,
history=False,
united=True,
identifier='id',
path='./validation_logs',
file_type='csv'
)
```

**Parameters**:
- `connection_string` (str): The database connection string.
- `table_name` (str): The name of the database table to be validated.
- `schema` (str, optional): The schema of the table in the database.
- `store` (bool, default False): Whether to store validation results.
- `history` (bool, default False): Whether to store logs with historical data.
- `united` (bool, default True): Whether to store all validations in one file or separately.
- `identifier` (str, optional): Column name to identify rows.
- `path` (str, default './validation_logs'): Directory path where logs will be stored.
- `file_type` (str, default 'pkl'): The file format for storing validation results.

#### Decorators

##### 1. range_check

Validates that the values in a specified column fall within given ranges.

```python
@alert_manager_db.range_check(column='column_name', borders=[(lower_bound, upper_bound)], name='Validation Name')
  def your_function():
  # Your data processing logic
  pass
```

**Parameters**:
- `column` (str): The column in the table to be validated.
- `borders` (list of tuple): A list of tuples, each containing two numeric values representing the lower and upper bounds.
- `name` (str): A name for the validation, used in logging.

##### 2. value_check

Validates that the values in a specified column are either allowed or not allowed.

```python
@alert_manager_db.value_check(column='column_name', allowed=['value1', 'value2'], not_allowed=['value3'], name='Validation Name')
  def your_function():
  # Your data processing logic
  pass
```

**Parameters**:
- `column` (str): The column in the table to be validated.
- `allowed` (list, optional): A list of allowed values for the column.
- `not_allowed` (list, optional): A list of not allowed values for the column.
- `name` (str): A name for the validation, used in logging.

##### 3. statistical

Applies statistical outlier detection on a database table column.

```python
@alert_manager_db.statistical(column='column_name', name='Validation Name', sensitivity='medium', data_type='continuous')
def your_function():
  # Your data processing logic
  pass
```

**Parameters**:
- `column` (str): The column in the table to be validated.
- `name` (str): A name for the validation, used in logging.
- `sensitivity` (str, default 'medium'): Adjusts the strictness of outlier detection.
- `data_type` (str, optional): Specify 'continuous' or 'discrete'.

##### 4. custom_check

Applies custom validation logic on a database table.

```python
@alert_manager_db.custom_check(custom_logic='column_name > value', name='Validation Name')
def your_function():
  # Your data processing logic
  pass
```

**Parameters**:
- `custom_logic` (str or callable): The custom logic for validation.
- `name` (str): A name for the validation, used in logging.

### Examples for Each Decorator

Assuming you have a database table named `users` with columns similar to the sample DataFrame.

#### Example 1: range_check

Validate that the `age` column values are between 0 and 120.

```python
@alert_manager_db.range_check(column='age', borders=[(0, 120)], name='Age Range Check')
def update_database():
  # Database update logic
  pass

update_database()
```

Explanation: Any records where age is less than 0 or greater than 120 will be flagged.

#### Example 2: value_check

Ensure that `status` is either 'active' or 'inactive'.

```python
@alert_manager_db.value_check(column='status', allowed=['active', 'inactive'], name='Status Value Check')
def update_database():
  # Database update logic
  pass

update_database()
```

Explanation: Records with a status of 'pending' or 'unknown' will be flagged.

#### Example 3: statistical

Detect outliers in the `salary` column.

```python
@alert_manager_db.statistical(column='salary', name='Salary Outlier Check', sensitivity='medium', data_type='continuous')
def update_database():
  # Database update logic
  pass

update_database()
```

Explanation: Uses the z-score method to detect outliers based on the sensitivity level.

#### Example 4: custom_check

Using a query string:

```python
@alert_manager_db.custom_check(custom_logic='age < 0 or age > 100', name='Custom Age Check')
def update_database():
  # Database update logic
  pass

update_database()
```

Explanation: Flags records where age is less than 0 or greater than 100.

### Configuration Options

AlertManager allows you to customize how and where alerts are stored.

**Initialization Parameters**:
- `store` (bool): Enable or disable the storing of validation results.
- `history` (bool): Enable historical logging by creating subdirectories based on the date.
- `united` (bool): Store all validations in a single file (True) or separate files (False).
- `identifier` (str): Specify a column to identify rows (e.g., primary key).
- `path` (str): Directory path where logs will be stored.
- `file_type` (str): Format for storing validation results ('csv', 'xlsx', 'pkl', 'txt').

#### Example Initialization with Custom Configuration

**LocalValidator**

```python
AlertManager = LocalValidator(
store=True,
history=True,
united=False,
identifier='id',
path='./my_alert_logs',
file_type='csv'
)
```

**DatabaseValidator**

```python
alert_manager_db = DatabaseValidator(
connection_string=connection_string,
table_name='users',
store=True,
history=True,
united=False,
identifier='id',
path='./my_alert_logs',
file_type='csv'
)
```

### Best Practices and Detailed Explanations

#### Decorator Usage

- **Function Positioning**: Place the decorator directly above the function definition you wish to apply the validation to.
- **Multiple Decorators**: You can stack multiple decorators on a single function to apply multiple validations.

```python
@AlertManager.range_check(column='age', borders=[(0, 120)], name='Age Range Check')
@AlertManager.value_check(column='status', allowed=['active', 'inactive'], name='Status Value Check')
def process_data(df):
  # Data processing logic
  return df
```

- **Execution Order**: Decorators are applied from the bottom up. In the example above, `value_check` will execute before `range_check`.

#### Statistical Outlier Detection Sensitivity

**Sensitivity Levels**:
- `'sensitive'`: More strict, flags more data points as outliers.
- `'medium'`: Balanced approach.
- `'insensitive'`: Less strict, flags fewer data points.

**Data Type Specification**:
- Specify `data_type` as `'continuous'` or `'discrete'` to ensure the correct outlier detection method is applied.
- If `data_type` is None, AlertManager will attempt to infer the type based on the data.

#### Custom Validation Logic

- **Query Strings**: Use Pandas query syntax for straightforward conditions.
- **Callable Functions**: Define complex logic in a function that accepts a DataFrame and returns a DataFrame or Series of invalid rows.

### Alert Management

- **Identifier Usage**: Use the `identifier` parameter to store only essential information in your logs, making it easier to track and address issues.
- **Historical Logging**: Enable `history` to maintain logs over time, which can be useful for monitoring data quality trends.
- **Unified vs. Separate Logs**:
  - **Unified (`united=True`)**: All validation results are stored in a single file.
  - **Separate (`united=False`)**: Each validation result is stored in a separate file, named after the validation.

### Error Handling

- **Missing Columns**: If a specified column is not found in the DataFrame or database table, AlertManager will raise a `ValueError`.
- **Type Checking**: AlertManager performs type checking on parameters to help prevent misconfiguration.
- **Database Connections**: Ensure that your database connection string is correct and that the necessary database drivers are installed.

## Conclusion

AlertManager is a powerful tool for integrating data validation into your data processing workflows, whether you're working with local Pandas DataFrames or directly with database tables. By providing decorators for common validation tasks and flexible alert management options, it helps ensure data integrity and facilitates proactive handling of data anomalies.

By adopting AlertManager, you can:

- Reduce the risk of data errors propagating through your system.
- Maintain high data quality standards.
- Efficiently manage and track data validation alerts.
- Integrate validations seamlessly into existing codebases and database operations.

## Contribution and Support

Contributions to AlertManager are welcome. If you encounter any issues or have suggestions for improvements, please submit an issue or a pull request on the GitHub repository.

[AlertManager on GitHub](https://github.com/Qubdi/AlertManager)

## License

This project is licensed under the MIT License.
