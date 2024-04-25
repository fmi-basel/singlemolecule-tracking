import pandas as pd
import numpy as np

def load_trackmate_spots(path):
    """
    Loads trackmate spots and removes first three rows.
    """
    spots = pd.read_csv(path)
    spots = spots.drop(labels=[0,1,2], axis=0, inplace=False)
    spots = spots.reset_index(drop=True)
    
    return spots

def load_trackmate_tracks(path):
    """
    Loads trackmate tracks and removes first three rows.
    """
    tracks = pd.read_csv(path)
    tracks = tracks.drop(labels=[0,1,2], axis=0, inplace=False)
    tracks = tracks.reset_index(drop=True)
    
    return tracks

def load_meanint_ROIs(path):
    """
    Loads mean intensities of ROIs, calculated with Fiji.
    """
    intensities = pd.read_csv(path)
    
    return intensities

def remove_shorttracks_3(df):
    """
    Removes tracks from track file that are <= 3 in length.
    """
    df["NUMBER_SPOTS"] = pd.to_numeric(df["NUMBER_SPOTS"])
    df['NUMBER_SPOTS'] = df['NUMBER_SPOTS'].astype(int)
    df = df[df["NUMBER_SPOTS"] > 3].reset_index(drop=True)
    
    return df

def remove_shorttracks_spotsfile(df, track_id_object):
    """
    Removes spots from spots file by trackID object, i.e., spots from tracks <=3 in length.
    """
    df = df.loc[df["TRACK_ID"].isin(track_id_object)]
    
    return df

def split_table_by_track(df):
    """
    Splits each spots file into seperate dfs by TRACK_ID, so that spots can be sorted and filtered by frame' 
    """
    df = df.groupby("TRACK_ID", sort = False, as_index = False)
    
    return df

def split_table_by_ROI_and_track(df):
    """
    Splits each spots file into seperate dfs by ROI_ID and TRACK_ID, so that spots can be sorted and filtered by frame' 
    """
    df = df.groupby(["ROI_ID","TRACK_ID"], sort = False, as_index = False)
    
    return df

def first_10_frames(df):
    """
    Sorts the split dfs by FRAME and extracts the first 10.
    """
    df['FRAME'] = df['FRAME'].astype(int) # Is probably necessary to have proper ordering of tracks by frame
    df = df.sort_values(by="FRAME").iloc[0:10]
    
    return df

def first_5_frames(df):
    """
    Sorts the split dfs by FRAME and extracts the first 5.
    """
    df['FRAME'] = df['FRAME'].astype(int) # Is probably necessary to have proper ordering of tracks by frame
    df = df.sort_values(by="FRAME").iloc[0:5]
    
    return df

def meanint_tracks_ch2(df):
    """
    Extracts columns "TRACK_ID" and "MEAN_INTENSITY_CH2" and calculates the mean of "MEAN_INTENSITY_CH2":
    
    .astypefloat converts values of 'MEAN_INTENSITY_CH2' to type 'float', so that 'groupby' operation in next line can be   perfomed
    .iloc selects the columns TRACK_ID and MEAN_INTENSITY_CH2; the ':' in the square brackets signifies that the rows are left   untouched
    .mean calculates mean intensities based on .groupby 'TRACK_ID'
    .round rounds the values to 2 decimals after calculating the mean
    
    """
    df['MEAN_INTENSITY_CH2'] = df['MEAN_INTENSITY_CH2'].astype(float)
    df = df.iloc[:, np.r_[2,21]].groupby("TRACK_ID", sort = False, as_index = False).mean().round(2)
    
    return df

def meanint_tracks_per_ROI_ch2(df):
    """
    Extracts columns "ROI_ID", "TRACK_ID" and "MEAN_INTENSITY_CH2" and calculates the mean of "MEAN_INTENSITY_CH2":
    
    .astypefloat converts values of 'MEAN_INTENSITY_CH2' to type 'float', so that 'groupby' operation in next line can be   perfomed
    .iloc selects the columns TRACK_ID and MEAN_INTENSITY_CH2; the ':' in the square brackets signifies that the rows are left   untouched
    .mean calculates mean intensities based on .groupby 'TRACK_ID'
    .round rounds the values to 2 decimals after calculating the mean
    
    """
    df['MEAN_INTENSITY_CH2'] = df['MEAN_INTENSITY_CH2'].astype(float)
    df = df.iloc[:, np.r_[0,3,22]].groupby(["ROI_ID","TRACK_ID"], sort = False, as_index = False).mean().round(2)
    
    return df

def meanint_tracks_ch1(df):
    """
    Extracts columns "TRACK_ID" and "MEAN_INTENSITY_CH1" and calculates the mean of "MEAN_INTENSITY_CH1":
    
    .astypefloat converts values of 'MEAN_INTENSITY_CH1' to type 'float', so that 'groupby' operation in next line can be   perfomed
    .iloc selects the columns TRACK_ID and MEAN_INTENSITY_CH1; the ':' in the square brackets signifies that the rows are left   untouched
    .mean calculates mean intensities based on .groupby 'TRACK_ID'
    .round rounds the values to 2 decimals after calculating the mean
    
    """
    df['MEAN_INTENSITY_CH1'] = df['MEAN_INTENSITY_CH1'].astype(float)
    df = df.iloc[:, np.r_[2,15]].groupby("TRACK_ID", sort = False, as_index = False).mean().round(2)
    
    return df
    
    