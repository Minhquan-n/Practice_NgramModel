# Cau 2: Xac dinh 10 unigram va 10 bigram xuat hien nhieu nhat.
# Tao bang unigram va bigram. Khong su dung cac phuong phap lam min
# Cac ket qua thu duoc luu vao thu muc KetQua/BaiTap2/Cau2

from collections import Counter

# Lay danh sach cac domain
def get_domain_list():
    domain_list = []
    with open('assignment/Stats.txt') as f:
        domain_list = [row.strip() for row in f.readlines()]
        del domain_list[0:3]
        del domain_list[27:len(domain_list)]
        domain_list = [list(filter(lambda i: i != '', item.split('\t')))[0].strip() for item in domain_list]

    return domain_list

def count_unigram_bigram(sentences, unigram, bigram, vocabulary):
    uni = dict(unigram)
    bi = dict(bigram)
    appeared = 0
    for sent in sentences:
        try:
            word_list = str(sent).split()
            if vocabulary.index(word_list[-1]) not in uni:
                uni[vocabulary.index(word_list[-1])] = 0
            uni[vocabulary.index(word_list[-1])] += 1
            for index in range(len(word_list) - 1):
                word1 = vocabulary.index(word_list[index])
                word2 = vocabulary.index(word_list[index + 1])

                uni[word1] = 1 if word1 not in uni else uni[word1] + 1
                if word1 not in bi:
                    bi[word1] = {word2: 1}
                bi[word1][word2] = 1 if word2 not in bi[word1] else bi[word1][word2] + 1
                appeared += 1
        except ValueError:
            continue
    return uni, bi, appeared

def get_10_common_unigram(unigram, vocabulary):
    top10 = sorted(unigram.items(), key=lambda x: x[1], reverse=True)[:10]
    common = []
    for item in top10:
        common.extend([vocabulary[item[0]], item[1]])
    return common
    
def get_10_common_bigram(bigram, vocabulary):
    top10 = []
    for item in bigram.items():
        top = sorted(item[1].items(), key=lambda x: x[1], reverse=True)[:10]
        top = list(map(lambda x: (item[0], x[0], x[1]), top))
        top10.extend(top)
        top10 = sorted(top10, key=lambda x: x[2], reverse=True)[:10]
    
    common = []
    for item in top10:
        common.extend([vocabulary[item[0]] + ' ' + vocabulary[item[1]], item[2]])
    return common

def get_thresh(counter):
    return list(counter.keys())[-1]


def good_turing(counter, thresh, total):
    new_counter = Counter()
    for item in list(counter.items()):
        if item[0] < thresh:
            if item[1] > 0:
                next = 1
                while counter[item[0] + next] == 0:
                    next += 1
                new_counter[item[0]] = ((item[0] + next) * (counter[item[0] + next])) / (total * counter[item[0]])
            else:
                next = 1
                while counter[item[0] + next] == 0:
                    next += 1
                new_counter[item[0]] = counter[item[0] + next] / total
        else:
            new_counter[item[0]] = counter[item[0]] / total
    return new_counter
    
def common_unigram_good_turing(unigram, vocabulary):
    uni = unigram
    counter = Counter(uni.values())
    thresh = get_thresh(counter)
    total = sum(counter.values())
    counter[0] += 0
    new_counter = good_turing(counter, thresh, total)
    
    for item in uni.items():
        uni[item[0]] = new_counter[item[1]]
    
    uni_total = sum(uni.values())

    for item in uni.items():
        uni[item[0]] /= uni_total
    common = get_10_common_unigram(uni, vocabulary)
    uni[vocabulary.index('<UNK>')] = new_counter[0] / uni_total
    return common, uni

def common_bigram_good_turing(bigram, vocabulary, unseen):
    bi = bigram   
    counter = Counter()
    for element in bi.values():
        for item in Counter(element.values()).items():
            counter[item[0]] += item[1]

    thresh = get_thresh(counter)
    total = sum(counter.values())
    counter[0] += unseen
    new_counter = good_turing(counter, thresh, total)
    bi_total = 0
    
    for element in bigram.items():
        for item in element[1].items():
            bi[element[0]][item[0]] += new_counter[bigram[element[0]][item[0]]]
        bi_total += sum(element[1].values())
    for element in bi.items():
        for item in element[1].items():
            bi[element[0]][item[0]] /= bi_total

    common = get_10_common_bigram(bi, vocabulary)
    bi[vocabulary.index('<UNK>')] = new_counter[0] / bi_total
    
    return common, bi