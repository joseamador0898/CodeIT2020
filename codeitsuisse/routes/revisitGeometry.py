import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/revisitgeometry', methods=['POST'])
def evaluateRevisitGeometry():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    shapeCoordinates = data.get("shapeCoordinates")
    lineCoordinates = data.get("lineCoordinates")

    listShapeCoordinates = []
    for i in range(len(shapeCoordinates)):
        listShapeCoordinates.append([shapeCoordinates[i].get("x"), shapeCoordinates[i].get("y")])

    listlineCoordinates = []
    for i in range(len(lineCoordinates)):
        listlineCoordinates.append([lineCoordinates[i].get("x"), lineCoordinates[i].get("y")])

    ShapeLines = []
    for i in range(len(listShapeCoordinates)-1):
        ShapeLines.append(line([listShapeCoordinates[i][0],listShapeCoordinates[i][1]], [listShapeCoordinates[i+1][0],listShapeCoordinates[i+1][1]]))
    ShapeLines.append(line([listShapeCoordinates[len(listShapeCoordinates)-1][0], listShapeCoordinates[len(listShapeCoordinates)-1][1]],
                           [listShapeCoordinates[0][0], listShapeCoordinates[0][1]]))

    linesLines = []
    for i in range(len(listlineCoordinates)-1):
        linesLines.append(line([listlineCoordinates[i][0],listlineCoordinates[i][1]], [listlineCoordinates[i+1][0],listlineCoordinates[i+1][1]]))

    Intersections = []
    for i in range(len(ShapeLines)):
        for j in range(len(linesLines)):
            R = intersection(ShapeLines[i], linesLines[j])
            if R:
                Intersections.append(R)
                print("Intersection detected:", R)
            else:
                print("No single intersection point detected")

    firstcoord = listShapeCoordinates[0]
    listShapeCoordinates.append(firstcoord)
    IntersectionsResults = []
    for j in Intersections:
        for i in range(len(listShapeCoordinates) - 1):
            if (min(listShapeCoordinates[i][0], listShapeCoordinates[i + 1][0]) <= j[0] <= max(listShapeCoordinates[i][0], listShapeCoordinates[i + 1][0]) and
                    min(listShapeCoordinates[i][1], listShapeCoordinates[i + 1][1]) <= j[1] <= max(
                        listShapeCoordinates[i][1], listShapeCoordinates[i + 1][1])):
                IntersectionsResults.append(j)
                break

    print(IntersectionsResults)
    result = []
    for inters in IntersectionsResults:
        result.append({"x" : inters[0], "y": inters[1]})
    logging.info("My result :{}".format(result))
    return json.dumps(result)



def line(p1, p2):
    A = (p1[1] - p2[1])
    B = (p2[0] - p1[0])
    C = (p1[0]*p2[1] - p2[0]*p1[1])
    return A, B, -C

def intersection(L1, L2):
    D  = L1[0] * L2[1] - L1[1] * L2[0]
    Dx = L1[2] * L2[1] - L1[1] * L2[2]
    Dy = L1[0] * L2[2] - L1[2] * L2[0]
    if D != 0:
        x = Dx / D
        y = Dy / D
        return x,y
    else:
        return False





