---
title: Neural Network Overview
date: 12 Aug 2019
modified: 17 Jan 2021
image: "https://i.pinimg.com/736x/09/37/a9/0937a96126d7f91fce1e1ecc9e404748.jpg"
image-height: "400px"
---

Ideally, we want to take first principles (i.e. $F=ma$) and develop a model of a system that we can
use. However, systems are inherently becoming more complex and more non-linear ($\hat x = f(x,t,u; \beta)$)
and we may not be able to develop them from first principles. Thus, we need to take data from sensors
and try to create a model (preferable lower dimensional and intuitive) that suits our purposes.
Generally, I am interested in:

- Controls
- Estimation (predict future states or guess at unmeasureable states)
- Anomoly detection
- Operations in noisy environments

![](activation-functions.png)

| Netowrk                 | Supervised | Use Case |
|-------------------------|---|:-------------------|
| ANN                     | Y | regression and classification, learns *long-term memory* through backpropagation (e.g., adjust weights) |
| CNN                     | Y | computer vision due to the use of convoution layers and leverages backpropagation |
| RNN                     | Y | time series analysis, introduces *short-term memory* |
| Self-Organizing Maps    | N | feature detection |
| Deep Boltzmann Machines | N | recommendation systems (e.g., Amazon cart) |
| AutoEncoders            | N | recommendation systems |

## Backpropagation

Backpropagation is a method for updating the weights of the NN. 

## Convolutional Neural Network (CNN)

The heart of this is convolution:

![](conv.gif)

- CNNs are **feedforward** systems, meaning, info is fed from one layer to the next
- CNNs only consider the current inputs
- Layers:
    - *Convolution layer:* most computational heavy lifting layer
    - *Pooling layer:* sandwiched aroun convolutional layers to reduce the size
    of what the cconvolutional layers produce. This helps to reduce memory
    requirements
    - *Normalizing layer:* converts all inputs to a value with zero mean and a
    standard deviation of 1. This improves performance and stability of the NN.
    There are many different normalizing layer topologies like ReLU.
- Common uses: object identification in computer vision
    - **Convolution** is a standard method in image processing for finding edges or changes
    in the local gradient
    - Summing these finding up (from a preceeding convolutional layer) helps the NN to
    identify features in an image


## Recursive Neural Network (RNN)

- Similar to CNN, but RNNs have a **feedback** capability
- RNNs concider both the current and previous inputs
    - can predicct what comes next because it learns order
- Common uses: stock prediction, trading stock, language, or anyting that
follows a pattern and changes with **time**
    - Feedback can be from a neuron to itself or to a previous layer

## Autoencoder (Shallow, linear)

- Transform a high dimensional data ($X$) to fewer dimension ($Z$) and then back to a
higher dimension ($\hat X$) which is an estimate of $X$
    - Essentially, implement Principle Component Analysis (PCA)
    - Allows compression of high dimensional down to the important dimension (PCA)
    - Can allow better understanding of the information, since it is reduced to fewer
    parameters ($Z$) than the original ($X$)

## Neural Networks (NN) Libraries

- **You Only Look Once(YOLO):** A single NN that looks a the whole image by
dividing it up into regions and predicts bounding boxes and probabilities for
each region. It is extremely fast.
    - Yolov3-tiny is a smaller version for constrained environments (embedded
        systems)
- **Tensorflow:** came from Google research and still used/backed by them.
    - Python and C++
    - Absorbed **Keras** in version Tensorflow 2.0
- **Open Neural Network eXchange (ONNX):** Large consordium of companies supporting
tools/architecture where models are trained in one framework and transfered
to another framework.
    - Supports: Caffe2, CNTK, MXNet, pyTorch, Tensorflow
    - Python and C++
- **Theano:** as of 2019, not funded or maintained anymore
- **Microsoft Cognitive Toolkit (CNTK):** not maintained anymore after version
2.7 based on disclaimer on github site. They suggest using ONNX
- **Tencent/ncnn:** A NN for cellphone/embedded systems
    - [github repo](https://github.com/Tencent/ncnn)

## Tools

- **Keras:** Highlevel NN tools written in python
    - Supports: Tensorflow, CNTK or Theano as the backend NN
    - Also funded by Google and large market support
        - Apple supports CoreML integration for iOS
    - Adopted by CERN and NASA
- **pyTorch:** Highlevel NN tools written in python and C++
    - Supports CUDA (NVIDIA GPU)

|          | Keras  | pyTorch | Tensorflow |
|----------|--------|---------|------------|
| Language | python | c++, python, CUDA (NVIDIA GPU) | python, c++ |
| Support  | Tensorflow, CNTK or Theano as the backend NN | | |
| Funding  | Google, Apple supports CoreML integration for iOS | | |
| Notes    | Adopted by CERN and NASA | now contains Caffe2 | came from Google Research |

- AI
    - ML: machine learing, supervised and unsupervised
        - DL: deep learning, supervised NN learning
- Tensor: multidimensional array or list

## Pre-trained

- **ResNet50:** a 50 layer, pretrained CNN on 1 million images that can
catagorize 1000 objects
    - image size: 224x224 px

# References

- [Deep learning on Raspberry Pi](https://medium.com/nanonets/how-to-easily-detect-objects-with-deep-learning-on-raspberrypi-225f29635c74)
- [ResNet Tensorflow example](https://github.com/taki0112/ResNet-Tensorflow)
- [Tensorflow Cookbook](https://github.com/taki0112/Tensorflow-Cookbook)
