
from PIL import Image, ImageDraw, ImageFont
import math
import os

from pixels import Color
from pixels import Picture


class Plotter:
    
    def __init__(self, **kwargs):
        self.width = kwargs.get('width', 2000)
        self.height = kwargs.get('height', 2000)
        self.scale = kwargs.get('scale', 100)
        self.x_scale = kwargs.get('x_scale', self.scale)
        self.y_scale = kwargs.get('y_scale', self.scale)
        self.bg_color = kwargs.get('background_color', Color.BLACK)
        
        self.picture = Picture.from_PIL_image(Image.new('RGB', (self.width, self.height), self.bg_color.rgb))

        self.draw = ImageDraw.Draw(self.picture.image)

    @property
    def center_x(self):
        return self.width//2
       
    @property
    def center_y(self):
        return self.height//2
       

    def draw_axes(self, **kwargs):

        color = kwargs.get('color', Color.WHITE)
        color_x = kwargs.get('color_x', color)
        color_y = kwargs.get('color_y', color)

        thickness = kwargs.get('thickness', 2)
        thickness_x = kwargs.get('thickness_x', thickness)
        thickness_y = kwargs.get('thickness_y', thickness)

        gridlines = kwargs.get('gridlines', False)
        gridlines_x = kwargs.get('gridlines_x', gridlines)
        gridlines_y = kwargs.get('gridlines_y', gridlines)

        grid_spacing = kwargs.get('grid_spacing', 1)
        grid_color = kwargs.get('grid_color', Color.GRAY)
        grid_thickness = kwargs.get('grid_thickness', 1)

        show_labels = kwargs.get('show_labels', gridlines)
        label_color = kwargs.get('label_color', Color.GRAY)
        label_size = kwargs.get('label_size', 40)
        font_path = os.path.join(os.path.dirname(__file__), '..', 'fonts', 'Helvetica.ttf')
        font = ImageFont.truetype(font_path, label_size)

        # X LINE
        self.draw.line((0, self.center_y, self.width, self.center_y), width=thickness_x, fill=color_x.rgb)

        if gridlines_x:
            pixel_spacing_x = self.x_scale * grid_spacing
            label_index = 0

            for i in range(0, self.width, int(pixel_spacing_x)):
                for sign in [-1, 1]:
                    x = self.center_x + sign * i
                    if 0 <= x < self.width:
                        self.draw.line((x, 0, x, self.height), fill=grid_color.rgb, width=grid_thickness)

                         # Add label on second positive gridline only
                        if sign == 1 and show_labels:
                            label_index += 1
                            if label_index == 2:
                                unit_value = i // self.x_scale
                                self.draw.text(
                                    (x + 4, self.center_y + 4),
                                    f"{unit_value}",
                                    font=font,
                                    fill=label_color.rgb
                                )


        # Y LINE
        self.draw.line((self.center_x, 0, self.center_x, self.height), width=thickness_y, fill=color_y.rgb)

        if gridlines_y:
            pixel_spacing_y = self.y_scale * grid_spacing
            label_index = 0

            for i in range(0, self.height, int(pixel_spacing_y)):
                for sign in [-1, 1]:
                    y = self.center_y + sign * i
                    if 0 <= y < self.height:
                        self.draw.line((0, y, self.width, y), fill=grid_color.rgb, width=grid_thickness)

                        # Add label on second upward gridline only
                        if sign == -1 and show_labels:
                            label_index += 1
                            if label_index == 2:
                                unit_value = i // self.y_scale
                                self.draw.text(
                                    (self.center_x + 4, y - 12),
                                    f"{unit_value}",
                                    font=font,
                                    fill=label_color.rgb
                                )





    def plot(self, func, **kwargs):

        if isinstance(func, Equation):
            func = func.as_lambda

        color = kwargs.get('color', Color.WHITE)
        thickness = kwargs.get('thickness', 4)

        prev_point = None

        for px in range(self.width):
            x = (px - self.center_x) / self.x_scale
            try:
                y = func(x)
                py = self.center_y - int(y * self.y_scale)
                if 0 <= py < self.height:
                    if prev_point:
                        self.draw.line((prev_point[0], prev_point[1], px, py), fill=color.rgb, width=thickness)
                    prev_point = (px, py)
                else:
                    v_point = None
            except:
                prev_point = None

    def plot_from_equation(equation: Equation):
        pass

    def plot_parametric(self, func_x, func_y, t_min, t_max, **kwargs):
            
            color = kwargs.get('color', Color.WHITE)
            steps = kwargs.get('steps', 1000)
            thickness = kwargs.get('thickness', 4)

            prev_point = None
            for i in range(steps):
                t = t_min + (t_max - t_min) * i / steps
                try:
                    x = func_x(t)
                    y = func_y(t)
                    px = int(self.center_x + x * self.x_scale)
                    py = int(self.center_y - y * self.y_scale)
                    if 0 <= px < self.width and 0 <= py < self.height:
                        if prev_point:
                            self.draw.line((prev_point[0], prev_point[1], px, py), fill=color.rgb, width=thickness)
                        prev_point = (px, py)
                    else:
                        prev_point = None
                except:
                    prev_point = None


    def plot_points(self, points, **kwargs):
        """Plot a list of (x, y) tuples.
        
        Args:
            points (list): List of (x, y) pairs
            color (str): Point or line color
            radius (int): Size of the dots
            connect (bool): Whether to connect the points with lines
            thickness (int): Line thickness if connecting
        """

        color = kwargs.get('color', Color.WHITE)
        radius = kwargs.get('radius', 4)
        connect = kwargs.get('connect', True)
        thickness = kwargs.get('thickness', 2)

        prev = None
        for x, y in points:
            try:
                px = int(self.center_x + x * self.x_scale)
                py = int(self.center_y - y * self.y_scale)
                if 0 <= px < self.width and 0 <= py < self.height:
                    # Draw a circle for the point
                    self.draw.ellipse((px - radius, py - radius, px + radius, py + radius), fill=color.rgb)
                    # Connect with line if requested
                    if connect and prev:
                        self.draw.line((prev[0], prev[1], px, py), fill=color.rgb, width=thickness)
                    prev = (px, py)
            except:
                prev = None

    


    def plot_histogram(self, data, **kwargs):
        """
        Plots a histogram based on a dictionary of data. 
        Each key in the dictionary represents the label for a column, and the corresponding value is the height.

        Args:
            data (dict): Dictionary where keys are labels and values are the heights of bars.
            bar_width (int): Width of each bar in the histogram.
            gap_width (int): The gap between each bar.
            color (Color): Color of the bars.
        """
        gap_width = kwargs.get('gap_width', 50)
        margin_y = kwargs.get('margin_y', 200)
        margin_x = kwargs.get('margin_x', 110)
        bar_width = (self.width - margin_x*2)/ len(data) - gap_width
        bar_width = kwargs.get('bar_width', bar_width)
        font_size = kwargs.get('font_size', 50)
        label_size = kwargs.get('label_size', 50)
        draw_bottom_line = kwargs.get('draw_bottom_line', True)
        draw_vertical_line = kwargs.get('draw_vertical_line', True)
        horizontal_lines = kwargs.get('horizontal_lines', True)
        horizontal_lines_interval = kwargs.get('horizontal_lines_interval', 2)
        color = kwargs.get('color', Color.WHITE)


        # Initialize starting position for the first bar
        x_pos = margin_x + gap_width

        for label, value in data.items():
            label = str(label)
            # The top of the bar's position
            top = self.height-margin_y - value * self.y_scale  # Direct height from value

            # Draw the rectangle for the bar
            self.draw.rectangle(
                [x_pos, top, x_pos + bar_width, self.height-margin_y],
                fill=color.rgb
            )

            # Get the width of the label text
            font_path = os.path.join(os.path.dirname(__file__), '..', 'fonts', 'Helvetica.ttf')
            font = ImageFont.truetype(font_path, label_size)
            label_width = self.draw.textlength(label, font=font)
            
            # Position for the label (centered on the x_pos)
            label_x_pos = x_pos + (bar_width - label_width) // 2  # Center text horizontally
            
            # Position for the label vertically (below the bar, with margin)
            label_y_pos = self.height - margin_y / 3 * 2

            # Draw the label centered on the coordinates
            self.draw.text(
                (label_x_pos, label_y_pos),
                label, fill=color.rgb, font=font, align="center"
            )

            # Move the x-position for the next bar, considering the width of the bar and gap between them
            x_pos += bar_width + gap_width

        # Draw Bottom Line
        if draw_bottom_line:
            self.draw.line([gap_width + margin_x, self.height-margin_y, self.width -20, self.height-margin_y], width=2, fill=color.rgb)

        if draw_vertical_line:
            self.draw.line([gap_width + margin_x - 10, self.height-margin_y + 10, gap_width + margin_x - 10, 30], width=2, fill=color.rgb)

        if horizontal_lines:
            for i in range(0, self.height - margin_y, self.y_scale):
                if i / self.y_scale % horizontal_lines_interval == 0:
                    self.draw.line([gap_width + margin_x - 20, self.height-margin_y - i, self.width - 20, self.height-margin_y - i], width=1, fill=color.rgb)

                    self.draw.text((margin_x/2, self.height-margin_y - i - font_size/2), str(i/self.y_scale), fill=color.rgb, align="center", font_size=font_size)




    def plot_pie_chart(self, data, **kwargs):
        """
        Plots a pie chart based on a dictionary of data. Each key is the label, and each value is the data to visualize.
        
        Args:
            data (dict): A dictionary where keys are labels and values are the sizes of the slices.
            colors (list): List of colors for the slices.
            radius (int): Radius of the pie chart.
            start_angle (int): The starting angle for the first slice.
        """
        colors = kwargs.get('colors', [Color.BLACK])
        border_color = kwargs.get('border_color', Color.WHITE)
        border_thickenss = kwargs.get('thickness', 10)  
        radius = kwargs.get('radius', min(self.width, self.height) / 2 - (5/100)*min(self.width, self.height))
        start_angle = kwargs.get('start_angle', 0)
        margin_x = kwargs.get('margin_x', self.center_x)
        margin_y = kwargs.get('margin_y', self.center_y)
        label_size = kwargs.get('label_size', 50)

        
        # Calculate total sum of data
        total = sum(data.values())
        
        # Draw the slices
        current_angle = start_angle
        for idx, (label, value) in enumerate(data.items()):
            # Calculate the angle of the slice
            angle = (value / total) * 360
            end_angle = current_angle + angle

            # Draw the slice (using PIL's pieslice method)
            self.draw.pieslice(
                [margin_x - radius, margin_y - radius, margin_x + radius, margin_y + radius],
                start=current_angle,
                end=end_angle,
                fill=colors[idx % len(colors)].rgb,
                outline=border_color.rgb,
                width = border_thickenss

            )

            # Move the starting angle for the next slice
            current_angle = end_angle

            # Optional: Add labels
            label_x = int(margin_x + radius * 0.6 * math.cos(math.radians((current_angle + current_angle - angle) / 2)))
            label_y = int(margin_y + radius * 0.6 * math.sin(math.radians((current_angle + current_angle - angle) / 2)))
            
            
            # Draw the label
            font_path = os.path.join(os.path.dirname(__file__), '..', 'fonts', 'Helvetica.ttf')
            font = ImageFont.truetype(font_path, label_size)
            label_width = self.draw.textlength(label, font=font)
            # Position for the label (centered on the x_pos)
            label_x = label_x - label_width // 2  # Center text horizontally 
            self.draw.text((label_x, label_y), label, font=font, fill=Color.WHITE.rgb)





    def save(self, path='plot.png'):
        self.picture.save(path)


    def show(self):
        self.picture.show()
