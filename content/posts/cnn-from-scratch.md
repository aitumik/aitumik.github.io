---
title: "Building a Convolutional Neural Network from Scratch with NumPy"
date: 2025-12-25T12:30:00+03:00
draft: false
categories: ["Deep Learning", "Python", "NumPy", "Systems"]
summary: "Understand the magic of ConvNets by building the forward pass layers purely in NumPy."
---

Convolutional Neural Networks (CNNs) are the backbone of modern computer vision. While frameworks like PyTorch and TensorFlow make it easy to train them, building one from scratch is the best way to truly understand what's happening under the hood.

In this post, we'll implement the core components of a CNN—Convolution and Max Pooling—using nothing but NumPy.

## 1. The Convolution Operation

At its core, a convolution filters an input image to extract features (edges, textures, shapes). Mathematically, it's actually cross-correlation. We slide a small filter (kernel) over the image and compute the dot product at each position.

Here is the discrete convolution formula for a 2D image $I$ and kernel $K$:

$$ (I * K)(i, j) = \sum_m \sum_n I(i+m, j+n) K(m, n) $$

Let's implement this efficiently in NumPy.

```python
import numpy as np

def convolve2d(image, kernel, stride=1, padding=0):
    # Add zero padding to the input image
    image = np.pad(image, [(padding, padding), (padding, padding)], mode='constant')
    
    kernel_h, kernel_w = kernel.shape
    padded_h, padded_w = image.shape
    
    output_h = (padded_h - kernel_h) // stride + 1
    output_w = (padded_w - kernel_w) // stride + 1
    
    output = np.zeros((output_h, output_w))
    
    for y in range(0, output_h):
        for x in range(0, output_w):
            # Extract the region of interest
            region = image[y*stride : y*stride+kernel_h, x*stride : x*stride+kernel_w]
            # Perform element-wise multiplication and sum
            output[y, x] = np.sum(region * kernel)
            
    return output
```

## 2. The Convolution Layer

A real layer processes 3D volumes (Height x Width x Channels) and applies multiple filters to create a new 3D volume of output features.

```python
class Conv3x3:
    # A simple 3x3 convolution layer with 8 filters.
    def __init__(self, num_filters):
        self.num_filters = num_filters
        # Filters are 3x3x3 (since input is typically RGB) or just randomly initialized
        # For simplicity, let's say input is 2D grayscale here:
        self.filters = np.random.randn(num_filters, 3, 3) / 9.0

    def iterate_regions(self, image):
        # Generates all valid 3x3 image regions
        h, w = image.shape
        for i in range(h - 2):
            for j in range(w - 2):
                im_region = image[i:(i + 3), j:(j + 3)]
                yield im_region, i, j

    def forward(self, input):
        h, w = input.shape
        output = np.zeros((h - 2, w - 2, self.num_filters))

        for im_region, i, j in self.iterate_regions(input):
            output[i, j] = np.sum(im_region * self.filters, axis=(1, 2))

        return output
```

## 3. Max Pooling

Pooling reduces the spatial dimensions of the input volume. It helps reduce computation and controls overfitting. Max pooling simply takes the maximum value in each window.

```python
class MaxPool2:
    # A Max Pooling layer using a pool size of 2.

    def iterate_regions(self, image):
        h, w, _ = image.shape
        new_h = h // 2
        new_w = w // 2

        for i in range(new_h):
            for j in range(new_w):
                im_region = image[(i * 2):(i * 2 + 2), (j * 2):(j * 2 + 2)]
                yield im_region, i, j

    def forward(self, input):
        h, w, num_filters = input.shape
        output = np.zeros((h // 2, w // 2, num_filters))

        for im_region, i, j in self.iterate_regions(input):
            output[i, j] = np.amax(im_region, axis=(0, 1))

        return output
```

## 4. Putting It Together

With these building blocks, a forward pass looks like this:

```python
# Assume we have a 28x28 grayscale image (like MNIST)
image = np.random.randn(28, 28)

conv = Conv3x3(8)
pool = MaxPool2()

output_conv = conv.forward(image) # 26x26x8 volume
output_pool = pool.forward(output_conv) # 13x13x8 volume

print(f"Input shape: {image.shape}")
print(f"Conv output shape: {output_conv.shape}")
print(f"Pool output shape: {output_pool.shape}")
```

## Conclusion

We've built the forward pass of a basic CNN. To make this a functional neural network, we would need to implement:
1.  **Activation Functions** (like ReLU).
2.  **Fully Connected Layers** (Softmax) for classification.
3.  **Backpropagation** to actually train the filters (calculating gradients $dL/dF$).

Implementing backpropagation for convolution is a great exercise in calculus and indexing, which we might cover in a future post!
