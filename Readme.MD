The preprocessing.ipnypb contains code which applies all preprocessing steps mentione din Readme.pdf on the given corpus. Unzip stories1.zip and run this notebook if needed.

We apply two different lemmatizers. We use wordnet lemmatizer and spacy lemmatizer. We observed space lemmatizer works better.

DocTerms_Spacy.pickle -  contains tokens extracted after preprocessing where space lemmatizer is used
DocTerms.pickle - contains tokens extracted after preprocessing where wordnet lemmatizer is used

dictionary_with_posting_lists.py - is run to generate the given corpus from the above pickle files.

Run intersection_and_union.py to query the inverted index. There are interactive prompts to get the input. The attached screenshot in readme.pdf 
gives an example input.