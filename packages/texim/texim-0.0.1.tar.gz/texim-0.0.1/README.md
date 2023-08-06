# texim

texim: text similarity
text similarity tool, and it works better for record linkage!

## Description

texim is text similarity tool, for record linkage task.  
we proposed 2 points for <kbd>cosine</kbd> and<kbd>jaccard </kbd> similarity:

* length sensitive weight
* semi-match method for field matching  

#### weight type

Classical cosine similarity use TF-IDF as weight of tokens, and we use TF here just for short string. It is common for record linkage to match some field. like name, email, address and so on.

we have 3 weight types here:  

- tf : token frequency of token
- len : length of token  
- 1 : const 1

#### semi-match
Abbreviations is common for us, "alan turing" vs "a turing", and semi-match can match "alan"="a" and "turing"="turing".

## Install
```bash
pip install texim 
```

## Examples
```python3
from texim import similarity, words_match

## semi-match 
tokens1 = ["vandesompele","j"]
tokens2 = ["jo", "vandesompele"]
words_match(tokens1, tokens2, semi_match=False)
# [("vandesompele", "vandesompele")]
words_match(tokens1, tokens2, semi_match=True)
# [("vandesompele", "vandesompele"), ("j", "jo")]

## cosine similarity
text1, text2 = "vandesompele j", "jo vandesompele"
text3, text4 = "a b b b v", "a b b c"
similarity(text1, text2, semi_match=False, wtype="len") # 0.98
similarity(text1, text2, semi_match=True, wtype="len")  # 1.0
similarity(text1, text2, semi_match=False, wtype="tf")  # 0.5
similarity(text3, text4, semi_match=False, wtype="tf")  # 0.86
similarity(text3, text4, semi_match=False, wtype="1")   # 0.67

## jaccard similarity
similarity(text1, text2, method="jaccard", semi_match=False, wtype="tf")  # 0.33
similarity(text1, text2, method="jaccard", semi_match=False, wtype="len")  # 0.8
similarity(text1, text2, method="jaccard", semi_match=True, wtype="tf")  # 1.0
similarity(text3, text4, method="jaccard", semi_match=False, wtype="tf")  # 0.64
similarity(text3, text4, method="jaccard", semi_match=False, wtype="1")  # 0.5
```

## Notice

* all fields need to be converted to <b>lower</b> case.
* you can call texim.cosine and texim.jaccard directly if you need a custom token cutting and weight countting.

## E-Mail
Check the setup.py pls!