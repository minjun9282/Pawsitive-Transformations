# 프로젝트 소개
- Pawsitive Transformations는 유기견의 공고사진의 배경과 바닥을 더 매력적이게 바꿔 유기견의 입양률에 도움을 주기 위해 개발된 서비스입니다.<br>

# 프로젝트 배경
- 매년 8만여마리 이상의 유기견이 발생하고 이들 중 약 30%만이 입양됩니다.
- 유기견의 공고가 올라온지 10일 이내 입양되지 않으면 유기견은 안락사 대기 상태에 놓입니다.
- 유기견의 공고사진은 예비 입양자들에게 주어지는 유일한 시각적인 정보로 첫 인상에 큰 영향을 미칩니다.
- 유기견 보호소는 각자의 환경과 여력에 따라 유기견의 공고사진을 신경써서 찍어주지 못하는 경우도 있습니다.
  이에 저희는 사용자가 유기견의 공고사진을 업로드하면 자동으로 공고사진의 배경과 바닥을 깔끔하게 변경하여 주는 서비스를 개발했습니다.

# 핵심 기능 소개
## 배경, 바닥, 강아지를 각각의 객체로 image segmentaton
facebook의 detectron2모델을 활용하여 업로드된 공고사진에서 배경, 바닥, 강아지에 대해 image segmentation을 진행합니다.
<img width="1103" alt="스크린샷 2023-11-30 오후 3 30 46" src="https://github.com/minjun9282/Pawsitive-Transformations/assets/54523704/af894142-0fe8-494a-ad72-a55fed7457ec">

## 이미지의 구도와 원근을 계산
segmentation된 결과물을 활용하여 업로드된 이미지에서 배경과 바닥의 구도를 계산합니다.<br>
또한 각 개체의 넓이를 활용하여 배경과 바닥에 대한 개의 원근을 고려합니다.
<img width="847" alt="스크린샷 2023-11-30 오후 3 24 05" src="https://github.com/minjun9282/Pawsitive-Transformations/assets/54523704/5dcdb6ba-8588-4678-8162-b1f9b57bb0cd">

## 유기견 공고사진 변환
기존 유기견 공고사진의 구도와 원근을 고려하여 배경과 바닥을 새롭게 합성하여 더 매력있게 변환해줍니다.
<img width="814" alt="스크린샷 2023-11-30 오후 3 33 51" src="https://github.com/minjun9282/Pawsitive-Transformations/assets/54523704/2a7e50d1-eceb-4343-bf79-07d4d37e366f">

## 모델을 편하게 이용할 수 있는 웹 개발
flask를 활용하여 사용자가 이미지를 업로드하고 변환된 이미지를 다운받을 수 있는 편리하고 직관적인 인터페이스를 개발했습니다.
<img width="799" alt="스크린샷 2023-11-30 오후 3 32 07" src="https://github.com/minjun9282/Pawsitive-Transformations/assets/54523704/fca3216e-b0ca-47af-b852-e245568a8c04">


<br>

# 프로젝트 구조<br>

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
# 데모 영상


https://github.com/minjun9282/Pawsitive-Transformations/assets/54523704/a8936084-068d-4dde-8bec-ba482deec83b


<br><br>
