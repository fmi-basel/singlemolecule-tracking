import pandas as pd

def load_trackmate_spots(path):
    """
    Load trackmate spots and remove first three rows.
    """
    spots = pd.read_csv(path)
    spots = spots.drop(labels=[0,1,2], axis=0, inplace=False)
    spots = spots.reset_index(drop=True)
    
    return spots    