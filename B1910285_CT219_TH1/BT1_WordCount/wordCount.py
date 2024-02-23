# Cau 2: Dem so luong cau, so luong tu, xac dinh cau dai nhat (do dai), cau ngan nhat (do dai) va do dai trung binh cau
# theo cac nhom corpus, train, test va domain
# Cac ket qua tong hop duoc luu tai thu muc KetQua/BaiTap1/Cau2

import pandas as pd
import os
import math
from underthesea import sent_tokenize, word_tokenize
# Khai bao cac bien
# corpus = [total_sentence, total_word, longest_sent, longest_sent_word_count, shortest_sent, shortest_sent_word_count, average_word]
CORPUS = [0, 0, '', 0, '', 0, 0]
# train = [total_train_sentence, total_train_word, train_longest_sent, train_longest_sent_word_count, train_shortest_sent, train_shortest_sent_word_count, train_average_word]
TRAIN = [0, 0, '', 0, '', math.inf, 0]
# test = [total_test_sentence, total_test_word, test_longest_sent, test_longest_sent_word_count, test_shortest_sent, test_shortest_sent_word_count, test_average_word]
TEST = [0, 0, '', 0, '', math.inf, 0]
# domain = [[total_domain_sentence, total_domain_word, domain_longest_sent, domain_longest_sent_word_count, domain_shortest_sent, domain_shortest_sent_word_count, domain_average_word], ...]
DOMAIN = []

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
                if s != '':
                    sent_list.append(s)

    return sent_list

# Xac dinh cau dai nhat, ngan nhat, so luong cau, so luong tu.
def extract_sent_word(sent_list):
    word_count = 0
    longest = {'sent': '', 'count': 0}
    shortest = {'sent': '', 'count': math.inf}

    for sent in sent_list:
        words = word_tokenize(sent)
        # Tong hop so luong cau, tu, cau dai nhat va ngan nhat
        word_count += len(words)

        if len(words) > longest['count']:
            longest = {'sent': sent, 'count': len(words)}

        if len(words) < shortest['count']:
            shortest = {'sent': sent, 'count': len(words)}

    return len(sent_list), word_count, longest, shortest

# Xac dinh cau dai nhat, ngan nhat, so luong cau, so luong tu.
def extract_from_sub_directory(path):
    sd_sent_count = 0
    sd_word_count = 0
    sd_longest = {'sent': '', 'count': 0}
    sd_shortest = {'sent': '', 'count': math.inf}

    for doc in os.listdir(path):
        sent_list = read_from_file(path+'/'+doc)

        sent_count, word_count, longest, shortest= extract_sent_word(sent_list)
        sd_sent_count += sent_count
        sd_word_count += word_count
        if (sd_longest['count'] < longest['count']):
            sd_longest = longest
        if (sd_shortest['count'] > shortest['count']):
            sd_shortest = shortest

    return sd_sent_count, sd_word_count, sd_longest, sd_shortest

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

    # Tong hop va cap nhat tap tu vung cua tap train
    train_sc, train_wc, train_longest, train_shortest= extract_from_sub_directory(train_path+domain)

    #  Tong hop va cap nhat tap tu vung cua tap test
    test_sc, test_wc, test_longest, test_shortest= extract_from_sub_directory(test_path+domain)

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

TRAIN[6] = TRAIN[1] // TRAIN[0]
TEST[6] = TEST[1] // TEST[0]

# Tong hop so cau, so tu, cau ngan nhat va dai nhat
CORPUS[2] = TRAIN[2] if TRAIN[3] > TEST[3] else TEST[2]
CORPUS[3] = TRAIN[3] if TRAIN[3] > TEST[3] else TEST[3]
CORPUS[4] = TRAIN[4] if TRAIN[5] < TEST[5] else TEST[4]
CORPUS[5] = TRAIN[5] if TRAIN[5] < TEST[5] else TEST[5]
CORPUS[0] = TRAIN[0] + TEST[0]
CORPUS[1] = TRAIN[1] + TEST[1]
CORPUS[6] = (TRAIN[1] + TEST[1]) // (TRAIN[0] + TEST[0])

column = ['Total Sentence', 'Total Word', 'Longest Sentence', 'Word count (longest)',
          'Shortest Sentences', 'Word count (shortest)', 'Average Word']
data = pd.DataFrame([TRAIN, TEST, CORPUS], columns=column, index=['Train', 'Test', 'Corpus'])
data.to_excel('assignment/B1910285_CT219_TH1/KetQua/BaiTap1/Cau2/SoLuongCauTu.xlsx')

domain_data = pd.DataFrame(DOMAIN, columns=column, index=domain_list)
domain_data.to_excel('assignment/B1910285_CT219_TH1/KetQua/BaiTap1/Cau2/SoLuongCauTuTheoDomain.xlsx')