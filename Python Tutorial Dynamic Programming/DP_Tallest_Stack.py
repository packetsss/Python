"""
Given a set of boxes with dimension (l, w, h) and find the tallest stack possible, length and width of the top box must
be smaller than the bottom box

- We find the base boxes first by sorting them by length/width

"""


def tallestStack(boxes):
    def canBeStacked(top, bottom):
        return top[0] < bottom[0] and top[1] < bottom[1]

    boxes.sort(key=lambda x: x[0])
    print(boxes)
    # sort the boxes by length first

    heights = {box: box[2] for box in boxes}
    print(heights)
    # use tuple (full dimension) as keys and height as value

    for i in range(1, len(boxes)):
        box = boxes[i]
        S = [boxes[j] for j in range(i) if canBeStacked(boxes[j], box)]
        print(S)
        # Checking each boxes that if boxes before it can stack on top of it
        # If possible, add the dimension tuple to the list

        heights[box] = box[2] + max([heights[box] for box in S], default=0)
        # Looking at the height of the current box and add the maximum height of whatever sub-box it has

    return max(heights.values())
    # return the maximum height


print(tallestStack([(4, 5, 3), (2, 3, 2), (3, 6, 2), (1, 5, 4), (2, 4, 1), (1, 2, 2)]))
