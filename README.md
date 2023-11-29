# 프로젝트 소개
- <br>


<b> </b><br><br>


# 핵심 기능 소개
## 유기견 공고사진 변환
기존 유기견 공고사진의 구도와 원근을 고려하여 배경과 바닥을 새롭게 합성하여 더 매력있게 변환해줍니다.
![image]<br>

## 프로젝트 구조<br>

```
├── local_datas
│   ├── model_final.pth
│   ├── combined.json
│   ├── img_source
│   └── dataset
├── web_datas
│   ├── input
│   └── output
├── utils
│   ├── image_segmentation.py
│   ├── make_contour_transparent.py
│   ├── connect_lines.py
│   ├── calculate_area_ratio.py
│   ├── determine_close_up.py
│   ├── perspective_transform.py
│   ├── modify_and_save_images.py
│   ├── remove_noise_and_apply_median_filter.py
│   └── delete_temp_files.py<br>
├── templates
│   └── home.html
├── static/images
└── app.py
```

<br><br>
