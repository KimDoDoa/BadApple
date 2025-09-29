import cv2
import numpy as np
import os
import time


ASCII_CHARS = " .,:;!coOC#@"


VIDEO_PATH = 'BadApple.mp4'


ASCII_WIDTH = 120


FRAME_DELAY = 1.0 / 30.0



def clear_console():
    """
    Clears the console screen, works on both Windows and Unix-based systems.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def convert_to_ascii(image, char_set):
    """
    Converts a grayscale image to a string of ASCII characters.

    Args:
        image (numpy.ndarray): The grayscale image array.
        char_set (str): The string of ASCII characters to use.

    Returns:
        str: The ASCII art representation of the image.
    """
  
    normalized_pixels = np.interp(image.flatten(), (0, 255), (0, len(char_set) - 1))
    
    
    ascii_string = "".join([char_set[int(pixel_value)] for pixel_value in normalized_pixels])

    return ascii_string

def get_resized_image(frame, width):
    """
    Resizes a frame to the specified width while maintaining its aspect ratio.

    Args:
        frame (numpy.ndarray): The video frame.
        width (int): The target width.

    Returns:
        numpy.ndarray: The resized image.
    """
    (h, w) = frame.shape[:2]
    
    aspect_ratio = w / float(h)
    new_height = int(width / aspect_ratio / 2) 
    
    return cv2.resize(frame, (width, new_height))



def main():
    """
    Main function to run the Bad Apple!! ASCII art player.
    """
    
    cap = cv2.VideoCapture(VIDEO_PATH)

    
    if not cap.isOpened():
        print(f"Error: Could not open video file '{VIDEO_PATH}'.")
        return

   
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_delay = 1.0 / fps

    try:
        while True:
            
            ret, frame = cap.read()

            # If frame is not read correctly, break the loop
            if not ret:
                break

            
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            
            resized_frame = get_resized_image(gray_frame, ASCII_WIDTH)

            
            ascii_art = convert_to_ascii(resized_frame, ASCII_CHARS)

            
            (h, w) = resized_frame.shape[:2]
            lines = [ascii_art[i:i + w] for i in range(0, len(ascii_art), w)]
            output = "\n".join(lines)

            
            clear_console()
            print(output, end='')

            
            time.sleep(frame_delay)

    except KeyboardInterrupt:
        print("\nPlayback stopped by user.")
    finally:
        
        cap.release()
        cv2.destroyAllWindows()
        print("Video playback finished.")

if __name__ == "__main__":
    main()
