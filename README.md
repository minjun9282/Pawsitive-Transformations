# 프로젝트 소개
- <br>


<b> </b><br><br>


# 핵심 기능 소개
## 유기견 공고사진 변환
기존 유기견 공고사진의 구도와 원근을 고려하여 배경과 바닥을 새롭게 합성하여 더 매력있게 변환해줍니다.
![image]<br>

## 프로젝트 구조
├── local_datas<br>
│   ├── model_final.pth<br>
│   ├── combined.json<br>
│   ├── img_source<br>
│   └── dataset<br>
├── web_datas<br>
│   ├── input<br>
│   └── output<br>
├── utils<br>
│   ├── image_segmentation.py<br>
│   ├── make_contour_transparent.py<br>
│   ├── connect_lines.py<br>
│   ├── calculate_area_ratio.py<br>
│   ├── determine_close_up.py<br>
│   ├── perspective_transform.py<br>
│   ├── modify_and_save_images.py<br>
│   ├── remove_noise_and_apply_median_filter.py<br>
│   └── delete_temp_files.py<br>
├── templates<br>
│   └── home.html<br>
├── static/images<br>
└── app.py<br>

<br><br>
