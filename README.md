# AAML

- [ ] Trying to solve the anti aliasing problem with machine learning models. In this project, 3x3 filter used for prediction the middle pixels RGBA values.

- [x] For this project .png, .jpg and .jpeg image files can be used for the dataset.

- [x] At this point, it is important to enlarge the data set. After that, training will be done using the machine learning model and dataset and tests will be done on many pictures.

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

## Latest Error Score

## Results

- Latest Result Date : 05/01/2023

Original                   | Row By Row by 3x3 filter  |  Full Image by 3x3 filter
:-------------------------:|:-------------------------:|:-------------------------:
![test](https://user-images.githubusercontent.com/76731692/210861435-ad89748d-e9e8-4989-bbd5-3ca8c0e45ca6.jpg) | ![index](https://user-images.githubusercontent.com/76731692/210861766-365dc726-e232-4cd3-ba08-71717fb83706.png)  |  ![image](https://user-images.githubusercontent.com/76731692/210861126-bf61f96d-1e83-4475-8601-51d97221b9e5.png)

- At the row by row version, model predicts one row and changes the pixel values and predict below row. This can be useful because when model is predicting it uses upper predicted row.

- At the full image version, model predicts with original image for all pixel values.
