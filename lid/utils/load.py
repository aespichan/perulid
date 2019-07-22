# coding: utf-8

from os import listdir
import os.path as path
from .clean import *
from ..models import *
from django.conf import settings

already_processed_files = ["educativoNL_Ship.txt","legalNL_Ship.txt", "religiosoNL_Ship.txt"]


def get_characters(word):
  characters = []
  i = 0
  while i < len(word):
    ch = word[i]
    if i+1 < len(word):
      if (ch in ['c','s','ĉ'] and word[i+1] == 'h') or (word[i+1] in ['̃','̈','́','̱','̲']):
        if i+2 < len(word) and word[i+2] in ['̃','̈','́','̱','̲']:
          characters.append(ch+word[i+1]+word[i+2])
          i += 3
        else:
          characters.append(ch+word[i+1])
          i += 2
        continue

    characters.append(ch)
    i += 1
  return characters


def save_sentence(sentence, source):
  clean_sentence = remove_punctuation(sentence).lower()

  if isValidSentence(clean_sentence):
    i_sentence = Inverted_Sentence(sentence=sentence, file=source)
    i_sentence.save()

    words = clean_sentence.split()
    for i in range(len(words)):
      word = words[i]
      Inverted_Word(word=word, position=i, sentence=i_sentence).save()
  else:
    return ""

  return clean_sentence


def get_native_sentences(filename, source, line_break):
  file = open(filename,"r", encoding="utf-8")
  data = file.readlines()

  sentence = ""
  native_sentences = []

  for line in data:
    
    # Clean special characters
    line = clean_line(line)
    # Delete spanish or english sentences
    line = remove_not_native(line)

    words = line.split()
      
    for word in words:
      clean_word = remove_punctuation(word)
      if isValidWord(clean_word):
        # If there was a previous sentence being constructed just add the new word
        # or if it is a new sentence, check if the new word's first letter is upper.
        if sentence.strip() != "" or clean_word[0].isupper():
          sentence += " " + word
          if len(sentence.split()) == 2 and not isNative(sentence):
            sentence = ""
      
      # If original word had a punctuation in it, then save the sentence and
      # start a new sentence.
      if (':' in word or '.' in word):
        if len(sentence.split()) > 1:
          sentence = save_sentence(sentence, source)
          if sentence != "":
            native_sentences.append(sentence)
        sentence = ""
    
    # If it was an already processed file, then every line is a sentence
    # so save it and start a new sentence. 
    if line_break:
      if len(sentence.split()) > 1:
        sentence = save_sentence(sentence, source)
        if sentence != "":
          native_sentences.append(sentence)
      sentence = ""

  file.close()
      
  return native_sentences


def load_file(language, file, line_break=False):
  filename = path.join(settings.REPOSITORY_DIR,language.iso_code,file)
  Inverted_Sentence.objects.filter(file__file=filename).delete()
  Inverted_Word.objects.filter(sentence__file__file=filename).delete()

  source = Repository_Source(language=language, file=filename)
  source.save()

  set_words = set()
  set_sentences = set()
  set_characters = set()
  list_tokens = []
  
  native_sentences = get_native_sentences(filename, source, line_break)
        
  for sentence in native_sentences:
    clean_sentence = sentence.lower()
    set_sentences.add(clean_sentence)
    words = clean_sentence.split()
    set_words.update(words)
    list_tokens.extend(words)
    
    for word in words:
      set_characters.update(get_characters(word))

  return {
    "sentences":set_sentences,
    "words":set_words,
    "characters":set_characters,
    "tokens":list_tokens
  }


def load_directory(language):
  Sentence.objects.filter(iso_code=language.iso_code).delete()
  Word.objects.filter(iso_code=language.iso_code).delete()
  Character.objects.filter(iso_code=language.iso_code).delete()
  Repository_Source.objects.filter(language__iso_code=language.iso_code).delete()
  
  set_words = set()
  set_sentences = set()
  set_characters = set()
  list_tokens = []

  files = [f for f in listdir(path.join(settings.REPOSITORY_DIR,language.iso_code)) if f[0] != "."]

  for file in files:
    line_break = False
    if file in already_processed_files:
      line_break = True
      
    result = load_file(language, file, line_break)
    set_words.update(result["words"])
    set_sentences.update(result["sentences"])
    set_characters.update(result["characters"])
    list_tokens.extend(result["tokens"])
    
  for word in set_words:
    Word(iso_code=language.iso_code, word=word, length=len(word)).save()
  for sentence in set_sentences:
    Sentence(iso_code=language.iso_code, sentence=sentence, length=len(sentence)).save()
  for character in set_characters:
    Character(iso_code=language.iso_code, character=character, length=len(character)).save()
  
  return {
    "sentences":len(set_sentences), 
    "words":len(set_words), 
    "files":len(files),
    "characters":len(set_characters),
    "tokens":len(list_tokens)
  }

def load_repository():
  languages = Language.objects.all()
  amount_sentences_total = 0
  
  for language in languages:
    print(language.language_name)
    # Para cada lengua, eliminar los registros que habian antes
    # (oraciones, palabras, caracteres, etc)
    # y volver a cargarlos con lo que haya en repositorio    
    # Clean document (delete spanish, english, some symbols, ...)
    result = load_directory(language)
    Repository_Detail.objects.filter(language__iso_code=language.iso_code).delete()
    amount_sentences = result["sentences"]
    amount_words = result["words"]
    amount_characters = result["characters"]
    amount_files = result["files"]
    amount_tokens = result["tokens"]

    Repository_Detail(language=language, words=amount_words, sentences=amount_sentences, 
      characters=amount_characters, tokens=amount_tokens, files=amount_files).save()

    amount_sentences_total += amount_sentences

  return amount_sentences







