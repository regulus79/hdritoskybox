from PIL import Image
import argparse
import cv2
import numpy as np
import math

parser = argparse.ArgumentParser(
    prog="python convert.py",
    description="Convert HDRIs into skyboxes"
)

parser.add_argument("input_path",type=str,help="Path to the input 360 image")
parser.add_argument("output_path",type=str,help="Path to where the script should save the skybox. NOTE: the program will automatically add '_top.png' and such to the end of the path, so it is best to give a path like 'images/my_skybox', so that it will save the 6 images to 'images/my_skybox_toppng' and so on.")
parser.add_argument("--brightness-scale",type=float,help="The multiplier for the brightness of the HDRI. By default, the output skybox is scaled so that the average brigthness of the HDRI is 255 in the output, since many HDRI's get very bright. Default: 1",nargs="?",default=1)
parser.add_argument("--width",type=int,help="The width of the output skybox images. Default: 256",nargs="?",default=256)
args=parser.parse_args()

input_path=args.input_path
output_path=args.output_path
brightness_scale=args.brightness_scale


# Read the HDRI, and fix the channel ordering
img=cv2.imread(input_path, cv2.IMREAD_ANYDEPTH)
img=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Save the average brightness for later when the final images are scaled.
average_value=np.average(img)

# Width of the output skybox images, default 256
width=args.width

# The direction parameter is a number from 0 to 6, in order of: x+, x-, y+, y-, z+, z-
def generate_tile(direction,width):
    tile=np.zeros((width,width,3))

    for x in range(-width//2,width//2):
        for y in range(-width//2,width//2):
            # Calculate initial yaw and pitch for direction = x+
            yaw=math.atan2(x,width//2)
            dist=math.sqrt(x*x+width/2*width/2)
            pitch=math.atan2(y,dist) + math.pi/2
            if direction==0:
                # Already done!
                pass
            if direction==1:
                # Turn about 180 degrees for back
                yaw+=math.pi
            if direction==2:
                # Turn 90 degrees for right
                yaw+=math.pi/2
            if direction==3:
                # Turn 270 degrees for left
                yaw+=3*math.pi/2
            if direction==4:
                # The top and bottom are more complicated.
                # Here, we recalculate the pitch and yaw for having the x,y above/below the origin, instead of to the side
                yaw=math.atan2(x,y)
                dist=math.sqrt(x*x+y*y)
                pitch=math.atan2(dist,width//2)
            if direction==5:
                # And make the pitch negative for the bottom. Numpy wraps negative indicies to an extent, so this works fine.
                yaw=-math.atan2(x,y)
                dist=math.sqrt(x*x+y*y)
                pitch=-math.atan2(dist,width//2)
            
            # Convert pitch and yaw into integer indicies
            x_index=round(yaw/2/math.pi*img.shape[1])
            y_index=round(pitch/math.pi*img.shape[0])

            #Write the correct pixel from the HDRI to the pixel of the skybox texture, and set the average HDRI brigthness ot be 255 (then multiplied by the user's scalar)
            tile[y+width//2,x+width//2]=img[y_index,x_index]*255/average_value*brightness_scale
    return tile

# Generate all six images
front=generate_tile(0,width)
back=generate_tile(1,width)
right=generate_tile(2,width)
left=generate_tile(3,width)
top=generate_tile(4,width)
bottom=generate_tile(5,width)

# Clamp them to make sure they are within 0-255
front=np.clip(front,0,255).astype("uint8")
back=np.clip(back,0,255).astype("uint8")
right=np.clip(right,0,255).astype("uint8")
left=np.clip(left,0,255).astype("uint8")
top=np.clip(top,0,255).astype("uint8")
bottom=np.clip(bottom,0,255).astype("uint8")

# Save them to the desired paths
Image.fromarray(front).save(output_path+"_front.png")
Image.fromarray(back).save(output_path+"_back.png")
Image.fromarray(right).save(output_path+"_right.png")
Image.fromarray(left).save(output_path+"_left.png")
Image.fromarray(top).save(output_path+"_top.png")
Image.fromarray(bottom).save(output_path+"_bottom.png")

print("Saved to: ")
print(output_path+"_front.png")
print(output_path+"_back.png")
print(output_path+"_right.png")
print(output_path+"_left.png")
print(output_path+"_top.png")
print(output_path+"_bottom.png")