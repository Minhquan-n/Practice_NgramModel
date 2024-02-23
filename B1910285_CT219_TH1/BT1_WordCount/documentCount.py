# Cau 1: Dem so luong sub-directories, so luong documents theo tung nhosm corpus, train, test va domain
# Ket qua tong hop duoc luu tai thu muc KetQua/BaiTap1/Cau1

import pandas as pd
import os

# So luong sub-directories trong corpus
# Ket qua luu vao file assignment/B1910285_CT219_TH1/KetQua/BaiTap1/DanhSachSub-Directories.xlsx
train_sub_directories = os.listdir('assignment/Train/new train')
test_sub_directories = os.listdir('assignment/Test/new test')
sub_directories_data = [
    [len(train_sub_directories), ', '.join(train_sub_directories)],
    [len(test_sub_directories), ', '.join(test_sub_directories)],
    [len(test_sub_directories) + len(train_sub_directories), ', '.join(test_sub_directories)]
  ]
sub_directories = pd.DataFrame(sub_directories_data,
                               columns=['So luong', 'Danh sach sub-directories'],
                               index=['Train', 'Test', 'Corpus'])
sub_directories.to_excel('assignment/B1910285_CT219_TH1/KetQua/BaiTap1/Cau1/SoLuongSub_directories.xlsx')

# So luong document trong corpus
# Theo tap train va test
train_document_data = []
train_document_sum = 0
test_document_data = []
test_document_sum = 0

for domain in train_sub_directories:
  documents = os.listdir(f'assignment/Train/new train/{domain}')
  train_document_data.append([domain, len(documents)])
  train_document_sum += len(documents)

for domain in test_sub_directories:
  documents = os.listdir(f'assignment/Test/new test/{domain}')
  test_document_data.append([domain, len(documents)])
  test_document_sum += len(documents)

train_test_documents = pd.DataFrame([[train_document_sum, test_document_sum, (train_document_sum + test_document_sum)]],
                                    columns=['Train', 'Test', 'Corpus'],
                                    index=['Total document'])
train_test_documents.to_excel('assignment/B1910285_CT219_TH1/KetQua/BaiTap1/Cau1/SoLuongDocument.xlsx')

# Theo tung domain. Ket qua luu tai file assignment/B1910285_CT219_TH1/KetQua/BaiTap1/SoLuongDocument.xlsx
# Ham lay ten domain tu mang
def get_domain_name(e):
  return e[0]

# Sap xep lai mang chua so luong document tap train va test
# Tap train va test deu co so luong (27 sub-directories) va ten cac sub-directories giong nhau
train_document_data = sorted(train_document_data, reverse=False, key=get_domain_name)

# Tao bang thong ke so luong document theo tung domain
domain_document_data = []
for index in range(len(train_document_data)):
  data = [train_document_data[index][0],
          train_document_data[index][1],
          test_document_data[index][1],
          (train_document_data[index][1] + test_document_data[index][1])]
  domain_document_data.append(data)

domain_documents = pd.DataFrame(domain_document_data, columns=['Domain', 'Train', 'Test', 'Total Document'])
domain_documents.to_excel('assignment/B1910285_CT219_TH1/KetQua/BaiTap1/Cau1/SoLuongDocument_domain.xlsx')