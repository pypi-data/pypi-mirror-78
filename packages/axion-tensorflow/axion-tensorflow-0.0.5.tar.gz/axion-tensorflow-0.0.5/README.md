## Introduction

This is an implementation of axion for TensorFlow >=2.2.

Current version provides quantized conv2d & dense layer. More layers are about to come.

## Installing & Usage

To install current release:

`pip install axion-tensorflow`

To use axion layer in your model, do

`import axion_tensorflow as axion`

Then you can use `axion.layers.Conv2D` & `axion.layers.Dense`