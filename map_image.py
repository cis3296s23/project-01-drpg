from PIL import Image, ImageDraw, ImageFont
import dungeon_generator

def generate_img(dungeon_obj, output_loc):
    # your 2D array of dungeon tiles
    dungeon = []
    for i in range(len(dungeon_obj)):
        dungeon.append([])
        for j in range(len(dungeon_obj[i])):
            # convert floor to 0 and emoty to 1
            if dungeon_obj[i][j] == dungeon_generator.Cells().floor or dungeon_obj[i][j] == dungeon_generator.Cells().player:
                dungeon[i].append(0)
            elif dungeon_obj[i][j] == dungeon_generator.Cells().door:
                dungeon[i].append(2)
            else:
                dungeon[i].append(1)
            
    print("done converting dungeon to 0s and 1s")    

    # load the wall and floor textures
    wall_texture = Image.open("dungeon_imgs/Wall.jpg")
    floor_texture = Image.open("dungeon_imgs/Floor.jpg")
    door_texture = Image.open("dungeon_imgs/Door.jpg")

    # set the size of each tile and grid cell in pixels
    tile_size = 20
    grid_size = 1

    # create a new blank image with the correct size
    width = len(dungeon[0]) * (tile_size + grid_size) + grid_size
    height = len(dungeon) * (tile_size + grid_size) + grid_size
    image = Image.new('RGB', (width, height), color=(255, 255, 255))

    # draw the tiles
    for y in range(len(dungeon)):
        for x in range(len(dungeon[0])):
            if dungeon[y][x] == 1:
                texture = wall_texture
            elif dungeon[y][x] == 0:
                texture = floor_texture
            elif dungeon[y][x] == 2:
                texture = door_texture
            x1 = x * (tile_size + grid_size) + grid_size
            y1 = y * (tile_size + grid_size) + grid_size
            x2 = x1 + tile_size
            y2 = y1 + tile_size
            image.paste(texture.resize((tile_size, tile_size)), (x1, y1))

    # draw the grid
    for y in range(len(dungeon) + 1):
        y_pos = y * (tile_size + grid_size)
        ImageDraw.Draw(image).line((0, y_pos, width, y_pos), fill=(0, 0, 0), width=grid_size)
    for x in range(len(dungeon[0]) + 1):
        x_pos = x * (tile_size + grid_size)
        ImageDraw.Draw(image).line((x_pos, 0, x_pos, height), fill=(0, 0, 0), width=grid_size)

    # add the labels for the rows and columns
    font = ImageFont.load_default()
    for y in range(len(dungeon)):
        label = chr(ord('a') + y)
        x_pos = 0
        y_pos = y * (tile_size + grid_size) + tile_size // 2
        ImageDraw.Draw(image).text((x_pos, y_pos), label, fill=(0, 0, 0), font=font)
    for x in range(len(dungeon[0])):
        label = str(x + 1)
        x_pos = x * (tile_size + grid_size) + tile_size // 2
        y_pos = 0
        ImageDraw.Draw(image).text((x_pos, y_pos), label, fill=(0, 0, 0), font=font)

    # save the image as a PNG file
    image.save(output_loc)


def place_token(original_image, token_image, token_pos, modified_image):
    # load the image and the goblin token image
    image = Image.open(original_image).convert("RGBA")
    goblin = Image.open(token_image).convert("RGBA")   

    # set the size and position of the token and the ellipse
    goblin_size = 50
    goblin_pos = ((token_pos[1]*21+1), (token_pos[0]*21+1))  # convert (row, col) to (x, y)
    ellipse_size = (20, 20)  # new size for the ellipse
    ellipse_pos = (goblin_pos[0] + goblin_size//2, goblin_pos[1] + goblin_size//2)

    print(f"Token image size: {goblin.size}")
    print(f"Ellipse size: {ellipse_size}")

    # resize the token image to match the size of the ellipse
    token = goblin.resize(ellipse_size)

    # create a new blank image with an alpha channel for the ellipse
    mask = Image.new("L", token.size, 0)  # updated size to match resized token image
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse((0, 0, ellipse_size[0], ellipse_size[1]), fill=255)

    # paste the token onto the ellipse
    image.paste(token, goblin_pos, mask=mask)

    # save the modified image
    image.save(modified_image)



if __name__ == '__main__':
    dobj = dungeon_generator.DungeonObj(6, 5, 16)
    generate_img(dobj.ascii, "output_imgs/dungeon.png")
    place_token("output_imgs/dungeon.png", "dungeon_imgs/Goblin.jpg", (15, 15), "output_imgs/dungeon_with_goblin.png")
