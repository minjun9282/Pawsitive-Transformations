import cv2

def adjust_brightness_and_saturation(image, saturation_factor, brightness_alpha, brightness_beta):
    # 이미지를 HSV로 변환
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # 채도 조절
    hsv[:,:,1] = np.clip(hsv[:,:,1] * saturation_factor, 0, 255)

    # 변환된 이미지를 다시 BGR로 변환
    adjusted_image = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    adjusted_image = cv2.convertScaleAbs(adjusted_image, alpha=brightness_alpha, beta=brightness_beta)
    return adjusted_image