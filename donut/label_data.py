from transformers import VisionEncoderDecoderModel, DonutProcessor
from pathlib import Path
import json
from PIL import Image
import os
import torch

def label_my_data(result_path, unlabeled_images_dir, input_size):
    """
    Use the saved Donut model to label unlabeled images and create a JSON file.

    Args:
        result_path (str): Path to the directory where the trained model is saved.
        unlabeled_images_dir (str): Directory containing unlabeled images.
        input_size (list): Input size for the model [width, height].
    """
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    # Load the trained model and processor
    model = VisionEncoderDecoderModel.from_pretrained(result_path)
    processor = DonutProcessor.from_pretrained(result_path)
    
    model.to(device)

    # Ensure the processor's image size matches the input size
    processor.image_processor.size = input_size[::-1]
    processor.image_processor.do_align_long_axis = False

    labeled_data = []
    
    decoder_input_ids = torch.full(
        (1, 1), model.config.decoder_start_token_id, device=device
    )

    # Iterate over all images in the unlabeled images directory
    for image_file in os.listdir(unlabeled_images_dir):
        image_path = os.path.join(unlabeled_images_dir, image_file)

        # Skip non-image files
        if not image_file.lower().endswith(('.png', '.jpg', '.jpeg')):
            continue

        # Open and preprocess the image
        image = Image.open(image_path).convert("RGB")
        pixel_values = processor(image, return_tensors="pt").pixel_values
        
        pixel_values = pixel_values.to(device)

        # Generate predictions
        outputs = model.generate(
            pixel_values,
            decoder_input_ids=decoder_input_ids,
            max_length=256,
            pad_token_id=processor.tokenizer.pad_token_id,
            eos_token_id=processor.tokenizer.eos_token_id,
            use_cache=True,
            num_beams=1,
        )
        predicted_text = processor.batch_decode(outputs, skip_special_tokens=True)[0]

        # Create a labeled entry
        labeled_data.append({
            "image": image_file,
            "predicted_text": predicted_text
        })

    return labeled_data