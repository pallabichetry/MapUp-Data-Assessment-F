import pandas as pd
import numpy as np


def generate_car_matrix(df)->pd.DataFrame:
    """
    Creates a DataFrame  for id combinations.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Matrix generated with 'car' values, 
                          where 'id_1' and 'id_2' are used as indices and columns respectively.
    """
    # Write your logic here
    df = pd.pivot_table(df, columns=['id_2'], index=["id_1"],values = ["car"], fill_value=0)
    return df


def get_type_count(df : pd.DataFrame)->dict:
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    # Write your logic here
    df["car_type"] = np.where(df["car"] <=15,"low",
                     np.where(df["car"].between(15,25, inclusive=False),"medium",
                     np.where(df["car"] > 25 ,"high", "NA")))
    
    output = df.groupby("car_type", sort=True)['car_type'].count().to_dict()
    
    return output


def get_bus_indexes(df)->list:
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
    # Write your logic here
    df = df[df["bus"]>2*df["bus"].mean()]
    return sorted(list(df.index))


def filter_routes(df)->list:
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    # Write your logic here
    df = df[["route","truck"]].groupby(by="route").mean()
    df = df[df["truck"]>7]
    

    return sorted(list(df.index))


def multiply_matrix(matrix)->pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    # Write your logic here
    matrix = matrix.applymap( lambda x : round(x*0.75,1) if x > 20 else round(x*1.25,1) )
    return matrix


def time_check(df)->pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """
    # Write your logic here
    
    df['startTimestamp'] = pd.to_datetime("2023-01-01" + ' '+ df['startDay'] + ' ' + df['startTime'] , format='%Y-%m-%W %A %H:%M:%S')
    df['endTimestamp'] = pd.to_datetime("2023-01-01" + ' '+ df['endDay'] + ' ' + df['endTime'] , format='%Y-%m-%W %A %H:%M:%S')

    df = df[["id","id_2","startTimestamp","endTimestamp"]].groupby(by=["id","id_2"]).agg( {
        'startTimestamp' : 'min',
        'endTimestamp' : 'max'    }
    )

    df["diffInDays"] = df["endTimestamp"] - df['startTimestamp']
    result_series = df["diffInDays"] == "6 days 23:59:59"
    return result_series


data = pd.read_csv(filepath_or_buffer="datasets\dataset-1.csv",delimiter=",")

data_2 = pd.read_csv(filepath_or_buffer="datasets\dataset-2.csv",delimiter=",")

#a = get_bus_indexes(data)

#type_count = get_type_count(data)

#print(data.head(100))
# matrix_data = generate_car_matrix(data)
# print(matrix_data)
# result = multiply_matrix(matrix_data)

#print(result)
a = time_check(data_2)
