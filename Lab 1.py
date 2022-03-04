import re
import statistics


# ----Main Functions----
def words_count():
    print("Source text:\n")
    frequency = {}
    document_text = open('text.txt', 'r')
    for line_ in document_text:
        print(line_)
    document_text = open('text.txt', 'r')
    text_string = document_text.read().lower()
    match_pattern = re.findall(r'\b[a-z]{2,15}\b', text_string)  # use regular names, "\b" check word boundary
    for word in match_pattern:
        count = frequency.get(word, 0)  # 0 - default value
        frequency[word] = count + 1
    frequency_list = frequency.keys()
    for words in frequency_list:
        print(words, "=>", frequency[words])


def open_file_and_clean():
    f = open('text.txt', 'r')
    f = f.read().lower()
    text = f.replace('?', '.').replace('!', '.').replace('...', '.').replace("Mr.", "mister").replace("Mrs.", "misses")
    text = text.replace("Dr.", "Doctor").replace("etc.", "etc")
    return text


def open_file_constants():
    f = open('input.txt', 'r')
    n = int(f.readline())
    k = int(f.readline())
    return n, k


def average_count_words():
    text = open_file_and_clean()
    sentences = text.split(' ')
    count_ = text.count('.')  # count of sentences
    print("Average count words: ", round(len(sentences) / count_))


def median_count_words():
    text = open_file_and_clean()
    print("Median count words: ", round(statistics.median([len(sentence.split()) for sentence in text.split(".")])))


def top_k(ngram_dict, k):
    ngram_dict = {k: ngram_dict[k] for k in sorted(ngram_dict, key=ngram_dict.get, reverse=True)}
    tmp_k = 0
    print("\nTop", k, "n-gram")
    for words in ngram_dict:
        if tmp_k < k:
            print("---- ", words, "=>", ngram_dict[words])
            tmp_k += 1


def n_gram_search(n, k):
    words_dict = {}
    ngram_dict = {}
    print("n=", n, "k=", k)
    text = open_file_and_clean()
    text = text.replace('.', ' ').replace(',', ' ').replace(':', ' ').replace('-', ' ')
    split_text = text.split()
    for word in split_text:
        count = words_dict.get(word, 0)  # 0 - default value
        words_dict[word] = count + 1
    for word in words_dict.keys():
        if len(word) >= n:
            tmp_word = word
            n_count = 0
            n_ends = n
            for i in range(len(word) - n_ends + 1):
                ngram = tmp_word[n_count:n_ends]
                if ngram in ngram_dict.keys():  # if ngram already exist in ngram_dict
                    ngram_dict[ngram] += words_dict[word]
                else:
                    ngram_dict[ngram] = words_dict[word]
                n_count += 1
                n_ends += 1
    top_k(ngram_dict, k)


def input_n_k():
    print("Do you want to leave the default values of N = 4 and K = 10? (y/n)")
    check = input()
    if check == 'y':
        n, k = open_file_constants()
        n_gram_search(n, k)
    else:
        n = input("Write n: ")
        k = input("Write k: ")
        n = int(n)
        k = int(k)
        n_gram_search(n, k)


# ----Call Main Functions----
def main():
    words_count()
    average_count_words()
    median_count_words()
    input_n_k()


if __name__ == "__main__":
    main()
