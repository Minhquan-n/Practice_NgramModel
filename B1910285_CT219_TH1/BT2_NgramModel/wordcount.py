# Cau 1: Xac dinh so luong cau, so luong tu, cau dai nhat, cau ngan nhat va do dai trung binh cua cau
# Cac ket qua thu duoc duoc luu vao thu muc KetQua/BaiTap2
# Tong hop tap tu vung theo tung nhom corpus, train, test, domain; tong hop danh sach cau theo tung domain

import math
import os
import pandas as pd
import string

from underthesea import sent_tokenize

# Khai bao cac bien
# corpus = [total_sentence, total_word, longest_sent, longest_sent_word_count, shortest_sent, shortest_sent_word_count, average_word]
CORPUS = [0, 0, '', 0, '', 0, 0]
# train = [total_train_sentence, total_train_word, train_longest_sent, train_longest_sent_word_count, train_shortest_sent, train_shortest_sent_word_count, train_average_word]
TRAIN = [0, 0, '', 0, '', math.inf, 0]
# test = [total_test_sentence, total_test_word, test_longest_sent, test_longest_sent_word_count, test_shortest_sent, test_shortest_sent_word_count, test_average_word]
TEST = [0, 0, '', 0, '', math.inf, 0]
# domain = [[total_domain_sentence, total_domain_word, domain_longest_sent, domain_longest_sent_word_count, domain_shortest_sent, domain_shortest_sent_word_count, domain_average_word], ...]
DOMAIN = []
# Corpus Vocabulary
VOCABULARY = {'<UNK>'}
# Train Vocabulary
TRAIN_VOCABULARY = {'<UNK>'}
# Test Vocabulary
TEST_VOCABULARY = {'<UNK>'}

# Lay danh sach cac domain
def get_domain_list():
    domain_list = []
    with open('assignment/Stats.txt') as f:
        domain_list = [row.strip() for row in f.readlines()]
        del domain_list[0:3]
        del domain_list[27:len(domain_list)]
        domain_list = [list(filter(lambda i: i != '', item.split('\t')))[0].strip() for item in domain_list]

    return domain_list

# Doc file va lay ra danh sach cac cau cua document
def read_from_file(path):
    sent_list = []

    with open(path, encoding='UTF-16') as f:
        data = list(filter(lambda i: i != '', [sent.strip() for sent in f.readlines()]))
        f.close()

        for item in data:
            # Chuyen ve chu thuong va duyet qua tat ca cac cau
            for s in sent_tokenize(item.lower()):
                # Loai bo dau cau va ky tu dac biet
                sent = str(s).translate(s.maketrans('','', (string.punctuation + '“”')))
                if sent != '':
                    sent_list.append(sent)

    return sent_list

# Xac dinh cau dai nhat, ngan nhat, so luong cau, so luong tu va cap nhat vocabulary trong danh sach cau
def extract_sent_word(sent_list):
    word_count = 0
    longest = {'sent': '', 'count': 0}
    shortest = {'sent': '', 'count': math.inf}
    word_list = set()

    for sent in sent_list:
        words = sent.split()
        if (len(words)) > 0:
            # Cap nhat tap vocabulary
            word_list.update(words)
            # Tong hop so luong cau, tu, cau dai nhat va ngan nhat
            word_count += len(words)
            if len(words) > longest['count']:
                longest = {'sent': sent, 'count': len(words)}
            if len(words) < shortest['count']:
                shortest = {'sent': sent, 'count': len(words)}

    return len(sent_list), word_count, longest, shortest, list(word_list)

# Xac dinh cau dai nhat, ngan nhat, so luong cau, so luong tu va cap nhat vocabulary trong 1 sub-directory
def extract_from_sub_directory(path):
    sd_sent_count = 0
    sd_word_count = 0
    sd_longest = {'sent': '', 'count': 0}
    sd_shortest = {'sent': '', 'count': math.inf}
    sentences = []
    word_list = set()
    for doc in os.listdir(path):
        sent_list = read_from_file(path+'/'+doc)
        sentences.extend(sent_list)

        sent_count, word_count, longest, shortest, words = extract_sent_word(sent_list)
        sd_sent_count += sent_count
        sd_word_count += word_count
        word_list.update(words)
        if (sd_longest['count'] < longest['count']):
            sd_longest = longest
        if (sd_shortest['count'] > shortest['count']):
            sd_shortest = shortest

    return sd_sent_count, sd_word_count, sd_longest, sd_shortest, sentences, list(word_list)

# Tong hop thong ke cua tap train, test va theo tung domain
train_path = 'assignment/Train/new train/'
test_path = 'assignment/Test/new test/'
domain_list = get_domain_list()

