import os
import cv2

# 미디안 필터 적용 함수 정의
def apply_median_filter(image, contours, filter_size):
    result_image = image.copy()
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        roi = image[y:y+h, x:x+w]

        # 이미지가 비어 있지 않은지 확인
        if not roi.size:
            continue

        # 적절한 크기와 채널 수를 가지고 있는지 확인
        if roi.shape[-1] == 3:  # 이미지가 3개의 채널(RGB)을 가져야 함
            filtered_roi = cv2.medianBlur(roi, filter_size)
            result_image[y:y+h, x:x+w] = filtered_roi

    return result_image

#노이즈 중 소금 후추 노이즈를 제거하는 함수 정의
def remove_noise_and_apply_median_filter(root_folder, filter_size):
    for root, dirs, _ in os.walk(os.path.join(root_folder, "segmented_images")):
        for dir_name in dirs:
            images_folder = os.path.join(root, dir_name)
            if os.path.exists(images_folder):
                changed_img_path = os.path.join(images_folder, "changed_image.png")
                if os.path.exists(changed_img_path):
                    # 이미지 불러오기
                    image = cv2.imread(changed_img_path)

                    # dogs.jpg를 사용하여 dogs 객체의 마스크를 얻습니다.
                    mask = cv2.imread(os.path.join(images_folder, "dogs.png"), 0)

                    # dogs 객체의 외부 라인을 얻습니다.
                    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

                    # 외부 라인을 사용하여 이미지에 미디안 필터 적용
                    result_image = apply_median_filter(image, contours, filter_size)

                    # 처리된 이미지 저장
                    output_image_path = os.path.join(images_folder, "result_image.jpg")
                    cv2.imwrite(output_image_path, result_image)