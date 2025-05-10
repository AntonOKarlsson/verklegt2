import os
from django.conf import settings
from django.core.files import File
from properties.models import Property
from property_images.models import PropertyImage

base_dir = os.path.join(settings.MEDIA_ROOT, 'property_images')  # ← your existing subfolders

for folder_name in os.listdir(base_dir):
    folder_path = os.path.join(base_dir, folder_name)

    if not os.path.isdir(folder_path):
        continue

    try:
        property_id = int(folder_name)
        prop = Property.objects.get(id=property_id)
    except (ValueError, Property.DoesNotExist):
        print(f"Skipping folder: {folder_name}")
        continue

    print(f"Linking images for Property ID {property_id}")

    for filename in os.listdir(folder_path):
        if not filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
            continue

        image_path = os.path.join(folder_path, filename)

        with open(image_path, 'rb') as img_file:
            image_file = File(img_file, name=filename)

            is_thumbnail = filename.split('.')[0] == str(property_id)

            PropertyImage.objects.create(
                property=prop,
                image=image_file,  # this will be saved into media/property_photos/
                is_thumbnail=is_thumbnail
            )
