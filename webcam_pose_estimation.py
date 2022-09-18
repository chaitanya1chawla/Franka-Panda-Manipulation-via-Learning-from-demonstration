import cv2
import mediapipe as mp
import numpy as np
import sys
from plot_utils import *
import math
import json
import keyword


mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose


# For webcam input:
#-->  '#put 0 for webcam input or "" video address
# different videos need to be uploaded manually, and name of json file also needs to be respectively updated 
cap = cv2.VideoCapture("/home/dhrikarl/Videos/Webcam/lifting_object_4.webm")
with mp_pose.Pose(
        modelgedit_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as pose:
    all_frames_results = []

    z_points = []
    y_points = []
    x_points = []
    #list of all points to be used to make dmps
    list_points = []

    fig = plt.figure(figsize=(10, 7))
    ax = plt.axes(projection="3d")
    ax.view_init(elev=20, azim=60)
    colors = np.array(range(140))
    k = 0
#--> #make this false for camera input
    FLAG_SAVE = True

    # Creating figure
    # converting 2D results to 3D
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_xlim3d(0.0, 1.0)
    ax.set_ylim3d(-0.2, 1.0)
    ax.set_zlim3d(0.0, 3.0)
    joint = mp_pose.PoseLandmark.RIGHT_WRIST
    label = "Right"
    #file1 = open("points_for_dmps.txt", "w")

    # using json file to record data points to be used in dmp
    out_file = open("myfile4.json", "w")

    #array which displays last 20 points in the graph
    points = []

    print("Press 'a' to start plotting")

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
#-->        # If loading a video, use 'break' instead of 'continue'.
            break
            #continue

        # To improve performance, optionally mark the image as not writeable to
        # pass by reference. (not by me)
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = pose.process(image)

        # Draw the hand annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results and FLAG_SAVE:

                all_frames_results.append(results)

                data_frames = [res.pose_world_landmarks.landmark[joint] for
                               res in all_frames_results]

                x_vector, y_vector, z_vector = [d.x for d in data_frames], [d.y for d in data_frames], [d.z for d in
                                                                                                        data_frames]
                #scaling the z coordinates as they were not being scaled linearly
                z_points.append(math.exp(-20 * z_vector[k]) - 1)
                x_points.append(x_vector[k])
                y_points.append(y_vector[k])

                list_points.append( [x_vector[k],y_vector[k],z_vector[k]])

                mp_drawing.draw_landmarks(
                    image,
                    results.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS,
                    )
                # this is used to print 20 points in realtime and delete older ones, because otherwise program
                # was getting very slow, due to lots of data points
                # later this was not used anymore, as we used start/stop of recording by user
                points.append(ax.scatter3D(x_vector[k], y_vector[k], (math.exp(-20 * z_vector[k]) - 1),
                                           color="blue"
                                           # c=colors
                                           ))
                print(x_vector[k], y_vector[k], z_vector[k])
                if k > 20:
                    points[0].remove()
                    points.pop(0)


                ax.plot3D(x_vector, y_vector, z_vector,
                     color="red"
                    )

                plt.title("{} hand - pose".format(label))

                plt.pause(0.1)


                k = k + 1

        # Flip the image horizontally for a selfie-view display.
        cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))
        # start/stop of recording of data according to user, to not have a lot of outliers
        pressedKey = cv2.waitKey(1) & 0xFF
        if pressedKey == ord('q'):
            print("q has been pressed")
            break
        elif pressedKey == ord('a'):
            print("a has been pressed")
            FLAG_SAVE = not FLAG_SAVE
    plt.show()


    nums = list(range(100))
    plt.plot(z_points)
    plt.xlabel('index')
    plt.ylabel('z coordinates')
    plt.grid(True)
    plt.show()

    json.dump(list_points, out_file, indent=6)
    #file1.close()
    out_file.close()

    print("[INFO] Plotting ...")

    #joint_to_plot = mp_pose.PoseLandmark.RIGHT_WRIST
    #plotJoint(all_frames_results, joint_to_plot, label="Right")

    '''
    for hand_landmarks in results.multi_hand_landmarks:
	    data_frames = [hand_landmarks.landmark[joint] for res in all_frames_results]

	    x_vector, y_vector, z_vector = [d.x for d in data_frames], [d.y for d in data_frames], [d.z for d in data_frames]
	    colors = np.array(range(len(x_vector)))

	    # Creating figure
	    fig = plt.figure(figsize=(10, 7))
	    ax = plt.axes(projection="3d")
	    ax.set_xlabel('X')
	    ax.set_ylabel('Y')
	    ax.set_zlabel('Z')

	    ax.scatter3D( x_vector, y_vector, z_vector,
		         #color = "blue"
		         c=colors
		         ) 

	    ax.plot3D(x_vector, y_vector, z_vector,
		           # c = colors
		          )

	    plt.title("Wrist")
	    plt.savefig("outputs/Wrist.jpg")
	    # show plot
	    plt.show()    
     '''
cap.release()
