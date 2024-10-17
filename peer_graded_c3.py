import os  # For file and directory operations
import pandas as pd  # For handling CSV data
import numpy as np  # For numerical operations like filtering signals
from PIL import Image as Img  # For image processing

# Define input and output directories
input_directory = "path/to/data"
output_directory = "path/to/output"

def getting_grey_scale_image(img_path):
    """
    Converts a given image to grayscale.
    
    Args:
        img_path (str): Path to the input image.
    
    Returns:
        graysc_img (PIL.Image): Grayscale version of the input image.
    """
    print(f"Converting {img_path} to grayscale...")
    img_orig = Img.open(img_path)  # Open the image
    graysc_img = img_orig.convert("L")  # Convert to grayscale
    return graysc_img

def apply_filter(signal, window_size):
    """
    Applies a moving average filter to the signal data.
    
    Args:
        signal (array-like): Input signal to be filtered.
        window_size (int): Size of the moving window.
    
    Returns:
        filtered_signal (ndarray): Filtered signal.
    """
    print(f"Applying filter with window size {window_size}...")
    # Use numpy's convolution function to apply the moving average filter
    filtered_signal = np.convolve(signal, np.ones(window_size) / window_size, mode="same")
    return filtered_signal

def getting_signal_data(signal_path, window_size):
    """
    Reads signal data from a CSV file and applies filtering.
    
    Args:
        signal_path (str): Path to the signal data file.
        window_size (int): Size of the filter window.
    
    Returns:
        signal_data (DataFrame): Original signal data.
        filtered_signal (ndarray): Filtered signal data.
    """
    print(f"Reading signal data from {signal_path}...")
    signal_data = pd.read_csv(signal_path)  # Read the CSV file
    filtered_signal = apply_filter(signal_data["signal"].values, window_size)  # Apply filter
    return signal_data, filtered_signal

def processing_image(img_path):
    """
    Processes an image by converting it to grayscale and saving it.
    
    Args:
        img_path (str): Path to the input image.
    """
    graysc_img = getting_grey_scale_image(img_path)  # Convert to grayscale
    output_path = os.path.join(output_directory, os.path.basename(img_path))  # Define output path
    print(f"Saving grayscale image to {output_path}...")
    graysc_img.save(output_path)  # Save the processed image

def processing_signal(signal_path):
    """
    Processes signal data by applying a filter and saving the result.
    
    Args:
        signal_path (str): Path to the signal data file.
    """
    window_size = 5  # Set window size for filtering
    signal_data, filtered_signal = getting_signal_data(signal_path, window_size)  # Get filtered data
    signal_data["filtered_signal"] = filtered_signal  # Add filtered signal to the DataFrame
    output_path = os.path.join(output_directory, os.path.basename(signal_path))  # Define output path
    print(f"Saving processed signal data to {output_path}...")
    signal_data.to_csv(output_path, index=False)  # Save the data as CSV

def main():
    """
    Main function to create output directory, process images, and process signals.
    """
    exist = True  # Allow existing directory without raising an error
    os.makedirs(output_directory, exist_ok=exist)  # Create output directory if not exists
    print(f"Output directory set to: {output_directory}")

    # Process image files
    image_files = [
        os.path.join(input_directory, f) 
        for f in os.listdir(input_directory) 
        if f.endswith((".jpg", ".png"))
    ]
    print(f"Found {len(image_files)} image(s) to process.")

    for image_file in image_files:
        processing_image(image_file)  # Process each image

    # Process signal files
    signal_files = [
        os.path.join(input_directory, f) 
        for f in os.listdir(input_directory) 
        if f.endswith(".csv")
    ]
    print(f"Found {len(signal_files)} signal file(s) to process.")

    for signal_file in signal_files:
        processing_signal(signal_file)  # Process each signal file

# Run the script only if executed directly
if __name__ == "__main__":
    main()
