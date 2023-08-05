import itertools
import re
import string
import subprocess
import sys
import unicodedata
from os import listdir
from os.path import isfile, join

from keras.callbacks import ModelCheckpoint
from keras.layers import Dense, Dropout, LSTM
from keras.models import Sequential


def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


try:

    import wordninja

except BaseException as e:

    install("wordninja")
    import wordninja

try:

    import PyPDF2

except BaseException as e:
    install("PyPDF2")
    import PyPDF2
import nltk
import numpy
import pandas as pd
from keras.utils import np_utils
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

# hide

# collapse-hide
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('popular')
nltk.download('words')
# Constants
# POS (Parts Of Speech) for: nouns, adjectives, verbs and adverbs
DI_POS_TYPES = {'NN': 'n', 'JJ': 'a', 'VB': 'v', 'RB': 'r'}
POS_TYPES = list(DI_POS_TYPES.keys())

# Constraints on tokens
MIN_STR_LEN = 3
RE_VALID = '[a-zA-Z]'


def parse_all_pdfs_in_curr_dir():
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    listofArticles = []
    art_records = []
    stringV = ''
    for file in onlyfiles:
        try:
            fileReader = PyPDF2.PdfFileReader(open(file, 'rb'))
            pages = fileReader.getNumPages()
            print(pages, "pages")
            filetext = ''
            count = 0

            while count < pages:
                pageObj = fileReader.getPage(count)
                text = pageObj.extractText()
                filetext += (text)
                stringV += (text)
                listofArticles.append(text)
                count += 1

            filename = str(file)
            tuple = (filename, filetext)
            art_records.append(tuple)
        except:
            pass
        fileDF = pd.DataFrame.from_records(art_records, columns=['Article', 'Text'])
        fileDF['Text'] = fileDF['Text'].str.replace('\d+', '')
        return fileDF


def stopStemLem(li_quotes):  # Get stopwords, stemmer and lemmatizer
    stopwords = nltk.corpus.stopwords.words('english')
    stemmer = nltk.stem.PorterStemmer()
    lemmatizer = nltk.stem.WordNetLemmatizer()

    # Remove accents function
    def remove_accents(data):
        return ''.join(x for x in unicodedata.normalize('NFKD', data) if x in string.ascii_letters or x == " ")

    # Process all quotes
    li_tokens = []
    li_token_lists = []
    li_lem_strings = []

    for i, text in enumerate(li_quotes):
        # Tokenize by sentence, then by lowercase word
        tokens = [word.lower() for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]

        # Process all tokens per quote
        li_tokens_quote = []
        li_tokens_quote_lem = []
        for token in tokens:
            # Remove accents
            t = remove_accents(token)

            # Remove punctuation
            t = str(t).translate(string.punctuation)
            li_tokens_quote.append(t)

            # Add token that represents "no lemmatization match"
            li_tokens_quote_lem.append("-")  # this token will be removed if a lemmatization match is found below

            # Process each token
            if t not in stopwords:
                if re.search(RE_VALID, t):
                    if len(t) >= MIN_STR_LEN:
                        # Note that the POS (Part Of Speech) is necessary as input to the lemmatizer
                        # (otherwise it assumes the word is a noun)
                        pos = nltk.pos_tag([t])[0][1][:2]
                        pos2 = 'n'  # set default to noun
                        if pos in DI_POS_TYPES:
                            pos2 = DI_POS_TYPES[pos]

                        stem = stemmer.stem(t)
                        lem = lemmatizer.lemmatize(t, pos=pos2)  # lemmatize with the correct POS

                        if pos in POS_TYPES:
                            li_tokens.append((t, stem, lem, pos))

                            # Remove the "-" token and append the lemmatization match
                            li_tokens_quote_lem = li_tokens_quote_lem[:-1]
                            li_tokens_quote_lem.append(lem)

        # Build list of token lists from lemmatized tokens
        li_token_lists.append(li_tokens_quote)

        # Build list of strings from lemmatized tokens
        str_li_tokens_quote_lem = ' '.join(li_tokens_quote_lem)
        li_lem_strings.append(str_li_tokens_quote_lem)

    # Build resulting dataframes from lists
    df_token_lists = pd.DataFrame(li_token_lists)

    print("df_token_lists.head(5):")
    print(df_token_lists.head(5).to_string())

    # Replace None with empty string
    for c in df_token_lists:
        if str(df_token_lists[c].dtype) in ('object', 'string_', 'unicode_'):
            df_token_lists[c].fillna(value='', inplace=True)

    df_lem_strings = pd.DataFrame(li_lem_strings, columns=['lem quote'])

    print()
    print("")
    print("df_lem_strings.head():")
    print(df_lem_strings.head().to_string())
    # hide-input
    print("Group by lemmatized words, add count and sort:")
    df_all_words = pd.DataFrame(li_tokens, columns=['token', 'stem', 'lem', 'pos'])
    df_all_words['counts'] = df_all_words.groupby(['lem'])['lem'].transform('count')
    df_all_words = df_all_words.sort_values(by=['counts', 'lem'], ascending=[False, True]).reset_index()

    print("Get just the first row in each lemmatized group")
    df_words = df_all_words.groupby('lem').first().sort_values(by='counts', ascending=False).reset_index()
    return df_words


