import cv2

def get_roi(image, x1, x2, y1, y2):
    """Extract and display the ROI from the image based on given coordinates."""
    roi = image[int(y1):int(y2), int(x1):int(x2)]
    return roi

def main():
    # Load an image (change 'input_image.png' to your image file)
    image_path = 'src_img.png'  # Path to your input image
    image = cv2.imread(image_path)

    if image is None:
        print("Error: Image not found.")
        return

    while True:
        # Display the original image

        # Input for ROI parameters
        params = input("Enter x1, x2, y1, y2 (or 'exit' to quit): ")

        if params.lower() == 'exit':
            break

        try:
            # Parse the input
            x1, x2, y1, y2 = map(float, params.split())

            # Get the ROI
            roi = get_roi(image, x1 * image.shape[1], x2 * image.shape[1], y1 * image.shape[0], y2 * image.shape[0])

            # Display the ROI
            cv2.imshow('ROI', roi)

            # Wait for a key press before moving on
            cv2.waitKey(0)

        except ValueError:
            print("Invalid input. Please enter four numbers separated by spaces.")

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()