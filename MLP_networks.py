#!/usr/bin/env python
# coding: utf-8

# # PyTorch Assignment: Multi-Layer Perceptron (MLP)

# **[Duke Community Standard](http://integrity.duke.edu/standard.html): By typing your name below, you are certifying that you have adhered to the Duke Community Standard in completing this assignment.**
# 
# Name: Bibekananda Bachhar

# ### Multi-Layer Perceptrons
# 
# The simple logistic regression example we went over in the previous notebook is essentially a one-layer neural network, projecting straight from the input to the output predictions.
# While this can be effective for linearly separable data, occasionally a little more complexity is necessary.
# Neural networks with additional layers are typically able to learn more complex functions, leading to better performance.
# These additional layers (called "hidden" layers) transform the input into one or more intermediate representations before making a final prediction.
# 
# In the logistic regression example, the way we performed the transformation was with a fully-connected layer, which consisted of a linear transform (matrix multiply plus a bias).
# A neural network consisting of multiple successive fully-connected layers is commonly called a Multi-Layer Perceptron (MLP). 
# In the simple MLP below, a 4-d input is projected to a 5-d hidden representation, which is then projected to a single output that is used to make the final prediction.
# 
# <img src="Figures/MLP.png" width="300"/>
# 
# For the assignment, you will be building a MLP for MNIST.
# Mechanically, this is done very similary to our logistic regression example, but instead of going straight to a 10-d vector representing our output predictions, we might first transform to a 500-d vector with a "hidden" layer, then to the output of dimension 10.
# Before you do so, however, there's one more important thing to consider.
# 
# ### Nonlinearities
# 
# We typically include nonlinearities between layers of a neural network.
# There's a number of reasons to do so.
# For one, without anything nonlinear between them, successive linear transforms (fully connected layers) collapse into a single linear transform, which means the model isn't any more expressive than a single layer.
# On the other hand, intermediate nonlinearities prevent this collapse, allowing neural networks to approximate more complex functions.
# 
# There are a number of nonlinearities commonly used in neural networks, but one of the most popular is the [rectified linear unit (ReLU)](https://en.wikipedia.org/wiki/Rectifier_(neural_networks)):
# 
# \begin{align}
# x = \max(0,x)
# \end{align}
# 
# There are a number of ways to implement this in PyTorch.
# We could do it with elementary PyTorch operations:

# In[4]:


import torch

x = torch.rand(5, 3)*2 - 1
x_relu_max = torch.max(torch.zeros_like(x),x)

print("x: {}".format(x))
print("x after ReLU with max: {}".format(x_relu_max))


# Of course, PyTorch also has the ReLU implemented, for example in `torch.nn.functional`:

# In[6]:


import torch.nn.functional as F

x_relu_F = F.relu(x)

print("x after ReLU with nn.functional: {}".format(x_relu_F))


# Same result.

# ### Assignment
# 
# Build a 2-layer MLP for MNIST digit classfication. Feel free to play around with the model architecture and see how the training time/performance changes, but to begin, try the following:
# 
# Image (784 dimensions) ->  
# fully connected layer (500 hidden units) -> nonlinearity (ReLU) ->  
# fully connected (10 hidden units) -> softmax
# 
# Try building the model both with basic PyTorch operations, and then again with more object-oriented higher-level APIs. 
# You should get similar results!
# 
# 
# *Some hints*:
# - Even as we add additional layers, we still only require a single optimizer to learn the parameters.
# Just make sure to pass all parameters to it!
# - As you'll calculate in the Short Answer, this MLP model has many more parameters than the logisitic regression example, which makes it more challenging to learn.
# To get the best performance, you may want to play with the learning rate and increase the number of training epochs.
# - Be careful using `torch.nn.CrossEntropyLoss()`. 
# If you look at the [PyTorch documentation](https://pytorch.org/docs/stable/nn.html#crossentropyloss): you'll see that `torch.nn.CrossEntropyLoss()` combines the softmax operation with the cross-entropy.
# This means you need to pass in the logits (predictions pre-softmax) to this loss.
# Computing the softmax separately and feeding the result into `torch.nn.CrossEntropyLoss()` will significantly degrade your model's performance!

# In[1]:


import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import matplotlib.pyplot as plt

from tqdm import tqdm
from torchvision import datasets,transforms

trainset = datasets.MNIST(root="./datasets", train=True, transform=transforms.ToTensor(), download=True)
testset = datasets.MNIST(root="./datasets", download = True, train = False, transform = transforms.ToTensor())

trainloader = torch.utils.data.DataLoader(trainset, batch_size = 10, shuffle = False)
testloader = torch.utils.data.DataLoader(testset, batch_size = 10, shuffle = True)


class MNIST_MLP_model(nn.Module):
    
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(28*28,500)
        self.fc2 = nn.Linear(500,10)
  
        
        
    
    
    def forward(self,X):
        Z = F.relu(self.fc1(X))
        Y = F.relu(self.fc2(Z))
        #print(Y.shape)
        return  Y

batches = iter(trainloader)

    
mymodel = MNIST_MLP_model()
optimizer = torch.optim.SGD(mymodel.parameters(),lr=0.01)
Loss = nn.CrossEntropyLoss()

for batch in tqdm(batches):
    images,labels = batch
    optimizer.zero_grad()
    #print(":",labels.shape,Y.shape)
    #print(labels,Y)
    Y = mymodel.forward(images.view(-1,28*28))
    loss = Loss(Y,labels)
    loss.backward()
    optimizer.step()

test_batch = iter(testloader)
correct = 0
total = 0

for batch in tqdm(test_batch):
    
    images,labels = batch
    
 

    for img,lbl in zip(images,labels):
        Y = mymodel.forward(img.view(-1,28*28))
        label = torch.argmax(Y,dim = 1)
        if(label == lbl): correct+=1
        total+=1


print(f"Accuracy: {(correct/total)*100} %")


# ### Short answer
# How many trainable parameters does your model have? 
# How does this compare to the logisitic regression example?

# There are 5489 trainable parameters in this model and in logistic regression model there were 542 trainable parameters`
