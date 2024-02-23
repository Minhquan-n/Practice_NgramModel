import ngram_func
import pandas as pd

result_uni = []
result_bi = []
result_uni_gt = []
result_bi_gt = []
domain_list = ngram_func.get_domain_list()
column = ['Word 1', 'Count', 'Word 2', 'Count', 'Word 3', 'Count', 'Word 4', 'Count', 'Word 5', 'Count',
          'Word 6', 'Count', 'Word 7', 'Count', 'Word 8', 'Count', 'Word 9', 'Count', 'Word 10', 'Count']

for domain in domain_list:
    print(domain)
    VOCABULARY = list(map(str, (pd.read_csv(f'assignment/vocabulary/domain/{domain}.csv', header=None))[0].to_list()))
    UNIGRAM = dict()
    BIGRAM = dict()
    total_bi = 0

    train_sentences = (pd.read_csv(f'assignment/sentences/train/{domain}.csv', header=None))[0].to_list()
    test_sentences = (pd.read_csv(f'assignment/sentences/test/{domain}.csv', header=None))[0].to_list()
    UNIGRAM, BIGRAM, appeared = ngram_func.count_unigram_bigram(train_sentences, UNIGRAM, BIGRAM, VOCABULARY)
    total_bi += appeared
    UNIGRAM, BIGRAM, appeared = ngram_func.count_unigram_bigram(test_sentences, UNIGRAM, BIGRAM, VOCABULARY)
    total_bi += appeared

    unseen = (len(VOCABULARY) * len(VOCABULARY)) - total_bi

    # Xac dinh 10 ngram khong ap dung lam min
    common_uni = ngram_func.get_10_common_unigram(UNIGRAM, VOCABULARY)
    result_uni.append(common_uni)
    common_bi = ngram_func.get_10_common_bigram(BIGRAM, VOCABULARY)
    result_bi.append(common_bi)

    # Xác đinh 10 ngram co ap dung good-turing
    common_uni_gt, UNIGRAM = ngram_func.common_unigram_good_turing(UNIGRAM, VOCABULARY)
    result_uni_gt.append(common_uni_gt)
    common_bi_gt, BIGRAM = ngram_func.common_bigram_good_turing(BIGRAM, VOCABULARY, unseen)
    result_bi_gt.append(common_bi_gt)

# Luu ket qua 10 ngram xuat hien nhieu nhat khong su dung phuong phap lam min
(pd.DataFrame(result_uni,columns=column,
              index=domain_list)).to_excel('assignment/B1910285_CT219_TH1/KetQua/BaiTap2/Cau2/unigram_domain.xlsx')
(pd.DataFrame(result_bi, columns=column,
              index=domain_list)).to_excel('assignment/B1910285_CT219_TH1/KetQua/BaiTap2/Cau2/bigram_domain.xlsx')

# Luu ket qua 10 ngram xuat hien nhieu nhat, ap dung good-turing
(pd.DataFrame(result_uni_gt, columns=column,
              index=domain_list)).to_excel('assignment/B1910285_CT219_TH1/KetQua/BaiTap2/Cau3/unigram_domain_goodturing.xlsx')
(pd.DataFrame(result_bi_gt, columns=column,
              index=domain_list)).to_excel('assignment/B1910285_CT219_TH1/KetQua/BaiTap2/Cau3/bigram_domain_goodturing.xlsx')

print('Done')