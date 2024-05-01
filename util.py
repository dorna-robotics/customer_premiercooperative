from camera import Camera
import pickle
import time
import cv2
import matplotlib.pyplot as plt
import numpy as np


def save_pickle(data, path):
    with open(path, 'wb') as file:
        pickle.dump(data, file)


def load_pickle(path):
    # Load data from the file
    with open(path, 'rb') as file:
        return pickle.load(file)


def collect_img():
    camera = Camera()
    camera.connect(filter={})
    
    while True:
        # get data
        depth_frame, ir_frame, color_frame, depth_img, ir_img, color_img, depth_int, frames, timestamp = camera.get_all()
        
        # show
        cv2.imshow("img",color_img)
        
        # read key
        key = cv2.waitKey(1)
        if key == ord("s"): # save
            name = str(int(time.time()))
            cv2.imwrite("data/img_"+name+".jpg", color_img)
            save_pickle({"depth_frame": depth_frame}, "data/depth_"+name+".pkl")
        elif key == ord('q'): # exit
            break
           
    camera.close()


def collect_motion(duration=3):
    camera = Camera()
    camera.connect(mode="motion", filter={})

    # start
    camera.motion_rec()

    # collect
    time.sleep(duration)

    # stop
    accel, gyro = camera.motion_stop()
    camera.close()

    # Example list of points
    points = gyro

    # Extract x, y, z, and tick from the points
    signal = np.array([np.linalg.norm(point[0:3]) for point in points])
    tick = np.array([point[3] for point in points])

    # Compute Fourier transformation
    fourier_transform = np.fft.fft(signal)
    frequencies = np.fft.fftfreq(len(signal), tick[1] - tick[0])  # Frequency values

    plt.subplot(2, 1, 1)
    plt.plot(tick, signal, "-")
    plt.title('Original Signal')
    plt.xlabel('Time')
    plt.ylabel('Amplitude')

    plt.subplot(2, 1, 2)
    plt.plot(frequencies, np.abs(fourier_transform), "-")
    plt.title('Fourier Transformation')
    plt.xlabel('Frequency')
    plt.ylabel('Magnitude')

    plt.show()


if __name__ == '__main__':
    pass
    #collect_img()
    #collect_motion(3)