for domain in domain_list:
    print(domain)
    domain_wc = 0
    domain_sc = 0
    domain_longest = {'sent': '', 'count': 0}
    domain_shortest = {'sent': '', 'count': math.inf}
    domain_vocabulary = {'<UNK>'}

    # Tong hop va cap nhat tap tu vung cua tap train
    train_sc, train_wc, train_longest, train_shortest, train_sentences, words = extract_from_sub_directory(train_path+domain)
    TRAIN_VOCABULARY.update(words)
    domain_vocabulary.update(words)
    (pd.DataFrame(train_sentences)).to_csv(f'assignment/sentences/train/{domain}.csv', sep=',', index=False, header=False)

    #  Tong hop va cap nhat tap tu vung cua tap test
    test_sc, test_wc, test_longest, test_shortest, test_sentences, words = extract_from_sub_directory(test_path+domain)
    TEST_VOCABULARY.update(words)
    domain_vocabulary.update(words)
    (pd.DataFrame(test_sentences)).to_csv(f'assignment/sentences/test/{domain}.csv', sep=',', index=False, header=False)

    # Luu tap tu vung cua domain vao file assignment/vocabulary/domain/{domain}.csv
    (pd.DataFrame(list(domain_vocabulary))).to_csv(f'assignment/vocabulary/domain/{domain}.csv', sep=',', index=False, header=False)

    # Tong hop so cau, so tu, cau dai nhat va ngan nhat cua tap train
    TRAIN[0] += train_sc
    TRAIN[1] += train_wc
    if TRAIN[3] < train_longest['count']:
        TRAIN[2] = train_longest['sent']
        TRAIN[3] = train_longest['count']
    if TRAIN[5] > train_shortest['count']:
        TRAIN[4] = train_shortest['sent']
        TRAIN[5] = train_shortest['count']

    # Tong hop so cau, so tu, cau dai nhat va ngan nhat cua tap test
    TEST[0] += test_sc
    TEST[1] += test_wc
    if TEST[3] < test_longest['count']:
        TEST[2] = test_longest['sent']
        TEST[3] = test_longest['count']
    if TEST[5] > test_shortest['count']:
        TEST[4] = test_shortest['sent']
        TEST[5] = test_shortest['count']

    # Tong hop so cau, so tu, cau dai nhat va ngan nhat theo tung domain
    domain_sc = train_sc + test_sc
    domain_wc = train_wc + test_wc
    domain_longest = train_longest if (train_longest['count'] > test_longest['count']) else test_longest
    domain_shortest = train_shortest if (train_shortest['count'] < test_shortest['count']) else test_shortest

    DOMAIN.append([domain_sc, domain_wc,
                   domain_longest['sent'], domain_longest['count'],
                   domain_shortest['sent'], domain_shortest['count'],
                   (domain_wc // domain_sc)])

# Tinh do dai trung binh cua cau
TRAIN[6] = TRAIN[1] // TRAIN[0]
TEST[6] = TEST[1] // TEST[0]

# Tong hop so cau, so tu, cau ngan nhat, dai nhat va do dai trung binh cau
CORPUS[2] = TRAIN[2] if TRAIN[3] > TEST[3] else TEST[2]
CORPUS[3] = TRAIN[3] if TRAIN[3] > TEST[3] else TEST[3]
CORPUS[4] = TRAIN[4] if TRAIN[5] < TEST[5] else TEST[4]
CORPUS[5] = TRAIN[5] if TRAIN[5] < TEST[5] else TEST[5]
CORPUS[0] = TRAIN[0] + TEST[0]
CORPUS[1] = TRAIN[1] + TEST[1]
CORPUS[6] = (TRAIN[1] + TEST[1]) // (TRAIN[0] + TEST[0])

# Luu cac ket qua tong hop cau dai nhat, ngan nhat, so luong cau, so luong tu va do dai trung binh cau cua nhom corpus, train, test
# Luu tai file KetQua/BaiTap2/Cau1/SoLuongCauTu.xlsx
column = ['Total Sentence', 'Total Word', 'Longest Sentence', 'Word count (longest)',
                             'Shortest Sentences', 'Word count (shortest)', 'Average Word']
data = pd.DataFrame([TRAIN, TEST, CORPUS],
                    columns=column,
                    index=['Train', 'Test', 'Corpus'])
data.to_excel('assignment/B1910285_CT219_TH1/KetQua/BaiTap2/Cau1/SoLuongCauTu.xlsx', index=['Train', 'Test', 'Corpus'])

# Luu cac ket qua tong hop cau dai nhat, ngan nhat, so luong cau, so luogn tu va do dai trung binh cau cua nhom cac domain
# Luu tai file KetQua/BaiTap2/Cau1/SoLuongCauTuTheoDomain.xlsx
domain_data = pd.DataFrame(DOMAIN, 
                           columns=column,
                           index=domain_list)
domain_data.to_excel('assignment/B1910285_CT219_TH1/KetQua/BaiTap2/Cau1/SoLuongCauTuTheoDomain.xlsx', index=domain_list)

# Luu cac tap tu vung vao cac file tuong ung tai thu muc assignment/vocabulary/
pd.DataFrame(list(TRAIN_VOCABULARY)).to_csv('assignment/vocabulary/train_vocabulary.csv', sep=',', index=False, header=False)
pd.DataFrame(list(TEST_VOCABULARY)).to_csv('assignment/vocabulary/test_vocabulary.csv', sep=',', index=False, header=False)
VOCABULARY.update(list(TRAIN_VOCABULARY))
VOCABULARY.update(list(TEST_VOCABULARY))
pd.DataFrame(list(VOCABULARY)).to_csv('assignment/vocabulary/vocabulary.csv', sep=',', index=False, header=False)