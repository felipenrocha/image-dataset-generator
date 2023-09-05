

# module to generate the dataset folder based on the bing results


# folder structure:
# countries_dataset
#   seg_pred
#   seg_train
#       aland
#       albania
#       ...
#   seg_test
#       aland
#       albania
#       ...


import os
import csv
import shutil
from dotenv.main import load_dotenv

load_dotenv()

MODEL_NAME = os.environ['MODEL_NAME']


def main():
    dataset_folders = ['../../dataset_bing/', '../../dataset_flickr']
    output_folder = '../../' + MODEL_NAME + '/'

    # create dataset folder

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # # Iterate through each folder and split it to generate the new dataset
    for dataset_folder in dataset_folders:
        class_index = 0
        for folder in os.listdir(dataset_folder):
            class_path = os.path.join(dataset_folder, folder)
            folder_len = len(os.listdir(class_path))
            # separate data (75% for training, 20% for testing 5% for predictions)

            # training split files
            start_index = 0
            end_index = int(folder_len * 0.75)
            dst_folder = output_folder + '/seg_train/' + str(class_index)
            copy_file_range(class_path, dst_folder, start_index, end_index)

            # test split files
            start_index = end_index + 1
            end_index = int(folder_len * 0.95)
            dst_folder = output_folder + '/seg_test/' + str(class_index)
            copy_file_range(class_path, dst_folder, start_index, end_index)

            # pred split files
            start_index = end_index + 1
            end_index = folder_len
            dst_folder = output_folder + '/seg_pred'
            copy_file_range(class_path, dst_folder, start_index, end_index)

            class_index += 1


def copy_file_range(source_folder, destination_folder, start_index, end_index):
    # Create the destination folder if it doesn't exist
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # List all files in the source folder
    files = os.listdir(source_folder)

    # Sort the files to ensure consistent order
    files.sort()
    current_index = 0
    # Iterate over the files within the specified range and copy them
    for filename in files[start_index:end_index]:
        source_path = os.path.join(source_folder, filename)
        destination_path = os.path.join(destination_folder, filename)
        shutil.copy2(source_path, destination_path)
        print(
            f"Copying {filename} to {destination_folder}, Current index: {current_index}")
        current_index = current_index + 1


if __name__ == "__main__":
    main()
