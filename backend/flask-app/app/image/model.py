import base64
from app.core.db import get_db

def load_image_to_db(file, image_code):
    db = get_db()
    collection = db['images']

    try:
        file_content = file.read()
        photo_data = base64.b64encode(file_content).decode('utf-8')

        existing_image = list(collection.find({"_id": image_code}))

        if existing_image:
            collection.update_one({"_id": image_code}, {"$set": {"photo": photo_data}})
            return {"message": "Photo successfully updated"}, 200
        else:
            collection.insert_one({"_id": image_code, "photo": photo_data})
            return {"message": "Photo successfully uploaded and linked to the card"}, 200
    except Exception as e:
        print(f"An error occurred: {e}")
        return {"error": f"An error occurred: {str(e)}"}, 500

def get_image(image_code):
    db = get_db()
    collection = db['images']

    image_data = list(collection.find({"_id": image_code}))
    return image_data