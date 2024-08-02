import streamlit as st
from PIL import Image, ImageFilter, ImageDraw, ImageFont, ImageEnhance, ImageOps
import io

# Image processing functions
def resize_image(image, size):
    return image.resize(size)

def convert_image_format(image, format):
    if format.lower() in ["jpeg", "jpg"]:
        image = image.convert("RGB")
    return image

def apply_filter(image, filter_type):
    if filter_type == 'grayscale':
        image = image.convert("L")
    elif filter_type == 'sepia':
        image = image.convert("RGB")
        width, height = image.size
        pixels = image.load()
        for py in range(height):
            for px in range(width):
                r, g, b = image.getpixel((px, py))
                tr = int(0.393 * r + 0.769 * g + 0.189 * b)
                tg = int(0.349 * r + 0.686 * g + 0.168 * b)
                tb = int(0.272 * r + 0.534 * g + 0.131 * b)
                pixels[px, py] = (min(255, tr), min(255, tg), min(255, tb))
    elif filter_type == 'blur':
        image = image.filter(ImageFilter.BLUR)
    return image

def add_watermark(image, watermark_text, position):
    image = image.convert("RGBA")
    width, height = image.size
    txt = Image.new('RGBA', image.size, (255, 255, 255, 0))
    font = ImageFont.truetype("arial.ttf", 36)
    d = ImageDraw.Draw(txt)
    text_bbox = d.textbbox((0, 0), watermark_text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    if position == 'center':
        position = ((width - text_width) // 2, (height - text_height) // 2)
    elif position == 'bottom_right':
        position = (width - text_width - 10, height - text_height - 10)
    d.text(position, watermark_text, fill=(255, 255, 255, 128), font=font)
    watermarked = Image.alpha_composite(image, txt)
    return watermarked

def rotate_image(image, angle):
    return image.rotate(angle, expand=True)

def crop_image(image, left, top, right, bottom):
    return image.crop((left, top, right, bottom))

def flip_image(image, mode):
    if mode == 'horizontal':
        return image.transpose(Image.FLIP_LEFT_RIGHT)
    elif mode == 'vertical':
        return image.transpose(Image.FLIP_TOP_BOTTOM)

def adjust_brightness(image, factor):
    enhancer = ImageEnhance.Brightness(image)
    return enhancer.enhance(factor)

def adjust_contrast(image, factor):
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(factor)

def adjust_sharpness(image, factor):
    enhancer = ImageEnhance.Sharpness(image)
    return enhancer.enhance(factor)

def draw_text(image, text, position, font_size=36, font_color=(255, 255, 255)):
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("arial.ttf", font_size)
    draw.text(position, text, fill=font_color, font=font)
    return image

def draw_rectangle(image, position, outline_color=(255, 0, 0), width=5):
    draw = ImageDraw.Draw(image)
    draw.rectangle(position, outline=outline_color, width=width)
    return image

def add_border(image, border_size, color=(0, 0, 0)):
    return ImageOps.expand(image, border=border_size, fill=color)

def resize_with_aspect_ratio(image, max_size):
    image.thumbnail((max_size, max_size))
    return image

def convert_color_mode(image, mode):
    return image.convert(mode)

# Streamlit UI
def main():
    st.title("Image Processing Application")

    uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption='Original Image', use_column_width=True)

        st.sidebar.title("Image Processing Options")

        # Initialize a mutable variable to hold the modified image
        modified_image = image

        # Resize
        st.sidebar.subheader("Resize Image")
        width = st.sidebar.number_input("Width", min_value=1, value=image.width)
        height = st.sidebar.number_input("Height", min_value=1, value=image.height)
        if st.sidebar.checkbox("Apply Resize"):
            modified_image = resize_image(modified_image, (width, height))

        # Rotate
        st.sidebar.subheader("Rotate Image")
        angle = st.sidebar.slider("Angle", 0, 360, 0)
        if st.sidebar.checkbox("Apply Rotate"):
            modified_image = rotate_image(modified_image, angle)

        # Crop
        st.sidebar.subheader("Crop Image")
        left = st.sidebar.number_input("Left", min_value=0, value=0)
        top = st.sidebar.number_input("Top", min_value=0, value=0)
        right = st.sidebar.number_input("Right", min_value=1, value=image.width)
        bottom = st.sidebar.number_input("Bottom", min_value=1, value=image.height)
        if st.sidebar.checkbox("Apply Crop"):
            modified_image = crop_image(modified_image, left, top, right, bottom)

        # Flip
        st.sidebar.subheader("Flip Image")
        flip_mode = st.sidebar.selectbox("Mode", ["None", "Horizontal", "Vertical"])
        if flip_mode != "None" and st.sidebar.checkbox("Apply Flip"):
            modified_image = flip_image(modified_image, flip_mode.lower())

        # Adjust Brightness
        st.sidebar.subheader("Adjust Brightness")
        brightness_factor = st.sidebar.slider("Brightness Factor", 0.1, 2.0, 1.0)
        if st.sidebar.checkbox("Apply Brightness"):
            modified_image = adjust_brightness(modified_image, brightness_factor)

        # Adjust Contrast
        st.sidebar.subheader("Adjust Contrast")
        contrast_factor = st.sidebar.slider("Contrast Factor", 0.1, 2.0, 1.0)
        if st.sidebar.checkbox("Apply Contrast"):
            modified_image = adjust_contrast(modified_image, contrast_factor)

        # Adjust Sharpness
        st.sidebar.subheader("Adjust Sharpness")
        sharpness_factor = st.sidebar.slider("Sharpness Factor", 0.1, 2.0, 1.0)
        if st.sidebar.checkbox("Apply Sharpness"):
            modified_image = adjust_sharpness(modified_image, sharpness_factor)

        # Draw Text
        st.sidebar.subheader("Draw Text")
        text = st.sidebar.text_input("Text", "Sample Text")
        text_x = st.sidebar.number_input("Text X Position", min_value=0, value=10)
        text_y = st.sidebar.number_input("Text Y Position", min_value=0, value=10)
        if st.sidebar.checkbox("Apply Text"):
            modified_image = draw_text(modified_image, text, (text_x, text_y))

        # Draw Rectangle
        st.sidebar.subheader("Draw Rectangle")
        rect_left = st.sidebar.number_input("Rectangle Left", min_value=0, value=0)
        rect_top = st.sidebar.number_input("Rectangle Top", min_value=0, value=0)
        rect_right = st.sidebar.number_input("Rectangle Right", min_value=1, value=image.width)
        rect_bottom = st.sidebar.number_input("Rectangle Bottom", min_value=1, value=image.height)
        if st.sidebar.checkbox("Apply Rectangle"):
            modified_image = draw_rectangle(modified_image, (rect_left, rect_top, rect_right, rect_bottom))

        # Add Border
        st.sidebar.subheader("Add Border")
        border_size = st.sidebar.number_input("Border Size", min_value=1, value=10)
        border_color = st.sidebar.color_picker("Border Color", "#000000")
        if st.sidebar.checkbox("Apply Border"):
            modified_image = add_border(modified_image, border_size, color=border_color)

        # Resize with Aspect Ratio
        st.sidebar.subheader("Resize with Aspect Ratio")
        max_size = st.sidebar.number_input("Max Size", min_value=1, value=512)
        if st.sidebar.checkbox("Apply Resize with Aspect Ratio"):
            modified_image = resize_with_aspect_ratio(modified_image, max_size)

        # Convert Color Mode
        st.sidebar.subheader("Convert Color Mode")
        color_mode = st.sidebar.selectbox("Color Mode", ["RGB", "L", "RGBA", "CMYK"])
        if st.sidebar.checkbox("Apply Color Mode"):
            modified_image = convert_color_mode(modified_image, color_mode)

        # Convert Format
        st.sidebar.subheader("Convert Image Format")
        format = st.sidebar.selectbox("Format", ["PNG", "JPEG", "BMP", "GIF"])
        if st.sidebar.checkbox("Apply Format Conversion"):
            modified_image = convert_image_format(modified_image, format)

        # Apply Filter
        st.sidebar.subheader("Apply Filter")
        filter_type = st.sidebar.selectbox("Filter", ["None", "Grayscale", "Sepia", "Blur"])
        if filter_type != "None" and st.sidebar.checkbox("Apply Filter"):
            modified_image = apply_filter(modified_image, filter_type.lower())

        # Add Watermark
        st.sidebar.subheader("Add Watermark")
        watermark_text = st.sidebar.text_input("Watermark Text", "Sample Watermark")
        position = st.sidebar.selectbox("Position", ["Center", "Bottom Right"])
        if st.sidebar.checkbox("Apply Watermark"):
            modified_image = add_watermark(modified_image, watermark_text, position.lower())

        st.image(modified_image, caption='Modified Image', use_column_width=True)

        # Download modified image
        buf = io.BytesIO()
        modified_image.save(buf, format="PNG")
        st.download_button(label="Download Modified Image", data=buf.getvalue(), file_name="modified_image.png", mime="image/png")

if __name__ == '__main__':
    main()
