import numpy as np
import time
import config
from ultralytics import YOLO


class Detection(object):
    """docstring for Detection"""
    def __init__(self, config):
        super(Detection, self).__init__()
        self.config = config


    # convert a point in camera frame to probe frame
    def _camera_to_probe(self, point_r_camera):
        point_r_probe = point_r_camera
        return point_r_probe


    """
    list of all points that you need to search
    """
    def _roi_list(self, width, height):
        roi_list = []

        if self.config.detection["direction"] == "height":
            # number of element
            number_roi = height/self.config.detection["height"]

            for i in range(np.floor(number_roi)):
                pxl_w = np.floor(width/number_roi * (i*self.config.detection["start"] + (number_roi-i)*self.config.detection["end"]))
                pxl_h = np.floor((i+1/2) * self.config.detection["height"] / 2)
                rect_top_left = [np.floor(pxl_w-self.config.detection["width"]/2), np.floor(pxl_h-self.config.detection["height"]/2)]
                rect_bottom_right = [np.floor(pxl_w+self.config.detection["width"]/2), np.floor(pxl_h+self.config.detection["height"]/2)]
                roi_list.append([[pxl_w, pxl_h], [width, height], rect_top_left, rect_bottom_right])

        elif self.config.detection["direction"] == "width":
            # number of element
            number_roi = width/self.config.detection["width"]

            for i in range(np.floor(number_roi)):
                pxl_h = np.floor(height/number_roi * (i*self.config.detection["start"] + (number_roi-i)*self.config.detection["end"]))
                pxl_w = np.floor((i+1/2) * self.config.detection["width"] / 2)
                rect_top_left = [np.floor(pxl_w-self.config.detection["width"]/2), np.floor(pxl_h-self.config.detection["height"]/2)]
                rect_bottom_right = [np.floor(pxl_w+self.config.detection["width"]/2), np.floor(pxl_h+self.config.detection["height"]/2)]
                roi_list.append([[pxl_w, pxl_h], [width, height], rect_top_left, rect_bottom_right])
        else:
            return roi_list

        return roi_list


    # given a point in camera perspective, finds if this point is inside the robot probe or not 
    def _point_is_in(self, xyz_r_camera, p1):
        #probe center of rotation
        probe_center_of_rotation = np.array([0, self.config.probe["l1"]*np.cos(np.deg2rad(p1)), self.config.probe["l1"]*np.sin(np.deg2rad(p1))])

        # point_r_probe
        xyz_r_probe = self._camera_to_probe(xyz_r_camera)

        # is in
        if np.linalg.norm(xyz_r_probe - probe_center_of_rotation) > self.config.probe["l1"]:
            point_in = False
        else:
            point_in = True
        
        # find the p1_2
        v1 = -probe_center_of_rotation
        v2 = xyz_r_probe - probe_center_of_rotation
        dot_product = np.dot(v1, v2)
        norm_v1 = np.linalg.norm(v1)
        norm_v2 = np.linalg.norm(v2)
        cos_theta = dot_product / (norm_v1 * norm_v2)
        angel_between = np.degrees(np.arccos(np.clip(cos_theta, -1.0, 1.0)))

        if point_r_probe[2] < 0:
            p1_2 = p1 + angel_between
        else:
            p1_2 = - angel_between

        return point_in, p1_2


    """
    Look at the image and validate if there is a region for probing
    """
    def find_roi(self, p1):
        # init
        roi_found = False
        p1_2 = p1
        roi = []

        # get all the camera data
        depth_frame, ir_frame, color_frame, depth_img, ir_img, color_img, depth_int, frames, timestamp = self.camera.get_all()
        height, width = color_img.shape[:2]
        
        # roi_list
        roi_list = self._roi_list(width, height)

        # xyz
        roi_xyz_list = [self.camera.xyz(roi[0], depth_frame, depth_int, wnd = roi[2], z_min = 10, z_max = 10000) for roi in roi_list]
        
        # loop over each window
        for roi in roi_list:
            # xyz_r_camera
            xyz_r_camera = self.camera.xyz(roi[0], depth_frame, depth_int, wnd = roi[2], z_min = self.config.detection["z_min"], z_max = self.config.detection["z_max"])
            
            # check if it is in
            point_in, p1_2 = self._point_is_in(xyz_r_camera, p1)
            if point_in:
                roi_found = True
                break

        return roi_found, p1_2, roi


