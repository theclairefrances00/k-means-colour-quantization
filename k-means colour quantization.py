import cv2
from matplotlib import pyplot as plt
import numpy as np
import sklearn
import math
from PIL import Image
import random

#initialize arrays and variables
global seeds 
seeds = [] #holds the k number of seeds (x,y)

global regionCenterColours
regionCenterColours = [] #holds lists containing BGR

global pixels #holds coordinates, colour in BGR, and region assigned to
pixels = [] #pixels[0] is coords, pixels[1] is colour BGR, pixels[2] is region

global means
means = [] #holds the means

global converge
converge = 0 #to see if all centers are similar enough to means to be considered converged

threshold = 50; #for comparing centers and means

#function for changing k with the trackbar
def changeK(x): 
    if(cv2.getTrackbarPos('K Value','image')):
        global k
        k = x
    else:
        k = 3 #default k is three

#function to randomly select k points
def getKPoints(k):
    for i in range(k):
        temp = [] #to hold the selected value
        temp.append(random.randint(0,img.shape[0]-1)) #add y then x to prevent order change
        temp.append(random.randint(0,img.shape[1]-1))
        seeds.append(temp) #add each coordinate to the list
    
#for the k number of region centers add their colours (in list form) to the array of regionCenterColours
def getRegionColours(regionCenters):
    for i in range(k):  
        regionCenterColours.append(list(getColour(regionCenters[i])))

#returns the colour of given point (x,y)
def getColour(point):
    colour = (img[point[0],point[1]])
    return colour
        
#a function to get the colour distance between the point's colour and each region's seed colour
#the point's region is the one with the smallest distance
def getRegion(colour):
    distances = []
    for i in range(k):
        distances.append(getDistance(colour, regionCenterColours[i]))
    minDistance = distances.index(min(distances))
    return minDistance

#function to check euclidean distance between 2 BGR values
def getDistance(p,q):
    #check if seed_colour and colour "similar"
    sblue, sgreen, sred = p
    blue, green, red = q
    sblue, sgreen, sred = map(int, (sblue, sgreen, sred))
    blue, green, red = map(int, (blue, green, red))
    
    tempb = abs(blue-sblue)
    tempg = abs(green-sgreen)
    tempr = abs(red-sred)
    euclideanDistance = math.sqrt( (tempb)**2 + (tempg)**2 + (tempr)**2  )
    return euclideanDistance

#get the mean BGR for given region        
def getMeans(kVal):
    meanb = 0
    meang = 0
    meanr = 0
    
    temp = []
    
    for i in range (len(pixels)): 
        if(pixels[i][2] == kVal): #if the pixel[2] region value is kVal it is in that region
            temp.append(pixels[i][1])
            
    for i in range (len(temp)):
        meanb= meanb+(temp[0][0])
        meang= meang+(temp[0][1])
        meanr= meanr+(temp[0][2])
    
    meanb = meanb//len(temp)
    meang = meang//len(temp)
    meanr = meanr//len(temp)

    mean = (meanb, meang, meanr)
    means.append(mean)
        
#check if means and center are similar enough
def checkConverge(mean,regionCenterColour):
    if((abs(mean[0]-regionCenterColour[0]) <= threshold) and (abs(mean[1]-regionCenterColour[1])<= threshold) and (abs(mean[2]-regionCenterColour[2])<=threshold)):
        return 1
    else:
        return 0

#function to set the colour 
def colourPixel(coords, colour):
    img[coords] = colour        

    

#Allows the user to select which image to use
choice = int(input("Enter 1 for baboon or 2 for SAFlag:"))

cv2.namedWindow('image')
cv2.createTrackbar('K Value','image',3,20,changeK) #k can be 1 - 20 with 3 as the starting value


while(1): #ends when esc is pressed
    if choice == 1:
        img = cv2.imread(r".\baboon.png") 
    else:
        img = cv2.imread(r".\SAFlag.png") 

    cv2.imshow("image", img) #opens img in a new window
    
    key = cv2.waitKey(1) & 0xFF
    if key == 27:
        break
        
getKPoints(k) #get the k number of seeds
getRegionColours(seeds) #get the colour values for each seed
    
while(1):
    #adds coords, colour, and region to pixels array
    for i in range(img.shape[0]-1):
        for j in range(img.shape[1]-1):
            colour = list(img[i,j])
            region = getRegion(colour)
            temp = ((i, j), colour , region)
            pixels.append(temp)

    #get the mean value for each k
    for i in range(k):
        getMeans(i)  
  
    #formerly known as checkIfDone
    converge = 0
    for i in range(k):
        #if converge is true then want to set the colour of all in region to regionColour
        #if not converge want to set regionColour to mean and back to step 2
        converge = converge + checkConverge(means[i], regionCenterColours[i])
    
    if(converge < k): #not all converged
        for i in range(k):   
            regionCenterColours[i] = means[i]
    else:
        break

#if done is true the loop is done. Now set the regions to their colours
for j in range(k):
    for i in range (len(pixels)): 
        if(pixels[i][2] == j): #if pixel is in this region
            colourPixel(pixels[i][0], regionCenterColours[j])
    
cv2.imshow("image", img) #update image    
cv2.waitKey(0)
cv2.destroyAllWindows()
