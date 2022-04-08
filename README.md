# Interactive Graph Cuts for Object Segmentation
This Repository implements an Interactive Graph Cuts Model for binary image segmentation whose optimal parameters are found with the metohod described in the [Paper](https://www.csd.uwo.ca/~yboykov/Papers/iccv01.pdf). 

# Problem Description:

Assume one got a markov network with a corresponding energy function to classify an image into "object" and "background" segments. Finding an optimal constellation of the parameters of the markov network is np-hard.

# Solution:

One builds an corresponding (s,t)-graph such that for every parameter in the energy function there is exactly one corresponding node in the (s,t)-graph. Since for every parameter configuration in the energy function (assignment of all pixels to either object or background) there exists one corresponding (s,t)-cut with every node either belonging to set s or t and vice versa one can say that if the value of any parameter configuration equals the value of the corresponding cut, then finding the minimum (s,t)-cut will be equal to finding the optimal parameter configuration.


# How does the cut value of the (s,t)-graph equal the value of the energy function ?

For visualizing we represent the energy function as the following markov network. It and its corresponding (s,t)-graph can be visualized as follows:

![image](https://user-images.githubusercontent.com/101547425/160617011-2a1a9ef8-b45d-414e-aab9-4958011e4bf2.png)

The markov network consits of "parameter nodes" (blue), whose optimal constellation for the minimum energy must be found. For every pixel in the image there is a parameter node which gets assigned either the value background or foregorund. Every parameter node has an edge to its neighboring parameter node. These edges is then assigned some estimator value for that two nodes (pixels) belonging to the same class.

Also every parameter node is connected to one "class node" (orange), which value is fixed. The weight of this edge corresponds to some measurement that the assignment of the parameter node is correct (based on class properties). The sum of all edges is then the energy of the model.

In the (s,t)-graph every pixel in the image also got a corresponding node, which we will call pixel node. Later, the assignment of this node to either set s or t will correspond to a assignment of the value foreground or background of the corresponding pixel. Also every parameter node in the (s,t)-graph is connected to the two terminal nodes, s and t.

Lets now create an energy function for the described markov network such that we can represent it as (s,t)-graph 

(1) Sum of energy from edges between parameter nodes and class nodes must be equal to the capacity of terminal cuts in the (s,t)-graph 

Assume the assignment of a parameter node yields to some energy between it and its class node. In the (s,t)-graph one can then assign the edge between a pixel node and a terminal node a corresponding capacity, such that the cut of this edge would have the same cost as assigning the node to the opposite terminal. Since one needs to cut exactly one terminal node from each pixel node, these terms will then be equal.

(2) Sum of energy between parameter nodes must be equal to the sum of non-terminal cuts in the (s,t)-graph 

Fo this we must chose the energy between two parameter nodes in the markov network to be zero when theys have the same assignment {foreground or background}, so the edge increases the energy of the markov network if and only if two neighboring nodes are assigned to different classes. The edge value of two neigbooured pixel-nodes is only included in the cut if these two are assigned to a different (s,t)-set (class). So if two parameter nodes in the markov network have a different assignment one can chose any energy value and then set the value in the (s,t)-graph to the same value.  

(for a more rigorous proof see the paper)

# Results:
We created directly the (s,t)-graph of an energy function and then found the optimal parameter configuration of it with the min (s,t)-cut of the graph.

For the capacity between two non-terminal nodes we computed a measurement of how good these two fit to each other.
We use the function:  α*(-1.5*math.log(diff)+10)  

Diff is the squared distance between the two pixels. We took it because it is exponentially decreasing, so the capacity between to very similar pixel is very high. Its max value is (nearly) equal to the max. terminal-capacity (with α=1).

Also we set the max value of diff to 780, so that the formula can t have negative values and we set its min value to some very small number (such that term can t be zero). 

Finally we use α to synchronize this term with the capacity between to non-terminal-edges.

For the capacity between a terminal and non-terminal node we used a probability measurement of how likely it is that a pixel belongs to the opposite  terminal, which works only for integer-pixel values. Also every click from the user selects 21*21 Pixel as seed, so this likelihood can be computed more accurately. We clicked three times on each for- and background for this results.

Results (α=1):

![image](https://user-images.githubusercontent.com/101547425/160604450-813bc513-74e1-47eb-9152-5a97a33ee56f.png)

![image](https://user-images.githubusercontent.com/101547425/160655269-d7086180-6a85-4f4d-9447-494a917a4480.png)

![image](https://user-images.githubusercontent.com/101547425/160605628-28a6c29f-f6fb-4c61-99a1-493ae4514041.png)

![image](https://user-images.githubusercontent.com/101547425/160606245-7b86fc7a-6cc2-4c3a-a512-0ef5bb968635.png)

![image](https://user-images.githubusercontent.com/101547425/160606643-018cdb61-3338-4553-8b38-653d92022350.png)




