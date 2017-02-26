import cv2
import numpy as np
from sklearn.metrics.pairwise import euclidean_distances

resource = '../resources/forest/video1.avi'


def normalize(arr):
    sum = (arr[:, :, 0] + arr[:, :, 1] + arr[:, :, 2]) / 3 + 1

    norm = np.zeros(arr.shape)
    for i in range(3):
        norm[:, :, i] = arr[:, :, i] / sum

    return norm


# cv2.mean(normalized)
def find_mean_channel(norm):
    channels_num = 1
    if len(norm.shape) == 3:
        channels_num = norm.shape[2]

    mean_channel = np.zeros(channels_num)
    for i in range(channels_num):
        mean_channel[i] = np.median(np.mean(norm))

    return mean_channel


def find_std_channel(norm):
    channels_num = 1
    if len(norm.shape) == 3:
        channels_num = norm.shape[2]

    std_channel = np.zeros(channels_num)
    for i in range(channels_num):
        std_channel[i] = np.mean(np.std(norm))

    return std_channel


def color_quantization(image, k=8):
    Z = image.reshape((-1, 3))

    # Convert to np.float32

    Z = np.float32(Z)

    # Define criteria, number of clusters(K) and apply kmeans()
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 5, 1.0)
    ret, label, center = cv2.kmeans(Z, k, None, criteria, 5, cv2.KMEANS_RANDOM_CENTERS)

    # Now convert back into uint8, and make original image
    center = np.uint8(center)
    result = center[label.flatten()]
    result = result.reshape((image.shape))

    return result


def canny_threshold(image, low_threshold=100, ratio=3, kernel_size=3):
    """Canny Threshold"""

    # Reduce noise with a kernel 3x3
    image = cv2.blur(image, (3, 3))

    # Canny detector
    image = cv2.Canny(image, low_threshold, low_threshold * ratio, kernel_size)

    return image


def find_edge(road, bumper, mean_channel, a=0.5):
    b = 1 - a

    normalized = normalize(road)
    height, width, channels_num = road.shape

    bw = np.zeros([height * width, channels_num])
    for_bumper = np.zeros([height * width, 1], np.uint8)

    for i in range(channels_num):
        bw[:, i] = normalized[:, :, i].flatten()

    rbw = euclidean_distances(bw, mean_channel)
    rbw = np.reshape(rbw, (height, width))

    ind = np.nonzero(rbw.flatten() > np.mean(rbw.flatten()) + np.std(rbw.flatten()) * 0.1)

    # For updating road pixels
    for_bumper[ind] = 255
    for_bumper = np.reshape(for_bumper, (height, width))
    bumper1_mask = for_bumper[bumper['y1']:bumper['y2'], bumper['x1']: bumper['x2']]
    bumper_ind = np.nonzero(bumper1_mask)
    bumper1_area = normalized[bumper['y1']:bumper['y2'], bumper['x1']: bumper['x2']]

    for i in range(channels_num):
        colormap = bumper1_area[:, :, i]
        colormap = colormap[:]
        colormap = np.delete(colormap, bumper_ind)
        mean_channel[i] = mean_channel[i] * a + np.median(colormap) * b

    return for_bumper, mean_channel


def find_edge_greyscale(road, bumper, mean_channel, a=0.5):
    b = 1 - a
    height, width = road.shape

    bw = np.zeros([height * width, 1])
    for_bumper = np.zeros([height * width, 1], np.uint8)

    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    normalized = clahe.apply(road)

    normalized = np.array(normalized.flatten())
    normalized = np.reshape(normalized, bw.shape)

    bw = normalized

    rbw = euclidean_distances(bw, mean_channel)
    rbw = np.reshape(rbw, (height, width))

    ind = np.nonzero(rbw.flatten() > np.mean(rbw.flatten()) + np.std(rbw.flatten()) * 0.1)

    # For updating road pixels
    for_bumper[ind] = 255
    for_bumper = np.reshape(for_bumper, (height, width))

    bumper1_area = road[bumper['y1']:bumper['y2'], bumper['x1']: bumper['x2']]
    # mean_channel = mean_channel * a + np.median(bumper1_area) * b

    return for_bumper, mean_channel


def nothing(x):
    pass


