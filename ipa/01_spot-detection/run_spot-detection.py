from tifffile import imread

def main(file):
    image = imread(file)
    
    # TODO: Add functionality from spot_detection.ipynb



if __name__ == "__main__":
    main(
        file = '/tungstenfs/scratch/gchao/bamfaile/Analysis/TUBB2B-KI/Batch20230223/D21/Denoised/100tp_561-100-50ms-1000g_4_conf561_merged.tif'
    )