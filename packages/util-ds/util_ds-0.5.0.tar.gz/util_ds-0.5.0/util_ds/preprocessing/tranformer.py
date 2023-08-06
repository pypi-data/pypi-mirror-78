from ..nlp.os import read_content

UNKNOWN_TOKEN = "[UNK]"
PAD_TOKEN = "[PAD]"
START_DECODING = "[START]"
STOP_DECODING = "[STOP]"

class Vocab():
    
    def __init__(self, vocab_file, max_size):
        self.word_to_id = {}
        self.id_to_word = {}
        self.count = 0
        self.max_size = max_size
        # initial the word and index 
        self.initial_word()
        self.build_vocab(vocab_file)

    def initial_word(self):
        # [UNK], [PAD], [START] and [STOP] get the ids 0,1,2,3.
        for w in [UNKNOWN_TOKEN, PAD_TOKEN,
                  START_DECODING, STOP_DECODING]:
            self.word_to_id[w] = self.count
            self.id_to_word[self.count] = w
            self.count += 1

    def build_vocab(self, vocab_file):
        """Read the vocab file to self.word_to_id and 
        self.id_to_word.
        """
        content = read_content(vocab_file)
        content = content.split("\n")
        for item in content: 
            # can not over the max size
            if self.count <= self.max_size:
                self.word_to_id[item.strip()] = self.count
                self.id_to_word[self.count] = item.strip()
                self.count += 1

    def size(self):
        return self.count 

    def word2id(self, word):
        """ Word to idx
        """
        if word not in self.word_to_id:
            return self.word_to_id[UNKNOWN_TOKEN]
        return self.word_to_id[word]

    def id2word(self, word_id):
        """ index to word
        """
        if word_id not in self.id_to_word:
            raise ValueError('Id not found in vocab: {}'.format(word_id))
        return self.id_to_word[word_id]


class transformer():

    def __init__(self, vocab_file, max_size):
        self.vocab = Vocab(vocab_file, max_size)

    def article2ids(self, article, oovs=[]):
        """

        # Arguments
            - article {str}: "w1 w2 w3"
        # Return
            - ids, oovs: ([13375, 536, 854, 269, 10, 23, 5, 3984, 5, 50001], ['。\r'])
        """
        ids = []
        # print(article)
        unk_id = self.vocab.word2id(UNKNOWN_TOKEN)
        article_words = article.split(" ")
        for w in article_words:
            w = w.strip()
            i = self.vocab.word2id(w)
            if i == unk_id: # If w is OOV
                if w not in oovs: # Add to list of OOVs
                    oovs.append(w)
                oov_num = oovs.index(w) # This is 0 for the first article OOV, 1 for the second article OOV...
                ids.append(self.vocab.size() + oov_num) # This is e.g. 50000 for the first article OOV, 50001 for the second...
            else:
                ids.append(i)
        return ids, oovs
    
    def outputids2words(self, id_list, article_oovs):
        """

        # Arguments
            - id_list {list}: [1,2,3]
            - article_oovs {list}: ['w1', 'w2']
        """
        words = []
        for i in id_list:
            try:
                w = self.vocab.id2word(i) # might be [UNK]
            except ValueError as e: # w is OOV
                assert article_oovs is not None, "Error: model produced a word ID that isn't in the vocabulary. This should not happen in baseline (no pointer-generator) mode"
                article_oov_idx = i - self.vocab.size()
                try:
                    w = article_oovs[article_oov_idx]
                except ValueError as e: # i doesn't correspond to an article oov
                    raise ValueError('Error: model produced word ID %i which corresponds to article OOV %i but this example only has %i article OOVs' % (
                        i, article_oov_idx, len(article_oovs)))
            words.append(w)
        return words