"""
define all the robot motion here
"""
class Probe(object):
    """docstring for Motion"""
    def __init__(self, robot, config):
        super(Motion, self).__init__()
        # config
        self.config = config


    # connect all the items
    def connect(self):
        # robot
        self.robot = Dorna()
        if not self.robot.connect(config.robot["ip"]):
            self.robot.log("Robot connection failed")
            return False

        # camera
        self.camera = Camera()
        if not self.camera.connect(filter=None):
            self.robot.log("Camera connection failed")
            return False

        # yolo
        self.model = YOLO(self.config.detection["model_path"], task="segment")

        self.robot.log("Probe is connected")
        return True


        # close all the items
        def close(self):
            self.robot.close()
            self.camera.close()



    def _engage_time(self, direction, degree):
        joint = ""
        if direction in ["left", "right"]:
            joint = "v0"
        elif direction in ["up", "down"]:
            joint = "v1"
        
        if not joint:
            return None
        
        return degree / self.config.probe[joint]


    def go(self, direction, step):
        if direction not in ["up", "down", "left", "right"]:
            return None

        if step < 0:
            if direction == "up":
                direction = "down"
            elif direction == "down":
                direction = "up"
            elif direction == "left":
                direction = "right"
            elif direction == "right":
                direction = "left"

        # engage time
        time_engage = self._engage_time(direction, np.abs(step))

        # engage
        start = time.time()
        robot.lmove(self.config.joystick["up"], vel=self.config.joystick["vel"], accel=self.config.joystick["accel"], jerk=self.config.joystick["jerk"])

        # remaining time
        time_passed = time.time()-start
        time.sleep(max(0, time_engage-time_passed))

        # go to standby
        return robot.lmove(self.config.joystick["standby"], vel=self.config.joystick["vel"], accel=self.config.joystick["accel"], jerk=self.config.joystick["jerk"])


    # engage the joystick
    def engage(self):
        self.robot.jmove(self.config.joystick["disengage_joint"], vel=self.config.joystick["vel_joint"], accel=self.config.joystick["accel_joint"], jerk=self.config.joystick["jerk_joint"])
        self.robot.jmove(self.config.joystick["standby_middle_joint"], vel=self.config.joystick["vel_joint"], accel=self.config.joystick["accel_joint"], jerk=self.config.joystick["jerk_joint"])
        return self.robot.lmove(self.config.joystick["standby"], vel=self.config.joystick["vel"], accel=self.config.joystick["accel"], jerk=self.config.joystick["jerk"])


    # disengage the joystick
    def disengage(self):
        self.robot.jmove(self.config.joystick["standby_middle_joint"], vel=self.config.joystick["vel_joint"], accel=self.config.joystick["accel_joint"], jerk=self.config.joystick["jerk_joint"])
        return self.robot.jmove(self.config.joystick["disengage_joint"], vel=self.config.joystick["vel_joint"], accel=self.config.joystick["accel_joint"], jerk=self.config.joystick["jerk_joint"])


    def home(self, direction):
        if direction not in ["up", "down", "left", "right"]:
            return None

        # go toward direction
        self.go(direction, self.config.home[direction]["step"])

        # system is homed
        standby_step = self.config.home[direction]["standby"]  - self.config.home[direction]["value"] 

        # standby
        self.go(direction, standby_step)


    """
    def home_copy(self, joint):
        home = False

        if joint not in ["p0", "p1"]:
            return None

        # connect to the camera
        self.camera.close()
        self.camera.connect(mode="motion")


        # run it for limited number of times
        for i in range(360/(self.config.home[joint]["step"])):
            # record data
            self.camera.motion_rec()

            # move
            self.go(self.config.home[joint]["direction"], self.config.home[joint]["step"])

            # accel and gyro
            accel, gyro = self.camera.motion_stop()

            # assign points
            points = gyro

            # Calculate the norm of the vector [x, y, z] for each point
            signal = np.array([np.linalg.norm(point[0:3]) for point in points])

            # tick
            tick = np.array([point[3] for point in points])

            # Compute Fourier transformation
            fourier_transform = np.fft.fft(signal)
            frequencies = np.fft.fftfreq(len(signal), tick[1] - tick[0])  # Frequency values

            # home position is reached
            if True:
                home = True
                break

        self.camera.close()

        # go to the standby
        if home:
            return 0
    """      