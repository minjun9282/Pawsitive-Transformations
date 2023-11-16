import os
from PIL import Image

#각 폴더 별로 원본 이미지와 result_image를 제외한 모든 파일 삭제
def delete_temp_files(img_source_path, root_folder):
    for root, dirs, files in os.walk(os.path.join(root_folder, "segmented_images")):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            # 원본 파일이나 result_image.jpg가 아닌 경우에 삭제
            if file_name != f"{os.path.basename(root)}.jpg" and file_name != "result_image.jpg":
                os.remove(file_path)
    result_image_path = os.path.join(root_folder, "segmented_images/uploaded_image/result_image.jpg")
    if os.path.exists(result_image_path) == False:
        error_image_path = os.path.join(img_source_path, "error.jpg")
        error_image = Image.open(error_image_path)
        error_image_rgb = error_image.convert('RGB') #혹시 error_image가 alpha channel 갖고 있으면 RGB형식으로 변환
        error_image_rgb.save(result_image_path)