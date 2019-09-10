from sklearn import svm
import cv2
import numpy as np
import os

train_images_path = os.getcwd() + "/dataset/training"
validation_images_path = os.getcwd() + "/dataset/validation"
test_images_path = os.getcwd() + "/dataset/test"

def get_images(src_path):
    list = []
    for filename in os.listdir(src_path):
        try:
            image = cv2.imread(src_path + "/" + filename, cv2.IMREAD_GRAYSCALE) # for grayscale 2D array
            list.append(image.flatten())
        except:
            continue
    return list

X_train = get_images(train_images_path)
X_validation = get_images(validation_images_path)

X_train_np = np.array(X_train)

# fit the model
clf = svm.OneClassSVM(nu=0.1, kernel="rbf", gamma=0.1)
clf.fit(X_train_np)

train_data = clf.predict(X_train_np)

X_validation_np = np.array(X_validation)
validation_data = clf.predict(X_validation_np)

n_error_train_data = train_data[train_data == -1].size
n_error_validation_data = validation_data[validation_data == -1].size

n_found_validation_data = validation_data[validation_data == 1].size

print(str(n_error_train_data / len(train_data)) + " errors in train data")
print(str((float(n_error_validation_data) / float(len(validation_data))) * 100) + " % Error rate in validation data")
print(str(n_found_validation_data) + " images contain esaa or jovita lastname")

test_images = get_images(test_images_path)
test_np = np.array(test_images)
test_data_result = clf.predict(test_np)

n_found_in_test_data = test_data_result[test_data_result == 1].size
print(str(n_found_in_test_data) + " images contain esaa or jovita lastname in test data")
