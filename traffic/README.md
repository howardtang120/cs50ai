# Neural network lab
## Abstract
This is my lab report on convolutional neural networks, tested on the German Traffic Sign Recognition Benchmark (GTSRB) dataset. The objective of the experiment is to evaluate the impact of different settings and layers on the accuracy and efficiency of a neural network, and design a model with the highest accuracy with a training time of under 5 minutes. The experiment uses a "base model" as benchmark, and changes only one parameter each time to observe the effect.

## Test method
The experiment utilized the full set of 43 images from the GTSRB dataset. All numerical comparisons are made relative to the base version.

The base version employed 10 epochs, a train_test_split of 0.4, and a dropout rate of 0.5. It consisted of a 32-feature convolutional layer, a 2x2 max pooling layer, followed by a dense layer with 128 nodes. The base model achieved an accuracy of approximately 96%, with a training time of 12 seconds per epoch.

The experiment investigated the effects of various modifications, such as increasing the number of epochs, adding or modifying convolutional layers, adjusting max pooling layer size, changing the dropout rate, and altering the train_test_split parameter.

## Analysis
Compared to the base version, the following observations were made:

1. Increasing the number of epochs improved accuracy but increased training time.
2. Adding a convolutional layer or increasing its size enhanced accuracy but slowed down training.
3. Using a larger max pooling layer size sped up training time slightly but reduced accuracy.
4. The dropout layer had unexpected effects. Removing the 0.5 dropout layer increased accuracy by 1%, while changing the rate to 0.2 improved accuracy by 1.5%. The small network size might have made it less susceptible to overfitting, and a large dropout rate could have hindered feature learning. Training time was not significantly affected.
5. Decreasing the train_test_split parameter from 0.4 to 0.2 increased accuracy by 1.5%, indicating that allocating more data to the training set helped the network learn more features. However, this change increased training time by 25%.
6. Changing the input image dimensions from 30x30 to 50x50 negatively impacted accuracy and significantly slowed down training.
7. Combining modifications, such as changing image dimensions and max pooling size simultaneously, had a cumulative effect on accuracy and training time.


## Data

*Compared to base version*

|Changes                    |Accuracy                   |Efficiency |
|---------------------------|---------------------------|-----------|
|+Convolution filter        |++accuracy                 |--speed    |
|+Max pooling               |-accuracy                  |++speed    |
|+Max pooling size          |--accuracy                 |+++speed   |
|+Convolution and pooling   |++accuracy                 |++speed    |
|+Dense layer size          |+accuracy (?)              |--speed    |
|+EPOCHS                    |+accuracy                  |--speed    |
|+Dropout 0.2               |+accuracy                  |-speed     |
|+Dropout 0.5               |-accuracy                  |-speed     |
|+Test_split 0.4 -> 0.2     |++accuracy                 |-speed     |
|+Input image dimentions    |--accuracy                 |---speed   |



## References
The experiment utilized the German Traffic Sign Recognition Benchmark (GTSRB) dataset, consisting of 43 classes of traffic signs. The experiment was conducted with guidance from Harvard's CS50AI course on artificial intelligence and neural networks.  

# Experiment data
Commas indicate layer sequence  
Each line is a full 10 epoch cycle  
CV = "convolution"  
MP = "max pooling"  
Base = "32 CV, 2x2 MP"  

### Base version (12s per epoch)
333/333 - 2s - loss: 0.0131 - accuracy: 0.9565 - 2s/epoch - 5ms/step  
333/333 - 2s - loss: 0.0098 - accuracy: 0.9691 - 2s/epoch - 5ms/step  
333/333 - 2s - loss: 0.0121 - accuracy: 0.9640 - 2s/epoch - 5ms/step  
333/333 - 2s - loss: 0.0134 - accuracy: 0.9661 - 2s/epoch - 5ms/step  
333/333 - 2s - loss: 0.0106 - accuracy: 0.9696 - 2s/epoch - 5ms/step  

## Single parameter change
### **CV 32 -> 64** (23s per epoch)
333/333 - 2s - loss: 0.0061 - accuracy: 0.9799 - 2s/epoch - 6ms/step  
333/333 - 1s - loss: 0.0075 - accuracy: 0.9731 - 1s/epoch - 4ms/step  
333/333 - 2s - loss: 0.0071 - accuracy: 0.9791 - 2s/epoch - 5ms/step  

