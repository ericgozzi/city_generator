

from .color import Color, string_to_colors, colors_to_string
from .picture import Picture, get_blank_picture, superimpose_pictures


# IF First pixel (0, 0) of slot is RGB(0, 0, 255) -> Data as Integer



class MetaPicture:

    def __init__(self, picture: Picture):
        self.picture = picture

    
    def from_picture(picture: Picture):
        picture = picture.copy()
        pic_w = picture.width
        pic_h = picture.height

        if pic_w != 1000 or pic_h != 1000:
            picture.resize(1000, 1000, keep_aspect_ratio=False, crop=False)

        
        sketch = get_blank_picture(1024, 1024, Color(0, 0, 0))
        sketch.paste_picture(picture, 24, 24)
        sketch = MetaPicture(sketch)

        return sketch
    
    def copy(self):
        meta_picture = MetaPicture(self.picture)
        return meta_picture
        

    def show(self):
        self.picture.show()

        
    def set_slot_int(self, slot_number: int, data: int) -> None:

        data = get_blank_picture(24, 24, Color.from_integer(data))

        # The first pixel is blue -> integer
        data.image.putpixel((0, 0), (0, 0, 255))

        if slot_number <= 41:
            x = slot_number * 24
            y = 0
        elif slot_number > 41:
            x = 0
            y = (slot_number-41) * 24

        self.picture.paste_picture(data, x, y)


    def set_slot_string(self, slot_number: int, data: str) -> None:

        data_pic = get_blank_picture(24, 24, Color.GREEN)

        color_list = []

        # The first pixel is yellow(255, 255, 0) -> string
        color_list.append(Color.YELLOW)
        # Convert the string into list of colors
        for color in string_to_colors(data):
            color_list.append(color)
        # Last color of the string is yellow
        color_list.append(Color.YELLOW)

        color_counter = 0
        exit_loops = False
        for y in range(24):
            for x in range(24):
                data_pic.image.putpixel((x, y), color_list[color_counter].color)
                color_counter += 1
                
                if color_counter >= len(color_list):
                    exit_loops = True
                    break  # Break the inner loop

            if exit_loops:  # Break the outer loop if flag is set
                break

        if slot_number <= 41:
            x = slot_number * 24
            y = 0
        elif slot_number > 41:
            x = 0
            y = (slot_number-41) * 24

        self.picture.paste_picture(data_pic, x, y)





    def get_slot_data(self, slot_number: int):
        slot = self.get_slot(slot_number)

        # Get type pixel
        type_color = slot.image.getpixel((0, 0))

        if type_color == (0, 0, 255): # It is an INTEGER
            color = slot.image.getpixel((12, 12))
            color = Color(color[0], color[1], color[2])
            return color.as_integer()
        
        elif type_color == (255, 255, 0): # It is a STRING
            start_yellow = False
            end_yellow = False
            color_list = []
            for y in range(24):
                for x in range(24):
                    color = slot.image.getpixel((x, y))
                    if color == (255, 255, 0) and not start_yellow:
                        start_yellow = True
                    elif color == (255, 255, 0 and start_yellow):
                        end_yellow = True
                    else:
                        color_list.append(color)
                    
                    if start_yellow and end_yellow:
                        break
                
                if start_yellow and end_yellow:
                    break
            color_list = [Color(color[0], color[1], color[2]) for color in color_list]
            string = colors_to_string(color_list)
            return string


            



    def get_slot(self, slot_number: int) -> Picture:
        slot = self.copy()

        if slot_number <= 41:
            left = slot_number * 24
            top = 0
            right = slot_number * 24 + 24
            bottom = 24
        elif slot_number > 41:
            left = 0
            top = (slot_number-41) * 24
            right = 24
            bottom = (slot_number-41) * 24 + 24
            
        slot = slot.picture.image.crop((left, top, right, bottom))

        slot = Picture.from_PIL_image(slot)
        return slot
    


    


    def get_all_metadata(self) -> list[Picture]:
        metadata = [self.get_slot(i) for i in range(0, 82)]
        return metadata



    
    
    
    def get_main_picture(self):
        picture = self.picture.image
        picture = picture.crop((24, 24, 1024, 1024))
        return Picture.from_PIL_image(picture)