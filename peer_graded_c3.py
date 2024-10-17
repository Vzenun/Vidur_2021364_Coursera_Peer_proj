import os
import pandas as pd
import numpy as np
from PIL import Image as Img

input_directory = "path/to/data"
output_directory = "path/to/output"

def getting_grey_scale_image(img_path):
    img_orig = Img.open(img_path)
    graysc_img = img_orig.convert("L")
    return graysc_img

def apply_filter(signal, window_size):
    filtered_signal = np.convolve(signal, np.ones(window_size) / window_size, mode="same")
    return filtered_signal

def getting_signal_data(signal_path, window_size):
    signal_data = pd.read_csv(signal_path)
    filtered_signal = apply_filter(signal_data["signal"].values,window_size)
    return signal_data,filtered_signal

def processing_image(img_path):
    graysc_img=getting_grey_scale_image(img_path)
    output_path = os.path.join(output_directory, os.path.basename(img_path))
    graysc_img.save(output_path)

def processing_signal(signal_path):
    window_size=5
    signal_data,filtered_signal = getting_signal_data(signal_path,window_size)
    signal_data["filtered_signal"] = filtered_signal
    output_path = os.path.join(output_directory, os.path.basename(signal_path))
    signal_data.to_csv(output_path, index=False)

def main():
    exist=True
    os.makedirs(output_directory, exist_ok=exist)

    image_files = []
    for f in os.listdir(input_directory):
        if f.endswith((".jpg", ".png")):
            image_files.append(os.path.join(input_directory, f))

    for image_file in image_files:
        processing_image(image_file)

    signal_files = []
    for f in os.listdir(input_directory):
        if f.endswith(".csv"):
            signal_files.append(os.path.join(input_directory, f))

    for signal_file in signal_files:
        processing_signal(signal_file)

if __name__ == "__main__":
    main()