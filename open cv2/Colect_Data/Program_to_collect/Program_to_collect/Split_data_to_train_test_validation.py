import cv2
import os
import numpy as np
import shutil

path_all_data = r"/Colect_Data/all_images/"
train_path=r"C:/Users/MILAD FOR COMPUTER/Desktop/open cv2/Colect_Data/Train_data"
test_path=r"C:/Users/MILAD FOR COMPUTER/Desktop/open cv2/Colect_Data/Test_Data"
validate_path=r"C:/Users/MILAD FOR COMPUTER/Desktop/open cv2/Colect_Data/Validate_Data"
train_ratio=0.5
test_ratio=0.35
validate_ratio=0.15
def main():
    all_images=os.listdir(path_all_data)
    list=[i for i in range(10)]

    random_list_len_images=np.random.permutation(len(all_images))
    size_train=int(train_ratio*len(random_list_len_images))
    size_test=int(test_ratio*len(random_list_len_images))
    size_validation=int(validate_ratio*len(random_list_len_images))
    print(f"Total size: {len(random_list_len_images)}  size_train : {size_train}  size_test:{size_test} size_validation : {size_validation}")
    for i in range(len(all_images)):
        if i<size_train:
            shutil.copy(path_all_data + all_images[random_list_len_images[i]], train_path)
        elif i<size_train+size_test:
            shutil.copy(path_all_data + all_images[random_list_len_images[i]], test_path)
        else:
            shutil.copy(path_all_data + all_images[random_list_len_images[i]], validate_path)

    # splitfolders.ratio(path, seed=1337, output="Chess-Splitted", ratio=(0.6, 0.2, 0.2))


if __name__ == "__main__":
    main()