import cv2
import radio_video
from rtlsdr import RtlSdr
import math
steplength = 100000
begfreq = 49000000
curfreq = begfreq
#-----------------------------------------------------------
def firstPot2Bigger(x):
    '''Returns the first power of 2 greater than x'''
    return math.pow(2, math.ceil((math.log(x,2))))
#-----------------------------------------------------------
def gainChange(x):
    '''Gain slider callback'''
    global sdr
    print "Gain changed to", x
    sdr.gain = x
#-----------------------------------------------------------

def changesteplength(x):
    steplength = x * 1000
    print("Step length changed to", x)
    
#-----------------------------------------------------------
rv = radio_video.radioVideo()
sdr = RtlSdr()

# configure device
sdr.sample_rate = 24e5  
sdr.center_freq = begfreq     
sdr.gain = 30

#create openCV window and gain slider
cv2.namedWindow('Video')
cv2.createTrackbar('Gain','Video',10,40,gainChange)
cv2.createTrackbar('Step Length','Video',1,4000,gainChange)

#RTL-SDR samples must be read in power of 2 sizes
samplesToRead = firstPot2Bigger(rv.SAMPLES_PER_FRAME)
pause = False
while True:
    curfreq = curfreq+steplength
    sdr.center_freq = curfreq
    iq = sdr.read_samples(samplesToRead)
    demodulated = rv.demodulateAM(iq[-rv.SAMPLES_PER_FRAME:])
    frame = rv.decodeStream(demodulated)
    if not pause:
        cv2.imshow('Video', frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord(' '):
        pause = not pause
