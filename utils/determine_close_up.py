import os
import json

# close up shot인지를 판단하는 함수 정의
def determine_close_up(area_json_path):
    if os.path.exists(area_json_path):
        # areas.json파일을 로드함
        with open(area_json_path, 'r') as json_file:
            areas_info = json.load(json_file)

        # close_up_shot 변수의 default값을 False로 설정
        close_up_shot = False

        # close up shot인지 판단
        if areas_info.get("Ground Percentage", 0) > 70 or areas_info.get("Background Percentage", 0) > 70:
            close_up_shot = True
        elif areas_info.get("Dogs Percentage", 0) > 35:
            close_up_shot = True

        return close_up_shot