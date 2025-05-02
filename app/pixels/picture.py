import math

import numpy as np

import os
import io


from PIL import Image
from PIL import ImageDraw
from PIL import ImageFilter
from PIL import ImageOps
from PIL import ImageEnhance
from PIL import ImageChops
from PIL import ImageFont

from .color import Color



class Picture:
    """
    # Picture Class

    The `Picture` class represent images.
    """

    def __init__(self, image):
        self.image = image

    
    def __str__(self):
        return f"<Picture: {self.image.width}x{self.image.height} image>"


    def _repr_png_(self):
        with io.BytesIO() as buf:
            self.image.save(buf, format='PNG')
            return buf.getvalue()
        
    


    
    # Constructors
    @classmethod
    def from_file_path(cls, image_path: str):
        """
        Create a `Picture` object from an image file.

        Args:
            image_path (str): File path of the image.

        Returns:
            `Picture`
        """
        image = Image.open(image_path)
        return cls(image)





    @classmethod
    def from_PIL_image(cls, image):
        """
        Create a `Picture`object from a PIL image.

        Args:
            image (PIL.Image): PIL Image object

        Returns:
            `Picture`
        """
        return cls(image)






    @classmethod
    def from_array(cls, array):
        """
        Convert a NumPy Array to a Picture Object

        Args:
            array (np.ndarray): A NumPy array representing an image, which will be converted into a PIL image.

        Returns:
            Picture: `Picture`

        """
        pil_image = Image.fromarray(array)
        return cls(pil_image)







    @property
    def size(self) -> tuple:
        """
        This property returns the dimensions (width, height) of the image.

        Returns:
            tuple: A tuple containing two integers representing the width and height of the image.

        Example:
            >>> picture = Picture(image)
            >>> print(picture.size)
            (width, height)
            This will print the size of the image as a tuple.
        """
        return self.image.size






    @property
    def width(self) -> int:
        """
        Returns the `width` of the image.

        Returns:
            int: The width of the image.
        """
        return self.image.size[0]






    @property
    def height(self) -> int:
        """
        Returns the `height` of the image.

        Returns:
            int: The height of the image.
        """
        return self.image.size[1]






    @property
    def entropy(self) -> float:
        """
        Return the `entropy` of the image.

        Returns:
            float: The `entropy` of the image.
        """
        return self.image.entropy()






    @property
    def mode(self):
        """
        Returns the color mode of the image, such as "RGB", "RGBA", "L", etc.

        Returns:
            str: The mode of the image, which represents the color system used.

        Example:
            >>> picture = Picture(image)
            >>> print(picture.mode)
            'RGB'
            This will print the mode of the image.

        Notes:
            - The mode is a string that indicates the image's color space.
            - Common modes include "RGB", "RGBA", "L" (grayscale), "P" (palette-based), and more.
        """
        return self.image.mode






    @property
    def red_channel(self):
        """
        Extract the Red Channel from the Image

        Returns:
            Picture: A Picture object containing the image with only the red channel of the original image.
        """
        r_values = self.image.split()[0]
        red_image = Image.merge("RGB", (r_values, Image.new("L", self.image.size, 0), Image.new("L", self.image.size, 0)))
        return Picture.from_PIL_image(red_image)






    @property
    def green_channel(self):
        """
        Extract the Green Channel from the Image

        Returns:
            Picture: A Picture object containing the image with only the green channel of the original image.
        """
        g_values = self.image.split()[1]
        green_image = Image.merge("RGB", (Image.new("L", self.image.size, 0), g_values, Image.new("L", self.image.size, 0)))
        return Picture.from_PIL_image(green_image)






    @property
    def blue_channel(self):
        """
        Extract the Blue Channel from the Image

        Returns:
            Picture: A Picture object containing the image with only the blue channel of the original image.
        """
        b_values = self.image.split()[2]
        blue_image = Image.merge("RGB", (Image.new("L", self.image.size, 0), Image.new("L", self.image.size, 0), b_values))
        return Picture.from_PIL_image(blue_image)






    @property
    def np_array(self):
        """
        The numpy array of the image.

        Returns:
            np.ndarray: A NumPy array representing the image, with shape (height, width, channels) for RGB images.

        """
        image_np = np.array(self.image)
        return image_np






    # General methods
    def show(self):
        """
        Displays the image using the default image viewer.
        """
        self.image.show()





    def save(self, output_path):
        """
        Saves the image to a file.

        Args:
            output_path (str): The pathe on which to save the image.
        """
        self.image.save(output_path)





    def copy(self):
        """
        Return a copy of the `Picture` instance.
        """
        return Picture.from_PIL_image(self.image.copy())





    def convert_to_grayscale(self):
        """
        Converts the image mode to grayscale (L).
        """
        self.image = self.image.convert('L')





    def convert_to_rgb(self):
        """
        Convert the image mode to RGB.
        """
        self.image = self.image.convert('RGB')





    def convert_to_rgba(self):
        """
        Convert the image mode to RGBA
        """
        self.image = self.image.convert('RGBA')





    def adjust_brightness(self, value: float):
        """
        Adjusts the exposurte of the image.
         - (1.0 = original, >1.0 = brighter, <1.0 = darker)

        Args:
            value (float): adjustment factor of the exposure.

        """
        enhancer = ImageEnhance.Brightness(self.image)
        enhanced_image = enhancer.enhance(value)
        self.image = enhanced_image





    def adjust_contrast(self, value: float):
        """
        Adjusts the contrast of the image.
         - (1.0 = original, >1.0 = more contrast, <1.0 = less contrast)

        Args:
            value (float): adjustment factor of the contrast.

        """
        enhancer = ImageEnhance.Contrast(self.image)
        enhanced_image = enhancer.enhance(value)
        self.image = enhanced_image





    def adjust_sharpness(self, value: float):
        """
        Adjusts the sharpness of the image.
         - (1.0 = original, >1.0 = sharper, <1.0 = duller)

        Args:
            value (float): adjustment factor of the sharpness.

        """
        enhancer = ImageEnhance.Sharpness(self.image)
        enhanced_image = enhancer.enhance(value)
        self.image = enhanced_image





    def adjust_saturation(self, value: float):
        """
        Adjusts the saturation of the image.
         - (1.0 = original, >1.0 = more saturated, <1.0 = less saturated)

        Args:
            value (float): adjustment factor of the saturation.

        """
        enhancer = ImageEnhance.Color(self.image)
        enhanced_image = enhancer.enhance(value)
        self.image = enhanced_image




    def get_pixel_color(self, coord_x: int, coord_y: int) -> Color:
        """
        Get the color of a pixel at the specified coordinates (coord_x, coord_y).
        
        Args:
            coord_x (int): The x-coordinate of the pixel.
            coord_y (int): The y-coordinate of the pixel.
        
        Returns:
            Color: The color of the pixel as a Color object.
        
        Raises:
            ValueError: If the pixel format is unexpected.
        """
        pixel_value = self.image.getpixel((coord_x, coord_y))

        if isinstance(pixel_value, int):  # Grayscale
            return Color(pixel_value, pixel_value, pixel_value)
        elif isinstance(pixel_value, tuple):
            if len(pixel_value) >= 3:
                return Color(pixel_value[0], pixel_value[1], pixel_value[2])
            # Handle other tuple lengths if needed

        # Fallback or raise an error
        raise ValueError(f"Unexpected pixel format: {pixel_value}")




    # Geometry
    def rotate(self, angle):
        """
        Rotates the image by the `angle` expressed in degrees.

        Args:
            angle (float): angle of rotation in degrees
        """
        self.image = self.image.rotate(angle)





    def resize(self, width, height, keep_aspect_ratio = True, crop = False):
        """
        Resizes the image according to the specified width and height, with options to maintain
        the aspect ratio and/or crop the image. Different resizing methods are used depending on the combination
        of options chosen.

        Args:
            width (int): The target width of the resized image.
            height (int): The target height of the resized image.
            keep_aspect_ratio (bool, optional): Whether to preserve the original aspect ratio of the image.
                                                Defaults to True. If True, the image is resized to fit within the
                                                specified dimensions.
                                                If False, the image is resized to exactly match the target dimensions.
            crop (bool, optional): Whether to crop the image to fit the specified dimensions. Defaults to False.
                                If True, the image will be cropped to maintain the aspect ratio after resizing
                                (used when `keep_aspect_ratio` is also True).
        """
        if keep_aspect_ratio and not crop:
            self.image = ImageOps.cover(self.image, (width, height))
        if (keep_aspect_ratio and crop) or crop:
            self.image = ImageOps.fit(self.image, (width, height))
        if not keep_aspect_ratio and not crop:
            self.image = self.image.resize((width, height))





    def crop(self, left_margin, top_margin, right_margin, bottom_margin):
        """
        Crops the image by removing the specified margins from the left, top, right, and bottom edges.

        Args:
            left_margin (int): The number of pixels to remove from the left edge of the image.
            top_margin (int): The number of pixels to remove from the top edge of the image.
            right_margin (int): The number of pixels to remove from the right edge of the image.
            bottom_margin (int): The number of pixels to remove from the bottom edge of the image.

        Example:
            >>> picture = Picture(image)
            >>> picture.crop(50, 30, 50, 30)
            This will crop the image by removing 50 pixels from the left, 30 from the top, 50 from the right,
            and 30 from the bottom.
        """
        width, height = self.size
        self.image = self.image.crop((left_margin, top_margin, width - right_margin, height - bottom_margin))





    def flip_horizontal(self):
        """
        Flips the image horizontally.
        """
        self.image = ImageOps.mirror(self.image)





    def flip_vertical(self):
        """
        Flips the image vertically.
        """
        self.image = ImageOps.flip(self.image)







    def get_main_colors(self, num_colors) -> list[Color]:
        """
        Return a list of the main $n$ colors of the image.

        Args:
            num_colors (int): number of main colors to return

        Returns:
            list[Color]: list of HAL.pixels.Color objects.
        """
        # Convert image to "P" mode (palette-based) with an adaptive palette
        image = self.image.convert("P", palette=Image.Palette.ADAPTIVE, colors=num_colors)

        # Get the palette (a list of RGB values, where every 3 values are an (R, G, B) triplet)
        palette = image.getpalette()
        if palette is None:
            return []

        palette = palette[:num_colors * 3]  # Only get requested number of colors

        # Convert flat list to list of RGB tuples
        colors = [tuple(palette[i:i+3]) for i in range(0, len(palette), 3)]
        colors = [Color(c[0], c[1], c[2]) for c in colors]
        return colors





    def get_color_palette(self, num_colors):
        """
        Return a `Picture` of the colorpalette of the image.

        Args:
            num_colors (int): number of colors to include in the color palette.

        Returns:
            Picture: color palette of the picture.
        """
        colors = self.get_main_colors(num_colors)
        color_pictures = []
        for color in colors:
            color_pictures.append(Picture.from_PIL_image(Image.new('RGB', (100, 100), color.rgb)))
        palette = create_grid_of_pictures(color_pictures, grid_size=(num_colors, 1), image_size=(100, 100))
        return palette





    # Dithering methods

    def dither_halftone(self, **kwargs):
        """
        Apply a Halftone Dither Effect to the Image

        This method converts the image to grayscale and applies a halftone dithering effect,
        where the brightness of the image is represented using dots of varying sizes. The dots
        are placed in a grid pattern, with darker areas having larger dots and lighter areas
        having smaller dots.

        Args:
            dot_color (Color, optional): The color of the halftone dots. Defaults to black.
            background_color (Color, optional): The background color for the image. Defaults to white.
            dot_spacing (int, optional): The spacing between the dots in the grid. Defaults to 12 pixels.
            dot_size (int, optional): The maximum size of the dots. Defaults to 8 pixels.

        Returns:
            None

        Example:
            >>> picture = Picture(image)
            >>> picture.dither_halftone(dot_color=RED, background_color=WHITE, dot_spacing=10, dot_size=5)
            This will apply a halftone dithering effect with red dots, a white background, and customized spacing and dot size.

        Notes:
            - The image is first converted to grayscale before applying the halftone effect.
            - The brightness of each pixel determines the size of the dots, with darker areas having larger dots.
            - The method uses a grid pattern with adjustable dot spacing and size to create the halftone effect.

        """
        # Kwargs
        dot_color = kwargs.get('dot_color', Color.BLACK)
        background_color = kwargs.get('background_color', Color.WHITE)
        dot_spacing = kwargs.get('dot_spacing', 12)
        dot_size = kwargs.get('dot_size', 8)

        # Open image and convert to grayscale
        self.convert_to_grayscale()
        width, height = self.size
        halftone = Image.new('RGB', (width, height), background_color.rgb)
        draw = ImageDraw.Draw(halftone)

        # Process image in a grid pattern
        for y in range(0, height, dot_spacing):
            for x in range(0, width, dot_spacing):
                # Get pixel brightness (0-255, where 0 is black and 255 is white)
                pixel_value = self.image.getpixel((x, y))

                # Handle different pixel formats
                if isinstance(pixel_value, int):  # Grayscale
                    brightness = float(pixel_value)
                elif isinstance(pixel_value, tuple) and len(pixel_value) > 0:
                    brightness = float(pixel_value[0])  # Take first channel
                else:
                    brightness = 0.0  # Default if pixel format is unexpected

                # Scale dot size based on brightness (darker areas have larger dots)
                radius = (1 - brightness / 255) * dot_size / 2

                if radius > 0:
                    draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=dot_color.rgb)

        self.image = halftone






    def dither_ordered(self, **kwargs):
        """
        Apply Ordered Dithering to the Image using Bayer Matrix

        This method applies ordered dithering to an image using a Bayer matrix, which is a technique
        to convert grayscale images to a binary representation using a threshold map. The method
        divides the image into a grid pattern and uses a Bayer matrix of a specified size to
        determine the threshold for dithering.

        Args:
            matrix_size (int, optional): The size of the Bayer matrix to use for dithering.
                                        Supported values are 2, 4, or 8. Defaults to 8.
            scale_factor (int, optional): The size of the grid to process in the dithering.
                                        Defaults to 5 pixels.
            color (Color, optional): The color for the "on" pixels in the dithering (typically white).
                                    Defaults to white.
            background_color (Color, optional): The color for the "off" pixels in the dithering (typically black).
                                                Defaults to black.

        Returns:
            None

        Example:
            >>> picture = Picture(image)
            >>> picture.dither_ordered(matrix_size=4, scale_factor=6, color=WHITE, background_color=BLACK)
            This will apply ordered dithering to the image using a 4x4 Bayer matrix,
            with a scale factor of 6 pixels for each grid and white for the "on" color.

        Notes:
            - The Bayer matrices of size 2, 4, and 8 are pre-defined, and the dithering is based on the threshold values
            derived from these matrices.
            - The method processes the image in blocks of the specified `scale_factor` and applies the dithering based on
            pixel brightness in relation to the corresponding threshold in the Bayer matrix.
        """
        # Kwargs
        matrix_size = kwargs.get('matrix_size', 8)
        scale_factor = kwargs.get('scale_factor', 5)
        color = kwargs.get('color', Color.WHITE)
        background_color = kwargs.get('background_color', Color.BLACK)

        # Bayer matrices of different sizes
        bayer_matrices = {
            2: np.array([[0, 2], [3, 1]]) / 4.0,
            4: np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]) / 16.0,
            8: np.array([
                [0, 32, 8, 40, 2, 34, 10, 42],
                [48, 16, 56, 24, 50, 18, 58, 26],
                [12, 44, 4, 36, 14, 46, 6, 38],
                [60, 28, 52, 20, 62, 30, 54, 22],
                [3, 35, 11, 43, 1, 33, 9, 41],
                [51, 19, 59, 27, 49, 17, 57, 25],
                [15, 47, 7, 39, 13, 45, 5, 37],
                [63, 31, 55, 23, 61, 29, 53, 21]
            ]) / 64.0
        }

        if matrix_size not in bayer_matrices:
            raise ValueError("Unsupported matrix size. Choose from 2, 4, or 8.")

        bayer_matrix = bayer_matrices[matrix_size]
        threshold_map = (bayer_matrix * 255).astype(np.uint8)

        # Open image and convert to grayscale
        self.convert_to_grayscale()
        width, height = self.image.size
        pixels = np.array(self.image, dtype=np.uint8)

        # Convert image to RGB to sore colore pixels
        color_pixels = np.zeros((height, width, 3), dtype=np.uint8)

        # Apply dithering
        for y in range(0, height, scale_factor):
            for x in range(0, width, scale_factor):
                threshold = threshold_map[(y // scale_factor) % matrix_size, (x // scale_factor) % matrix_size]
                color_pixels[y:y+scale_factor, x:x+scale_factor] = color.rgb if pixels[y, x] > threshold else background_color.rgb

        dithered_image = Image.fromarray(color_pixels, mode='RGB')
        self.image =  dithered_image






    def dither_floyd_steinberg(self, **kwargs):
        """
        Apply Floyd-Steinberg Dithering to the Image

        This method applies the Floyd-Steinberg dithering algorithm, a popular error-diffusion technique
        used to convert grayscale images into a binary representation while preserving the appearance of
        continuous tones. The method scales the image, applies the dithering, and then resizes it back to
        the original size.

        Args:
            scale_factor (int, optional): The scaling factor for the image before applying the dithering.
                                        A larger value reduces the amount of scaling applied to the image.
                                        Defaults to 3.

        Returns:
            None

        Example:
            >>> picture = Picture(image)
            >>> picture.dither_floyd_steinberg(scale_factor=4)
            This will apply Floyd-Steinberg dithering to the image with a scale factor of 4.

        Notes:
            - The image is first converted to grayscale before applying the dithering.
            - The algorithm works by diffusing the error between the pixel value and the nearest threshold
            (either 0 or 255) to neighboring pixels.
            - The image is scaled down by the specified `scale_factor` to speed up the dithering process,
            and then scaled back to the original dimensions after dithering.
            - The error diffusion weights for the Floyd-Steinberg algorithm are as follows:
            - (7/16) to the pixel to the right
            - (3/16) to the pixel below-left
            - (5/16) to the pixel below
            - (1/16) to the pixel below-right
        """

        scale_factor = kwargs.get('scale_factor', 3)

        self.convert_to_grayscale()
        pixels = np.array(self.image, dtype=np.float32)
        height, width = pixels.shape

        scaled_height = int(height / scale_factor)
        scaled_width = int(width / scale_factor)
        scaled_image = Image.fromarray(pixels.astype(np.uint8)).resize((scaled_width, scaled_height), Image.Resampling.NEAREST)
        pixels = np.array(scaled_image, dtype=np.float32)

        for y in range(scaled_height):
            for x in range(scaled_width):
                old_pixel = pixels[y, x]
                new_pixel = 255 if old_pixel > 127 else 0
                pixels[y, x] = new_pixel
                quant_error = old_pixel - new_pixel

                if x < scaled_width - 1:
                    pixels[y, x + 1] += quant_error * (7 / 16)
                if y < scaled_height - 1:
                    if x > 0:
                        pixels[y + 1, x - 1] += quant_error * (3 / 16)
                    pixels[y + 1, x] += quant_error * (5 / 16)
                    if x < scaled_width - 1:
                        pixels[y + 1, x + 1] += quant_error * (1 / 16)

        dithered_image = Image.fromarray(np.clip(pixels, 0, 255).astype(np.uint8), mode='L')
        dithered_image = dithered_image.resize((width, height), Image.Resampling.NEAREST)
        self.image = dithered_image




    # OTHER OPERATIONS

    def binarize(self, **kwargs):
        """
        Convert the Image to Binary (Black and White) using a Threshold

        This method converts the image into a binary image, where each pixel is either black or white,
        based on a specified threshold. The method also allows for color customization when the image
        is in color mode, and it includes options for converting the image to grayscale or color before
        applying the threshold.

        Args:
            threshold (int, optional): The pixel intensity threshold used to decide whether a pixel becomes
                                        white (255) or black (0). Values greater than the threshold will be
                                        set to white. Default is 128.
            grayscale (bool, optional): If True, the image will be converted to grayscale before binarization.
                                        Default is True.
            color (Color, optional): A color to replace black pixels in the image when `grayscale` is False.
                                    If None, the black pixels will remain black. Default is None.

        Returns:
            None: The method modifies the image in place, converting it to binary (black and white).

        Example:
            >>> picture = Picture(image)
            >>> picture.binarize(threshold=100, grayscale=False, color=RED)
            This will binarize the image with a threshold of 100, and replace black pixels with red color.

        Notes:
            - If `grayscale` is True or `color` is specified, the image is first converted to grayscale.
            - The image is processed pixel by pixel, and each pixel value is compared to the threshold.
            If the pixel value is above the threshold, it is set to white (255), and if it is below, it is
            set to black (0).
            - If `color` is specified, black pixels will be replaced with the given color.
        """

        threshold = kwargs.get("threshold", 128)
        grayscale = kwargs.get("grayscale", True)
        color = kwargs.get("color", None)

        if grayscale or color:
            self.convert_to_grayscale()

        binarized_image = self.image.point(lambda p: 255 if p > threshold else 0)
        self.image = binarized_image

        if color:
            self.convert_to_rgb()
            pixels = self.image.load()  # This returns an object that can be indexed, not None
            if pixels is not None:  # Add a check to ensure pixels is not None
                for y in range(self.image.height):
                    for x in range(self.image.width):
                        if pixels[x, y] == (0, 0, 0):
                            pixels[x, y] = color.rgb





    # MASKS

    def create_alpha_mask(self):
        """
        Create an Alpha Mask for the Image

        This method generates an alpha mask for the image, where pixels with a value of 0 (black)
        are set to fully transparent (alpha = 0) and non-zero pixels are set to partially transparent
        (alpha = 1). It creates an RGBA image with the alpha channel representing the mask.

        The image is first copied and then processed to create an RGBA version where the alpha channel
        is set based on the binarized pixel values. After creating the mask, the image is converted
        back to grayscale.

        Returns:
            None

        Notes:
            - The method assumes that the image is already in a format that can be binarized.
            - The alpha mask is based on the binary representation of the image.
            - The image is processed pixel by pixel, and an RGBA image is created.
        """
        binarized_image = self.copy()
        self.convert_to_rgba()
        for y in range(self.image.height):
            for x in range(self.image.width):
                pixel_value = binarized_image.image.getpixel((x, y))
                if pixel_value == 0:
                    self.image.putpixel((x, y), (255, 255, 255, 0))
                else:
                    self.image.putpixel((x, y), (0, 0, 0, 1))
        self.convert_to_grayscale()







    def apply_alpha_mask(self, mask):
        """
        Apply an Alpha Mask to the Image

        This method applies an alpha mask to the current image. The alpha mask should be a binary image
        (with an alpha channel) that defines transparency values for the image. The mask is applied by
        setting the alpha channel of the current image according to the mask's alpha channel.

        The method expects that the mask is a `Picture` object with an image that contains an alpha channel.
        It uses the alpha values of the mask to modify the transparency of the original image.

        Args:
            mask (Picture): A `Picture` object that contains the alpha mask to be applied.
                            The mask image should be in RGBA mode.

        Returns:
            None

        Example:
            >>> picture = Picture(image)
            >>> alpha_mask = Picture(mask_image)
            >>> picture.apply_alpha_mask(alpha_mask)
            This will apply the alpha mask to the original image, altering its transparency based on the mask.

        Notes:
            - The mask should be an RGBA image where the alpha channel defines transparency.
            - The current image must be in a format that supports an alpha channel (e.g., RGBA).
        """
        self.image.putalpha(mask.image)






    def paste_picture(self, picture_to_paste, coord_x: int, coord_y: int):
        """
        Paste one picture onto another at the specified coordinates while handling transparency.
        
        Args:
            picture_to_paste (Picture): The picture to be pasted.
            coord_x (int): The x-coordinate where the picture should be pasted.
            coord_y (int): The y-coordinate where the picture should be pasted.
        """
        mask = picture_to_paste.copy()
        mask.convert_to_rgba()
        self.image.paste(picture_to_paste.image, (coord_x, coord_y), mask.image)





    # Filters
    def blur(self, radius: float):
        """
        Apply a Gaussian Blur to the Image

        This method applies a Gaussian blur filter to the current image, which softens the image by
        averaging nearby pixels. The intensity of the blur is determined by the radius parameter.
        Larger values for the radius will result in a stronger blur effect.

        Args:
            radius (float): The radius of the blur. A higher radius value results in a more blurred image.

        Returns:
            None
        """
        self.image = self.image.filter(ImageFilter.GaussianBlur(radius))




    def invert_colors(self):
        """
        Invert the Colors of the Image

        This method inverts the colors of the current image, transforming all pixels in the image
        to their complementary color. Each pixel's red, green, and blue values are inverted, meaning
        that the color channels are flipped to their opposite values. For example, a white pixel (255, 255, 255)
        would become black (0, 0, 0), and vice versa.

        Args:
            None: This method operates directly on the current image.

        Returns:
            None
        """
        self.image = ImageOps.invert(self.image)





    def apply_color_filter(self, color):
        """
        This method applies a color filter to the current image by multiplying the image with a solid color.
        The resulting image will have a tint of the provided color, blending the original image with the filter color.

        Args:
            color (Color): The `Color` object representing the filter color. This color will be multiplied
                        with each pixel in the image to apply the filter effect.

        Returns:
            None
        """
        color_filter = Image.new("RGB", self.image.size, color.rgb)
        self.image = ImageChops.multiply(self.image, color_filter)











    # DRAWING 


    def draw_line(self, start: tuple, end: tuple, **kwargs) -> None:
        """
        Draw a line between two points on the image.
        
        Args:
            start (tuple): The starting point of the line (x1, y1).
            end (tuple): The ending point of the line (x2, y2).
            width (int, optional): The width of the line. Defaults to 3.
            **kwargs: Optional keyword arguments for customization. 
                    - 'color' (Color): The color of the line. Defaults to `Color.WHITE`.
                    - 'width' (int): The width of the line. Defaults to 3.
        
        Returns:
            None
        """
        color = kwargs.get('color', Color.WHITE)
        width = kwargs.get('width', 3)

        draw = ImageDraw.Draw(self.image)
        draw.line([start, end], fill=color.rgb, width=width)




    def draw_circle(self, center: tuple[int, int], radius: int, **kwargs) -> None:
        """
        Draw a circle on the image with the given center and radius.
        
        Args:
            center (tuple): The center point of the circle (x, y).
            radius (int): The radius of the circle.
            **kwargs: Optional keyword arguments for customization.
                    - 'color': The color of the circle. Defaults to `Color.WHITE`.
        
        Returns:
            None
        """
        color: Color = kwargs.get('color', Color.WHITE)

        draw = ImageDraw.Draw(self.image)
        x, y = center
        bounding_box = [x - radius, y - radius, x + radius, y + radius]
        draw.ellipse(bounding_box, width=5, fill=color.rgb)





    def draw_text(self, text: str, position: tuple[int, int], font_size, **kwargs) -> None:
        """
        Draw text on the image at the specified position with the given font size.
        
        Args:
            text (str): The text to be drawn.
            position (tuple): The (x, y) position where the text's baseline will be.
            font_size (int): The font size.
            **kwargs: Optional keyword arguments for customization.
                    - 'color': The color of the text. Defaults to `Color.BLACK`.
        
        Returns:
            None
        """
        color = kwargs.get('color', Color.BLACK)

        draw = ImageDraw.Draw(self.image)
        font_path = os.path.join(os.path.dirname(__file__), '..', 'fonts', 'font_test.ttf')
        font = ImageFont.truetype(font_path, font_size)

        # Measure text size
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        # Adjust position if centering
        x, y = position
        x -= text_width // 2
        y -= text_height // 2

        draw.text((x, y), text, fill=color.rgb, font=font)





    def draw_arrow(self, start: tuple, end: tuple, width=3, arrowhead_length=50, arrowhead_angle=30, **kwargs) -> None:
        color = kwargs.get('color', Color.WHITE)

        draw = ImageDraw.Draw(self.image)

        # Draw the main shaft
        draw.line([start, end], fill=color.rgb, width=width)

        # Direction vector
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        angle = math.atan2(dy, dx)

        # Arrowhead points
        left_angle = angle + math.radians(arrowhead_angle)
        right_angle = angle - math.radians(arrowhead_angle)

        left_point = (
            end[0] - arrowhead_length * math.cos(left_angle),
            end[1] - arrowhead_length * math.sin(left_angle)
        )
        right_point = (
            end[0] - arrowhead_length * math.cos(right_angle),
            end[1] - arrowhead_length * math.sin(right_angle)
        )

        # Draw filled triangle for arrowhead
        draw.polygon([end, left_point, right_point], fill=color.rgb)















# Blendings
def blend_images(image1: Picture, image2: Picture, **kwargs) -> Picture:
    """
    This function blends two images of the same size and mode together using a specified alpha value.
    The blending is done using the `Image.blend` function from the PIL library, which combines the two
    images by mixing their pixel values based on the alpha parameter.

    Args:
        image1 (Picture): The first image (a `Picture` object) to blend.
        image2 (Picture): The second image (a `Picture` object) to blend.
        alpha (float, optional): A float value between 0 and 1 representing the blending factor.
                                 Default is 0.5, meaning an equal blend of both images.
                                 An alpha of 0.0 means the result will be entirely `image1`,
                                 and an alpha of 1.0 means the result will be entirely `image2`.

    Returns:
        Picture: A new `Picture` object containing the blended image.

    Raises:
        ValueError: If the two images do not have the same size or mode.

    Example:
        >>> image1 = Picture(image1_data)
        >>> image2 = Picture(image2_data)
        >>> blended_image = blend_images(image1, image2, alpha=0.7)

    Notes:
        - Both images must have the same size and mode (e.g., both should be in RGB or RGBA).
        - The alpha value determines the influence of each image in the final blend. A value of 0.5 results in an equal blend of both images.
        - The result is a new image that blends the pixel values of the two input images based on the alpha value.
    """

    if image1.size != image2.size:
        raise ValueError("Images must have the same size.")
    if image1.mode != image2.mode:
        raise ValueError("Images must have the same mode.")
    alpha = kwargs.get('alpha', 0.5)
    pil_image = Image.blend(image1.image, image2.image, alpha)
    return Picture.from_PIL_image(pil_image)








def screen_blend(pic1: Picture, pic2: Picture) -> Picture:
    """
    Blends two PIL images using the 'Screen' blend mode.
    Both images must be RGB or RGBA and will be resized to match the size of image1 if needed.
    """
    # Convert images to same mode and size
    pic1.convert_to_rgb()
    pic2.convert_to_rgb()

    # Convert to numpy arrays
    arr1 = np.asarray(pic1.image).astype('float')
    arr2 = np.asarray(pic2.image).astype('float')

    # Apply screen blending formula
    blended = 255 - ((255 - arr1) * (255 - arr2) / 255)

    # Clip and convert back to uint8
    blended = np.clip(blended, 0, 255).astype('uint8')

    return Picture.from_PIL_image(Image.fromarray(blended))














def create_grid_of_pictures(pictures: list[Picture], **kwargs) -> Picture:
    """
    Create a Grid of Pictures

    This function arranges a list of `Picture` objects into a grid layout. The grid is constructed based on
    the number of pictures provided, and each picture is resized to fit a uniform image size. The resulting
    grid of pictures is returned as a new `Picture` object.

    Args:
        pictures (list[Picture]): A list of `Picture` objects to be arranged into the grid.
        grid_size (tuple, optional): A tuple representing the number of columns and rows in the grid.
                                      If not provided, the grid will be created with an optimal square
                                      layout based on the number of pictures. Default is determined
                                      by the square root of the number of pictures.
        image_size (tuple, optional): A tuple representing the size (width, height) of each individual image
                                      in the grid. Default is (720, 720).

    Returns:
        Picture: A new `Picture` object containing the collage of images arranged in the grid.

    Raises:
        ValueError: If the input list of pictures is empty.

    Example:
        >>> picture1 = Picture(image1_data)
        >>> picture2 = Picture(image2_data)
        >>> pictures = [picture1, picture2, picture3]
        >>> grid_picture = create_grid_of_pictures(pictures, grid_size=(2, 2), image_size=(500, 500))

    Notes:
        - The images are resized to fit the specified `image_size`, and if necessary, the images are centered
          on a blank white background to maintain the aspect ratio.
        - If the number of pictures exceeds the grid size (cols * rows), extra images are ignored.
        - The resulting collage will have a white background for empty spaces.
    """

    grid_size = kwargs.get('grid_size', (math.ceil(math.sqrt(len(pictures))), math.ceil(math.sqrt(len(pictures)))))
    image_size = kwargs.get('image_size', (720, 720))


    cols, rows = grid_size
    collage_width = cols * image_size[0]
    collage_height = rows * image_size[1]

    collage = Image.new('RGB', (collage_width, collage_height))

    for index, picture in enumerate(pictures):
        if index >= cols * rows:
            break

        img = picture.image
        img.thumbnail(image_size)  # Maintain aspect ratio while resizing

        # Create a blank image with the target size and paste the resized image at the center
        temp_img = Image.new('RGB', image_size, (255, 255, 255))  # White background
        x_offset = (image_size[0] - img.size[0]) // 2
        y_offset = (image_size[1] - img.size[1]) // 2
        temp_img.paste(img, (x_offset, y_offset))

        x_offset = (index % cols) * image_size[0]
        y_offset = (index // cols) * image_size[1]

        collage.paste(temp_img, (x_offset, y_offset))

    return Picture.from_PIL_image(collage)





def superimpose_pictures(picture_1, picture_2):
    """
    Superimpose Two Pictures

    This function overlays one picture on top of another, using the alpha channel of the second image
    to determine transparency. The second image is pasted on top of the first one, and the result is returned
    as a new `Picture`.

    Args:
        picture_1 (Picture): The base image onto which the second image will be pasted.
        picture_2 (Picture): The image to be superimposed on top of the first image.

    Returns:
        Picture: A new `Picture` object with the second image superimposed on top of the first image.

    Example:
        >>> picture_1 = Picture(image1_data)
        >>> picture_2 = Picture(image2_data)
        >>> superimposed_picture = superimpose_pictures(picture_1, picture_2)

    Notes:
        - The function assumes that `picture_2` has an alpha channel (RGBA) for transparency.
        - The superimposition is done at the (0, 0) coordinate, aligning the top-left corners of the two images.
        - This function does not modify the original `picture_1`, instead it returns a new `Picture` with the superimposed images.
    """
    picture_1 = picture_1.copy()
    picture_1.image.paste(picture_2.image, (0, 0), picture_2.image)
    return picture_1












def get_blank_picture(width: int, height: int, color: Color, border_thickness=0, border_color=Color(0, 0, 0)) -> Picture:
    image = Image.new("RGB", (width, height), color.rgb)

    draw = ImageDraw.Draw(image)
    draw.rectangle([0, 0, width - 1, height - 1], outline=border_color.rgb, width=border_thickness)

    picture = Picture.from_PIL_image(image)
    return picture




def add_centered_text(picture: Picture, text: str, **kwargs) -> Picture:

    # Function to wrap text
    def wrap_text(draw, text, font, max_width):
        lines = []
        words = text.split()
        current_line = []

        for word in words:
            # Join current line with the new word and calculate its width
            current_line.append(word)
            line_width, _ = draw.textbbox((0, 0), ' '.join(current_line), font=font)[2:4]

            # If line exceeds max width, start a new line
            if line_width > max_width:
                lines.append(' '.join(current_line[:-1]))  # Add previous line (without last word)
                current_line = [word]  # Start a new line with the current word

        lines.append(' '.join(current_line))  # Add the last line
        return lines



    text_color = kwargs.get('color', Color(0, 0, 0))
    font_size = kwargs.get('font_size', 40)


    picture = picture.copy()
    # Initialize ImageDraw object
    draw = ImageDraw.Draw(picture.image)


    # Get the path to the .ttf font in the parent directory (relative path)
    font_path = os.path.join(os.path.dirname(__file__), '..', 'fonts', 'InterVariable.ttf')
    font = ImageFont.truetype(font_path, font_size)
    #font = ImageFont.load_default()

    # Wrap the text
    max_width = picture.width - 20  # Max width of the text block (with some padding)
    lines = wrap_text(draw, text, font, max_width)


    # Calculate the total height of the text block
    total_text_height = sum([draw.textbbox((0, 0), line, font=font)[3] for line in lines])

    # Calculate the starting position to center the text vertically
    y_start = (picture.height - total_text_height) // 2

    # Set the starting position for the text (horizontally centered)
    x_start = (picture.width - max_width) // 2

    # Draw each line of text
    y = y_start
    for line in lines:
        line_width = draw.textbbox((0, 0), line, font=font)[2]  # Calculate the width of the current line
        x_start = (picture.width - line_width) // 2  # Center the line horizontally
        draw.text((x_start, y), line, fill=text_color.rgb, font=font)
        y += draw.textbbox((0, 0), line, font=font)[3]  # Move to the next line's position


    return picture
