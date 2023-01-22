# AAML

[Attributes](https://github.com/alpertunga-bile/AAML#attributes) | [Results](https://github.com/alpertunga-bile/AAML#results)

- [ ] Trying to solve the anti-aliasing problem with machine learning models. In this project, a 3x3 filter was used to estimate the middle pixel values based on RGBA. As an alternative research, it is tried to increase the image quality with these models.

- [x] For this project PNG, JPG and JPEG image files can be used for the dataset.

- [x] At this point, it is important to enlarge the data set. After that, training will be done using the machine learning model and dataset then tests will be done on many pictures.

- [x] Currently "ADAM_RGB" and "model" is trained and the results are taken with "model" at 15/01/2023 and before. The training is ongoing.

- [x] Using Python 3.7.8. Used packages can be found in requirements.txt file.

## Attributes

- top_left_r
- top_left_g
- top_left_b
- top_left_a
- top_r
- top_g
- top_b
- top_a
- top_right_r
- top_right_g
- top_right_b
- top_right_a
- left_r
- left_g
- left_b
- left_a
- right_r
- right_g
- right_b
- right_a
- bottom_left_r
- bottom_left_g
- bottom_left_b
- bottom_left_a
- bottom_r
- bottom_g
- bottom_b
- bottom_a
- bottom_right_r
- bottom_right_g
- bottom_right_b
- bottom_right_a
- middle_r
- middle_g
- middle_b
- middle_a

## Results

- At the row by row version, model predicts one row and changes the pixel values and predict below row. This can be useful because when model is predicting it uses upper predicted row.

- At the full image version, model predicts with all of the original image's pixel values then changes the pixel values.

---------------------------------------

- Latest Result Date : 15/01/2023

Original                   | Row By Row by 3x3 filter  |  Full Image by 3x3 filter
:-------------------------:|:-------------------------:|:-------------------------:
![test](https://user-images.githubusercontent.com/76731692/210861435-ad89748d-e9e8-4989-bbd5-3ca8c0e45ca6.jpg) | ![row](https://user-images.githubusercontent.com/76731692/212498916-35dd40b5-9dcf-4c33-b28b-8bb94e4da7a9.png) | ![full](https://user-images.githubusercontent.com/76731692/212498921-92b83d31-dad2-4cc8-9c4a-9134b6477611.png)

---------------------------------------


- Latest Result Date : 11/01/2023

Original                   | Row By Row by 3x3 filter  |  Full Image by 3x3 filter
:-------------------------:|:-------------------------:|:-------------------------:
![test](https://user-images.githubusercontent.com/76731692/210861435-ad89748d-e9e8-4989-bbd5-3ca8c0e45ca6.jpg) | ![index](https://user-images.githubusercontent.com/76731692/211912066-fb25fe50-d27d-45ae-bc1c-7b14bb768f7e.png) | ![index](https://user-images.githubusercontent.com/76731692/211912160-c75e4eea-837e-471c-9734-40e67b017c90.png)

---------------------------------------

- Latest Result Date : 10/01/2023

Original                   | Row By Row by 3x3 filter  |  Full Image by 3x3 filter
:-------------------------:|:-------------------------:|:-------------------------:
![test](https://user-images.githubusercontent.com/76731692/210861435-ad89748d-e9e8-4989-bbd5-3ca8c0e45ca6.jpg) | ![index](https://user-images.githubusercontent.com/76731692/211661444-db05ad67-578a-4871-86e8-bd6ea98cab75.png) | ![index](https://user-images.githubusercontent.com/76731692/211661555-fb05eabb-e888-483b-b156-9612e9a09627.png)

---------------------------------------

- Latest Result Date : 05/01/2023

Original                   | Row By Row by 3x3 filter  |  Full Image by 3x3 filter
:-------------------------:|:-------------------------:|:-------------------------:
![test](https://user-images.githubusercontent.com/76731692/210861435-ad89748d-e9e8-4989-bbd5-3ca8c0e45ca6.jpg) | ![index](https://user-images.githubusercontent.com/76731692/210861766-365dc726-e232-4cd3-ba08-71717fb83706.png)  |  ![image](https://user-images.githubusercontent.com/76731692/210861126-bf61f96d-1e83-4475-8601-51d97221b9e5.png)
