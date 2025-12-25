---
title: "Implementing a JPEG Encoder in Python (Part 1)"
date: 2025-12-25T12:00:00+03:00
draft: false
summary: "A deep dive into the inner workings of JPEG compression, building an encoder from scratch in pure Python."
---

JPEG is everywhere. It's the standard for compressing continuous-tone images like photographs. But how does it actually work? In this two-part series, we're going to build a JPEG codec from scratch in Python to understand the magic behind the compression.

In Part 1, we will focus on the **Encoder**—taking a raw image and crunching it down.

## The Pipeline

Encoding a JPEG involves several distinct steps. We'll implement them one by one:

1.  **Color Space Conversion**: RGB to YCbCr.
2.  **Subsampling**: Reducing color resolution.
3.  **Blocking**: Splitting the image into 8x8 blocks.
4.  **DCT (Discrete Cosine Transform)**: Converting spatial data to frequency domain.
5.  **Quantization**: Throwing away the high-frequency detail.
6.  **Entropy Coding**: Compressing the result (we'll implement a basic version of this).

Let's dive in.

## 1. Color Space Conversion (RGB to YCbCr)

Computers usually represent images in RGB (Red, Green, Blue). However, the human eye is more sensitive to brightness (Luminance) than color (Chrominance). JPEG takes advantage of this by separating these components.

- **Y**: Luminance (Brightness)
- **Cb**: Blue-difference chroma
- **Cr**: Red-difference chroma

Here is the formula and the Python implementation:

```python
import numpy as np
from PIL import Image

def rgb_to_ycbcr(r, g, b):
    y  =  0.299 * r + 0.587 * g + 0.114 * b
    cb = -0.1687 * r - 0.3313 * g + 0.5 * b + 128
    cr =  0.5 * r - 0.4187 * g - 0.0813 * b + 128
    return y, cb, cr

# Ideally, we process the image as numpy arrays for speed
def convert_image(image_path):
    img = Image.open(image_path)
    img_arr = np.array(img, dtype=float)
    r, g, b = img_arr[:,:,0], img_arr[:,:,1], img_arr[:,:,2]
    return rgb_to_ycbcr(r, g, b)
```

## 2. 8x8 Blocking & Subsampling

JPEG processes images in 8x8 distinct blocks. All subsequent operations (DCT, Quantization) happen on these independent blocks.

We also perform **Chroma Subsampling** here. Since eyes are less sensitive to color, we can halve the resolution of the Cb and Cr channels (e.g., 4:2:0 subsampling) without much perceptible loss.

```python
def make_blocks(channel, N=8):
    h, w = channel.shape
    # Pad to multiple of 8
    h_pad = (h + N - 1) // N * N
    w_pad = (w + N - 1) // N * N
    padded = np.zeros((h_pad, w_pad))
    padded[:h, :w] = channel
    
    blocks = []
    for i in range(0, h_pad, N):
        for j in range(0, w_pad, N):
            blocks.append(padded[i:i+N, j:j+N])
    return blocks
```

## 3. Discrete Cosine Transform (DCT)

This is the heart of JPEG. The DCT transforms our 8x8 pixel block from the *spatial domain* (pixel values) to the *frequency domain* (coefficients). 

The top-left coefficient (DC) represents the average color of the block. The bottom-right coefficients represent high-frequency details (noise, sharp edges).

```python
import scipy.fftpack

def dct_2d(block):
    # Perform 2D DCT (Type II)
    return scipy.fftpack.dct(
        scipy.fftpack.dct(block.T, norm='ortho').T, norm='ortho'
    )
```

## 4. Quantization

This is where the "lossy" part happens. We divide our DCT coefficients by a "Quantization Table" and round to the nearest integer. The tables are carefully tuned to discard high-frequency information that we can't see well.

```python
# Standard JPEG Luminance Quantization Table
Q_TABLE = np.array([
    [16, 11, 10, 16, 24, 40, 51, 61],
    [12, 12, 14, 19, 26, 58, 60, 55],
    [14, 13, 16, 24, 40, 57, 69, 56],
    [14, 17, 22, 29, 51, 87, 80, 62],
    [18, 22, 37, 56, 68, 109, 103, 77],
    [24, 35, 55, 64, 81, 104, 113, 92],
    [49, 64, 78, 87, 103, 121, 120, 101],
    [72, 92, 95, 98, 112, 100, 103, 99]
])

def quantize(block, q_table):
    return np.round(block / q_table)
```

After quantization, you'll find that most of your 64 coefficients are now **zeros**, especially in the bottom-right corner. This is why JPEG compresses so well!

## 5. Zigzag Scan & Entropy Coding

To store these coefficients efficiently, we linearize the 8x8 matrix using a "zigzag" pattern, grouping the zeros at the end. We can then use Run-Length Encoding (RLE) to say "skip 15 zeros" instead of writing "0, 0, 0...".

Finally, these symbols are Huffman encoded.

*(Full Huffman implementation is a bit verbose for this post, but you can find the complete source code in the gist below!)*

## Conclusion

We've transformed raw pixels into quantized frequency coefficients. The file size is now a fraction of the original.

In **Part 2**, we will reverse this entire process to build the **Decoder** and view our compressed image.

[Check out the full Encoder Implementation here (Gist)](https://gist.github.com/aitumik)
