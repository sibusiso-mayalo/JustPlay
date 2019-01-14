import cv2
class VideoHandler:

    def __init__(self, source):
        self.video = cv2.VideoCapture(source) # get the Video

        try:
            #get the width and height to setup the widget sizes
            self.video_width = self.video.get(cv2.CAP_PROP_FRAME_WIDTH)
            self.video_height = self.video.get(cv2.CAP_PROP_FRAME_HEIGHT)
        except ValueError as e:
            print("Could not open video", e)

    def __del__(self):
        if self.video.isOpened():
            self.video.release() #close or destroy the video
        self.window.mainloop()

    def get_frame(self):
        if self.video.isOpened(): #check if binding of clas to video source is successful
            returnValue, frame = self.video.read() #get continuous stream of frames (video images)

            if returnValue:
                return (returnValue, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (returnValue, None)
        else:
            return (returnValue, None)
