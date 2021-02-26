import pickle
import joblib

# pre-processed text
corpus = {} 

# file to document number mapping
document_map = {}

# key and corresponding posting list
dictionary = {}

with open('DocTerms_Spacy.pickle', 'rb') as handle:
  corpus = pickle.load(handle)

# creating file to document mapping

counter = 0

for key in corpus.keys():
  if (key not in document_map.keys()):
    counter += 1
    document_map[key] = counter

# creating the postings

for key in corpus.keys():
  
  list_of_words = corpus[key][0]

  for word in list_of_words:

    if (word in dictionary.keys()):
      l = dictionary[word]
      l[1].append(document_map.get(key))
    else :
      dictionary[word] = [[],[document_map.get(key)]]

# removing duplicates

for key in dictionary.keys():
  unique_postings = list(dict.fromkeys(dictionary[key][1]))
  dictionary[key][1] = unique_postings

# inserting document count

for key in dictionary.keys():
  doc_count = len(dictionary[key][1])
  dictionary[key][0].append(doc_count)
  

print('Number of unique terms in dictionary : ' + str(len(dictionary.keys())))
print()
print('Document count of term -> play : ' + str(dictionary['play'][0][0]))
print()
print('Posting list of play -> ' + str(dictionary['play'][1]))
print()
print(dictionary.get('play'))
joblib.dump(dictionary,'inverted_index')
