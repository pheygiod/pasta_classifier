import hashlib
from pathlib import Path
from PIL import Image
import shutil
import os

# Cleaning the images 
def clean_images(main_dir, min_img_size):
    num_of_images = 0
    num_of_deleted_images = 0
    
    for child_dir in main_dir.iterdir():
        if (child_dir / '.ipynb_checkpoints').is_dir():
            shutil.rmtree(child_dir / '.ipynb_checkpoints')
        for file_path in child_dir.iterdir():
            try:
                im = Image.open(file_path)

                if im.size[0] > min_img_size and im.size[1] > min_img_size:
                    num_of_images += 1
                else: 
                    os.remove(file_path)
                    num_of_deleted_images += 1
            except:
                os.remove(file_path)
                num_of_deleted_images += 1 
                
                
    return {
        "files_remaning": num_of_images,
        "files_deleted": num_of_deleted_images,
    }


def remove_duplicates(main_dir):
    hash_dict = {}
    for child_dir in main_dir.iterdir():
        if (child_dir / '.ipynb_checkpoints').is_dir():
            shutil.rmtree(child_dir / '.ipynb_checkpoints')
        for file_path in child_dir.iterdir():
            hashstr = hashlib.sha1(open(str(file_path), "rb").read()).hexdigest()
            if hashstr not in hash_dict:
                hash_dict[hashstr] = [str(file_path)]
            else:
                hash_dict[hashstr].append(str(file_path))

    deleted_files = 0 
    for hashstr in hash_dict:
        if len(hash_dict[hashstr]) > 1:
            deleted_files += len(hash_dict[hashstr]) - 1
            
            for file_to_delete in hash_dict[hashstr][1:]:
                os.remove(file_to_delete)

    files_remaining = len(hash_dict)
    return {
        "files_remaning": files_remaining,
        "files_deleted": deleted_files,
    }

    

# Resizing the images 
def resize_image(img, resize_size):
    width, height = img.size
    ratio = min(width, height) / resize_size
    resize_img = img.resize((int(width / ratio), int(height / ratio)))
    return resize_img


# Cropping the images 
def cropping_image(img, cropped_size):
    
    width, height = img.size
    
    # Setting the points for cropped images 
    x_crop = (width - cropped_size) / 2
    left = x_crop
    right = width - x_crop

    y_crop = (height - cropped_size) / 2
    lower = y_crop
    upper = height - y_crop
    
    cropping_tuple = (left, lower, right, upper)
    cropped_img = img.crop(cropping_tuple)
    
    return cropped_img


# Creating a grid of images 
def image_grid(imgs, rows, cols):
    assert len(imgs) == rows*cols # testing that the image's length condition is met 

    w, h = imgs[0].size
    grid = Image.new('RGB', size=(cols*w, rows*h))
    grid_w, grid_h = grid.size
    
    for i, img in enumerate(imgs):
        grid.paste(img, box=(i%cols*w, i//cols*h))
    return grid


# Checking the yellowness of an image
def yellowness_img(red_hist, green_hist, blue_hist):
    list_of_checks = []
    for r, g, b, in zip(red_hist[100:220], green_hist[100:220], blue_hist[100:220]):
        
        # If red and green are higher than blue (i.e., if there is yellow) 
        if r > b and g > b:
            list_of_checks.append(1)
        else:
            list_of_checks.append(0)
    return sum(list_of_checks) / len(list_of_checks)