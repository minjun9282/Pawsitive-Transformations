import os
import cv2
import numpy as np
import json
from PIL import Image
from utils.determine_close_up import determine_close_up
from utils.perspective_transform import perspective_transform

# 이미지 수정 및 저장 함수 정의
def modify_and_save_images(img_source_path, root_folder):
    for root, dirs, _ in os.walk(os.path.join(root_folder, "segmented_images")):
        for dir_name in dirs:
            images_folder = os.path.join(root, dir_name)
            if os.path.exists(images_folder):
                ground_img_path = os.path.join(images_folder, "line_ground.jpg")
                background_img_path = os.path.join(images_folder, "line_background.jpg")
                dogs_img_path = os.path.join(images_folder, "dogs.png")
                areas_json_path = os.path.join(images_folder, "areas.json")
                lines_json_path = os.path.join(images_folder, "lines.json")
                if os.path.exists(ground_img_path) and os.path.exists(background_img_path) and os.path.exists(dogs_img_path):
                    # 이미지 수정 작업을 수행하고 modified_image에 반영
                    ground_image = Image.open(ground_img_path)
                    background_image = Image.open(background_img_path)
                    dogs_image = Image.open(dogs_img_path)
                    if determine_close_up(areas_json_path) == True:
                        new_ground_image = Image.open(os.path.join(img_source_path, "carpet6.jpg"))
                        new_background_image = Image.open(os.path.join(img_source_path, "carpet6.jpg"))
                    else:
                        # lines.json파일을 로드함
                        with open(lines_json_path, 'r') as json_file:
                            lines_info = json.load(json_file)

                        # perspective_transform함수에 입력할 argument
                        new_ground_image = Image.open(os.path.join(img_source_path, "carpet6.jpg"))
                        width, height = background_image.size
                        new_background_path = os.path.join(img_source_path, "blank wall.jpg")
                        background_result_path = os.path.join(images_folder, 'perspective_background.jpg')

                        if lines_info["line2"]["exists"] == False:
                            if lines_info["line1"]["exists"] == True:
                                line_slope = 0
                                line_intercept = lines_info["line1"]["line_intercept"]
                                pts = [(0, 0), (width, 0), (width, line_slope * width + line_intercept), (0, line_intercept)] #변환 후 좌표(좌상단, 우상단, 우하단, 좌하단)
                                perspective_transform(background_image, new_background_path, pts, line_slope, line_intercept, background_result_path)
                                new_background_image = Image.open(os.path.join(images_folder, "perspective_background.jpg"))
                            elif lines_info["line3"]["exists"] == True:
                                line_slope = 0
                                line_intercept = lines_info["line3"]["line_intercept"]
                                pts = [(0, 0), (width, 0), (width, line_slope * width + line_intercept), (0, line_intercept)] #변환 후 좌표(좌상단, 우상단, 우하단, 좌하단)
                                perspective_transform(background_image, new_background_path, pts, line_slope, line_intercept, background_result_path)
                                new_background_image = Image.open(os.path.join(images_folder, "perspective_background.jpg"))
                        else:
                            #new_background_image의 경우 원근변환을 적용한 후 생성된 perspective_background.jpg를 이용
                            line_slope = lines_info["line2"]["slope"]
                            line_intercept = lines_info["line2"]["line_intercept"]
                            pts = [(0, 0), (width, 0), (width, line_slope * width + line_intercept), (0, line_intercept)] #변환 후 좌표(좌상단, 우상단, 우하단, 좌하단)
                            perspective_transform(background_image, new_background_path, pts, line_slope, line_intercept, background_result_path)
                            new_background_image = Image.open(os.path.join(images_folder, "perspective_background.jpg"))

                    # 이미지 로드
                    ground_image = cv2.imread(ground_img_path)
                    source_image = cv2.imread(os.path.join(img_source_path, "carpet6.jpg"))

                    # ground_image의 크기에 맞춰서 source_image의 크기를 변경
                    source_image_resized = cv2.resize(source_image, (ground_image.shape[1], ground_image.shape[0]))

                    # 하얀색인 부분을 마스킹
                    white_mask = cv2.inRange(ground_image, (200, 200, 200), (255, 255, 255))

                    # source_image에서 마스킹 영역에 해당하는 부분 계산
                    masked_region = cv2.bitwise_and(source_image_resized, source_image_resized, mask=white_mask)

                    # ground_image에서 마스킹 영역을 source_image에서 마스킹 영역에 해당했던 부분으로 덮어씌우기
                    result_image = np.copy(ground_image)
                    result_image[white_mask != 0] = masked_region[white_mask != 0]

                    # result_image 크기에 맞게 new_background_image 크기 조정
                    new_background_image_image_resized = new_background_image.resize((result_image.shape[1], result_image.shape[0]))
                    new_background_image_image_array = np.array(new_background_image_image_resized)

                    # line_ground_image.jpg에서 하얀색인 부분을 마스킹
                    line_ground_image = cv2.imread(ground_img_path)
                    white_mask = cv2.inRange(line_ground_image, (200, 200, 200), (255, 255, 255))

                    # result_image에서 위의 마스킹 영역에 해당하는 부분 계산
                    masked_region = cv2.bitwise_and(result_image, result_image, mask=white_mask)

                    # new_background_image의 검은색 부분에 result_image에서 마스킹 영역에 해당했던 부분으로 덮어씌우기
                    combined_image = np.copy(new_background_image_image_array)
                    combined_image[white_mask != 0] = masked_region[white_mask != 0]

                    # 깔끔하게 합성된 combined_background위에 dogs.png 합성
                    combined_background = Image.fromarray(combined_image)
                    overlay = Image.open(dogs_img_path)
                    changed_image = Image.alpha_composite(combined_background.convert('RGBA'), overlay.convert('RGBA'))

                    # 결과 이미지 저장
                    changed_image.save(os.path.join(images_folder, "changed_image.png"))
