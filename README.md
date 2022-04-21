# PNGcrypt
## Hiding messages in plain sight
For the time being, use `pngcrypt.py`. Run with `> python3 pngcrypt.py --help` for usage. **NOTE: Some unknown bug is causing issues. There is a high chance this tool will break and write a corrupt .png file. The original file will remain unedited. To this end, no examples exist yet.**


### What does it do?
This project leans on the `pypng` library that can be found [here](https://pypi.org/project/pypng/).

The idea is somewhat simple: with `pypng`, one can read the lines of pixels in a .png file as color values that range 0-255. These pixel color values can be converted into binary, edited, restored into a collection of other pixels, and written into a new file. By editing the least-significant bits of a handful of seemingly random pixels scattered around the image, one could split binary interpretations of UTF-8 characters in a message and hide them in the colors that represent the pixels. The result is almost unnoticeable, especially when using higher resolution images.


### Coming up
There are plenty of features I want to implement in the future. This is a short list of what's on the horizon:
- Refactor for less user input, implementing the `argparse` library
- Seed a password into a pixel selection algorithm that lets sender and recipient have exclusive access to the message
- Add `--message []`, `--message-file []`, `--password []`, and `--password-file []` arguments


## DISCLAIMER
This project is in early stages! **DO NOT** rely on it for any sort of secret sharing. Data saved using this program could potentially be mined with relative ease.
