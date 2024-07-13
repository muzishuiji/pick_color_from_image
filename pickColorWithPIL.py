from PIL import Image
import time

def get_dominant_colors(image_path, num_colors=10):
    start_time = time.time()
    image = Image.open(image_path)
    small_image = image.resize((80, 80))
    result = small_image.convert("P", palette=Image.ADAPTIVE, colors=num_colors)
    palette = result.getpalette()
    color_counts = sorted(result.getcolors(), reverse=True)
    colors = [tuple(palette[i*3:i*3+3]) for i in range(num_colors)]
    end_time = time.time()
    execute_time = (end_time - start_time) * 1000
    print(f"execute_time: {execute_time}", colors)
    return colors

get_dominant_colors('./images/cover1.jpg')