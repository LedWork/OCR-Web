import yaml
from augment_data.augment import DataAugmentation
from augment_data.change_color_aug import ChangeColorDataAugmentation
from augment_data.decolorized_aug import DecolorizedDataAugmentation
from augment_data.edge_enhanced_aug import EdgeEnhancedDataAugmentation
from augment_data.rotate_aug import RotateDataAugmentation
from augment_data.salient_edge_map_aug import SalientEdgeMapDataAugmentation
import shutil
from train import train
from dataset_create import create_dataset, remove_dataset
import json
import os
from label_data import label_my_data

def merge_json_files(file1, file2, output_file):
    """Merge two JSON files and save the result to the output file."""
    with open(file1, 'r', encoding='utf-8') as f1, open(file2, 'r', encoding='utf-8') as f2:
        data1 = json.load(f1)
        data2 = json.load(f2)
    
    # Assuming both files contain lists of objects
    merged_data = data1 + data2
    
    with open(output_file, 'w', encoding='utf-8') as out:
        json.dump(merged_data, out, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    
    # Load the configuration file
    with open('conf/config.yaml', 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file)
    
    shutil.copy(config["labels_in"], config["labels_out"])
    
    # augment data with json path parameter
    augmentation_classes = [
        DataAugmentation,
        ChangeColorDataAugmentation,
        DecolorizedDataAugmentation,
        EdgeEnhancedDataAugmentation,
        RotateDataAugmentation,
        SalientEdgeMapDataAugmentation
    ]
    
    labels_temp_path = config["labels_out"]
    
    for index_of_circle in range(config["num_of_cicles"]):

        # Augment the data
        for AugClass in augmentation_classes:
            augmenter = AugClass(labels_temp_path)
            augmenter.augment()
            
        if index_of_circle != 0:
            merge_json_files(labels_temp_path, config["labels_out"], config["labels_out"])
            os.remove(labels_temp_path)
            remove_dataset("my_dataset")
        
        # Create dataset
        create_dataset(
            json_file_path=config["labels_out"],
            images_dir="images/aug",
            dataset_name="my_dataset"
        )
        
        # Set configuration for training
        config = {
            "max_epochs": 30,
            "lr": 1e-5,
            "batch_size": 2,
            "max_length": 256,
            "pretrained_model_name_or_path": "naver-clova-ix/donut-base-finetuned-cord-v2",
            "result_path": config["result_path"],
            "dataset_name_or_path": "dataset",
            "input_size": config["input_size"],
            "early_stopping_patience": 5
        }

        # Train the model
        train(config)
        
        # TODO: task I: put images in images/unlabeled
        
        # Labeling new data
        labeled_data = label_my_data(
            result_path=config["result_path"],
            unlabeled_images_dir="images/unlabeled", #TODO set task I
            input_size=config["input_size"]
        )
        
        # TODO: task II: change labeled_data to our json format, example: 
        # OCR-Web/donut/labels/readme.md
        
        # TODO: task III: with requests create HTTP to send images and labels to our web
        # OCR-Web/backend/flask-app/app/app/retraining/views.py
        # then we need to wait for labeling data. can be created mock for testing
        # and request GET for our new data
        
        # TODO: task IV: before saving our new json in labels_temp, we need to check if data is not in
        # labels_out. After that we can create labels_temp
        
        labels_temp_path = config["labels_temp"]
        
        
        

    