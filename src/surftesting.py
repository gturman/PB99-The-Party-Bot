import cv2
import imutils
import time
from rgbmatrix import Adafruit_RGBmatrix

matrix = Adafruit_RGBmatrix(32, 1)

#tweak these
resizefactor = 4
frameresize = 5
threshold =600
canny_beer = 0
best = 2 #k= for knnMatches for bruteforce matcher
bfcheck = 0.90
lines = 10
flanncheck = 0.6

#load frame images
frame_bl = cv2.imread('test_bl.jpg',cv2.IMREAD_GRAYSCALE)
h,w= frame_bl.shape
frame_bl = imutils.resize(frame_bl, width=w/frameresize)

frame_null = cv2.imread('test_null.jpg',cv2.IMREAD_GRAYSCALE)
h,w= frame_null.shape
frame_null = imutils.resize(frame_null, width=w/frameresize)

frame_pbr = cv2.imread('test_pbr.jpg',cv2.IMREAD_GRAYSCALE)
h,w= frame_pbr.shape
frame_pbr = imutils.resize(frame_pbr, width=w/frameresize)


#load beer templates
badbeer = cv2.imread('beer/budlight.jpg',cv2.IMREAD_GRAYSCALE)
h,w= badbeer.shape
badbeer = imutils.resize(badbeer, width=w/resizefactor)

itsbeer = cv2.imread('beer/pbr.jpg',cv2.IMREAD_GRAYSCALE)
h,w= itsbeer.shape
itsbeer = imutils.resize(itsbeer, width=w/resizefactor)


#try canny
if (canny_beer):
	badbeer = imutils.auto_canny(badbeer)
	itsbeer = imutils.auto_canny(itsbeer)
#if (canny_frames):
#frame_bl = imutils.auto_canny(frame_bl)
#frame_null = imutils.auto_canny(frame_null)
#frame_pbr = imutils.auto_canny(frame_pbr)


surf = cv2.xfeatures2d.SURF_create(threshold)
#SURF on template
surf_badbeer = badbeer
surf_itsbeer = itsbeer
#compute surf time on badbeer
start=time.time()
kp_badbeer, des_badbeer = surf.detectAndCompute(surf_badbeer,None)
end=time.time()
badbeer_surftime = end - start
print "badbeer surf: " + str(badbeer_surftime)
#compute surf time on itsbeer
start=time.time()
kp_itsbeer, des_itsbeer = surf.detectAndCompute(surf_itsbeer,None)
end=time.time()
itsbeer_surftime = end - start
print "itsbeer surf: " + str(itsbeer_surftime)
#show keypoints on beers
surf_badbeer = cv2.drawKeypoints(surf_badbeer,kp_badbeer,None,(0,0,255),4)
surf_itsbeer = cv2.drawKeypoints(surf_itsbeer,kp_itsbeer,None,(0,0,255),4)
cv2.imwrite('surf_badbeer.jpg',surf_badbeer)
cv2.imwrite('surf_itsbeer.jpg',surf_itsbeer)

#SURF on frames
surf_frame_bl = frame_bl
surf_frame_null = frame_null
surf_frame_pbr = frame_pbr
start=time.time()
kp_frame_bl, des_frame_bl = surf.detectAndCompute(surf_frame_bl,None)
kp_frame_null, des_frame_null = surf.detectAndCompute(surf_frame_null,None)
kp_frame_pbr, des_frame_pbr = surf.detectAndCompute(surf_frame_pbr,None)
end=time.time()
threeframe_surftime = end - start
print "threeframe surf: " + str(threeframe_surftime)
surf_frame_bl = cv2.drawKeypoints(surf_frame_bl,kp_frame_bl,None,(0,0,255),4)
surf_frame_null = cv2.drawKeypoints(surf_frame_null,kp_frame_null,None,(0,0,255),4)
surf_frame_pbr = cv2.drawKeypoints(surf_frame_pbr,kp_frame_pbr,None,(0,0,255),4)
cv2.imwrite('surf_test_bl.jpg',surf_frame_bl)
cv2.imwrite('surf_test_null.jpg',surf_frame_null)
cv2.imwrite('surf_test_pbr.jpg',surf_frame_pbr)

