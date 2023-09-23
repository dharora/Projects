import matplotlib.pyplot as plt
from skimage.feature import hog
import numpy as np
import pickle
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import LabelBinarizer
from sklearn.metrics import precision_score, recall_score, accuracy_score, confusion_matrix

# Specify the path to the directory containing CIFAR-10 dataset files
cifar10_dir = '/Users/dhruvarora/Downloads/cifar-10-batches-py'

# Load CIFAR-10 dataset
#reads a CIFAR-10 data file and returns its contents
def unpickle(file):
    with open(file, 'rb') as fo:
        data = pickle.load(fo, encoding='bytes')
    return data

#load the CIFAR-10 dataset into training and testing sets. Call the unpickle function to read data files and organize them into NumPy arrays.
def load_cifar10_data():
    train_data = []
    train_labels = []
    for i in range(1, 6):
        batch = unpickle(f'{cifar10_dir}/data_batch_{i}')
        train_data.extend(batch[b'data'])
        train_labels.extend(batch[b'labels'])

    test_batch = unpickle(f'{cifar10_dir}/test_batch')
    test_data = test_batch[b'data']
    test_labels = test_batch[b'labels']

    return np.array(train_data), np.array(train_labels), np.array(test_data), np.array(test_labels)

X_train, y_train, X_test, y_test = load_cifar10_data()

# Visualize an example image
plt.imshow(X_train[0].reshape(3, 32, 32).transpose(1, 2, 0))
plt.show()

# Flatten the images
X_train_flat = X_train.reshape(X_train.shape[0], -1)
X_test_flat = X_test.reshape(X_test.shape[0], -1)

# Extract HOG features for each channel separately and concatenate into a single feature vector
def extract_hog_features(image):
    hog_features = []
    for channel in range(image.shape[0]):
        channel_feature, _ = hog(image[channel], orientations=9, pixels_per_cell=(8, 8), cells_per_block=(2, 2), visualize=True, block_norm='L2')
        hog_features.extend(channel_feature)
    return np.array(hog_features)

X_train_hog = np.array([extract_hog_features(image.reshape(3, 32, 32)) for image in X_train])
X_test_hog = np.array([extract_hog_features(image.reshape(3, 32, 32)) for image in X_test])

# Create a label binarizer to convert class labels into one-hot encoded vectors for multi-class classification.
lb = LabelBinarizer()
lb.fit(y_train)
y_train_one_hot = lb.transform(y_train)
y_test_one_hot = lb.transform(y_test)

# Create an MLP classifier
clf = MLPClassifier(hidden_layer_sizes=(128, 64, 10), solver='sgd', learning_rate_init=0.001, max_iter=30)

# Fit/Train the classifier
clf.fit(X_train_hog, y_train_one_hot)

# Predict on the test set
y_pred_one_hot = clf.predict(X_test_hog)

# Inverse transform to get class labels
y_pred = lb.inverse_transform(y_pred_one_hot)

# Evaluate the classifier
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

precision = precision_score(y_test, y_pred, average=None)
print("Precision:", precision)

recall = recall_score(y_test, y_pred, average=None)
print("Recall:", recall)

conf_mat = confusion_matrix(y_test, y_pred)
print("Confusion Matrix:")
print(conf_mat)

# Print class-wise confusion matrix
class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']
for i in range(len(class_names)):
    print(f"Class '{class_names[i]}' - Precision: {precision[i]}, Recall: {recall[i]}")
