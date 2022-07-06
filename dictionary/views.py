from django.shortcuts import render
from PyDictionary import PyDictionary
import requests
from bs4 import BeautifulSoup
import nltk
nltk.download('omw-1.4')
from nltk.corpus import wordnet
from googletrans import Translator
#from jmespath import search
# Create your views here.

def synn(term):
    response = requests.get('https://www.thesaurus.com/browse/{}'.format(term))
    soup = BeautifulSoup(response.text, 'html.parser')
    soup.find('section', {'class': 'css-191l5o0-ClassicContentCard e1qo4u830'})
    return [span.text for span in soup.findAll('a', {'class': 'css-1kg1yv8 eh475bn0'})] 

def index(request):
    return render(request,'home1.html')

def word(request):
    search = request.GET.get('search')
    print(search)
    antonyms = []
    for syn in wordnet.synsets(search):
        for lm in syn.lemmas():
            if lm.antonyms():
                antonyms.append(lm.antonyms()[0].name())
    dictionary = PyDictionary()
    meaning = dictionary.meaning(search)
    synonyms = synn(search)
    trans = Translator()
    btext = trans.translate(search,dest='bn')
    htext = trans.translate(search,dest='hi')
    #translated = dictionary.translate(search,'bn')
    #print(meaning,synonyms,antonyms)
    return render(request,'home.html', context={'meanings':meaning,'synonyms':synonyms,'antonyms':antonyms,'word':search,'btext':btext.text,'htext':htext.text})