def main():
    cap = cv2.VideoCapture(resource)

    cv2.namedWindow('Colors Correction')
    cv2.createTrackbar('Alpha:', 'Colors Correction', 15, 100, nothing)
    cv2.createTrackbar('Beta:', 'Colors Correction', 5, 100, nothing)
    cv2.namedWindow('With Applied Algorithms')
    cv2.createTrackbar('a:', 'With Applied Algorithms', 5, 10, nothing)

    width = int(cap.get(3) / 2)
    height = int(cap.get(4) / 2)

    horizontal_mid_point = round(width / 2)
    vertical_mid_point = round(height / 2)

    horizontal_offset_low = round(horizontal_mid_point / 1.5)
    horizontal_offset_mid = round(horizontal_offset_low / 1.5)
    horizontal_offset_high = round(horizontal_offset_mid / 2)

    vertical_offset_low = height
    vertical_offset_mid = vertical_offset_low - round(vertical_mid_point / 4)
    vertical_offset_high = vertical_offset_mid - round(vertical_mid_point / 4)

    bumper = {
        'y1': int(vertical_offset_mid),
        'y2': int(vertical_offset_mid + round(vertical_mid_point / 4)),
        'x1': int(horizontal_mid_point - horizontal_offset_mid),
        'x2': int(horizontal_mid_point - horizontal_offset_mid + horizontal_offset_mid * 2)
    }

    current_frame_num = 0

    # Capture first frame100
    cap.set(1, 300)  # Where frame_no is the frame you want
    ret, previous_frame = cap.read()
    cv2.imwrite('image.jpg', previous_frame)

    # Resize first frame
    previous_frame = cv2.resize(previous_frame, (0, 0), fx=0.5, fy=0.5)

    # For frames mean
    frames = [previous_frame]

    normalized = normalize(previous_frame)

    mean_channel = find_mean_channel(normalized)
    # std_channel = find_std_channel(normalized)

    # mean_channel = np.mean(frames)

    while True:
        frame = previous_frame
        frame = cv2.medianBlur(frame, 5)

        colors_correction = frame

        alpha_value = cv2.getTrackbarPos('Alpha:', 'Colors Correction')
        beta_value = cv2.getTrackbarPos('Beta:', 'Colors Correction')
        colors_correction = colors_correction * (alpha_value / 10) + beta_value
        colors_correction = np.array(colors_correction)

        a_value = cv2.getTrackbarPos('a:', 'With Applied Algorithms') / 10
        processed, mean_channel = find_edge(colors_correction, bumper, mean_channel, a_value)

        colors_correction = np.uint8(colors_correction)

        cv2.imshow('Default View', frame)
        cv2.imshow('Colors Correction', colors_correction)
        cv2.imshow('With Applied Algorithms', processed)

        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break

    cv2.destroyAllWindows()

    '''while cap.isOpened():
        print('Current frame: ', current_frame_num)
        frames.append(previous_frame)
        # Capture current frame
        ret, current_frame = cap.read()

        # Resize current frame
        current_frame = cv2.resize(current_frame, (0, 0), fx=0.5, fy=0.5)

        # Add current frame and make data array
        frames.append(current_frame)
        data = np.array(frames)

        std_image = np.std(data, axis=0).astype(np.uint8)
        mean_image = np.mean(data, axis=0).astype(np.uint8)

        print(mean_image.shape, std_image.shape)

        frame = mean_image

        colors_correction = mean_image

        # frame = cv2.medianBlur(frame, 5)
        # frame = cv2.GaussianBlur(frame, (5, 5), 0)

        ''''''processed = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        processed = cv2.equalizeHist(processed)
        processed = cv2.cvtColor(processed, cv2.COLOR_GRAY2BGR)

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # convert it to hsv
        hsv[:, :, 2] += 125
        processed = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)''''''

        alpha_value = cv2.getTrackbarPos('Alpha:', 'Colors Correction')
        beta_value = cv2.getTrackbarPos('Beta:', 'Colors Correction')
        colors_correction = colors_correction * (alpha_value / 10) + beta_value

        # colors_correction = np.uint8(colors_correction)

        # colors_correction = color_quantization(colors_correction, 5)

        # canny_threshold_value = cv2.getTrackbarPos('Min Threshold:', 'With Applied Algorithms')
        # processed = canny_threshold(frame, canny_threshold_value)

        # processed, mean_channel = find_edge(frame, bumper, mean_channel)
        # processed = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # processed = cv2.equalizeHist(processed)

        # processed = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # convert it to hsv
        # hsv[:, :, 2] += 1
        # processed = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

        # processed = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        # processed = clahe.apply(processed)

        processed, mean_channel = find_edge(colors_correction, bumper, mean_channel)

        # processed, mean_channel = find_edge_greyscale(processed, bumper, mean_channel)

        # canny_threshold_value = cv2.getTrackbarPos('Min Threshold:', 'With Applied Algorithms')
        # processed = canny_threshold(processed, canny_threshold_value)

        # processed = cv2.Canny(processed, 10, 200)

        colors_correction = np.uint8(colors_correction)

        # Display the resulting frame
        cv2.imshow('Default View', frame)
        cv2.imshow('Colors Correction', colors_correction)
        cv2.imshow('With Applied Algorithms', processed)

        # Quit the video
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        current_frame_num += 1

        previous_frame = current_frame
        frames = [previous_frame]
        # cv2.waitKey(0)
        # break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()'''


if __name__ == "__main__":
    main()


'''
Weight1 + bias1 + W2 + b2 = Y

'''