def format_stopstemlem(df_words):
    dfList_pos = []

    for v in POS_TYPES:
        df_pos = df_words[df_words['pos'] == v]
        # print()
        # print("POS_TYPE:", v)
        # print(df_pos.head(10).to_string())
        df = df_pos.reset_index(inplace=False)
        dfList_pos.append(df.head(10))
    return dfList_pos


def find_patterns(file):
    def tokenize_words(input):
        # lowercase everything to standardize it
        input = input.lower()

        # instantiate the tokenizer
        tokenizer = RegexpTokenizer(r'\w+')
        tokens = tokenizer.tokenize(input)

        # if the created token isn't in the stop words, make it part of "filtered"
        filtered = filter(lambda token: token not in stopwords.words('english'), tokens)
        return " ".join(filtered)

    # preprocess the input data, make tokens
    processed_inputs = tokenize_words(file)

    chars = sorted(list(set(processed_inputs)))
    char_to_num = dict((c, i) for i, c in enumerate(chars))

    input_len = len(processed_inputs)
    vocab_len = len(chars)
    print("Total number of characters:", input_len)
    print("Total vocab:", vocab_len)

    # collapse-hide
    seq_length = 100
    x_data = []
    y_data = []

    # collapse-hide
    # loop through inputs, start at the beginning and go until we hit
    # the final character we can create a sequence out of
    for i in range(0, input_len - seq_length, 1):
        # Define input and output sequences
        # Input is the current character plus desired sequence length
        in_seq = processed_inputs[i:i + seq_length]

        # Out sequence is the initial character plus total sequence length
        out_seq = processed_inputs[i + seq_length]

        # We now convert list of characters to integers based on
        # previously and add the values to our lists
        x_data.append([char_to_num[char] for char in in_seq])
        y_data.append(char_to_num[out_seq])

    # collapse-hide
    n_patterns = len(x_data)
    print("Total Patterns:", n_patterns)
    X = numpy.reshape(x_data, (n_patterns, seq_length, 1))
    X = X / float(vocab_len)
    y = np_utils.to_categorical(y_data)
    outTuple = (x_data,X, y, chars)
    return outTuple


def set_model_params(X, y):
    model = Sequential()
    model.add(LSTM(256, input_shape=(X.shape[1], X.shape[2]), return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(256, return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(128))
    model.add(Dropout(0.2))
    model.add(Dense(y.shape[1], activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam')
    filepath = "model_weights_saved.hdf5"
    checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=True, mode='min')
    desired_callbacks = [checkpoint]
    model.fit(X, y, epochs=5, batch_size=200, callbacks=desired_callbacks)
    return model


def what_does_the_robot_say(x_data,model, chars,filename="model_weights_saved.hdf5"):
    model.load_weights(filename)
    model.compile(loss='categorical_crossentropy', optimizer='adam')
    num_to_char = dict((i, c) for i, c in enumerate(chars))

    numberOfSamples = 12

    # sample = ("\"", ''.join([num_to_char[value] for value in pattern]), "\"")

    essay = []
    essays = ''

    for i in range(numberOfSamples):
        start = numpy.random.randint(0, len(x_data) - 1)

        pattern = x_data[start]
        o = (''.join([num_to_char[value] for value in pattern]))

        output = re.sub(r'\d+', '', o)
        print(output)
        essays += output

        # essay.append(sample)
        # essay.append(".")
    tokens = nltk.word_tokenize(essays)
    words = set(nltk.corpus.words.words())
    # screen for broken words with english corpus |
    string_tokens = (str(" ".join(tokens)))
    print(string_tokens)

    remove_broken_words = " ".join(w for w in nltk.wordpunct_tokenize(string_tokens) \
                                   if w.lower() in words or not w.isalpha())
    return remove_broken_words


def clean_plain_text_for_training(stringV):
    cleanedText = []
    for i in stringV:
        split = wordninja.split(i)
        cleanedText.append(split)
    # b = wordninja.split(stringV)

    print(len(cleanedText))
    out = []
    words = set(nltk.corpus.words.words())

    for i in cleanedText:
        screened = " ".join(w for w in nltk.wordpunct_tokenize(str(i)) \
                            if w.lower() in words or not w.isalpha())

        out.append(screened)
    cleanedText_S = (list(itertools.chain.from_iterable(cleanedText)))
    return cleanedText_S
