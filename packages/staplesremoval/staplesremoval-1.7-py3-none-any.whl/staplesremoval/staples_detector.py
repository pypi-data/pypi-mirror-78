import skimage
from enum import Enum
from skimage.color import rgb2hsv
from skimage import morphology
from typing import Tuple
import numpy
import scipy


class GradientMode(Enum):
    VERTICAL_GRADIENT = 0
    HORIZONTAL_GRADIENT = 1
    COMBINED_GRADIENT = 2


def generate_mask(image: numpy.ndarray) -> Tuple[numpy.ndarray, numpy.ndarray]:
    """
    Computes the mask and the colormask using the vertical gradient, with four final dilations.

    Args:
        image: An RGB image.

    Returns:
        An RGB image with the mask overlapped and the binary mask.
    """
    return generate_mask_with_configuration(image, GradientMode.VERTICAL_GRADIENT, 4)


def generate_mask_with_configuration(image: numpy.ndarray,
                                     gradient_mode: GradientMode,
                                     number_dilations: int) -> Tuple[numpy.ndarray, numpy.ndarray]:
    """
    Computes the mask using the gradient method.

    Args:
      image: An RGB image.
      gradient_mode: A GradientMode value, representing the gradient to be computed.
      number_dilations: An integer, representing the number of dilations.

    Returns:
      An RGB image with the mask overlapped and the binary mask.
    """
    hsv_image = convert_image_to_HSV(image)
    v_channel = get_V_channel(hsv_image)

    if gradient_mode == GradientMode.VERTICAL_GRADIENT:
        gradient_vertical = calculate_sobel_vertical_gradient(v_channel)

        return calculate_staple_process(original_image=image,
                                        gradient=gradient_vertical,
                                        number_dilations=number_dilations)
    elif gradient_mode == GradientMode.HORIZONTAL_GRADIENT:
        gradient_horizontal = calculate_sobel_horizontal_gradient(v_channel)

        return calculate_staple_process(original_image=image,
                                        gradient=gradient_horizontal,
                                        number_dilations=number_dilations)
    elif gradient_mode == GradientMode.COMBINED_GRADIENT:
        gradient_vertical = calculate_sobel_vertical_gradient(v_channel)
        gradient_horizontal = calculate_sobel_horizontal_gradient(v_channel)

        vertical_colormask, vertical_mask = calculate_staple_process(original_image=image,
                                                                     gradient=gradient_horizontal,
                                                                     number_dilations=number_dilations)
        horizontal_colormask, horizontal_mask = calculate_staple_process(original_image=image,
                                                                         gradient=gradient_vertical,
                                                                         number_dilations=number_dilations)

        final_mask = vertical_mask | horizontal_mask

        return get_drawn_mask(image, final_mask), final_mask


def calculate_staple_process(original_image: numpy.ndarray,
                             gradient: numpy.ndarray,
                             number_dilations: int) -> Tuple[numpy.ndarray, numpy.ndarray]:
    BY = binarize_image(gradient, 60 / 255)

    se = numpy.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]])
    C = morphological_closing(BY, se)

    holes = fill_small_holes(C)
    filtered = remove_small_objects(holes, 50)

    dilated_mask = filtered
    for _ in range(number_dilations):
        dilated_mask = dilate_mask(dilated_mask, se)
    colormask = get_drawn_mask(original_image, dilated_mask)

    return colormask, dilated_mask


def convert_image_to_HSV(image):
    """
    Converts the image from RGB to HSV color space.

    Args:
      image: An RGB image.
    Returns:
      An HSV image.
    """
    return (rgb2hsv(image))


def get_V_channel(hsvImage):
    """Gets the V channel.

    Args:
      hsvImage: An HSV image.
    Returns:
      The first channel (H) of the hsvImage.
    """
    return (hsvImage[:, :, 2])


def calculate_sobel_vertical_gradient(image):
    """
    Computes the Sobel gradient in the vertical direction

    Args:
      image: An RGB image.
    Returns:
      The grayscale image containing the Sobel gradient.
    """
    ky = numpy.array([[1, 2, 1],
                      [0, 0, 0],
                      [-1, -2, -1]])
    return scipy.ndimage.convolve(image, ky)


def calculate_sobel_horizontal_gradient(image):
    """
    Computes the Sobel gradient in the horizontal direction

    Args:
      image: An RGB image.
    Returns:
      The grayscale image containing the Sobel gradient.
    """
    kx = numpy.array([[-1, 0, 1],
                      [-2, 0, 2],
                      [-1, 0, 1]])
    return scipy.ndimage.convolve(image, kx)


def binarize_image(image, threshold):
    """Binarizes an image given threshold.

    Args:
      image: A grayscale image.
      threshold: A real number in the interval [0,1].
    Returns:
      Binary image.
    """
    binary = image.copy()
    binary[binary > threshold] = 1
    binary[binary <= threshold] = 0

    return binary


def morphological_closing(image, structuring_element):
    """Computes the binary morphological closing.

    Args:
      image: A binary image.
      structuring_element: A structuring element.
    Returns:
      A binary image.
    """
    return (skimage.morphology.binary_closing(image,
                                              structuring_element))


def fill_small_holes(image):
    """Computes the hole filling.

    Args:
      image: A binary image.
    Returns:
      A binary image without holes.
    """
    return (scipy.ndimage.morphology.binary_fill_holes(image))


def remove_small_objects(image, area):
    """Removes the small objects in a binary image whose area is
    less than a given area.

    Args:
      image: A binary image.
      area: An integer.
    Returns:
      A binary image without small objects.
    """
    return (skimage.morphology.remove_small_objects(image, area))


def dilate_mask(mask, structuring_element):
    """Computes the binary morphological dilation.

    Args:
      mask: A binary image.
      structuring_element: A structuring element.
    Returns:
      A binary image.
    """
    return (skimage.morphology.binary_dilation(mask,
                                               structuring_element))


def get_drawn_mask(image, mask):
    """Computes the image with the mask overlapped.

    Args:
      image: An RGB image.
      mask: A binary image.
    Returns:
      An RGB image with the mask drawn with different color.
    """
    colormask = image.copy()

    colormask[mask[:, :] == True] = [70 / 255, 253 / 255, 52 / 255]

    return colormask
