from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont



font = TTFont('HAL/fonts/InterVariable.ttf')

instance = instantiateVariableFont(font, {"wght": 800}, inplace=False)


instance.save("HAL/fonts/font_test.ttf")







from HAL.pixels import Picture, create_grid_of_pictures

pics = [Picture.from_file_path('flower_opening/F1H.png'),
        Picture.from_file_path('flower_opening/F2H.png'),
        Picture.from_file_path('flower_opening/F3H.png'),
        Picture.from_file_path('flower_opening/F4H.png'),
        Picture.from_file_path('flower_opening/F5H.png'),
        Picture.from_file_path('flower_opening/F6H.png')]

c = 450
for pic in pics: pic.crop(c, c, c, c)

grid = create_grid_of_pictures(pics, grid_size=(2, 3), image_size=(1000, 1000))
grid.image