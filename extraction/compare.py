import librosa
import numpy as np
from scipy.spatial.distance import cdist
import os

# Hàm để trích xuất đặc trưng từ một tệp âm thanh
def extract_features(file_path):
    y, sr = librosa.load(file_path)  # Tải tệp âm thanh và trả về chuỗi âm thanh y và tần số mẫu sr
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)  # Trích xuất các hệ số MFCC từ chuỗi âm thanh
    mfccs_mean = np.mean(mfccs, axis=1)  # Tính giá trị trung bình của các hệ số MFCC theo từng hàng
    return mfccs_mean  # Trả về giá trị trung bình của các hệ số MFCC

# Hàm để tìm các tệp tương tự nhất
def find_similar_files(reference_file, files_directory, top_n=3):
    reference_features = extract_features(reference_file)  # Trích xuất đặc trưng từ tệp tham chiếu
    similarities = []  # Khởi tạo danh sách để lưu các tệp tương tự và độ tương tự của chúng

    for file_name in os.listdir(files_directory):  # Duyệt qua tất cả các tệp trong thư mục
        file_path = os.path.join(files_directory, file_name)  # Tạo đường dẫn đầy đủ đến tệp
        if file_path.endswith('.mp3') and file_path != reference_file:  # Kiểm tra xem tệp có phải là tệp mp3 và không phải là tệp tham chiếu không
            features = extract_features(file_path)  # Trích xuất đặc trưng từ tệp hiện tại
            similarity = np.linalg.norm(reference_features - features)  # Tính độ tương tự (khoảng cách Euclidean) giữa tệp tham chiếu và tệp hiện tại
            similarities.append((file_name, similarity))  # Thêm tên tệp và độ tương tự vào danh sách

    similarities.sort(key=lambda x: x[1])  # Sắp xếp danh sách dựa trên độ tương tự (giá trị thấp hơn có độ tương tự cao hơn)
    return similarities[:top_n]  # Trả về top N tệp tương tự nhất


# Paths to the reference file and the directory containing MP3 files
reference_file = os.getcwd()+'\\audio_new\\new\\1- The Environment _ English Conversation (128 kbps).mp3'
files_directory = os.getcwd()+'\\audio_new\\1_Environment'
files_directory = os.getcwd()+'\\audio_new\\2_Ai'

# Find and print the most similar files
most_similar_files = find_similar_files(reference_file, files_directory)
for file_name, similarity in most_similar_files:
    print(f"File: {file_name}, Similarity: {similarity}")
