from PIL import Image


def get_average_color(image_path):
    # Open the image
    img = Image.open(image_path)

    # Get image size
    width, height = img.size

    # Initialize variables to store total color values
    total_red = 0
    total_green = 0
    total_blue = 0

    # Loop through each pixel and accumulate color values
    for y in range(height):
        for x in range(width):
            pixel = img.getpixel((x, y))
            total_red += pixel[0]
            total_green += pixel[1]
            total_blue += pixel[2]

    # Calculate average color values
    num_pixels = width * height
    avg_red = total_red // num_pixels
    avg_green = total_green // num_pixels
    avg_blue = total_blue // num_pixels

    return avg_red, avg_green, avg_blue


if __name__ == "__main__":
    # Get the average color
    average_color = get_average_color("../media/img/vellum-plain-background-repeating.jpg")

    print("Average Color: {:02X}{:02X}{:02X}".format(*average_color))