#bruteforce = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)
bruteforce = cv2.BFMatcher()
start=time.time()
badbeer_match_true = bruteforce.knnMatch(des_badbeer,des_frame_bl,k=best)
itsbeer_match_other = bruteforce.knnMatch(des_itsbeer,des_frame_bl,k=best)
end=time.time()
matchtimebl = end - start
print "bf match beers w/ bl frame: " + str(matchtimebl)
start=time.time()
itsbeer_match_none = bruteforce.knnMatch(des_itsbeer,des_frame_null,k=best)
badbeer_match_none = bruteforce.knnMatch(des_badbeer,des_frame_null,k=best)
end=time.time()
matchtimenull = end - start
print "bf match beers w/ null frame: " + str(matchtimenull)
start=time.time()
badbeer_match_other = bruteforce.knnMatch(des_badbeer,des_frame_pbr,k=best)
itsbeer_match_true = bruteforce.knnMatch(des_itsbeer,des_frame_pbr,k=best)
end=time.time()
matchtimepbr = end - start
print "bf match beers w/ pbr frame: " + str(matchtimepbr)


#show BF matches
bfmatches = [badbeer_match_true, badbeer_match_none,badbeer_match_other , itsbeer_match_true, itsbeer_match_none,itsbeer_match_other]
goodmatches = [0,1,2,3,4,5]
for index in range(len(bfmatches)):
	for match in bfmatches:
		good = []
		for m,n in match:
			if m.distance < bfcheck*n.distance:
				good.append([m])
		goodmatches[index] = good

show_badbeer_match_true_bruteforce = cv2.drawMatchesKnn(surf_badbeer,kp_badbeer,surf_frame_bl,kp_frame_bl,goodmatches[0][:lines],None,flags=2)
show_badbeer_match_none_bruteforce = cv2.drawMatchesKnn(surf_badbeer,kp_badbeer,surf_frame_null,kp_frame_null,goodmatches[1][:lines],None,flags=2)
show_badbeer_match_other_bruteforce = cv2.drawMatchesKnn(surf_badbeer,kp_badbeer,surf_frame_pbr,kp_frame_pbr,goodmatches[2][:lines],None,flags=2)
show_itsbeer_match_true_bruteforce = cv2.drawMatchesKnn(surf_itsbeer,kp_itsbeer,surf_frame_pbr,kp_frame_pbr,goodmatches[3][:lines],None,flags=2)
show_itsbeer_match_none_bruteforce = cv2.drawMatchesKnn(surf_itsbeer,kp_itsbeer,surf_frame_null,kp_frame_null,goodmatches[4][:lines],None,flags=2)
show_itsbeer_match_other_bruteforce = cv2.drawMatchesKnn(surf_itsbeer,kp_itsbeer,surf_frame_bl,kp_frame_bl,goodmatches[5][:lines],None,flags=2)

#flann!!1
FLANN_INDEX_KDTREE=0
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees=5)
search_params = dict(checks=50)
flann=cv2.FlannBasedMatcher(index_params,search_params)

start=time.time()
badbeer_fmatch_true = flann.knnMatch(des_badbeer,des_frame_bl,k=best)
itsbeer_fmatch_other = flann.knnMatch(des_itsbeer,des_frame_bl,k=best)
end=time.time()
matchtimebl = end - start
print "flann match beers w/ bl frame: " + str(matchtimebl)
start=time.time()
itsbeer_fmatch_none =  flann.knnMatch(des_itsbeer,des_frame_null,k=best)
badbeer_fmatch_none = flann.knnMatch(des_badbeer,des_frame_null,k=best)
end=time.time()
matchtimenull = end - start
print "flann match beers w/ null frame: " + str(matchtimenull)
start=time.time()
badbeer_fmatch_other = flann.knnMatch(des_badbeer,des_frame_pbr,k=best)
itsbeer_fmatch_true = flann.knnMatch(des_itsbeer,des_frame_pbr,k=best)
end=time.time()
matchtimepbr = end - start
print "flann match beers w/ pbr frame: " + str(matchtimepbr)

