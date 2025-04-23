import json
import numpy as np
from datasets import Dataset, Image
import sys
import random
import shutil
import os

def prepare_dataset_dict(json_file, images_dir):
  ds_dict_train = {
    "image": [],
    "ground_truth": []
  }

  ds_dict_val = {
    "image": [],
    "ground_truth": []
  }

  random.shuffle(json_file)

  middle_point = len(json_file) * 0.8
  
  for i, single_json in enumerate(json_file):
    for aug in single_json["aug"]:

      if i < middle_point:
        image_name = aug + "_" + single_json['image_code']
        ds_dict_train["image"].append(f"{images_dir}/{image_name}")

        json_str = str(single_json).replace('\'', '\"')
        ds_dict_train["ground_truth"].append(json_str)
      else:
        image_name = aug + "_" + single_json['image_code']
        ds_dict_val["image"].append(f"{images_dir}/{image_name}")

        json_str = str(single_json).replace('\'', '\"')
        ds_dict_val["ground_truth"].append(json_str)

  return ds_dict_train, ds_dict_val


def to_rgb(elem):
  elem['image'] = elem['image'].convert("RGB")
  return elem


def create_dataset(json_file_path, images_dir, dataset_name):
  
  file = open(json_file_path, encoding='utf8')  

  json_file = json.load(file)
  out_dict_train, out_dict_val = prepare_dataset_dict(json_file, images_dir)

  # Save train dataset
  train_dataset = Dataset.from_dict(out_dict_train).cast_column("image", Image())
  train_dataset.save_to_disk(f'datasets/{dataset_name}_train')

  # Save validation dataset
  validation_dataset = Dataset.from_dict(out_dict_val).cast_column("image", Image())
  validation_dataset.save_to_disk(f'datasets/{dataset_name}_validation')

  print(f"Train dataset saved to datasets/{dataset_name}_train")
  print(f"Validation dataset saved to datasets/{dataset_name}_validation")

def remove_dataset(dataset_name):
  """Remove train and validation datasets from disk."""
  train_dataset_path = f'datasets/{dataset_name}_train'
  validation_dataset_path = f'datasets/{dataset_name}_validation'

  # Remove train dataset directory if it exists
  if os.path.exists(train_dataset_path):
      shutil.rmtree(train_dataset_path)
      print(f"Removed train dataset at {train_dataset_path}")
  else:
      print(f"Train dataset at {train_dataset_path} does not exist.")

  # Remove validation dataset directory if it exists
  if os.path.exists(validation_dataset_path):
      shutil.rmtree(validation_dataset_path)
      print(f"Removed validation dataset at {validation_dataset_path}")
  else:
      print(f"Validation dataset at {validation_dataset_path} does not exist.")