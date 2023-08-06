from imageObjects.ContourObject import ContourObject
from matplotlib import pyplot as plt
import numpy as np
import cv2
import sys


class ImageObject:
    """
    This creates an object from a cv2 compatible image which can then create new images from itself, or update itself by
    its inherent methods.
    """
    def __init__(self, image):
        self.image = image

    def __repr__(self):
        """
        Return for debug
        """
        return f"{self.image.shape}"

    def __str__(self):
        """
        Clearer message of what the current instance contains
        """
        if self.channels < 3:
            channels_type = "Mono"
        else:
            channels_type = "Colour"

        return f"Height: {self.height}\nWidth: {self.width}\nType: {channels_type}\nChannels: {self.channels}"

    def __copy__(self):
        """
        Allow duplication of instance
        """
        return ImageObject(self.image.copy())

    @property
    def height(self):
        """
        The height of the image in pixels
        """
        return self.image.shape[0]

    @property
    def width(self):
        """
        The width of the image in pixels
        """
        return self.image.shape[1]

    def pixel_total(self):
        """
        Total number of pixels in the image
        """
        return self.width * self.height

    @property
    def channels(self):
        """
        The number of channels of colour data that exist in the image
        """
        if len(self.image.shape) < 3:
            return 1
        else:
            return self.image.shape[2]

    @staticmethod
    def _key_return(method_name, dict_name, dict_of_values, key):
        """
        Many of our operations require a mode that is set via a dict, this will return the mode requested if it exists
        or raise a key error with information to the user of what they submitted vs what was expected.
        """
        try:
            return dict_of_values[key]
        except KeyError:
            raise KeyError(f"{method_name}s {dict_name} only takes {list(dict_of_values.keys())} but found {key}")

    def _create_temp_image(self, colour=True):
        """
        Sometimes we need to create a temporary image, when certain operations require a mono or three channel or more
        image and the current image is not of that type. This creates a colour image by default, but can also create
        mono image, of the current image. If the current image actually meets those specifications, then it is just
        duplicated.
        """
        if colour and self.channels < 3:
            image = self.colour_covert(new_image=True).image
        elif not colour and self.channels > 2:
            image = self.mono_convert(new_image=True).image
        else:
            image = self.image.copy()

        return image

    def _update_or_export(self, image, export):
        """
        Check if the user said to update or export our image
        """
        if export:
            return ImageObject(image)
        else:
            self.image = image

    def show(self, window_name="Image"):
        """
        Show the image and wait for a button to be pressed to continue. Mainly designed for debugging processes
        """
        cv2.namedWindow(window_name, cv2.WINDOW_GUI_EXPANDED)
        cv2.imshow(window_name, self.image)
        cv2.waitKey()

    def notebook_show(self, title="Image"):
        """
        For jupyter we don't want to create a new window, and instead want to show an image via matplotlib.
        """
        plt.imshow(self.bgr_to_rgb(new_image=True).image)
        plt.title(title)
        plt.show()

    def bgr_to_rgb(self, new_image=False):
        """
        cv2 uses bgr rather than rgb, but this can be changed via this method
        """
        return self._update_or_export(cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB), new_image)

    def colour_covert(self, new_image=False):
        """
        Convert image to colour
        """
        return self._update_or_export(cv2.cvtColor(self.image, cv2.COLOR_GRAY2BGR), new_image)

    def change_pixel_colour(self, pixel_column_index, pixel_row_index, colour):
        """
        Change a specific pixel to a certain colour via column and row indexes
        """
        self.image[pixel_column_index, pixel_row_index] = colour

    def mono_convert(self, new_image=False):
        """
        Convert to a mono channel gray image
        """
        return self._update_or_export(cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY), new_image)

    def change_a_colour(self, current_colour, new_colour, new_image=False):
        """
        Change all current pixels of one bgr colour to a different bgr colour
        """
        if new_image:
            image = self.image.copy()
            image[np.where((image == [current_colour]).all(axis=2))] = [new_colour]
            return ImageObject(image)
        else:
            self.image[np.where((self.image == [current_colour]).all(axis=2))] = [new_colour]

    def invert_image(self, new_image=False):
        """
        Invert the current image
        """
        return self._update_or_export(cv2.bitwise_not(self.image), new_image)

    def morphology(self, morph_type, kernel_vertical, kernel_horizontal, kernel_type="rect", new_image=False):
        """
        This applies one of cv2's morph types to the image, or returns a new one if requested.

        morph_types
        ------------
        morph_types takes on of the following keywords: erode, dilate, open, close, gradient, tophat, blackhat

        kernel_types
        ------------
        kernel_type can take on the following keywords: rect, cross, ellipse. It defaults to rect
        """
        # Set kernel
        kernel_values = {"rect": cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_vertical, kernel_horizontal)),
                         "cross": cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_vertical, kernel_horizontal)),
                         "ellipse": cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_vertical, kernel_horizontal))}
        kernel = self._key_return("morphology", "kernel_type", kernel_values, kernel_type)

        # Set morphology type
        morph_values = {"erode": 0, "dilate": 1, "open": 2, "close": 3, "gradient": 4, "tophat": 5, "blackhat": 6}
        morph_type = self._key_return("morphology", "morph_type", morph_values, morph_type)

        if morph_type == 0:
            morphed = cv2.erode(self.image, kernel)
        elif morph_type == 1:
            morphed = cv2.dilate(self.image, kernel)
        elif 1 < morph_type < 7:
            morphed = cv2.morphologyEx(self.image, morph_type, kernel)
        else:
            sys.exit("CRITICAL ERROR: ImageObject.morphology\n"
                     "dict value return from morph_values fell outside of operating range")

        return self._update_or_export(morphed, new_image)

    def find_contours(self, retrieval_mode, simple_method=True, hierarchy_return=False):
        """
        Find contours within the current image. Since find contours only works on mono channel images, if the current
        image is a colour image a new image is create that will not change the one in memory so it is not necessary to
        change the image to gray manually.

        retrieval_mode
        ---------------
        retrieval_mode can take on of the following values: external, list, ccomp, tree, floodfill

        simple_method
        --------------
        Simple methods will only use the extremes, so for a straight line it will store the first and last point. If you
        turn this off it will keep all the points on the line but this can lead to a very large over head so it is not
        recommend unless you have a specific need for all those points.

        hierarchy_return
        ----------------
        If you don't want to return the hierarchy you can leave this as default, otherwise set it to true
        """
        # Set retrieval mode
        retrieval_values = {"external": 0, "list": 1, "ccomp": 2, "tree": 3, "floodfill": 4}
        retrieval = self._key_return("find_contours", "retrieval_mode", retrieval_values, retrieval_mode)

        # Setup of extraction methods
        if simple_method:
            approx = cv2.CHAIN_APPROX_SIMPLE
        else:
            approx = cv2.CHAIN_APPROX_NONE

        # Look for contours base on the setup
        contours, hierarchy = cv2.findContours(self._create_temp_image(colour=False), retrieval, approx)

        # If we find any contours, return the contours and the hierarchy if requested
        if len(contours) > 0:
            if hierarchy_return:
                return [ContourObject(cnt) for cnt in contours], hierarchy
            else:
                return [ContourObject(cnt) for cnt in contours]
        else:
            if hierarchy_return:
                return None, None
            else:
                return None

    def alpha_mask(self, new_image=False):
        """
        Takes a 4 channel image and returns the alpha channel as a mask
        """
        _, mask = cv2.threshold(self.image[:, :, 3], 0, 255, cv2.THRESH_BINARY)
        return self._update_or_export(mask, new_image)

    def blank_like(self, new_image=False):
        """
        Create a blank image of the same dimensions as the image
        """
        return self._update_or_export(np.zeros_like(self.image), new_image)

    def inset_border(self, colour=(0, 0, 0), size=1, new_image=False):
        """
        This function is overlays a hollow square on the image to create an inset border
        """
        return self._update_or_export(cv2.rectangle(self.image.copy(), (0, 0), (self.width, self.height), colour, size),
                                      new_image)

    def crop(self, height_min, height_max, width_min, width_max, relative=True, new_image=False):
        """
        Cropping can be relative or actual. If relative, each value represents a 0.0 - 1.0 range that acts as a
        percentage that the height and width will be cropped by. Otherwise, the actual pixel starting and ending values
        will be the input which should be in a range of 0-width/height max.
        """
        if relative:
            width = self.width
            height = self.height
        else:
            width = 1
            height = 1

        image = self.image.copy()
        crop = image[int(height * height_min):int(height * height_max), int(width * width_min):int(width * width_max)]

        # If we want to know where the crop points started, we can return these values
        return self._update_or_export(crop, new_image)

    def overlay_image(self, image_to_overlay, y_start, x_start, new_image=False):
        """
        This overlays a smaller image onto the current image, based on starting y and x position of the overlay.
        """
        original = self.image.copy()

        if isinstance(image_to_overlay, ImageObject):
            overlay = image_to_overlay
        else:
            overlay = ImageObject(image_to_overlay)

        original[y_start: y_start + overlay.height, x_start: x_start + overlay.width] = overlay.image

        return self._update_or_export(original, new_image)

    def extend_bounds(self, uniform=True, size=1, top=1, bottom=1, left=1, right=1, colour=(0, 0, 0), new_image=False):
        """
        This will extend the bounds of the image, if uniform is selected then you only need to adjust size and all
        borders will extend by that amount. Otherwise you can find tweak the size increase through the top, bottom,
        left, right parameters.
        """
        if uniform:
            output_border = cv2.copyMakeBorder(self.image, size, size, size, size, cv2.BORDER_CONSTANT, value=colour)
        else:
            output_border = cv2.copyMakeBorder(self.image, top, bottom, left, right, cv2.BORDER_CONSTANT, value=colour)

        self._update_or_export(output_border, new_image)

    def shape_mask(self, lower_thresh, upper_thresh, new_image=False):
        """
        Isolate shapes within a given bgr range.
        """
        return self._update_or_export(cv2.inRange(self._create_temp_image(), lower_thresh, upper_thresh), new_image)

    def mask_image(self, mask, new_image=False):
        """
        This will use another image as a mask for this image. Can be an ImageObject or any cv2 compatible image.
        """
        if isinstance(mask, ImageObject):
            masked = cv2.bitwise_and(self.image, self.image, mask=mask.image)
        else:
            masked = cv2.bitwise_and(self.image, self.image, mask=mask)

        return self._update_or_export(masked, new_image)

    def binary_threshold(self, binary_threshold, binary_mode="binary", binary_max=255, new_image=False):
        """
        Create or push the image to a binary black on white image based on a threshold of mono pixel values.
        """
        binary_values = {"binary": 0, "binary_inv": 1, "trunc": 2, "to_zero": 3, "to_zero_inv": 4}
        binary_mode = self._key_return("binary_threshold", "binary_mode", binary_values, binary_mode)

        _, threshold_image = cv2.threshold(self.image, binary_threshold, binary_max, binary_mode)

        return self._update_or_export(threshold_image, new_image)

    def adaptive_threshold(self, assignment_value=255, gaussian_adaptive=True, binary_mode="binary",
                           neighborhood_size=51, subtract_constant=20, new_image=False):
        """
        This will apply by default a gaussian adaptive threshold using the binary method
        """
        # Set binary mode
        binary_values = {"binary": 0, "binary_inv": 1, "trunc": 2, "to_zero": 3, "to_zero_inv": 4}
        binary_mode = self._key_return("adaptive_threshold", "binary_mode", binary_values, binary_mode)

        # Set adaptive method
        if gaussian_adaptive:
            adaptive_mode = cv2.ADAPTIVE_THRESH_GAUSSIAN_C
        else:
            adaptive_mode = cv2.ADAPTIVE_THRESH_MEAN_C

        thresh = cv2.adaptiveThreshold(self._create_temp_image(colour=False), assignment_value, adaptive_mode,
                                       binary_mode, neighborhood_size, subtract_constant)

        return self._update_or_export(thresh, new_image)

    def calculate_alpha_beta(self, clip_hist_percent=1):
        """
        This calculates the current alpha and beta values from an image

        From https://stackoverflow.com/questions/56905592/automatic-contrast-and-brightness-adjustment-of-a-color-photo-
        of-a-sheet-of-paper
        """
        gray = self._create_temp_image(colour=False)

        hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
        hist_size = len(hist)

        # Calculate cumulative distribution from the histogram
        previous = float(hist[0])
        accumulator = [previous]
        for index in range(1, hist_size):
            previous = previous + float(hist[index])
            accumulator.append(previous)

        # Locate points to clip
        maximum = accumulator[-1]
        clip_hist_percent *= (maximum / 100.0)
        clip_hist_percent /= 2.0

        # Locate left cut
        minimum_gray = 0
        while accumulator[minimum_gray] < clip_hist_percent:
            minimum_gray += 1

        # Locate right cut
        maximum_gray = hist_size - 1
        while accumulator[maximum_gray] >= (maximum - clip_hist_percent):
            maximum_gray -= 1

        # Calculate alpha and beta values
        alpha = 255 / (maximum_gray - minimum_gray)
        beta = -minimum_gray * alpha

        return alpha, beta

    def perspective_transform(self, clockwise_points, new_image=False):
        """
        This will apply a perspective transformation on a image based on set of points given in order of:

        bottom_left, bottom_right, top_right, top_left
        """
        bottom_left, bottom_right, top_right, top_left = clockwise_points

        # 2) Set output dimensions
        diff_x = int(bottom_left[0] - bottom_right[0])
        diff_y = int(bottom_right[1] - top_right[1])

        # 3)Set output points
        out_top_left = (0, 0)
        out_top_right = (abs(diff_x), 0)
        out_bottom_left = (0, diff_y)
        out_bottom_right = (abs(diff_x), diff_y)

        # 4) Calculate transformation matrix
        pts1 = np.float32([[top_left], [top_right], [bottom_left], [bottom_right]])
        pts2 = np.float32([[out_top_left], [out_top_right], [out_bottom_left], [out_bottom_right]])
        matrix = cv2.getPerspectiveTransform(pts1, pts2)

        # 5) Apply the matrix transform on these points lists
        self._update_or_export(cv2.warpPerspective(self.image, matrix, (abs(diff_x), diff_y)), new_image)