flannmatches=[badbeer_fmatch_true,badbeer_fmatch_none,badbeer_fmatch_none,itsbeer_fmatch_true,itsbeer_fmatch_none,itsbeer_fmatch_none]
masks = [0,1,2,3,4,5]
draw_params = [0,1,2,3,4,5]
for index in range(len(flannmatches)):
	masks[index] = [[0,0] for i in xrange(len(flannmatches[index]))]
	for i,(m,n) in enumerate(flannmatches[index]):
		if m.distance < flanncheck*n.distance:
			masks[index][i]=[1,0]
	draw_params[index]= dict(matchColor = (0,255,0),singlePointColor = (255,0,0),matchesMask = masks[index],flags = 0)

show_badbeer_match_true_flann = cv2.drawMatchesKnn(badbeer,kp_badbeer,frame_bl,kp_frame_bl,flannmatches[0],None,**draw_params[0])
show_badbeer_match_none_flann = cv2.drawMatchesKnn(badbeer,kp_badbeer,frame_null,kp_frame_null,flannmatches[1],None,**draw_params[1])
show_badbeer_match_other_flann = cv2.drawMatchesKnn(badbeer,kp_badbeer,frame_pbr,kp_frame_pbr,flannmatches[2],None,**draw_params[2])
show_itsbeer_match_true_flann= cv2.drawMatchesKnn(itsbeer,kp_itsbeer,frame_pbr,kp_frame_pbr,flannmatches[3],None,**draw_params[3])
show_itsbeer_match_none_flann = cv2.drawMatchesKnn(itsbeer,kp_itsbeer,frame_null,kp_frame_null,flannmatches[4],None,**draw_params[4])
show_itsbeer_match_other_flann = cv2.drawMatchesKnn(itsbeer,kp_itsbeer,frame_bl,kp_frame_bl,flannmatches[5],None,**draw_params[5])

'''
cv2.putText(surf_badbeer,str(badbeer_surftime),(w-(w*4),h-(h/4)), cv2.FONT_HERSHEY_SIMPLEX,12,(255,0,0),cv2.LINE_AA)
cv2.putText(surf_itsbeer,str(itsbeer_surftime),(w-(w*4),h-(h/4)), cv2.FONT_HERSHEY_SIMPLEX,12,(255,0,0),cv2.LINE_AA)
cv2.putText(surf_badbeer,str(badbeer_surftime),(w-(w*4),h-(h/4)), cv2.FONT_HERSHEY_SIMPLEX,12,(255,0,0),cv2.LINE_AA)
cv2.putText(surf_itsbeer,str(itsbeer_surftime),(w-(w*4),h-(h/4)), cv2.FONT_HERSHEY_SIMPLEX,12,(255,0,0),cv2.LINE_AA)
cv2.putText(surf_badbeer,str(badbeer_surftime),(w-(w*4),h-(h/4)), cv2.FONT_HERSHEY_SIMPLEX,12,(255,0,0),cv2.LINE_AA)
cv2.putText(surf_itsbeer,str(itsbeer_surftime),(w-(w*4),h-(h/4)), cv2.FONT_HERSHEY_SIMPLEX,12,(255,0,0),cv2.LINE_AA)
'''
cv2.imwrite('bruteforce_badbeer_match_bl.jpg',show_badbeer_match_true_bruteforce)
cv2.imwrite('bruteforce_badbeer_match_null.jpg',show_badbeer_match_none_bruteforce)
cv2.imwrite('bruteforce_badbeer_match_pbr.jpg',show_badbeer_match_other_bruteforce)

cv2.imwrite('bruteforce_itsbeer_match_bl.jpg',show_itsbeer_match_other_bruteforce)
cv2.imwrite('bruteforce_itsbeer_match_null.jpg',show_itsbeer_match_none_bruteforce)
cv2.imwrite('bruteforce_itsbeer_match_pbr.jpg',show_itsbeer_match_true_bruteforce)

cv2.imwrite('flann_badbeer_match_bl.jpg',show_badbeer_match_true_flann)
cv2.imwrite('flann_badbeer_match_null.jpg',show_badbeer_match_none_flann)
cv2.imwrite('flann_badbeer_match_pbr.jpg',show_badbeer_match_other_flann)

cv2.imwrite('flann_itsbeer_match_bl.jpg',show_itsbeer_match_other_flann)
cv2.imwrite('flann_itsbeer_match_null.jpg',show_itsbeer_match_none_flann)
cv2.imwrite('flann_itsbeer_match_pbr.jpg',show_itsbeer_match_true_flann)

exit()
