import enchant
import re

_d_es = enchant.Dict("es")
_d_en = enchant.Dict("en")

_phonetic_characters = [u'ŋ',u'ş',u'ø',u'ç']
_punctuation = ['.',':',',',';','¿','?','¡','!']

_regexs = [r'\(*([\d]* *[\w]+\.* [\d]+\.[\d]+-*[\d]*;* *)+\)*', # (Mr. 1.22; Lc. 6.47-49)
      r'\(\d+,\d+\w*\)', # (11,17b)
      r'[\w]+(-[\dA-Z]+\.*[\w]*)+', # say-1.OBJ-3 Tana-PL-TOP
      r'[\w]+-[\w]+(-[\w]+)+', # kida-ku-shun qalqaliya-m shamu-ya-n Chukllaklla-paq Hongos-paq
      r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', # aeslinares@gmail.com
      r'(\([\w]+:[\w]+\))', # (cid:2629)
      r'(\d+:*)+(\.\d+)*', #00:04:35.743
      r'\w+(_\w+)+', # n_infl
      r'\[\w*\]', #[acu]
      r" '", r"' ", # comillas que no son entre palabras
      r'\w+:(\/\w+)+(\.\w+)*', # file:/Users/Documents/Quechua/Yauyos_ELAN/Shutco_MG_Frog_Dog_Mouse_Bird.eaf
      r'S\/\.\d+,*\d*', # S/.200,000
      r'S/', # http://creativecommons.org/licenses/by-nc-nd/3.0
      r'\d+', r'[ªº$&+=@#|<>^*()%¡!~—\-–“”‘’„‟"˻˼°…½«»‹›_·∂´{}\[\]\/\\]+']

_ignored_chars = ['̃','̈','́','̱','̲']
_replace_chars = {
    'ä' : 'ä',
    'ë' : 'ë',
    'ï' : 'ï',
    'ö' : 'ö',
    'ü' : 'ü',
    'ÿ' : 'ÿ',
    'ã' : 'ã',
    'ñ' : 'ñ',
    'õ' : 'õ',
    'á' : 'á',
    'é' : 'é',
    'í' : 'í',
    'ó' : 'ó',
    'ú' : 'ú',
}

def inDictionary(sentence):
  words = sentence.split()
  adj_es = 0
  adj_en = 0
  for word in words:
    if _d_es.check(word):
      adj_es += 1
    else:
      adj_es = 0
      
    if _d_en.check(word):
      adj_en += 1
    else:
      adj_en = 0
      
    if adj_es == 2 or adj_en == 2:
      return True
  
  return False


def clean_line(line):
  p1 = re.compile('\w+-\w+\.*\w*(-\w+\.*\w*)+') # say-1.OBJ-3 Tana-PL-TOP
  if p1.search(line):
    return ""
  
  line = re.sub("[ꞌʼ]", "'", line)
  line = " " + line + " "
  
  for r in _regexs:
    line = re.sub(r, ' ', line)

  for r in _replace_chars:
    line = line.replace(r,_replace_chars[r])

  for i in _ignored_chars:
    line = line.replace(i,"")
    
  line = re.sub("'\.", ". ", line) # '.
  line = line.replace(".",". ")
  line = line.replace(",",", ")
  line = line.replace(";","; ")
  line = line.replace(":",": ")

  line = ' '.join(line.split())
  
  return line


def isValidWord(word):
  word = word.lower()
  if len(word) < 2 and word not in 'aeiou':
    return False
  
  for c in _phonetic_characters:
    if c in word:
      return False

  return word != ""


def isNative(sentence):
  try:
    ans = not inDictionary(sentence)# or detect(sentence) not in d_lang
  except (KeyboardInterrupt, SystemExit):
    raise
  except:
    #print("No features in: " + sentence)
    ans = False
    
  if ans:
    contiguous_one_letter = 0
    words = sentence.split()
    for word in words:
      if len(word) == 1:
        contiguous_one_letter += 1
      else:
        contiguous_one_letter = 0
        
      if contiguous_one_letter == 2:
        return False
    
  return ans

def isValidSentence(sentence):
  return len(sentence.split()) > 1 and isNative(sentence)

def remove_punctuation(text):
  for p in _punctuation:
    text = text.replace(p,"")
  return text.strip()

def remove_not_native(line):
  sentences = line.split('.')
  clean_line = ""
    
  for sentence in sentences:
    test_line = sentence.strip().lower()
    if test_line.strip() != "" and isNative(test_line):
      clean_line += sentence
      if sentence != sentences[-1]:
        clean_line += "."
  return clean_line


def split_text(text):
  s_period = text.split(".")

  sentences = []
  sentence = ""

  for s in s_period:
    s = s.strip()
    if (s != ""):
      if (sentence != ""):
        sentences.append(sentence + ".")
      sentence = s
    else:
      if (sentence != ""):
        sentence += "."

  if (sentence != ""):
    sentences.append(sentence)

  return sentences

def clean_text(text):
  text = clean_line(text.lower())
  sentences = split_text(text)

  clean = []
  for sentence in sentences:
    clean_sentence = remove_punctuation(sentence)
    if (clean_sentence!=""):
      clean.append(clean_sentence)

  return clean


def clean_sentences(sentences):
  return list(map(lambda x: remove_punctuation(clean_line(x.lower())), sentences))