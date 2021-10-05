import cv2 
import numpy as np

def filter_image(colors,image):
    # Read in image and create black canvas of same shape
    img = cv2.imread(image)
    canvas = np.zeros(img.shape)
    
    color_list = colors.split()

    # BLUE [:,:,0] GREEN [:,:,1] RED: [:.:.2]
    color_dict = {
                    'blue':0,
                    'Blue':0,
                    'green':1,
                    'Green':1,
                    'red':2,
                    'Red':2
                }

    if colors == 'gray' or colors == 'Gray':
      canvas = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    elif colors == 'b&w' or colors == 'B&w':
      canvas = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
      _,canvas = cv2.threshold(canvas,127,255,cv2.THRESH_BINARY)
    elif colors == 'edges' or colors =='Edges': 
      canvas = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
      canvas = cv2.GaussianBlur(canvas,(3,3),sigmaX=0)
      canvas = cv2.Canny(canvas,25,75)
    elif len(color_list) == 2:   
        # Converting color names to values         
        color_list[0] = color_dict[color_list[0]]
        color_list[1] = color_dict[color_list[1]]
       
        # Pasting onto canvas
        canvas[:,:,color_list[0]] = img[:,:,color_list[0]]
        canvas[:,:,color_list[1]] = img[:,:,color_list[1]]
    else:
        color_list[0] = color_dict[color_list[0]]
        canvas[:,:,color_list[0]] = img[:,:,color_list[0]]

    # End result
    cv2.imwrite('images_folder/new_image.jpg',canvas)

def cartoon_image(image):
  img = cv2.imread(image)

  # Detecting edges
  gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
  gray = cv2.medianBlur(gray,7)
  edges = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,7,7)

  # Color quantization
  data = np.float32(img).reshape((-1,3))
  criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER,20,0.001)

  ret, label, center = cv2.kmeans(data,9,None,criteria, 10,cv2.KMEANS_RANDOM_CENTERS)
  center = np.uint8(center)

  result = center[label.flatten()]
  result = result.reshape(img.shape)

  # Bilateral filter to reduce noise in image: Blurred and sharpness reduction
  blurred = cv2.bilateralFilter(result,d=7,sigmaColor=200,sigmaSpace=200)

  # Edge mask with colored image
  cartoon = cv2.bitwise_and(blurred,blurred,mask=edges)

  # End result
  cv2.imwrite('images_folder/new_image.jpg',cartoon)
