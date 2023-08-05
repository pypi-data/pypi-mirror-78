# Titanicbc

Titanicbc provides a simple graphical user interface (GUI) for training and using PyTorch neural networks with custom hyper-parameters. The current version allows
training a binary classifier network for the famous Kaggle Titanic dataset (Dataset available at https://www.kaggle.com/c/titanic/data).

The aim of this package is to allow those with little or no neural network coding experience to explore how different hyper-parameter 
combinations affect neural network training through an easy-to-use interface. The package also includes a pre-trained neural network for demonstrating how networks make predictions
once trained.

Later versions will expand the package to contain networks for other classic datasets,
including image and text datasets with convolutional and recurrent neural networks.

### Installation

You can install Titanicbc from PyPI

___
***pip install Titanicbc***

___

## How to use

___

To customise hyper-parameters and train a neural network or make predictions using a pre-trained neural network, 
simply run ***python -m Titanicbc*** from the command line or terminal. This brings up the Titanicbc GUI detailed in the User Interface section below.

To begin training a network, enter the desired hyper-parameters in the interface. Next, click "Confirm network configuration and train"
to begin training a model. Leave the terminal window open in which you ran ***python -m Titanicbc*** as this is where the 
training process will be displayed. (Note that the training process is launched in a seperate thread so if you wish to quit the
application during training you must also close the terminal window seprately). 

The new model will overwrite the current trained model and predictions made by the new model will be saved into a file named "output.csv". To view output.csv in your
computer's default csv viewing software, simply click "Open output.csv" from the user interface.
The output columns are in the Kaggle required format (the PassengerId and the prediction of whether that passenger survived).

The accuracy of a newly trained model is computed on a validation set and is displayed below the final training epoch,
above the prediction output dataframe. This accuracy on unseen data provides a way of comparing the effectiveness of 
different models on out-of-sample data.

If you wish to predict using the pre-trained network included in the package instead, select "Predict using last trained model"
from the interface. This will immediately make predictions using the included network and write them out to "output.csv".
If you have already trained a model previously then this option will make predictions using the last model you trained to completion,
rather than the included network.

___

##  User Interface

Training neural networks using the Titanicbc package is made easy through the Graphical User Interface. The hyper-parameters
that can be customised from the GUI are given below in the following format;

***Key (value options or input type) - info*** 

hidden_dim (Integer) - Number of neurons in each of the 3 hidden layers within the network.

num_epochs (Integer) - Number of passes the network will make over the training data when training a new model.

learning_rate (float) - Parameter multiplied to the weight updates during stochastic gradient descent. Currently only the Adam optimiser is used.

weight_init (uniform, xavier) - Tells the network which of the Pytorch initialisations to use for the model weights. 
Xavier is currently recommended

weight_decay (float) -  Weight decay acts as l2 regularlisation on the neural network.

___
