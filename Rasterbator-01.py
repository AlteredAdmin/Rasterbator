from PIL import Image

def rasterbate(image_path, output_prefix, tile_size=(100, 100), overlap=10):
    # Open the image
    img = Image.open(image_path)
    img_width, img_height = img.size

    # Calculate the number of tiles
    num_tiles_x = img_width // (tile_size[0] - overlap)
    num_tiles_y = img_height // (tile_size[1] - overlap)

    # Loop through each tile and save it
    for y in range(num_tiles_y):
        for x in range(num_tiles_x):
            # Calculate coordinates for cropping
            left = x * (tile_size[0] - overlap)
            upper = y * (tile_size[1] - overlap)
            right = min(left + tile_size[0], img_width)
            lower = min(upper + tile_size[1], img_height)

            # Crop the tile
            tile = img.crop((left, upper, right, lower))

            # Save the tile
            tile.save(f"{output_prefix}_{x}_{y}.png")

if __name__ == "__main__":
    image_path = "input_image.jpg"  # Provide the path to your input image
    output_prefix = "output_tile"    # Prefix for output tiles
    tile_size = (100, 100)           # Size of each tile
    overlap = 10                     # Overlap between tiles

    rasterbate(image_path, output_prefix, tile_size, overlap)
