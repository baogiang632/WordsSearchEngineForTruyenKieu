# -*- coding: utf-8 -*-
"""SearchEngine_20127446.ipynb

## 0. Student information

Tên: Giang Gia Bảo
MSSV: 20127446
Lớp: 20TGMT
"""
## Import thư viện
import pandas as pd
import re
from nltk import ngrams
from gensim.models import Word2Vec
import unidecode
input_file_path = "truyen_kieu_data.txt" # original file
output_file_path = "truyen_kieu_dict.txt" # file dictionary
file_unidecode = "truyen_kieu_unidecode.txt" # file after lọc hết dấu

"""## 1. Các hàm đọc ghi file và tạo Dictionary

### 1.1 Hàm lọc dấu cho văn bản
"""

def remove_digits_punctuation(input_string):
    # Loại bỏ số
    output_string = re.sub(r'\d+', '', input_string)

    # Loại bỏ dấu chấm và dấu phẩy
    # output_string = output_string.replace('.', '').replace(',', '').replace(':', '')
    output_string = re.sub(r'[^\w\s]', '', output_string)

    return output_string

"""### 1.2 Đọc file và tạo dictionary"""

def save_words_to_dictionary(file_path):
    dictionary = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()  # Loại bỏ dấu xuống dòng và khoảng trắng thừa
            line = remove_digits_punctuation(line)  # Loại bỏ số và dấu trong câu
            line = line.lower()
            words = line.strip().split()
            for word in words:
                if word in dictionary:
                    dictionary[word].append(line_number)
                else:
                    dictionary[word] = [line_number]
    return dictionary

"""### 1.3 Hàm ghi Dictionary vào file txt và ghi văn bản đã lọc dấu"""

def write_dictionary_to_file(dictionary, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        for word, line_numbers in dictionary.items():
            line = f"{word}: {', '.join(map(str, line_numbers))}\n"
            file.write(line)

def save_words_to_FileTXT(input_file_path, output_file_path2):
    fileWrite = open(output_file_path2, 'w', encoding='utf-8')
    with open(input_file_path, 'r', encoding='utf-8') as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()  # Loại bỏ dấu xuống dòng và khoảng trắng thừa
            line = remove_digits_punctuation(line)  # Loại bỏ số và dấu trong câu
            fileWrite.write(line + '\n')

"""## 2. Các hàm xử lý Dictionary, Words Search

### 2.1 Đọc Dictionary từ file txt
"""

def read_dictionary_file(file_path):
    dictionary = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            word, line_numbers = line.strip().split(':')
            line_numbers = [int(num) for num in line_numbers.split(',')]
            dictionary[word.strip()] = line_numbers
    return dictionary

"""### 2.2 Hàm Words Search"""

# Search 1 từ
def search_lines_by_word(dictionary, word):
    word = word.lower()  # Chuyển đổi từ nhập vào thành chữ thường
    lines = []
    if word in dictionary:
        line_numbers = dictionary[word]
        with open(input_file_path, 'r', encoding='utf-8') as file:
            for line_number, line in enumerate(file, start=1):
                if line_number in line_numbers:
                    lines.append(line.strip())
    return lines

# Search 2 từ
def search_lines_by_2word(dictionary, word):
    word = word.lower()  # Chuyển đổi từ nhập vào thành chữ thường
    lines = []
    if word in dictionary:
        line_numbers = dictionary[word]
        with open(input_file_path, 'r', encoding='utf-8') as file:
            for line_number, line in enumerate(file, start=1):
                if line_number in line_numbers:
                    lines.append(line.strip())
    return lines

# Search tổ hợp nhiều từ
def search_lines_by_words(dictionary, words):
    normalized_words = [word.lower() for word in words]  # Chuyển đổi các từ nhập vào thành chữ thường
    lines = []

    # Kiểm tra nếu tất cả các từ đều tồn tại trong từ điển
    if all(word in dictionary for word in normalized_words):
        line_numbers = [dictionary[word] for word in normalized_words]
        common_line_numbers = set.intersection(*map(set, line_numbers))

        with open(file_unidecode, 'r', encoding='utf-8') as file:
            for line_number, line in enumerate(file, start=1):
                if line_number in common_line_numbers:
                    line_combined = str(line_number) + '. ' + line.strip()
                    lines.append(line_combined)

    return lines

"""## 3. Run search engine

### 3.1 Đọc file data và tạo Dictionary
"""

# Tạo Dictionary từ file data input
dict_result = save_words_to_dictionary(input_file_path)
# Ghi văn bản đã lọc số, dấu vào file txt
save_words_to_FileTXT(input_file_path, file_unidecode)
# Ghi từ điển đã tạo vào file txt
write_dictionary_to_file(dict_result, output_file_path)

"""### 3.2 Run word search engine"""

search_words = input("Nhập các từ cần tìm kiếm: ").split()
search_words = [word.strip() for word in search_words]

lines_containing_word = search_lines_by_words(dict_result, search_words)
if lines_containing_word:
    print(f"Các dòng chứa từ '{search_words}':")
    for line in lines_containing_word:
        print(line)
else:
    print(f"Từ '{search_words}' không tồn tại trong từ điển.")