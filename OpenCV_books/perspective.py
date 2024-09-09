import cv2
import sys
import imgporc

im_to_read = sys.argv[1]
im_to_write = sys.argv[2]
points = []

img = cv2.imread(im_to_read)
img_cpy = img.copy()
cv2.imshow("image", img_cpy)



def add_point(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x,y))
        cv2.circle(img_cpy,(x,y),3,[0,0,0],-1)

        if len(points) == 4:
            height = 640
            width = 480
            ref_points = [(0,0),(width - 1,0),(width-1,height-1),(0,height-1)]
            params = imgporc.find_trans_points(points,ref_points)
            rectified_image = imgporc.corect_perspective(img,params, width, height)
            cv2.imshow("rectified image",rectified_image)
            cv2.imwrite(im_to_write, rectified_image)


cv2.setMouseCallback("image",add_point)


while True:
    cv2.imshow("image", img_cpy)
    key= cv2.waitKey(1)
    if key ==ord("q"):
        break


