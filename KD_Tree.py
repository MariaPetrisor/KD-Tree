#!/usr/bin/python2.7

'''
    File name: KD_Tree.py 
    Author: Maria Petrisor
    Date created: 09/06/2018
    Python Version: 2.7
'''


import math
import sys

# Every node has a name, a corresponding set of points, a threshold on which the 
# branch was made and left and right node (constructed on the division of the previous
# points set)
class Node:
    def __init__(self, name, points_set, threshold, left, right):
        self.name = name
        self.points_set = points_set
        self.threshold = threshold
        self.left = left
        self.right = right

# The distance between two points
def distance(point1, point2):
    return math.sqrt((point1[1] - point2[1])**2 + (point1[2] - point2[2])**2)

# Find the nearest point in the points set of a node regarding a target point
def get_nearest_point(target, node):
    points_set = node.points_set
    min_distance = sys.maxint
    for entry in points_set:
        if distance(target, entry) < min_distance:
            min_distance = distance(target, entry)

    return min_distance

# Traverse the k-d tree in order to find the nearest node to the target point
def find_nearest(node, target, depth=1):
    print "Chose ", node.points_set

    axis = depth % 2 + 1
    
    # Return the nearest point when it is the leaf
    if node.left == None and node.right == None:
        return node.points_set

    if axis == 1:
        orientation = "Width"
    else:
        orientation = "Height"
    print "{} > {}? NO: {} YES: {}".format(orientation, node.threshold, node.left.points_set, node.right.points_set)

    # Compare the target, in the axis of comparison, against the current node's threshold
    # The result determines the likely set
    if(target[axis] > node.threshold):
        likely_node = node.right
        unlikely_node = node.left
    else:
        likely_node = node.left
        unlikely_node = node.right
    
    # Find the nearest neighbor in the likely set
    likely_set_min = get_nearest_point(target, likely_node)
    distance_to_boundary = abs(target[axis] - node.threshold)


    # Determine whether the distance to the nearest neighbor in the likely set is less than or equal to the 
    # distance to the other set's boundary in the axis of comparison
    if likely_set_min <= distance_to_boundary:
        return find_nearest(likely_node, target, depth + 1)
    else:
        unlikely_set_min = get_nearest_point(target, unlikely_node)
        # If it is, report the nearest neighbor in the likely set
        if likely_set_min <= unlikely_set_min:
            return find_nearest(likely_node, target, depth + 1)
        # If not, check the unlikely and return the nearer of the neighbors in the likely set and unlikely set
        else:
            return find_nearest(unlikely_node, target, depth + 1)

# KD tree generation. Depth starts at 1 since we want to start with the vertical axis
def generateKD(points, depth = 1):
    
    # If there is only one case, stop
    if len(points) == 1:
        return Node(points[0][0], points, 0, None, None)

    # Start the devision with the vertical axis, afterwards pick them successively 
    # Add 1 because the first element of the tuple is the name, then the coordinates
    axis = depth % 2 + 1;

    # Sort the points depending on the selected axis in order to divide it
    points.sort(key=lambda x: x[axis])

    # Split the set in the middle, branching the tree
    middle = len(points)/2

    # The median between the two separated sets
    threshold = (points[middle][axis] + points[middle - 1][axis])/float(2)

    # Prepare for the new branch
    node = Node(points[middle][0], points, threshold, None, None)

    # Left side is the first half of the previous set.
    node.left = generateKD(points[0:middle], depth + 1)

    # Right side is the second half of the previous set.
    node.right = generateKD(points[middle:], depth + 1)

    return node

if __name__ == "__main__":

    # Points to be grouped into the k-d tree. Unknown point will be at (1, 4)
    points = [("Red", 2, 6),
              ("Yellow", 5, 6),
              ("Orange", 2, 5),
              ("Purple", 6, 5),
              ("Red", 1, 2),
              ("Blue", 4, 2),
              ("Violet", 2, 1),
              ("Green", 6, 1)
              ]

    # Generate the k-d tree
    root = generateKD(points)

    # Finding the nearest node to the unknown one in order to guess its color
    unknown_color_point = ("Unknown", 1, 4)
    print find_nearest(root, unknown_color_point)
