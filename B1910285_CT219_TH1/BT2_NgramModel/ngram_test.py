import ngram_func
import pandas as pd

TEST_VOCABULARY = list(map(str, (pd.read_csv('assignment/vocabulary/test_vocabulary.csv', header=None))[0].to_list()))
TEST_UNIGRAM = dict()
TEST_BIGRAM = dict()
total_bi = 0
domain_list = ngram_func.get_domain_list()
column = ['Word 1', 'Count', 'Word 2', 'Count', 'Word 3', 'Count', 'Word 4', 'Count', 'Word 5', 'Count',
          'Word 6', 'Count', 'Word 7', 'Count', 'Word 8', 'Count', 'Word 9', 'Count', 'Word 10', 'Count']
index = ['Unigram', 'Bigram']

for domain in domain_list:
    print(domain)
    test_sentences = (pd.read_csv(f'assignment/sentences/test/{domain}.csv', header=None))[0].to_list()
    TEST_UNIGRAM, TEST_BIGRAM, appeared = ngram_func.count_unigram_bigram(test_sentences, TEST_UNIGRAM, TEST_BIGRAM, TEST_VOCABULARY)
    total_bi += appeared

unseen = (len(TEST_VOCABULARY) * len(TEST_VOCABULARY)) - total_bi

# Xac dinh 10 ngram khong ap dung lam min
test_common_uni = ngram_func.get_10_common_unigram(TEST_UNIGRAM, TEST_VOCABULARY)
test_common_bi = ngram_func.get_10_common_bigram(TEST_BIGRAM, TEST_VOCABULARY)
(pd.DataFrame([test_common_uni, test_common_bi],
              columns=column, index=index)).to_excel('assignment/B1910285_CT219_TH1/KetQua/BaiTap2/Cau2/ngram_test.xlsx')

# Xác đinh 10 ngram co ap dung good-turing
test_common_uni_gt, TEST_UNIGRAM = ngram_func.common_unigram_good_turing(TEST_UNIGRAM, TEST_VOCABULARY)
test_common_bi_gt, TEST_BIGRAM = ngram_func.common_bigram_good_turing(TEST_BIGRAM, TEST_VOCABULARY, unseen)
(pd.DataFrame([test_common_uni_gt, test_common_bi_gt],
              columns=column, index=index)).to_excel('assignment/B1910285_CT219_TH1/KetQua/BaiTap2/Cau3/ngram_test_goodturing.xlsx')

print('Done')