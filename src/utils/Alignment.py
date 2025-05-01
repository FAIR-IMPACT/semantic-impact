from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_distances
import re
import torch
import requests

class CosineDistance:
    def __init__(self, query, DEBUG=False, SPARQLMUSE=False):
        self.query = query
        self.DEBUG = DEBUG
        self.context_set = {}
        self.MIN_WORDS = 3
        self.THRESHOLD = 0.6
        self.MIN_DISTANCE = 0.000000001
        self.model_name = "all-MiniLM-L6-v2"
        self.model_name = "all-mpnet-base-v2" 
        self.unique_words = []
        self.filtered_words = []
        self.definitions = []
        self.identifiers = []
        self.labels = {}
        if SPARQLMUSE:
            self.host = SPARQLMUSE
        self.filter = ['them'] #, 'a', 'an', 'could'] #, 'why', 'thing', 'have' 'next', 'with', 'as', 'by', 'for', 'of', 'at', 'to', 'in', 'is', 'was', 'were', 'will', 'would', 'should', 'can', 'could', 'may', 'might', 'must', 'should', 'would', 'and']
        if torch.cuda.is_available():
            if self.DEBUG:
                print(f"Using GPU: {torch.cuda.get_device_name(0)}")
            self.model = SentenceTransformer(self.model_name, device='cuda')
        else:
            if self.DEBUG:
                print("CUDA not available, using CPU")
            self.model = SentenceTransformer(self.model_name)

    def clean_text(self, text):
        # Remove URLs
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        # Remove special characters and extra whitespace
        text = re.sub(r'[^\w\s]', ' ', text)
        # Remove multiple spaces
        text = re.sub(r'\s+', ' ', text)
        # Remove leading/trailing whitespace
        text = text.strip()
        # Remove repeated words while preserving order
        words = text.split()
        seen = set()
        for word in words:
            word_lower = word.lower()
            if len(word_lower) >= self.MIN_WORDS or word[0].isupper():
                if word_lower not in seen:
                    seen.add(word_lower)
                    self.unique_words.append(word_lower)
        
        for f in self.filter:
            if not f in self.unique_words:
                self.unique_words.append(f)
        return ' '.join(self.unique_words)

    def get_context(self):
        keywords = self.clean_text(self.query).split(" ")
        if len(keywords) > 1:
            sentences = keywords
        else:
            sentences = [self.query, 'concept']

        # Encode sentences to get dense vectors
        embeddings = self.model.encode(sentences)

        # Compute cosine distances between all pairs
        distances = cosine_distances(embeddings)

        # Display results
        context_set = {}
        #self.THRESHOLD = 0.9
        for i, s1 in enumerate(sentences):
            for j, s2 in enumerate(sentences):
                if float(distances[i, j]) > self.MIN_DISTANCE and float(distances[i, j]) < self.THRESHOLD:
                    if self.DEBUG:
                        print(f"Distance between '{s1}' and '{s2}': {distances[i, j]:.4f}")
                    if s1 not in context_set:
                        context_set[s1] = []
                    if s2 in ['the', 'a', 'an']:
                        self.filter.append(s1)
                    else:
                        context_set[s1].append(s2)

        #if self.DEBUG:
        #print(f"\t[DEBUG CONTEXT] {context_set}")
        for key, value in context_set.items():
            if key not in self.filter:
                for ranking in ('', 'rankingweights'):
                    self.filtered_words.append(key)
                    property = "property"
                    wikilink = f"{self.host}/wikilink/?term={key}&context={'+'.join(value)}&language=en&format=json&property={property}"
                    if ranking:
                        wikilink += f"&rankingweights={ranking}"
                    #print(f"{wikilink}")
                    dataitem = {}
                    if self.DEBUG:
                        print(f"\t[DEBUG CONTEXT one] {key} {' '.join(value)}")
                    try:
                        response = requests.get(wikilink)
                        dataitem['id'] = response.json()['title']
                        dataitem['label'] = response.json()['label']
                        dataitem['description'] = response.json()['description']
                        candidates = [str(f"{key} {' '.join(value)}"), str(dataitem['label'] + ' is a ' + dataitem['description']).replace('"', ' ').lower()]

                    except Exception as e:
                        candidates = []
                        continue
                    testembeddings = self.model.encode(candidates)
                    distances = cosine_distances(testembeddings)
                    if distances[0, 1] < self.THRESHOLD:
                        if self.DEBUG:
                            print(f"\t[DECISION] {dataitem['id']} {dataitem['label']} - {dataitem['description']} {distances}")
                        self.identifiers.append(dataitem['id'].replace("Property:", ""))
                        self.definitions.append(dataitem['label'] + ' ' + dataitem['description'])
                        self.labels[dataitem['id'].replace("Property:", "")] = dataitem['label']
