import librosa
from flask import Blueprint, request, jsonify
file_pb = Blueprint('file',__name__)
import os
import numpy as np
from extraction.word_extraction_new import extraction
from database.database import db

@file_pb.route('/file/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filepath = os.path.join(os.getcwd()+'\\audio_new\\new', file.filename)
    file.save(filepath)
    db.save_audio_name(file.filename,'new')
    check_list = db.get_all_information_without_test()

    # Paths to the reference file and the directory containing MP3 files
    reference_file = os.getcwd() + f'\\audio_new\\new\\{file.filename}'

    # Find and print the most similar files
    most_similar_files = find_similar_files(reference_file, check_list)

    return most_similar_files


# Hàm để trích xuất đặc trưng từ một tệp âm thanh
def extract_features(file_path):
    y, sr = librosa.load(file_path)  # Tải tệp âm thanh và trả về chuỗi âm thanh y và tần số mẫu sr
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)  # Trích xuất các hệ số MFCC từ chuỗi âm thanh
    mfccs_mean = np.mean(mfccs, axis=1)  # Tính giá trị trung bình của các hệ số MFCC theo từng hàng
    return mfccs_mean  # Trả về giá trị trung bình của các hệ số MFCC

# Hàm để tìm các tệp tương tự nhất
def find_similar_files(reference_file, check_list, top_n=3):
    reference_features = extract_features(reference_file)  # Trích xuất đặc trưng từ tệp tham chiếu

    for check in check_list:  # Duyệt qua tất cả các tệp trong thư mục
        file_path = os.path.join(os.getcwd()+'\\audio_new\\'+check['category'], check['name'])  # Tạo đường dẫn đầy đủ đến tệp
        if file_path.endswith('.mp3') and file_path != reference_file:  # Kiểm tra xem tệp có phải là tệp mp3 và không phải là tệp tham chiếu không
            features = extract_features(file_path)  # Trích xuất đặc trưng từ tệp hiện tại
            similarity = np.linalg.norm(reference_features - features)  # Tính độ tương tự (khoảng cách Euclidean) giữa tệp tham chiếu và tệp hiện tại
            check['similarity'] = float(similarity)  # Thêm tên tệp và độ tương tự vào danh sách

    check_list.sort(key=lambda x: x['similarity'])  # Sắp xếp danh sách dựa trên độ tương tự (giá trị thấp hơn có độ tương tự cao hơn)
    return check_list[:top_n]  # Trả về top N tệp tương tự nhất


