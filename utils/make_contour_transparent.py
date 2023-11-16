import os
import cv2
import numpy as np

# dogs.png 파일의 contour line을 투명화 하는 함수 정의
def make_contour_transparent(root_folder):
    for root, dirs, _ in os.walk(os.path.join(root_folder, "segmented_images")):
        for dir_name in dirs:
            images_folder = os.path.join(root, dir_name)
            if os.path.exists(images_folder):
                input_path = os.path.join(images_folder, "dogs.png")
                # 이미지 로드
                dogs_image = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)

                # 그레이스케일로 변환
                gray = cv2.cvtColor(dogs_image[:, :, :3], cv2.COLOR_BGR2GRAY)

                # 외곽선 찾기
                _, thresh = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)
                contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_L1)

                # 컨투어 라인 그리기 (외곽선만 그림)
                contour_image = np.zeros_like(dogs_image)
                cv2.drawContours(contour_image, contours, -1, (255, 255, 255, 255), 8)

                # 이미지를 저장
                contour_path = os.path.join(images_folder, "dogs_contour.jpg")
                cv2.imwrite(contour_path, contour_image)

                # 이미지 로드
                dogs_image = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
                contour_image = cv2.imread(contour_path, cv2.IMREAD_UNCHANGED)

                # contour line 투명화 적용
                for i in range(contour_image.shape[0]):
                    for j in range(contour_image.shape[1]):
                        # contour_image에서 해당 위치의 픽셀 값 확인
                        contour_pixel = contour_image[i, j]

                        # contour_pixel이 (255, 255, 255, 255)이면 해당 위치의 투명도를 0으로 설정
                        if all(value == 255 for value in contour_pixel):
                            dogs_image[i, j, 3] = 0

                # 새로운 PNG 파일로 저장
                output_path = os.path.join(images_folder, "dogs.png")
                cv2.imwrite(output_path, dogs_image)