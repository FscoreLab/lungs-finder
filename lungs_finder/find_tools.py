from . import haar_finder
from . import hog_finder
from . import lbp_finder


def find_max_rectangle(rectangles):
    max_rectangle = None
    max_area = 0

    for rectangle in rectangles:
        x, y, width, height = rectangle
        area = width * height

        if area > max_area:
            max_area = area
            max_rectangle = rectangle

    return max_rectangle

def square_bbox(image, x, y, width, height):
    max_dim = max(width, height)
    if image.shape[0] < max_dim:
        print('Image too narrow to squarize')
        return x, y, width, height
    if image.shape[1] < max_dim:
        print('Image too short to squarize')
        return x, y, width, height

    d_width, d_height = max_dim - width, max_dim - height
    half_dw, half_dh = d_width//2, d_height//2
    x_n, y_n, width_n, height_n = x - half_dw, y - half_dh, max_dim, max_dim
    if x_n < 0:
        x_n = 0
    if y_n < 0:
        y_n = 0
    if x_n + width_n > image.shape[1]:
        x_n = image.shape[1] - width_n
    if y_n + height_n > image.shape[0]:
        y_n = image.shape[0] - height_n
    return x_n, y_n, width_n, height_n

def get_lungs(image, padding=15, return_image=True, square=False):
    right_lung = hog_finder.find_right_lung_hog(image)
    left_lung = hog_finder.find_left_lung_hog(image)

    if right_lung is not None and left_lung is not None:
        x_right, y_right, width_right, height_right = right_lung
        x_left, y_left, width_left, height_left = left_lung

        if abs(x_right - x_left) < min(width_right, width_left):
            right_lung = lbp_finder.find_right_lung_lbp(image)
            left_lung = lbp_finder.find_left_lung_lbp(image)

    if right_lung is None:
        right_lung = haar_finder.find_right_lung_haar(image)

    if left_lung is None:
        left_lung = haar_finder.find_left_lung_haar(image)

    if right_lung is None:
        right_lung = lbp_finder.find_right_lung_lbp(image)

    if left_lung is None:
        left_lung = lbp_finder.find_left_lung_lbp(image)

    if right_lung is None and left_lung is None:
        return None
    elif right_lung is None:
        x, y, width, height = left_lung
        spine = width / 5
        right_lung = int(x - width - spine), y, width, height
    elif left_lung is None:
        x, y, width, height = right_lung
        spine = width / 5
        left_lung = int(x + width + spine), y, width, height

    x_right, y_right, _, height_right = right_lung
    x_left, y_left, width_left, height_left = left_lung
    x_right -= padding
    y_right -= padding
    height_right += padding * 2
    y_left -= padding
    width_left += padding
    height_left += padding * 2

    if x_right < 0:
        x_right = 0

    if y_right < 0:
        y_right = 0

    if x_left < 0:
        x_left = 0

    if y_left < 0:
        y_left = 0

    if y_right + height_right > image.shape[0]:
        height_right = image.shape[0] - y_right

    if x_left + width_left > image.shape[1]:
        width_left = image.shape[1] - x_left

    if y_left + height_left > image.shape[0]:
        height_left = image.shape[0] - y_left

    top_y = min(y_right, y_left)
    bottom_y = max(y_right + height_right, y_left + height_left)
    x, y, width, height = x_right, top_y, x_left + width_left - x_right, bottom_y - top_y

    if square:
        x, y, width, height = square_bbox(image, x, y, width, height)

    if return_image:
        return image[y:y+height, x:x+width]
    else:
        return (x, y, width, height)
