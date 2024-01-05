# General Information

I’m uploading the pasta classifier I trained to detect different pasta shapes!💻🍝 

# Table of Contents
- General Info
- Setup
- Usage
- Challenges
- Project Results 
- Future Data Exploration Ideas
- Acknowledgements
- Contact

The goal was to explore the data available online. Once that's done, I used those pictures to train an ML model and detect the right shape of pastas. I also want to support other coders who are pasta lovers like me and are willing to train their own classifier!🗺️🔎👣

I used online images which are available on the Google Search and found a way to download them. The classes of the data are 12. I then explored the data, resized the images, cropped them, and saved them in a new file path.

# Setup
First off, make sure you have conda🐍👀:

`conda create -n <replace-with-name-you-want> python=3.11`

`conda activate <replace-with-name-you-want>`

`pip install -r requirements.txt`

# Usage
Check out these files in my repo to see how I've processed the data, built and trained the models!

- `data_cleansing.ipynb`

- `data_processing.ipynb`

- `model_building.ipynb`

# Challenges
I wanted to retrieve a lot of good quality images, but the web has lots of duplicated images. This didn’t make the data I downloaded that useful. So to solve this issue in the short-term, I got rid of all those duplicates. I’m aiming at taking pictures of different pasta shapes in a span of 6 months. In that way, I can use them to train my machine learning models better! 

Another challenge was to find a quick way to label the cleansed images and store them in a new directory. I wanted to add the label to each picture manually, but then I realised that this would’ve taken me too long. So I created a dictionary with the substring of pasta shape as key, and the list of images of that pasta as the value. 

I also created a function to check the level of yellowness in a picture. I thought that this could help me train an ML model better, but then I realised that some pics had green or red pasta. I also found many kinds of pasta shapes in the same picture. This could have confused the model, so I ended up not checking for yellowness. 

It was also challenging to find the right size of images. This was necessary to perform the right matrix multiplication. I ended up shrinking the images by 4. 

# Project Results
I trained a Convolutional Neural Network four times. I performed a hyper parameter tuning optimisation documented in `'model_building.ipynb'`. The model with the highest values is the third one, with an accuracy of 0.09. Yet, this is already a low result, which indicates that the model is not learning well.

# Future Data Exploration Ideas

We could try to take more pics to train the model better. We could also explore alternative HPO techniques to train the machine learning model.

# Acknowledgements
A massive thank you to `Ward Haddadin`! Your fantastic support and inspiration provided along the way were amazing! This wouldn't have been possible if it wasn't for your words of encouragement and tell on how to debug my codes!

# Contact
For any question, drop me a line at giorgiadt14@gmail.com and I'll be happy to help you out! Feel free to message me on LinkedIn too! Happy coding!