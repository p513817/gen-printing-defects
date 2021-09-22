# gen-printing-defects
This program can generate printing defects with white background

![cover](figures/cover_generate_printing_defects.gif)

## Features
1. Apply more transform's options with random value. 
2. User can select target area to generate defects.
3. Press 's' to save , 'q' to leave, other key to continue.

## How to use
```
$ python3 generate_dust.py --help

usage: generate_dust.py [-h] [-s] [-i IMAGE] [-d DENSITY] [-o OUTPUT_DIR]

optional arguments:
  -h, --help            show this help message and exit
  -s, --select          select the target area.
  -i IMAGE, --image IMAGE
                        input images which you want to generate dust.
  -d DENSITY, --density DENSITY
                        fix dust's density. value:0~1
  -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                        output directory.
```

## Detail

1. Select target area you want to generate printing defects.
2. Create black image which with same size of input image.
3. Generate white dust on it, and let user control density.
4. Crop the target area and add black border to fit the original size.

## Future work

* Improve the method of generate dusts