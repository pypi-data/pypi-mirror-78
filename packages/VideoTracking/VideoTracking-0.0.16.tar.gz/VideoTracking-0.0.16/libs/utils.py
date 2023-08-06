from libs.shape import Shape
from PyQt5.QtCore import QPointF


def shape2box(shape):
    shape_xmax = 0
    shape_xmin = 99999
    shape_ymax = 0
    shape_ymin = 99999
    for p in shape.points:
        if shape_xmax < p.x():
            shape_xmax = p.x()
        if shape_ymax < p.y():
            shape_ymax = p.y()
        if shape_xmin > p.x():
            shape_xmin = p.x()
        if shape_ymin > p.y():
            shape_ymin = p.y()
    return (shape_xmin, shape_ymin, shape_xmax - shape_xmin, shape_ymax - shape_ymin)


def box2shape(box, label):
    shape = Shape(label=label)
    shape.addPoint(QPointF(box[0], box[1]))
    shape.addPoint(QPointF(box[0]+box[2], box[1]))
    shape.addPoint(QPointF(box[0]+box[2], box[1]+box[3]))
    shape.addPoint(QPointF(box[0], box[1]+box[3]))
    shape._closed=True
    return shape


def IOU(boxA, boxB):
    # print(boxA, boxB)
    boxA_xmax = 0
    boxA_xmin = 99999
    boxA_ymax = 0
    boxA_ymin = 99999
    boxB_xmax = 0
    boxB_xmin = 99999
    boxB_ymax = 0
    boxB_ymin = 99999
    for p in boxA:
        if boxA_xmax < p.x():
            boxA_xmax = p.x()
        if boxA_ymax < p.y():
            boxA_ymax = p.y()
        if boxA_xmin > p.x():
            boxA_xmin = p.x()
        if boxA_ymin > p.y():
            boxA_ymin = p.y()

    for p in boxB:
        if boxB_xmax < p.x():
            boxB_xmax = p.x()
        if boxB_ymax < p.y():
            boxB_ymax = p.y()
        if boxB_xmin > p.x():
            boxB_xmin = p.x()
        if boxB_ymin > p.y():
            boxB_ymin = p.y()
    A = (boxA_xmax - boxA_xmin) * (boxA_ymax - boxA_ymin)
    B = (boxB_xmax - boxB_xmin) * (boxB_ymax - boxB_ymin)
    boxI_xmax = min(boxA_xmax, boxB_xmax)
    boxI_xmin = max(boxA_xmin, boxB_xmin)
    boxI_ymax = min(boxA_ymax, boxB_ymax)
    boxI_ymin = max(boxA_ymin, boxB_ymin)
    I = (boxI_xmax - boxI_xmin) * (boxI_ymax - boxI_ymin)
    return I/(A+B-I)

