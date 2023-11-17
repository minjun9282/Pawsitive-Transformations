from flask import Flask, render_template, request, send_file, jsonify
import os
import shutil
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2 import model_zoo
from detectron2.data.datasets import register_coco_instances
from utils.image_segmentation import image_segmentation
from utils.make_contour_transparent import make_contour_transparent
from utils.connect_lines import connect_lines
from utils.calculate_area_ratio import calculate_area_ratio
from utils.modify_and_save_images import modify_and_save_images
from utils.remove_noise_and_apply_median_filter import apply_median_filter
from utils.remove_noise_and_apply_median_filter import remove_noise_and_apply_median_filter
from utils.delete_temp_files import delete_temp_files
from utils.determine_close_up import determine_close_up
from utils.perspective_transform import perspective_transform

# 데이터 로딩 및 Detectron2용 등록
register_coco_instances("my_dataset", {}, "/Users/minjun9282/PycharmProjects/myflask/local_datas/combined.json",
                            "/Users/minjun9282/PycharmProjects/myflask/local_datas/dataset")

app = Flask(__name__)

# Set the paths
output_directory = "/Users/minjun9282/PycharmProjects/myflask/web_datas/output/segmented_images" # 이미지 합성을 완료한 결과물을 저장하는 ouput 폴더 경로
root_folder = "/Users/minjun9282/PycharmProjects/myflask/web_datas/output" #위의 segmented_images폴더의 상위 폴더
img_source_path = "/Users/minjun9282/PycharmProjects/myflask/local_datas/img_source" #합성에 사용될 이미지를 포함하는 경로
input_dataset_directory = "/Users/minjun9282/PycharmProjects/myflask/web_datas/input"
# Ensure the output directory exists
os.makedirs(output_directory, exist_ok=True)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' in request.files:
        image = request.files['image']

        # image_segmentation 진행 전 기존에 남아있던 결과물들 삭제
        temp_results_path = os.path.join(output_directory, "uploaded_image")
        if os.path.exists(temp_results_path):
            shutil.rmtree(temp_results_path)

        # 업로드된 이미지를 input 디렉토리에 저장
        input_image_path = os.path.join(input_dataset_directory, "uploaded_image.jpg")
        image.save(input_image_path)

        # 이미지 처리 작업 진행
        processed_image_path = process_image(input_image_path)
        """ return render_template('home.html', processed_image_path=processed_image_path) """
        return jsonify({"status": "success", "message": "이미지가 성공적으로 업로드되었습니다.", "processed_image_path": processed_image_path})

    
@app.route('/download', methods=['GET'])
def download_image():
    output_image_path = "/Users/minjun9282/PycharmProjects/myflask/web_datas/output/segmented_images/uploaded_image/result_image.jpg"
    return send_file(output_image_path, as_attachment=True)

def process_image(input_image_path):
    # 훈련된 모델 불러오기
    cfg = get_cfg()
    cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
    cfg.MODEL.ROI_HEADS.NUM_CLASSES = 4  # 클래스 개수
    cfg.MODEL.ROI_BOX_HEAD.POOLING_MODE = "ROIAlign"
    cfg.MODEL.DEVICE = 'cpu'
    model_path = "/Users/minjun9282/PycharmProjects/myflask/local_datas/model_final.pth"  # 저장된 모델의 경로
    cfg.MODEL.WEIGHTS = model_path
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.1
    cfg.DATASETS.TEST = ("my_dataset",)
    predictor = DefaultPredictor(cfg)

    # 이미지 처리 작업 진행
    image_segmentation(predictor, input_dataset_directory, output_directory) #여기서 input_image_path가 아닌 그 이미지가 속한 폴더를 넣어줘야함. 함수에 predictor를 인자로 넣어줌.
    make_contour_transparent(root_folder)
    connect_lines(root_folder)
    calculate_area_ratio(root_folder)
    modify_and_save_images(img_source_path, root_folder)
    remove_noise_and_apply_median_filter(root_folder, filter_size=3)
    delete_temp_files(img_source_path, root_folder)
    return "/Users/minjun9282/PycharmProjects/myflask/web_datas/output/segmented_images/uploaded_image/result_image.jpg"

if __name__ == '__main__':
    app.run(debug=True)
