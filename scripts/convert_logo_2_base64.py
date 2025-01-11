import base64

def convert_image_to_base64(image_path):
    """
    Converts an image to a Base64-encoded string.
    
    :param image_path: Path to the image file.
    :return: Base64-encoded string of the image.
    """
    try:
        with open(image_path, "rb") as image_file:
            # Read the image file in binary mode
            image_data = image_file.read()
            
            # Convert the image to Base64
            base64_encoded = base64.b64encode(image_data).decode('utf-8')
            
            # Wrap the Base64 string in a data URI for embedding in HTML
            mime_type = "image/png" if image_path.lower().endswith(".png") else "image/jpeg"
            base64_logo = f"data:{mime_type};base64,{base64_encoded}"
            
            return base64_logo
    except FileNotFoundError:
        return "Error: File not found."
    except Exception as e:
        return f"Error: {e}"

# Example usage
image_path = r"../images/MyEngine1563x1563.png"  # Replace with your image path
base64_logo = convert_image_to_base64(image_path)

if base64_logo.startswith("Error"):
    print(base64_logo)
else:
    print("Base64-encoded logo:")
    print(base64_logo)
