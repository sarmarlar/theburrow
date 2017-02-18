# CS 121: Drawing TreeMaps
# Sarah Larson

import sys
import csv
import json

from drawing import ChiCanvas, ColorKey


MIN_RECT_SIDE=0.01
MIN_RECT_SIDE_FOR_TEXT=0.03
X_SCALE_FACTOR=12
Y_SCALE_FACTOR=10


def get_weight(t):
    '''
    Sets the weights of each nodes in tree t as the sum of its children's weights. 
    Inputs: t (a tree)
    Returns: weighted tree 
    '''

    kids = t.get_children_as_list()

    if kids:
        for kid in kids: 
            t.weight += get_weight(kid)
    return t.weight


def get_partitions(t, parent_rect, is_vertical):
    '''
    Partition the parent rectangle according to the weight of its children, alternating orientation. 

    Inputs:
        t: a tree
        is_vertical: boolean value to determine if the partitions are to be oriented vertically or horizontally.
                     If True, cut parent vertically
                     If False, cut parent horizontally 
        parent-rect: a tuple representing the parent rectangle (x-coordinate, y-coordinate, height, width, code, label)

    Returns: 
        rectangles_list: list of partitioned rectangles as tuples (x-coordinate, y-coordinate, height, width, code, label)
    '''

    kids = t.get_children_as_list()
    rectangles_list = []

    if not kids:
        return [parent_rect]

    (xpos, ypos, pw, ph, _ , _) = parent_rect

    if is_vertical:  


            for kid in kids:

                w = (kid.weight / t.weight) * pw
                kid_rect = (xpos, ypos, w, ph, kid.code, kid.label)
                rectangles_list += get_partitions(kid, kid_rect, False)

                xpos += w

            return rectangles_list


    else: #partition horizontally 


            for kid in kids:

                h = (kid.weight / t.weight) * ph
                kid_rect = (xpos, ypos, pw, h, kid.code, kid.label)
                rectangles_list += get_partitions(kid, kid_rect, True)

                ypos += h

            return rectangles_list


def list_relevant_codes(t):
    '''
    Genreates list containing the code for each leaf in the tree.  
    
    Inputs: t (a tree)
    
    Returns: codes: list of leaf codes. 
    '''

    codes = []
    kids = t.get_children_as_list()

    if not kids: 
        return [t.code]

    if kids:
        for kid in kids:
            codes += list_relevant_codes(kid)

    return codes

    
def draw_treemap(t, 
                 bounding_rec_height=1.0,
                 bounding_rec_width=1.0,
                 output_filename=None):

    '''
    Draw a treemap and the associated color key

    Inputs:
        t: a tree

        bounding_rec_height: the height of the bounding rectangle.

        bounding_rec_width: the width of the bounding rectangle.

        output_filename: (string or None) the name of a file for
        storing a the image or None, if the image should be shown.
    '''

    ### START: DO NOT CHANGE THIS CODE ###
    c = ChiCanvas(X_SCALE_FACTOR, Y_SCALE_FACTOR)

    # define coordinates for the initial rectangle for the treemap
    x_origin_init_rect = 0
    y_origin_init_rect = 0
    height_init_rect = bounding_rec_height
    width_init_rect = bounding_rec_width

    ### END: DO NOT CHANGE THIS CODE ###
    assert t is not None

    get_weight(t)

    ck = ColorKey(list_relevant_codes(t))

    intital_parent = (x_origin_init_rect, y_origin_init_rect, width_init_rect, height_init_rect, t.code, t.label)
    rectangles_list = get_partitions(t, intital_parent, True)

    for rect in rectangles_list:

        print("rectangle: ", rect)
        x0 = rect[0]
        y0 = rect[1]
        w = rect[2]
        h = rect[3]
        code = rect[4]
        label = rect[5]

        c.draw_rectangle(x0, y0, x0+w, y0+h, fill=ck.get_color(code)) 

        print("label: ", label)

        if w >= MIN_RECT_SIDE_FOR_TEXT and h >= MIN_RECT_SIDE_FOR_TEXT:
            if w >= h:
                c.draw_text(x0+w/2.0, y0+h/2.0, w*0.85, str(label), fg="black")
            else:
                c.draw_text_vertical(x0+w/2.0, y0+h/2.0, h*0.95, str(label), fg="black")


    ### START: DO NOT CHANGE THIS CODE ###
    # save or show the result.
    if output_filename:
        print("saving...", output_filename)
        c.savefig(output_filename)
    else:
        c.show()
    ### END: DO NOT CHANGE THIS CODE ###