### **No max pooling** (36s per epoch)
333/333 - 1s - loss: 0.0104 - accuracy: 0.9689 - 1s/epoch - 4ms/step  
333/333 - 1s - loss: 0.0112 - accuracy: 0.9666 - 1s/epoch - 4ms/step  
333/333 - 2s - loss: 0.0114 - accuracy: 0.9617 - 2s/epoch - 5ms/step  

### **Dropout 0.5 -> 0.2** (11s per epoch)
333/333 - 2s - loss: 0.0072 - accuracy: 0.9743 - 2s/epoch - 6ms/step  
333/333 - 2s - loss: 0.0074 - accuracy: 0.9742 - 2s/epoch - 6ms/step  
333/333 - 2s - loss: 0.0067 - accuracy: 0.9747 - 2s/epoch - 5ms/step

### **No dropout** (12s per epoch)
333/333 - 1s - loss: 0.0074 - accuracy: 0.9715 - 901ms/epoch - 3ms/step  
333/333 - 1s - loss: 0.0082 - accuracy: 0.9707 - 1s/epoch - 3ms/step  
333/333 - 1s - loss: 0.0068 - accuracy: 0.9769 - 993ms/epoch - 3ms/step  

### **Adamax** (11s per epoch)
333/333 - 1s - loss: 0.0208 - accuracy: 0.9229 - 884ms/epoch - 3ms/step  
333/333 - 2s - loss: 0.0207 - accuracy: 0.9161 - 2s/epoch - 5ms/step  
333/333 - 1s - loss: 0.0186 - accuracy: 0.9324 - 949ms/epoch - 3ms/step  

### **Dense activation = sigmoid** (11s per epoch)
333/333 - 2s - loss: 0.0081 - accuracy: 0.9753 - 2s/epoch - 5ms/step  
333/333 - 2s - loss: 0.0096 - accuracy: 0.9707 - 2s/epoch - 5ms/step  
333/333 - 2s - loss: 0.0083 - accuracy: 0.9700 - 2s/epoch - 6ms/step  

### **Dense 128 -> 256** (19s per epoch)
333/333 - 2s - loss: 0.0066 - accuracy: 0.9758 - 2s/epoch - 6ms/step  
333/333 - 2s - loss: 0.0069 - accuracy: 0.9777 - 2s/epoch - 6ms/step  
333/333 - 2s - loss: 0.0070 - accuracy: 0.9812 - 2s/epoch - 6ms/step  

### **15 epochs** (12s per epoch)
333/333 - 1s - loss: 0.0089 - accuracy: 0.9747 - 1s/epoch - 3ms/step  
333/333 - 1s - loss: 0.0115 - accuracy: 0.9682 - 1s/epoch - 3ms/step  
333/333 - 1s - loss: 0.0096 - accuracy: 0.9722 - 1s/epoch - 3ms/step  

### **Testing set 0.4 --> 0.2** (15s per epoch)
167/167 - 1s - loss: 0.0085 - accuracy: 0.9732 - 923ms/epoch - 6ms/step  
167/167 - 1s - loss: 0.0103 - accuracy: 0.9765 - 985ms/epoch - 6ms/step  
167/167 - 1s - loss: 0.0136 - accuracy: 0.9685 - 962ms/epoch - 6ms/step  

### **MP (2x2) -> (3x3)** (6s per epoch)
333/333 - 1s - loss: 0.0108 - accuracy: 0.9624 - 1s/epoch - 3ms/step  
333/333 - 1s - loss: 0.0145 - accuracy: 0.9481 - 1s/epoch - 3ms/step  
333/333 - 1s - loss: 0.0155 - accuracy: 0.9428 - 1s/epoch - 3ms/step  

### **IMAGE width/height 30 -> 50** (35s per epoch)
333/333 - 3s - loss: 0.0140 - accuracy: 0.9566 - 3s/epoch - 8ms/step  
333/333 - 2s - loss: 0.0143 - accuracy: 0.9516 - 2s/epoch - 7ms/step  
333/333 - 2s - loss: 0.0115 - accuracy: 0.9637 - 2s/epoch - 7ms/step  

