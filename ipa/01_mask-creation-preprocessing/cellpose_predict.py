import os
import glob
import yaml
import numpy as np
from pathlib import Path
from cellpose import models
import tifffile
import logging
from tqdm import tqdm

def setup_directories(output_path):
    """Create output directory if it doesn't exist."""
    if not os.path.exists(output_path):
        os.makedirs(output_path)
        print(f"Created output directory: {output_path}")

def load_config(config_path):
    """Load configuration from YAML file."""
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    print(f"Loaded configuration from {config_path}")
    return config

def run_cellpose(image_path, output_path, model_path, n_iter=4, cellprob_threshold=0.0, flow_threshold=0.4):
    """Run cellpose on a single image and save the output mask."""
    try:
        # Load the image
        img = tifffile.imread(image_path)
        
        # Load the model
        model = models.CellposeModel(pretrained_model=model_path, gpu=False)
        
        # Run the model
        masks, _, _ = model.eval(
            img, 
            diameter=213,
            channels=[0, 0],
            flow_threshold=flow_threshold,
            cellprob_threshold=cellprob_threshold,
            niter=n_iter
        )
        
        # Save the mask
        tifffile.imwrite(output_path.replace('.tif','_whole_cell_mask.tif'), masks.astype(np.uint16))
        print(f"Saved mask to {output_path}")
        return True
    except Exception as e:
        print(f"Error processing {image_path}: {str(e)}")
        return False

def process_treatment_folder(treatment_folder, config):
    """Process all images in a treatment folder."""
    print(f"Processing treatment folder: {treatment_folder}")
    
    halo_dir = os.path.join(treatment_folder, "Max_projections_separate", "Halo")
    
    if not os.path.exists(halo_dir):
        print(f"Halo directory not found in {treatment_folder}")
        return
    
    whole_cell_dir = os.path.join(treatment_folder, "ROIs", "Whole_cell")
    
    setup_directories(whole_cell_dir)
    
    image_files = glob.glob(os.path.join(halo_dir, "*.tif")) + glob.glob(os.path.join(halo_dir, "*.tiff"))
    
    if not image_files:
        print(f"No image files found in {halo_dir}")
        return
    
    successful = 0
    for image_file in tqdm(image_files, desc=f"Processing {os.path.basename(treatment_folder)}"):
        image_name = os.path.basename(image_file)
        
        # Output paths
        whole_cell_output = os.path.join(whole_cell_dir, image_name)
        
        # Run whole cell segmentation
        whole_cell_success = run_cellpose(
            image_file, 
            whole_cell_output, 
            config['whole_cell_model'],
            config['n_iter'],
            config['cellprob_threshold'],
            config['flow_threshold']
        )
                
        if whole_cell_success:
            successful += 1
    
    print(f"Successfully processed {successful}/{len(image_files)} images in {treatment_folder}")

def main():
    config = load_config('cellpose_config.yaml')
    
    input_path = config['input_path']
    
    if not os.path.exists(input_path):
        print(f"Input path {input_path} not found.")
        return
    
    if os.path.basename(input_path).startswith('D'):
        treatment_folders = [f for f in glob.glob(os.path.join(input_path, "*")) if os.path.isdir(f)]
    else:
        # If input is a specific treatment folder
        treatment_folders = [input_path]
    
    print(f"Found {len(treatment_folders)} treatment folders to process")
    
    # Process each treatment folder
    for treatment_folder in treatment_folders:
        process_treatment_folder(treatment_folder, config)
    
    print("Processing completed.")

if __name__ == "__main__":
    main()