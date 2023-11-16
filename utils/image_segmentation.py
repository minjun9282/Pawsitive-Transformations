# 필수 라이브러리 import
import os
import cv2
from rembg import remove
from PIL import Image
from utils.determine_close_up import determine_close_up

#사용자의 input 이미지를 받아 image segmentaion 진행 및 segmentaion 결과 저장.
def image_segmentation(predictor, input_dataset_directory, output_directory):
  for root, _, files in os.walk(input_dataset_directory):  # input_dataset의 모든 이미지 파일에 대한 image segmentation 진행 후 결과 저장
    for file in files:
        if file.endswith(".jpg"):  # 이미지 파일인 경우
            image_path = os.path.join(root, file)
            im = cv2.imread(image_path)  # 이미지 로드
            outputs = predictor(im)
            mask = outputs["instances"].pred_masks  # 마스크 추출

            image_filename = os.path.splitext(file)[0]  # 파일 이름에서 확장자 제거
            image_directory = os.path.join(output_directory, image_filename)
            os.makedirs(image_directory, exist_ok=True)

            # 원본 이미지 저장
            original_filename = os.path.join(image_directory, f"{image_filename}.jpg")
            cv2.imwrite(original_filename, im)
            # 직접 categories 설정
            categories = ['ground', 'background', 'eyes', 'dogs']
            category_masks = {category: [] for category in categories}

            for category_label in range(len(outputs["instances"])):
                category_name = categories[outputs["instances"].pred_classes[category_label]]
                category_mask = mask[category_label].cpu().numpy()  # 현재 카테고리에 해당하는 마스크

                if category_name in category_masks:
                    if not category_masks[category_name]:
                        category_masks[category_name].append(category_mask)
                    else:
                        combined_mask = category_masks[category_name][0] | category_mask
                        category_masks[category_name][0] = combined_mask

            # 각 카테고리별로 이미지 저장
            for category_name, category_mask_list in category_masks.items():
                category_segmented_region = im.copy()
                for category_mask in category_mask_list:
                    category_segmented_region[~category_mask] = 0  # 마스크 밖의 영역을 제거

                category_filename = os.path.join(image_directory, f"{category_name}.jpg")
                cv2.imwrite(category_filename, category_segmented_region)

            #dogs.jpg는 rembg를 활용하여 새롭게 생성
            input_image = Image.open(image_path)
            output = remove(input_image)
            output.save(os.path.join(image_directory, "dogs.png"))