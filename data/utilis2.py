# File containing functions for internshiptask
import pandas as pd
from datetime import timedelta

# Function to substract years from date
def subtract_years(dt, years):
    try:
        return dt - timedelta(days=365*years)
    except:
        return dt 

#  Function to replace NaN values with a hyphen in the 'Heart_rhythm' column.
def replace_nan_with_hyphen(value):
    if pd.isna(value):  # Checking if the value is NaN
        return '-'
    else:
        return value
    
# Function to clean the data
def clean_data(df):
    # Drop the null values in hearthrate column
    df.dropna(subset=["heartrate"], inplace=True)
    # Drop the duplicates
    df.drop_duplicates(inplace=True)
    # Drop the column that is not needed
    df.drop('Unnamed: 0', axis=1, inplace=True)
    # Rename columns 
    df.rename(columns={
        'subject_id': 'Patient_ID',
        'stay_id': 'Stay_ID',
        'charttime': 'Examination_time',
        'heartrate': 'Heart_rate',
        'rhythm': 'Heart_rhythm'}, inplace=True)
    # Convert Examination_time column to datetime
    df['Examination_time'] = pd.to_datetime(df['Examination_time'])
    # Subtract 178 years from the Examination_time
    df['Examination_time'] = df['Examination_time'].apply(lambda x: subtract_years(x, 178))
    # Replace specific string values with more descriptive terms
    df['Heart_rhythm'] = df['Heart_rhythm'].replace({'afib': 'Atrial Fibrillation', 'sr': 'Sinus Rhythm'})
    # Apply replace_nan_with_hyphen function to the 'Heart_rhythm' column to deal with NaN values
    df['Heart_rhythm'] = df['Heart_rhythm'].apply(replace_nan_with_hyphen)

    return df

# Function that calculates and prints minimum and maximum value from "Examination_time" column, also counts and prints unique patinets ID from "Patinent_ID" and unique "Stay_ID" 
def dataset_basic_info(df):
    # Extract the minimum and maximum examination times
    min_value = df['Examination_time'].min()
    max_value = df['Examination_time'].max()
    print(f"First record in our dataset is from: {min_value}")
    print(f"Last record in our dataset is from: {max_value}")
    
    # Calcule unique Patient_ID and Stay_ID counts
    unique_patient_ids = len(df['Patient_ID'].unique())
    unique_stay_ids = len(df['Stay_ID'].unique())
    
    # Print the results
    print(f"The number of unique patients: {unique_patient_ids}")
    print(f"The number of unique examinations: {unique_stay_ids}")

# Function that caclulates average, min and max stastistics 
def calculate_stay_statistics(df):
    patient_stay_counts = df.groupby('Patient_ID')['Stay_ID'].nunique()
    average_value = round(patient_stay_counts.mean(), 1)
    min_value = patient_stay_counts.min()
    max_value = patient_stay_counts.max()
    statistics_df = pd.DataFrame({
        'Statistic': ['Minimum', 'Average', 'Maximum'],
        'Number of Stays': [min_value, average_value, max_value]
    })
    
    # Print it
    print(statistics_df.to_string(index=False))
    
   # Function to count occurencies of 0 time examination
def count_min_time_difference_occurrences(df):
    # Making sure examintaion_time in in data format
    df['Examination_time'] = pd.to_datetime(df['Examination_time'])
    # Filter back df for groups 
    df_filtered = df[df.groupby('Stay_ID')['Examination_time'].transform('count') > 0]
    # Calculate min and max examination times for each Stay_ID
    min_max_times = df_filtered.groupby('Stay_ID')['Examination_time'].agg(['min', 'max'])
    # Calculate the time difference in hours
    min_max_times['Time_Diff_Hours'] = (min_max_times['max'] - min_max_times['min']).dt.total_seconds() / 3600
    # Find the minimum time difference and count occurrences
    min_time_diff_hours = min_max_times['Time_Diff_Hours'].min()
    count_min_time_diff = (min_max_times['Time_Diff_Hours'] == min_time_diff_hours).sum()

    print("Count of only one examination time records per stay id in our data base is", (count_min_time_diff))

 
 # Function that calculates heart_rate_min, heart_rate_max and heart_rate_average and converts them into small dataframe and returns them
def calculate_heart_rate_statistics(df):
    heart_rate_min = round(df['Heart_rate'].min(), 1)
    heart_rate_max = round(df['Heart_rate'].max(), 1)
    heart_rate_average = round(df['Heart_rate'].mean(), 1)
    
    heart_rate_statistics = pd.DataFrame({
        'Heart Rate': [heart_rate_min, heart_rate_max, heart_rate_average]
    }, index=['Minimum', 'Maximum', 'Average'])

    return(heart_rate_statistics)

# Functiont for calculating heart rate summary using the .describe function
def calculate_heart_rate_summary(df, decimal_places=1):
    heart_rate_summary = df['Heart_rate'].describe()
    heart_rate_summary_rounded = heart_rate_summary.round(decimal_places)
    heart_rate_summary_table = pd.DataFrame(heart_rate_summary_rounded)
    heart_rate_summary_table = pd.DataFrame(heart_rate_summary_rounded).rename(columns={'Heart_rate': 'Heart Rate'})
    
    return(heart_rate_summary_table)
    
  # Function that calculates % of the hearth rate anomalies
def calculate_percentage_anomalies(num_anomalies, total_measurements):
    percentage_anomalies = (num_anomalies / total_measurements) * 100
    formatted_percentage = "{:.2f}%".format(round(percentage_anomalies, 2))
    print("Anomalies make up", (formatted_percentage), "of the hearth rate results.")