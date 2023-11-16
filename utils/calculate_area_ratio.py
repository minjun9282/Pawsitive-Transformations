import os
import cv2
import json

# 이미지의 구도 파악하기2
# 이미지에서 ground, background, dogs가 각각 차지하는 비율 계산(close-up shot에 해당하는지 판단할 때 활용)
def calculate_area_ratio(root_folder):
    for root, dirs, _ in os.walk(os.path.join(root_folder, "segmented_images")):
        for dir_name in dirs:
            images_folder = os.path.join(root, dir_name)
            if os.path.exists(images_folder):
                ground_img_path = os.path.join(images_folder, "ground.jpg")
                background_img_path = os.path.join(images_folder, "background.jpg")
                dogs_img_path = os.path.join(images_folder, "dogs.jpg")

                if os.path.exists(ground_img_path) and os.path.exists(background_img_path) and os.path.exists(dogs_img_path):
                    ground_image = cv2.imread(ground_img_path)
                    background_image = cv2.imread(background_img_path)
                    dogs_image = cv2.imread(dogs_img_path)

                    # 각각의 이미지를 활용하여 마스크 계산
                    ground_mask = cv2.imread(os.path.join(images_folder, "ground.jpg"), 0)
                    background_mask = cv2.imread(os.path.join(images_folder, "background.jpg"), 0)
                    dogs_mask = cv2.imread(os.path.join(images_folder, "dogs.jpg"), 0)

                    # 각 객체의 마스크 영역을 활용하여 컨투어(외곽선) 검출
                    ground_contours, _ = cv2.findContours(ground_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                    background_contours, _ = cv2.findContours(background_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                    dogs_contours, _ = cv2.findContours(dogs_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                    # 각 객체의 면적 계산
                    ground_area = sum(cv2.contourArea(contour) for contour in ground_contours)
                    background_area = sum(cv2.contourArea(contour) for contour in background_contours)
                    dogs_area = sum(cv2.contourArea(contour) for contour in dogs_contours)

                    # 전체 이미지 면적 계산
                    total_area = ground_area + background_area + dogs_area

                    # 면적을 백분율로 변환
                    ground_percentage = (ground_area / total_area) * 100
                    background_percentage = (background_area / total_area) * 100
                    dogs_percentage = (dogs_area / total_area) * 100

                    # 결과를 JSON 파일에 저장
                    result_dict = {
                        "Ground Percentage": ground_percentage,
                        "Background Percentage": background_percentage,
                        "Dogs Percentage": dogs_percentage
                    }
                    result_file = os.path.join(images_folder, "areas.json")
                    with open(result_file, "w") as json_file:
                        json.dump(result_dict, json_file, indent=4)
