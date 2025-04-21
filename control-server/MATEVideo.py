import cv2
import os

image_folder = "/Users/anyali/Downloads/MATE Map Images"

images = [img for img in os.listdir(image_folder) if img.endswith(('.PNG', '.jpg', '.jpeg'))]
images.sort()

frame_width = 480  
frame_height = 640 
output_file = "output_video.avi" 
fps = 1  

fourcc = cv2.VideoWriter_fourcc(*'DIVX')
out = cv2.VideoWriter(output_file, fourcc, fps, (frame_width, frame_height))

font = cv2.FONT_HERSHEY_SIMPLEX

org = (50, 50)

fontScale = 1
 
color = (0, 0, 255)

thickness = 2

print(len(images))
year = 2016
i=0
for image in images:

    img_path = os.path.join(image_folder, image)
    print(f"Processing image: {img_path}")

    img = cv2.imread(img_path)
    if img is None:
        print(f"Warning: Could not load image {img_path}. Skipping...")
        continue

    img_resized = cv2.resize(img, (frame_width, frame_height))
    text = str(2016+i)
    imageText = cv2.putText(img_resized, text, org, font, fontScale, color, thickness, cv2.LINE_AA)
    out.write(img_resized)
    i=i+1

out.release()
print(f"Video saved as {output_file}")
