#region imports
from PIL import Image
import glob
import numpy as np
from ImageSegmentationGUI import Chose_initial_values_image_segmantation
import maxflow
import math
#endregion


''' How to use:
(1) Select path for input image
(2) Run File 
(3) The image will open, then you can select with every click on the image a small area (21*21 pixel)
which belongs to the foreground. After clicked atleast one time, close the image. 
(4) The image will open, then you can select with every click on the image a small area (21*21 pixel)
which belongs to the background. After clicked atleast one time, close the image. 
(5) See the resulting segmentation 
'''

#region load Image
path = '' #YourPath
image=Image.open(path).convert('L')
#Select seeds for background and foreground
image, pixels_object,pixels_object_indexes = Chose_initial_values_image_segmantation(image)
image,pixels_background,pixels_background_indexes = Chose_initial_values_image_segmantation(image)
image_np = np.array(image,dtype=np.int32)
#endregion

'''
This region creates a list with 256 entrys, one belonging to the (procentual) appearence of each pixel value 
in the seed values. The 'get_prob_value_from_list' function then calculates a score for any value belonging to a
class based on this list 
'''
#region Create Params for graph
def get_measurement_for_value_fitting_to_list(val,list):
    start = max(0,val-9)
    end = min(255,val+9)
    prob = 0
    fac = 1
    for i in range(start,end+1):
        fac = 1 - abs(val-i)/10
        prob += list[i]*fac
    return prob
object_num_vals = len(pixels_object)
unique, counts = np.unique(pixels_object, return_counts=True)
prob_object_dict = {}
for i in range(0,len(unique)):
    prob_object_dict[unique[i]]=counts[i]/object_num_vals
background_num_vals = len(pixels_object)
unique, counts = np.unique(pixels_background, return_counts=True)
prob_background_dict = {}
for i in range(0,len(unique)):
    prob_background_dict[unique[i]]=counts[i]/object_num_vals
#Create List of values
object_vals = []
for i in range(0,256):
    val = prob_object_dict[i] if i in prob_object_dict.keys() else 0
    object_vals.append(val)
background_vals = []
for i in range(0,256):
    val = prob_background_dict[i] if i in prob_background_dict.keys() else 0
    background_vals.append(val)
#endregion


'''
This region creates the (s,t)-graph with the maxflow library and then finds its min-cut using the library tools.
After finding the min cut, it shows the image segmentation represented through the cut 
'''
#region segment graph and create image
def segment_image(alpha):

    image_rows = image_np.shape[0]
    image_columns = image_np.shape[1]
    image_size = image_rows * image_columns
    graph = maxflow.Graph[float](0, 0)
    nodes = graph.add_nodes(image_size)
    delta = 0.000001
    #create node and edges for every pixel in the image
    for r in range(0, image_rows):
        for c in range(0, image_columns):
            #mapping from row and column to node id in graph
            current_node = r * image_columns + c
            right_node = current_node + 1
            lower_node = current_node + image_columns
            pixel_value = image_np[r, c]
            # create edges to right node
            if (c + 1 < image_columns):
                diff = (pixel_value - image_np[r, c + 1])**2
                diff = max(diff,0.000001)
                # weight formula for neighbouring edges
                weight =alpha * ( -1.5*math.log(diff+delta)+10)
                graph.add_edge(nodes[current_node], nodes[right_node], weight, weight)
            # create edges to lower node
            if (r + 1 < image_rows):
                diff =  (pixel_value - image_np[r + 1, c])**2
                diff = max(diff,0.000001)
                #weight formula for neighbouring edges
                weight = alpha *(-1.5*math.log(diff)+10)
                graph.add_edge(nodes[current_node], nodes[lower_node], weight, weight)

            # Create edges to terminals
            #Use created list to get some measurement of the node to belonging to one class
            measure_foreground = get_measurement_for_value_fitting_to_list(pixel_value, object_vals)
            measure_background = get_measurement_for_value_fitting_to_list(pixel_value, background_vals)
            measure_foreground = max(measure_foreground, 0.0001)
            measure_background = max(measure_background, 0.0001)
            # S is foreground terminal
            weight_s = -math.log(measure_background)
            # T is background terminal
            weight_t = -math.log(measure_foreground)
            graph.add_tedge(nodes[current_node], weight_s, weight_t)

    #now we change the weights of the seed pixels so that they will certainly belong to the correct class

    # change edges from selected foreground pixels
    for i in range(0, len(pixels_object_indexes)):
        row = pixels_object_indexes[i, 0]
        col = pixels_object_indexes[i, 1]
        node_index = row * image_columns + col
        graph.add_tedge(nodes[node_index], 41, 0)
    # change edges from selected background pixels
    for i in range(0, len(pixels_background_indexes)):
        row = pixels_background_indexes[i, 0]
        col = pixels_background_indexes[i, 1]
        node_index = row * image_columns + col
        graph.add_tedge(nodes[node_index], 0, 41)

    #calculate min (s,t)-cut and show corresponding image
    flow = graph.maxflow()
    recovered_image = np.zeros(shape=(image_rows, image_columns), dtype=np.uint8)
    # create segmented image from s,t class
    for r in range(0, image_rows):
        for c in range(0, image_columns):
            current_node = r * image_columns + c
            # segment one ore white means background
            recovered_image[r, c] = graph.get_segment(nodes[current_node]) * 255

    Image.fromarray(recovered_image).show()

'''
This Region runs the method to segment an image given the seeds 
'''
#segment the image with given seeds
segment_image(alpha=1)