### **IMAGE width/height 30 -> 50, MP (2x2) -> (3x3)** (20s per epoch)
333/333 - 2s - loss: 0.0098 - accuracy: 0.9657 - 2s/epoch - 6ms/step  
333/333 - 2s - loss: 0.0118 - accuracy: 0.9591 - 2s/epoch - 5ms/step  
333/333 - 2s - loss: 0.0124 - accuracy: 0.9565 - 2s/epoch - 6ms/step  

## Convolution experiments
### **Base, 32 CV, 2x2 MP** (8s per epoch)
333/333 - 2s - loss: 0.0090 - accuracy: 0.9703 - 2s/epoch - 6ms/step  
333/333 - 2s - loss: 0.0078 - accuracy: 0.9767 - 2s/epoch - 6ms/step  
333/333 - 2s - loss: 0.0078 - accuracy: 0.9756 - 2s/epoch - 6ms/step  

### **Base, 32 CV, 2x2 MP, no dropout** (7s per epoch)
333/333 - 1s - loss: 0.0055 - accuracy: 0.9829 - 1s/epoch - 4ms/step  
333/333 - 1s - loss: 0.0060 - accuracy: 0.9815 - 1s/epoch - 4ms/step  
333/333 - 1s - loss: 0.0067 - accuracy: 0.9766 - 1s/epoch - 4ms/step  

### **Base - MP, 32 CV, 2x2 MP** (25s per epoch)
333/333 - 3s - loss: 0.0053 - accuracy: 0.9893 - 3s/epoch - 8ms/step  
333/333 - 3s - loss: 0.0077 - accuracy: 0.9839 - 3s/epoch - 8ms/step  
333/333 - 3s - loss: 0.0062 - accuracy: 0.9848 - 3s/epoch - 8ms/step  
  
### **Base, 64 CV, 2x2 MP** (11s per epoch)
333/333 - 2s - loss: 0.0069 - accuracy: 0.9788 - 2s/epoch - 7ms/step  
333/333 - 2s - loss: 0.0059 - accuracy: 0.9831 - 2s/epoch - 7ms/step  
333/333 - 2s - loss: 0.0065 - accuracy: 0.9839 - 2s/epoch - 7ms/step  

### **Base, 64 CV, 2x2 MP, no dropout** (11s per epoch)
333/333 - 2s - loss: 0.0043 - accuracy: 0.9875 - 2s/epoch - 7ms/step  
333/333 - 3s - loss: 0.0037 - accuracy: 0.9898 - 3s/epoch - 8ms/step  
333/333 - 2s - loss: 0.0048 - accuracy: 0.9847 - 2s/epoch - 7ms/step  

### **BASE - MP, 64 CV, 2x2 MP** (35s per epoch)
333/333 - 2s - loss: 0.0059 - accuracy: 0.9884 - 2s/epoch - 7ms/step  
333/333 - 3s - loss: 0.0051 - accuracy: 0.9887 - 3s/epoch - 8ms/step  
333/333 - 3s - loss: 0.0040 - accuracy: 0.9905 - 3s/epoch - 8ms/step  

### **Base, 128 CV, 2x2 MP** (13s per epoch)
333/333 - 2s - loss: 0.0053 - accuracy: 0.9838 - 2s/epoch - 5ms/step  
333/333 - 1s - loss: 0.0062 - accuracy: 0.9815 - 1s/epoch - 4ms/step  
333/333 - 2s - loss: 0.0051 - accuracy: 0.9844 - 2s/epoch - 5ms/step  

### **32 CV, 2x2 MP, 128 CV, 2x2 MP** (18s per epoch)
-->test_split 0.2, dropout 0.2, epoch=10  
167/167 - 2s - loss: 0.0022 - accuracy: 0.9940 - 2s/epoch - 9ms/step    
167/167 - 1s - loss: 0.0016 - accuracy: 0.9957 - 1s/epoch - 8ms/step  
167/167 - 2s - loss: 0.0021 - accuracy: 0.9955 - 2s/epoch - 9ms/step  
