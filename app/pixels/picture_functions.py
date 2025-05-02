from PIL import Image, ImageDraw, ImageFont

import math

from .picture import Picture

from .color import Color


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






# GRID

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








def get_blank_picture(width: int, height: int, color: Color, border_thickness=0, border_color=Color(0, 0, 0)) -> Picture:
    """
    Create a blank image with a customizable background color and optional border.

    Args:
        width (int): The width of the image.
        height (int): The height of the image.
        color (Color): The background color of the image.
        border_thickness (int): The thickness of the border around the image (default is 0 for no border).
        border_color (Color): The color of the border (default is black).

    Returns:
        Picture: A Picture object containing the generated image.
    """
    image = Image.new("RGB", (width, height), color.color)

    draw = ImageDraw.Draw(image)
    draw.rectangle([0, 0, width - 1, height - 1], outline=border_color.color, width=border_thickness)

    picture = Picture.from_PIL_image(image)
    return picture






def add_centered_text(picture: Picture, text: str, **kwargs) -> Picture:
    """
    Adds wrapped, centered text to the picture.

    Args:
        picture (Picture): The picture to which the text will be added.
        text (str): The text to be added to the picture.
        font_size (int): The size of the font.
        kwargs: Additional optional keyword arguments for customization (e.g., text color).

    Returns:
        Picture: The picture with the centered text.
    """
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
    font_path = os.path.join(os.path.dirname(__file__), '..', 'fonts', 'Helvetica.ttf')
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
        draw.text((x_start, y), line, fill=text_color.color, font=font)
        y += draw.textbbox((0, 0), line, font=font)[3]  # Move to the next line's position

    return picture
