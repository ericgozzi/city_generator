import math
import colorsys

class Color:
    """
    Color Class

    Represents a color.

    Attributes:
        red (int): Red component (0–255).
        green (int): Green component (0–255).
        blue (int): Blue component (0–255).
    """



    

    def __init__(self, red, green, blue):
        """
        Initializes a Color instance with RGB values.

        Args:
            red (int): Red component (0–255).
            green (int): Green component (0–255).
            blue (int): Blue component (0–255).
        """
        self.red = red
        self.green = green
        self.blue = blue







    def __str__(self) -> str:
        """
        Returns a string representation of the color using ANSI background color escape codes.

        This allows the color to be displayed as a colored block in compatible terminals.
        """
        return f"\033[48;2;{self.red};{self.green};{self.blue}m  \033[0m"
    





    def __repr__(self) -> str:
        """
        Returns a developer-friendly string representation of the color as a colored block.

        Mirrors the behavior of __str__ for quick previews in terminal-based debugging or REPLs.
        """
        return f"\033[48;2;{self.red};{self.green};{self.blue}m  \033[0m"





    

    #OPERATOR METHODS

    def __add__(self, other: 'Color') -> 'Color':
        """
        Adds two Color instances by combining their RGB values, clamped between 0–255.
        """
        if isinstance(other, Color):
            # You can call a custom function here, for example:
            return add_colors(self, other)
        else:
            raise ValueError("You can only add another Color instance")
        




    
    def __sub__(self, other: 'Color') -> 'Color':
        """
        Subtracts one Color instance from another by RGB values, clamped between 0–255.
        """
        if isinstance(other, Color):
            # You can call a custom function here, for example:
            return subtract_colors(self, other)
        else:
            raise ValueError("You can only subtract another Color instance")







    # CONSTRUCTORS
    @classmethod
    def from_rgb(cls, red: int, green: int, blue: int):
        """
        Initiliaze the color from a RGB values.

        Args:
            red (int): The red value in the range (0 - 255)
            green (int): The green value in the range (0 - 255)
            blue (int): The blue value in the range (0 - 255)

        Returns
            Color: A color object
        """
        return cls(red, green, blue)
    




    @classmethod
    def from_hsv(cls, h, s, v):
        """
        Constructs from HSV (Hue, Saturation, Value) to RGB and return a Color object.

        Args:
            h (float): The hue in degrees (0–360).
            s (float): The saturation (0–1).
            v (float): The value (brightness) (0–1).

        Returns:
            Color: A Color object representing the color in RGB.
        """
        h = h / 360  # Normalize the hue to [0, 1] range
        s = max(0, min(s, 1))  # Saturation must be in [0, 1]
        v = max(0, min(v, 1))  # Value must be in [0, 1]

        c = v * s
        x = c * (1 - abs((h * 6) % 2 - 1))
        m = v - c

        if 0 <= h < 1/6:
            r, g, b = c, x, 0
        elif 1/6 <= h < 2/6:
            r, g, b = x, c, 0
        elif 2/6 <= h < 3/6:
            r, g, b = 0, c, x
        elif 3/6 <= h < 4/6:
            r, g, b = 0, x, c
        elif 4/6 <= h < 5/6:
            r, g, b = x, 0, c
        else:
            r, g, b = c, 0, x

        r = int((r + m) * 255)
        g = int((g + m) * 255)
        b = int((b + m) * 255)

        return Color(r, g, b)
    




    @classmethod
    def from_hsl(cls, h, s, l):
        """
        Convert from HSL (Hue, Saturation, Lightness) to RGB and return a Color object.

        Args:
            h (float): The hue in degrees (0–360).
            s (float): The saturation (0–1).
            l (float): The lightness (0–1).

        Returns:
            Color: A Color object representing the color in RGB.
        """
        h = h / 360  # Normalize the hue to [0, 1]
        s = max(0, min(s, 1))  # Saturation must be in [0, 1]
        l = max(0, min(l, 1))  # Lightness must be in [0, 1]

        c = (1 - abs(2 * l - 1)) * s
        x = c * (1 - abs((h * 6) % 2 - 1))
        m = l - c / 2

        if 0 <= h < 1 / 6:
            r, g, b = c, x, 0
        elif 1 / 6 <= h < 2 / 6:
            r, g, b = x, c, 0
        elif 2 / 6 <= h < 3 / 6:
            r, g, b = 0, c, x
        elif 3 / 6 <= h < 4 / 6:
            r, g, b = 0, x, c
        elif 4 / 6 <= h < 5 / 6:
            r, g, b = x, 0, c
        else:
            r, g, b = c, 0, x

        r = int((r + m) * 255)
        g = int((g + m) * 255)
        b = int((b + m) * 255)

        return Color(r, g, b)
    





    # CONVERTERS
    @property
    def cmyk(self) -> tuple:
        """
        Convertes the color to the cmyk format.

        Returns:
            tuple(4): A 4 dimensional color with (C, M, Y, K) values.
        """
        r = self.red
        g = self.green
        b = self.blue
        # Find the Key (Black) value
        k = 1 - max(r, g, b)

        if k < 1:  # If not black
            c = (1 - r - k) / (1 - k)
            m = (1 - g - k) / (1 - k)
            y = (1 - b - k) / (1 - k)
        else:  # If black
            c = m = y = 0

        # Convert CMYK to percentage (0-100 scale)
        return (c * 100, m * 100, y * 100, k * 100)
    






    @property
    def hex(self) -> str:
        """
        Convert RGB values (0–255) to a HEX string.

        Returns:
            str: The color represented as a HEX string (e.g., '#FF5733').
        """
        return "#{:02X}{:02X}{:02X}".format(self.red, self.green, self.blue)
    







    @property
    def xyz(self) -> tuple:
        """
        Convert RGB values (0–255) to CIE XYZ color space.

        The conversion uses the sRGB color space with the D65 illuminant.

        Returns:
            tuple: The XYZ values rounded to four decimal places.
        """

        # Normalize RGB values to [0, 1]
        r = self.red / 255.0
        g = self.green / 255.0
        b = self.blue / 255.0

        # Apply gamma correction
        def gamma(c):
            return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

        r, g, b = gamma(r), gamma(g), gamma(b)

        # Convert to XYZ using sRGB matrix (D65)
        x = r * 0.4124 + g * 0.3576 + b * 0.1805
        y = r * 0.2126 + g * 0.7152 + b * 0.0722
        z = r * 0.0193 + g * 0.1192 + b * 0.9505

        return (round(x, 4), round(y, 4), round(z, 4))
    







    @property
    def lab(self) -> tuple:
        """
        Convert RGB (0–255) to CIELAB (L*, a*, b*) using D65 reference white.

        Returns:
            tuple: The LAB values (L*, a*, b*) rounded to four decimal places.
        """

        # First, convert to XYZ
        x, y, z = self.xyz

        # Normalize using D65 reference white
        x /= 0.95047
        y /= 1.00000
        z /= 1.08883

        # Helper for nonlinear transformation
        def f(t):
            return t ** (1 / 3) if t > 0.008856 else (7.787 * t + 16 / 116)

        fx, fy, fz = f(x), f(y), f(z)

        L = 116 * fy - 16
        a = 500 * (fx - fy)
        b = 200 * (fy - fz)

        return (round(L, 4), round(a, 4), round(b, 4))
    






    @property
    def hsl(self):
        """
        Return the color as HSL (Hue 0–360, Saturation 0–1, Lightness 0–1).

        Returns:
            tuple: The HSL values (Hue, Saturation, Lightness) rounded to two and four decimal places respectively.
        """

        r, g, b = self.red / 255.0, self.green / 255.0, self.blue / 255.0
        max_c = max(r, g, b)
        min_c = min(r, g, b)
        delta = max_c - min_c

        # Lightness
        l = (max_c + min_c) / 2

        # Saturation
        if delta == 0:
            s = 0
            h = 0  # undefined hue for gray
        else:
            s = delta / (1 - abs(2 * l - 1))

            # Hue
            if max_c == r:
                h = ((g - b) / delta) % 6
            elif max_c == g:
                h = (b - r) / delta + 2
            else:  # max_c == b
                h = (r - g) / delta + 4
            h *= 60  # convert to degrees

        return (round(h, 2), round(s, 4), round(l, 4))
    






    
    @property
    def hsv(self):
        """Return color as HSV (Hue 0–360, Saturation 0–1, Value 0–1)."""
        r, g, b = self.red / 255.0, self.green / 255.0, self.blue / 255.0
        max_c = max(r, g, b)
        min_c = min(r, g, b)
        delta = max_c - min_c

        # Hue
        if delta == 0:
            h = 0
        elif max_c == r:
            h = ((g - b) / delta) % 6
        elif max_c == g:
            h = (b - r) / delta + 2
        else:
            h = (r - g) / delta + 4
        h *= 60

        # Saturation
        s = 0 if max_c == 0 else delta / max_c

        # Value
        v = max_c

        return (round(h, 2), round(s, 4), round(v, 4))

    




    @property
    def rgb(self):
        """
        Return the color as an RGB tuple (Red, Green, Blue).

        Returns:
            tuple: The RGB values as a tuple (Red, Green, Blue) in the range 0–255.
        """
        return (self.red, self.green, self.blue)





    # METHODS ON COLOWHEEL

    def get_complementary(self):
        """
        Returns the complementary color.

        Complementary colors are those that are opposite each other on the color wheel.
        This method works by shifting the hue by 180 degrees.

        Returns:
            Color: A new Color object representing the complementary color.
        """
        h, s, v = self.hsv
        h += 180
        return Color.from_hsv(h, s, v)
    






    def get_analogus(self, n=3, angle = 30):
        """
        Returns a list of analogous colors. Analogous colors are colors that are next to each other on the color wheel.

        Args:
            n (int): The number of analogous colors to generate. Must be an even number (default is 3).
            angle (int): The angle between each analogous color on the color wheel (default is 30 degrees).

        Returns:
            list: A list of Color objects representing the analogous colors.
        """
        if n % 2 != 0:
            n -= 1
        n = int(n/2)

        h, s, v = self.hsv
        colors = []
        for i in range(-angle*n, angle*n+1, angle):
            color = Color.from_hsv(h + i, s, v)
            colors.append(color)
        return colors
    

    # CONSTANTS
    @classmethod
    def constants(cls):

        #: Pure red color (RGB: 255, 0, 0)
        cls.RED = cls(255, 0, 0)

        #: Pure green color (RGB: 0, 255, 0)
        cls.GREEN = cls(0, 255, 0)

        #: Pure blue color (RGB: 0, 0, 255)
        cls.BLUE = cls(0, 0, 255)

        #: Yellow color, a mix of red and green (RGB: 255, 255, 0)
        cls.YELLOW = cls(255, 255, 0)

        #: Cyan color, a mix of green and blue (RGB: 0, 255, 255)
        cls.CYAN = cls(0, 255, 255)

        #: Magenta color, a mix of red and blue (RGB: 255, 0, 255)
        cls.MAGENTA = cls(255, 0, 255)

        #: Pure white color (RGB: 255, 255, 255)
        cls.WHITE = cls(255, 255, 255)

        #: Very light gray, slightly darker than white (RGB: 192, 192, 192)
        cls.VERY_LIGHT_GRAY = cls(192, 192, 192)

        #: Light gray color (RGB: 192, 192, 192)
        cls.LIGHT_GRAY = cls(192, 192, 192)

        #: Moderate light gray, between light gray and white (RGB: 224, 224, 224)
        cls.MODERATE_LIGHT_GRAY = cls(224, 224, 224)

        #: Neutral gray, midway between black and white (RGB: 128, 128, 128)
        cls.GRAY = cls(128, 128, 128)

        #: Moderate dark gray, slightly darker than neutral gray (RGB: 96, 96, 96)
        cls.MODERATE_DARK_GRAY = cls(96, 96, 96)

        #: Dark gray, significantly darker than neutral gray (RGB: 80, 80, 80)
        cls.DARK_GRAY = cls(80, 80, 80)

        #: Very dark gray, close to black but not completely black (RGB: 64, 64, 64)
        cls.VERY_DARK_GRAY = cls(64, 64, 64)

        #: Pure black color (RGB: 0, 0, 0)
        cls.BLACK = cls(0, 0, 0)

        #: Orange color (RGB: 255, 165, 0)
        cls.ORANGE = cls(255, 165, 0)

        #: Purple color (RGB: 128, 0, 128)
        cls.PURPLE = cls(128, 0, 128)

        #: Brown color (RGB: 165, 42, 42)
        cls.BROWN = cls(165, 42, 42)

        #: Pink color (RGB: 255, 192, 203)
        cls.PINK = cls(255, 192, 203)

        #: Violet color (RGB: 238, 130, 238)
        cls.VIOLET = cls(238, 130, 238)

        #: Indigo color (RGB: 75, 0, 130)
        cls.INDIGO = cls(75, 0, 130)

        #: Teal color (RGB: 0, 128, 128)
        cls.TEAL = cls(0, 128, 128)

        #: Gold color (RGB: 255, 215, 0)
        cls.GOLD = cls(255, 215, 0)

        #: Coral color (RGB: 255, 127, 80)
        cls.CORAL = cls(255, 127, 80)

        #: Turquoise color (RGB: 64, 224, 208)
        cls.TURQUOISE = cls(64, 224, 208)

        #: Rose color (RGB: 255, 0, 128)
        cls.ROSE = cls(255, 0, 128)

        #: Heliotrope color (RGB: 223, 115, 255)
        cls.HELIOTROPE = cls(223, 115, 255)

        #: Azure color (RGB: 0, 127, 255)
        cls.AZURE = cls(0, 127, 255)

        #: Sea Green color (RGB: 46, 139, 87)
        cls.SEA_GREEN = cls(46, 139, 87)

        #: Spring Green color (RGB: 0, 250, 154)
        cls.SPRING_GREEN = cls(0, 250, 154)

        #: Olive color (RGB: 107, 142, 35)
        cls.OLIVE = cls(107, 142, 35)

        #: Yellow Green color (RGB: 154, 205, 50)
        Color.YELLOW_GREEN = cls(154, 205, 50)

        #: Army Green color (RGB: 75, 83, 32)
        Color.ARMY_GREEN = cls(75, 83, 32)








    # Strange things happening down here, don't look!

    @classmethod
    def rgb_distance(cls, color1, color2):
        """Calculate the Euclidean distance between two RGB colors."""
        r1, g1, b1 = color1.rgb
        r2, g2, b2 = color2.rgb
        return math.sqrt((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2)

    




    def as_integer(self):
        integer = self.red + self.green + self.blue
        return integer


    @classmethod
    def from_integer(cls, integer: int):
        red, green, blue = 0, 0, 0
        if integer > 255:
            red = 255
            integer -= 255
        else:
            red = integer
            return Color(red, green, blue)
        if integer > 255:
            green = 255
            integer -= 255
        else:
            green = integer
            return Color(red, green, blue)

        if integer > 255:
            raise ValueError("Integer too big")
        else:
            blue = integer
            return Color(red, green, blue)


    def as_char(self):
        """
        Decodes a single character from an RGB color.
        """
        if not (isinstance(self.color, tuple) and len(self.color) == 3):
            raise ValueError("Color must be a tuple of (R, G, B).")

        r, g, b = self.color
        if not (0 <= r <= 255):
            raise ValueError("Red channel must be between 0 and 255.")
        return chr(g)

    @classmethod
    def from_char(cls, char: str):
        """
        Encodes a single character to an RGB color.
        """
        if len(char) != 1:
            raise ValueError("Input must be a single character.")

        ascii_val = ord(char)
        if not 0 <= ascii_val <= 255:
            raise ValueError("Character out of ASCII range.")

        # Encode ASCII value into the Red channel
        return cls(0, ascii_val, 0)

    @classmethod
    def constants(cls):

        #: Pure red color (RGB: 255, 0, 0)
        cls.RED = cls(255, 0, 0)

        #: Pure green color (RGB: 0, 255, 0)
        cls.GREEN = cls(0, 255, 0)

        #: Pure blue color (RGB: 0, 0, 255)
        cls.BLUE = cls(0, 0, 255)

        #: Yellow color, a mix of red and green (RGB: 255, 255, 0)
        cls.YELLOW = cls(255, 255, 0)

        #: Cyan color, a mix of green and blue (RGB: 0, 255, 255)
        cls.CYAN = cls(0, 255, 255)

        #: Magenta color, a mix of red and blue (RGB: 255, 0, 255)
        cls.MAGENTA = cls(255, 0, 255)

        #: Pure white color (RGB: 255, 255, 255)
        cls.WHITE = cls(255, 255, 255)

        #: Very light gray, slightly darker than white (RGB: 192, 192, 192)
        cls.VERY_LIGHT_GRAY = cls(192, 192, 192)

        #: Light gray color (RGB: 192, 192, 192)
        cls.LIGHT_GRAY = cls(192, 192, 192)

        #: Moderate light gray, between light gray and white (RGB: 224, 224, 224)
        cls.MODERATE_LIGHT_GRAY = cls(224, 224, 224)

        #: Neutral gray, midway between black and white (RGB: 128, 128, 128)
        cls.GRAY = cls(128, 128, 128)

        #: Moderate dark gray, slightly darker than neutral gray (RGB: 96, 96, 96)
        cls.MODERATE_DARK_GRAY = cls(96, 96, 96)

        #: Dark gray, significantly darker than neutral gray (RGB: 80, 80, 80)
        cls.DARK_GRAY = cls(80, 80, 80)

        #: Very dark gray, close to black but not completely black (RGB: 64, 64, 64)
        cls.VERY_DARK_GRAY = cls(64, 64, 64)

        #: Pure black color (RGB: 0, 0, 0)
        cls.BLACK = cls(0, 0, 0)

        #: Orange color (RGB: 255, 165, 0)
        cls.ORANGE = cls(255, 165, 0)

        #: Purple color (RGB: 128, 0, 128)
        cls.PURPLE = cls(128, 0, 128)

        #: Brown color (RGB: 165, 42, 42)
        cls.BROWN = cls(165, 42, 42)

        #: Pink color (RGB: 255, 192, 203)
        cls.PINK = cls(255, 192, 203)

        #: Violet color (RGB: 238, 130, 238)
        cls.VIOLET = cls(238, 130, 238)

        #: Indigo color (RGB: 75, 0, 130)
        cls.INDIGO = cls(75, 0, 130)

        #: Teal color (RGB: 0, 128, 128)
        cls.TEAL = cls(0, 128, 128)

        #: Gold color (RGB: 255, 215, 0)
        cls.GOLD = cls(255, 215, 0)

        #: Coral color (RGB: 255, 127, 80)
        cls.CORAL = cls(255, 127, 80)

        #: Turquoise color (RGB: 64, 224, 208)
        cls.TURQUOISE = cls(64, 224, 208)

        #: Rose color (RGB: 255, 0, 128)
        cls.ROSE = cls(255, 0, 128)

        #: Heliotrope color (RGB: 223, 115, 255)
        cls.HELIOTROPE = cls(223, 115, 255)

        #: Azure color (RGB: 0, 127, 255)
        cls.AZURE = cls(0, 127, 255)

        #: Sea Green color (RGB: 46, 139, 87)
        cls.SEA_GREEN = cls(46, 139, 87)

        #: Spring Green color (RGB: 0, 250, 154)
        cls.SPRING_GREEN = cls(0, 250, 154)

        #: Olive color (RGB: 107, 142, 35)
        cls.OLIVE = cls(107, 142, 35)

        #: Yellow Green color (RGB: 154, 205, 50)
        Color.YELLOW_GREEN = cls(154, 205, 50)

        #: Army Green color (RGB: 75, 83, 32)
        Color.ARMY_GREEN = cls(75, 83, 32)


def string_to_colors(text: str) -> list[Color]:
    """Encodes a string into a list of RGB colors."""
    return [Color.from_char(c) for c in text]


def colors_to_string(colors) -> str:
    """Decodes a string from a list of RGB colors."""
    return ''.join(color.as_char() for color in colors)



def add_colors(color1, color2):
        # Add corresponding RGB values, ensuring no value exceeds 255
        r = min(color1.red + color2.red, 255)
        g = min(color1.green + color2.green, 255)
        b = min(color1.blue + color2.blue, 255)
        return Color(r, g, b)

def subtract_colors(color1, color2):
        r = max(color1.red - color2.red, 0)
        g = max(color1.green - color2.green, 0)
        b = max(color1.blue - color2.blue, 0)
        return Color(r, g, b)






