import cv2
import numpy as np

# 원근 변환 적용하는 함수
def perspective_transform(line_background, new_background_path, pts, line_slope, line_intercept, result_path):

    # "new_background.jpg" 이미지를 읽기
    new_background = cv2.imread(new_background_path)

    # 이미지의 높이, 너비 및 채널 수 얻기
    nb_height, nb_width, _ = new_background.shape

    # line_background의 크기를 얻기
    background_width, background_height = line_background.size

    # line_background과 동일한 크기와 비율을 갖게 new_background를 리사이즈
    new_background_resized = cv2.resize(new_background, (background_width, background_height))

    # 원근 변환을 위한 변환 행렬 계산
    # pts1 = np.float32([[0, height-line_intercept], [width, height -(line_slope*width +line_intercept)], [width, height], [0, height]]) #변환 전 좌표(좌상단, 우상단, 우하단, 좌하단)
    pts1 = np.float32([[0, background_height - line_intercept], [background_width, background_height - line_slope * background_width - line_intercept], [background_width, background_height], [0, background_height]])
    pts2 = np.float32(pts) # 변환 후 좌표

    perspective_matrix = cv2.getPerspectiveTransform(pts1, pts2)

    # 원근 변환 적용
    perspective_result = cv2.warpPerspective(new_background_resized, perspective_matrix, (background_width, background_height))

    # 변환된 이미지 저장
    cv2.imwrite(result_path, perspective_result)