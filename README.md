# python_tesseract
This repository conntains codes which augment english word images, runs the tesseract OCR on them and saves the predictions onto local disk


## How to run the code 

```bash 
python main.py  -p 8 -o outputs/
```
## Parameters to be set

1. -p sets the segmentation mode to handle word images
2. -o path to output directory where the augmentated images will be stored


The above code will generate a `predictions.txt' containing the uinique ID for each 
image and it's correponding prediction.