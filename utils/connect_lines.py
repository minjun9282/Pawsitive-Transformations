import os
import cv2
import json

# 이미지의 구도 파악하기 1 - background 및 ground의 어핀 변환에 활용
def connect_lines(root_folder):# background.jpg와 ground.jpg의 contour lines의 교차점을 노란색 직선으로 이어 background와 ground의 구도 파악
    for root, dirs, _ in os.walk(os.path.join(root_folder, "segmented_images")):
        for dir_name in dirs:
            images_folder = os.path.join(root, dir_name)
            if os.path.exists(images_folder):
                ground_img_path = os.path.join(images_folder, "ground.jpg")
                background_img_path = os.path.join(images_folder, "background.jpg")

                if os.path.exists(ground_img_path) and os.path.exists(background_img_path):
                    # 이미지 불러오기
                    ground_image = cv2.imread(ground_img_path, cv2.IMREAD_GRAYSCALE)
                    background_image = cv2.imread(background_img_path, cv2.IMREAD_GRAYSCALE)

                    # 이미지에서 엣지 검출 (Canny 엣지 검출)
                    background_edges = cv2.Canny(background_image, 400, 400)
                    ground_edges = cv2.Canny(ground_image, 400, 400)

                    # 빨간색과 파란색 직선의 교차점 찾기
                    yellow_color = (0, 255, 255)  # 노란색
                    result_image = cv2.cvtColor(ground_image, cv2.COLOR_GRAY2BGR)

                    # 이미지 높이 및 너비 가져오기
                    height, width = ground_image.shape

                    # 교차점 좌표 초기화
                    x1, y1, x2, y2, x3, y3, x4, y4 = 0, 0, 0, 0, 0, 0, 0, 0

                    # 첫 번째 교차점 찾기 (왼쪽에서 오른쪽으로)
                    for x in range(width):
                        for y in range(height):
                            if x <= width // 2 and background_edges[y, x] != 0 and ground_edges[y, x] != 0:
                                if x1 == 0 and y1 == 0:
                                    x1, y1 = x, y
                                    if x1 > width // 2:
                                        break

                    # 두 번째 교차점 찾기 (중간에서 시작하여 왼쪽으로)
                    x = width // 2
                    while x > 0 and x2 == 0 and y2 == 0:
                        for y in range(height):
                            if background_edges[y, x] != 0 and ground_edges[y, x] != 0:
                                x2, y2 = x, y
                                break
                        x -= 1

                    # 세 번째 교차점 찾기 (오른쪽에서 시작하여 왼쪽으로)
                    x = width - 1
                    while x >= 0 and x3 == 0 and y3 == 0:
                        for y in range(height):
                            if background_edges[y, x] != 0 and ground_edges[y, x] != 0:
                                x3, y3 = x, y
                                if x3 < width // 2:
                                    break
                        if x3 != 0:
                            break
                        x -= 1

                    # 네 번째 교차점 찾기 (중심에서 시작하여 오른쪽으로)
                    x = width // 2
                    while x < width and x4 == 0 and y4 == 0:
                        for y in range(height):
                            if background_edges[y, x] != 0 and ground_edges[y, x] != 0:
                                x4, y4 = x, y
                                break
                        x += 1

                    # 첫번째 교차점과 세번째 교차점 찾을때 오류가 중앙선을 넘어 반대편에서 찾는 오류가 있음.
                    # 일단 강제로 고정하고 차후에 수정.
                    if x2 == 0 and y2 == 0:
                        x1, y1 = 0, 0
                    if x4 == 0 and y4 == 0:
                        x3, y3 = 0, 0

                    # 교차점들을 노란색 선으로 연결
                    if x1 <= width // 2 and x3 >= width // 2:
                        # 첫 번째와 세 번째 교차점이 중앙선을 넘지 않을 때, 두 번째 교차점과 네번째 교차점도 연결
                        cv2.line(result_image, (x1, y1), (x2, y2), yellow_color, 2)
                        cv2.line(result_image, (x3, y3), (x4, y4), yellow_color, 2)
                        cv2.line(result_image, (x2, y2), (x4, y4), yellow_color, 2)
                    elif x1 > width // 2 and x3 >= width // 2:
                        # 첫 번째 교차점이 중앙선을 넘고 세 번째 교차점이 중앙선을 넘지 않을때 세번째 교차점과 네번째 교차점만 연결
                        cv2.line(result_image, (x3, y3), (x4, y4), yellow_color, 2)
                    elif x1 <= width // 2 and x3 < width // 2:
                        # 세 번째 교차점이 중앙선을 넘고 첫 번째 교차점이 중앙선을 넘지 않을때 첫번째 교차점과 두번째 교차점만 연결
                        cv2.line(result_image, (x1, y1), (x2, y2), yellow_color, 2)

                    # 선분의 유무 및 기울기, 길이 계산
                    if x1 > 0 and y1 > 0 and (x1 != x2 or y1 != y2):
                        line1_exists = True
                    else:
                        line1_exists = False

                    if x3 > 0 and y3 > 0 and (x3 != x4 or y3 != y4):
                        line3_exists = True
                    else:
                        line3_exists = False

                    if line1_exists and line3_exists:
                        line2_exists = True
                    else:
                        line2_exists = False

                    # 우리가 생각하는 기울기로 바꾸려면 부호를 바꿔줘야 함.(시작 좌표가 (0, 0) 이여서)
                    line1_slope = (y2 - y1) / (x2 - x1) if line1_exists else 0.0
                    line2_slope = (y4 - y2) / (x4 - x2) if line2_exists else 0.0
                    line3_slope = (y3 - y4) / (x3 - x4) if line3_exists else 0.0

                    # 결과를 파일에 저장
                    result_file = os.path.join(images_folder, 'lines.json')
                    line_data = {
                        "line1": {"exists": line1_exists, "slope": line1_slope, "line_intercept": (y1 + y2) // 2},
                        "line2": {"exists": line2_exists, "slope": line2_slope, "line_intercept": y2 - line2_slope * x2},
                        "line3": {"exists": line3_exists, "slope": line3_slope, "line_intercept": (y3 + y4) // 2},
                    }
                    with open(result_file, "w") as json_file:
                        json.dump(line_data, json_file, indent=4)

                    # 구한 line을 활용하여 새로운 마스킹 영역을 갖는 line_ground.jpg와 line_background.jpg 저장
                    if line1_exists == True and line2_exists == False:
                        # (x1, y1), (x2, y2)의 중점의 y좌표를 계산한다
                        mid_y = (y1 + y2) // 2
                        # 해당 이미지에서 중점의 y좌표값보다 작은 y좌표값을 갖는 모든 픽셀을 하얀색으로, 중점의 y좌표보다 크거나 같은 y좌표값을 갖는 모든 픽셀을 검은색으로 칠한 line_background.jpg를 생성한다.
                        line_background = result_image.copy()
                        line_background[:mid_y, :] = 255
                        line_background[mid_y:, :] = 0
                        # 해당 이미지에서 중점의 y좌표값보다 작은 y좌표값을 갖는 모든 픽셀을 검은색으로, 중점의 y좌표보다 크거나 같은 y좌표값을 갖는 모든 픽셀을 하얀색으로 칠한 line_ground.jpg를 생성한다.
                        line_ground = result_image.copy()
                        line_ground[:mid_y, :] = 0
                        line_ground[mid_y:, :] = 255
                        # 결과 이미지 저장
                        cv2.imwrite(os.path.join(images_folder, 'line_background.jpg'), line_background)
                        cv2.imwrite(os.path.join(images_folder, 'line_ground.jpg'), line_ground)
                    elif line3_exists == True and line2_exists == False:
                        # (x3, y3), (x4, y4)의 중점의 y좌표를 계산한다.
                        mid_y = (y3 + y4) // 2
                        # 해당 이미지에서 중점의 y좌표값보다 작은 y좌표값을 갖는 모든 픽셀을 하얀색으로, 중점의 y좌표보다 크거나 같은 y좌표값을 갖는 모든 픽셀을 검은색으로 칠한 line_background.jpg를 생성한다.
                        line_background = result_image.copy()
                        line_background[:mid_y, :] = 255
                        line_background[mid_y:, :] = 0
                        # 해당 이미지에서 중점의 y좌표값보다 작은 y좌표값을 갖는 모든 픽셀을 검은색으로, 중점의 y좌표보다 크거나 같은 y좌표값을 갖는 모든 픽셀을 하얀색으로 칠한 line_ground.jpg를 생성한다.
                        line_ground = result_image.copy()
                        line_ground[:mid_y, :] = 0
                        line_ground[mid_y:, :] = 255
                        # 결과 이미지 저장
                        cv2.imwrite(os.path.join(images_folder, 'line_background.jpg'), line_background)
                        cv2.imwrite(os.path.join(images_folder, 'line_ground.jpg'), line_ground)
                    elif line2_exists == True and line2_slope != 0:
                        # (x2, y2), (x4, y4)를 지나는 직선의 y절편을 line_intercept로 두고 (0, y_intercept), (width, height-y_intercept)를 지나는 직선으로 영역을 분할 (기울기를 감소시키기 위함)
                        # 이때는 result_image에 있는 모든 x좌표값의 범위에 대해 x좌표값이 동일할때 위에서 그린 직선의 y좌표값 보다 작은 y좌표값을 갖는 모든 픽셀을 하얀색으로, 크거나 같은 y좌표값을 갖는 모든 픽셀을 검은색으로 칠한 line_background.jpg를 생성한다.
                        # 또한 result_image에 있는 모든 x좌표값의 범위에 대해 x좌표값이 동일할때 위에서 그린 직선의 y좌표값 보다 작은 y좌표값을 갖는 모든 픽셀을 검은색으로, 크거나 같은 y좌표값을 갖는 모든 픽셀을 하얀색으로 칠한 line_ground.jpg를 생성한다.
                        line_slope = line2_slope
                        line_intercept = y2 - line_slope * x2

                        # (0, line_intercept)을 지나고 line_slope를 기울기로 갖는 adjusted_slope_line을 생성
                        line_background = result_image.copy()
                        line_ground = result_image.copy()

                        for x in range(width):
                            adjusted_slope_line = int(line_slope * x + line_intercept)

                            # line_background에서 위를 흰색, 아래를 검은색으로 칠함
                            line_background[:adjusted_slope_line, x] = 255
                            line_background[adjusted_slope_line:, x] = 0

                            # line_ground에서 위를 검은색, 아래를 흰색으로 칠함
                            line_ground[:adjusted_slope_line, x] = 0
                            line_ground[adjusted_slope_line:, x] = 255

                        # bilateralFilter를 사용하여 line_ground와 line_background의 경계선을 더욱 매끈하게 처리함
                        smoothed_line_background = cv2.bilateralFilter(line_background, d=-1, sigmaColor=10, sigmaSpace=5)
                        smoothed_line_ground = cv2.bilateralFilter(line_ground, d=-1, sigmaColor=10, sigmaSpace=5)

                        # 결과 이미지 저장
                        cv2.imwrite(os.path.join(images_folder, 'line_background.jpg'), smoothed_line_background)
                        cv2.imwrite(os.path.join(images_folder, 'line_ground.jpg'), smoothed_line_ground)
