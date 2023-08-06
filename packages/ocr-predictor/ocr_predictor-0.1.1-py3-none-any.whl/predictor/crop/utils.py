import math
import time
import numpy as np
import cv2
from imutils.perspective import order_points

def top_left(coords):
    coords = [(x, y, i) for i, (x, y) in enumerate(coords)]
    pts = np.asarray(coords)
    
    xSorted = pts[np.argsort(pts[:, 0]), :]

    # grab the left-most and right-most points from the sorted
    # x-roodinate points
    leftMost = xSorted[:2, :]
    rightMost = xSorted[2:, :]

    # now, sort the left-most coordinates according to their
    # y-coordinates so we can grab the top-left and bottom-left
    # points, respectively
    leftMost = leftMost[np.argsort(leftMost[:, 1]), :]
    (tl, bl) = leftMost
    return tl

def four_point_transform(image, pts):
    # obtain a consistent order of the points and unpack them
    # individually
    rect = pts
    (tl, tr, br, bl) = rect
    
    # compute the width of the new image, which will be the
    # maximum distance between bottom-right and bottom-left
    # x-coordiates or the top-right and top-left x-coordinates
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    # compute the height of the new image, which will be the
    # maximum distance between the top-right and bottom-right
    # y-coordinates or the top-left and bottom-left y-coordinates
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))

    # now that we have the dimensions of the new image, construct
    # the set of destination points to obtain a "birds eye view",
    # (i.e. top-down view) of the image, again specifying points
    # in the top-left, top-right, bottom-right, and bottom-left
    # order
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")
    
    # compute the perspective transform matrix and then apply it
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

    # return the warped image
    return warped


def distance(p1, p2):
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    d = math.sqrt(dx**2 + dy**2)
    return d

def perpendicular_distance(p, p1, p2):    
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    d = math.sqrt(dx**2 + dy**2)
    
    if d==0:
        return distance(p, p1)
        
    return abs(p[0] * dy - p[1] * dx + p2[0] * p1[1] - p2[1] * p1[0])/d

def simplifyDouglasPeucker(points, pointsToKeep, isclose):
    if isclose:
        points = points + [points[0]]
        
    length = len(points)    
    weights = [0]*length
    
    def douglasPeucker(start, end):
        if (end > start + 1):
            maxDist = -1
            maxDistIndex = 0            
            for i in range(start + 1, end):                
                dist = perpendicular_distance(points[i], points[start], points[end])
                if dist > maxDist:
                    maxDist = dist
                    maxDistIndex = i

            weights[maxDistIndex] = maxDist

            douglasPeucker(start, maxDistIndex)
            douglasPeucker(maxDistIndex, end)

    douglasPeucker(0, length - 1)
    weights[0] = float("inf")
    weights[-1] = float("inf")
    weightsDescending = weights
    weightsDescending = sorted(weightsDescending, reverse=True)
    maxTolerance = weightsDescending[pointsToKeep - 1]
    result = [
        point for i, point in enumerate(points) if weights[i] >= maxTolerance
    ]

    return result

def crop(im, mask, order):
    mask = mask*255
    mask = np.uint8(mask)

    contours, hierarchy = cv2.findContours(mask, cv2.RETR_CCOMP, cv2.cv2.CHAIN_APPROX_SIMPLE)

    largestcnt = max(contours, key = lambda x: cv2.arcLength(x, True))
    epsilon = 0.01*cv2.arcLength(largestcnt, True)
    approx = cv2.approxPolyDP(largestcnt, epsilon, True)

    approx = simplifyDouglasPeucker(approx.squeeze(1).tolist() , 5, isclose=True)[:-1]
    approx = np.asarray(approx)

    order_pts = order_points(approx)
    order_pts = order_pts.tolist()
    order_pts = order_pts[-order:] + order_pts[:-order]

    crop_img = four_point_transform(im, np.asarray(order_pts, dtype='float32')) 

    return crop_img
