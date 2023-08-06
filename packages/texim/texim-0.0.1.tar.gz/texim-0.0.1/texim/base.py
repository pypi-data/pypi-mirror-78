import math
import copy

class InvalidMehtod(BaseException):
    pass

weight_func_map = {
    "len": lambda x: len(x),
    "tf": lambda x: 1,
    "1": lambda x: 0,
}

def _text_split(field):
    return field.split()

def _get_weight(parsed_field, wtype):
    """
    field: string field content
    wtype: weight type
        - len : token length as weight
        - tf  : token frequence as weight
        - 1   : const 1 as weight
    """
    assert wtype in weight_func_map, "not supported weight type"
    if wtype == "1":
        return {w: 1 for w in parsed_field}
    weight_map = {}
    get_weight = weight_func_map[wtype]
    for word in parsed_field:
        weight_map[word] = weight_map.get(word, 0) + get_weight(word)
    return weight_map

def item_match(x, y, semi_match):
    if semi_match:
        ml = min(len(x), len(y))
        return x[:ml] == y[:ml] 
    else:
        return x == y

def words_match(xs, ys, semi_match=False):
    # longest token first
    xls = sorted(xs, key=lambda x: len(x), reverse=True)
    nys = copy.copy(ys)
    pairs = []
    for x in xls:
        if not x: continue
        for y in nys:
            if not y: continue
            if item_match(x, y, semi_match):
                pairs.append( (x, y) )
                nys.remove(y)
    return pairs

def l2_norm(xs):
    return math.sqrt(sum([x**2 for x in xs]))

def cosine(tokens1, tokens2, weight_map1, weight_map2, semi_match=False):
    base_1 = l2_norm(weight_map1.values())
    base_2 = l2_norm(weight_map2.values())
    sim = 0.0
    if not (base_1 and base_2):
        return sim
    weight_square_sum = 0.00
    inter_token_pairs = words_match(tokens1, tokens2, semi_match=semi_match)
    for w1, w2 in set(inter_token_pairs):
        weight_square_sum += weight_map1[w1] * weight_map2[w2]
    sim = round(weight_square_sum/(base_1 * base_2), 2)
    return sim

def jaccard(tokens1, tokens2, weight_map1, weight_map2, semi_match=False):
    sim = 0.0
    if not (tokens1 and tokens2):
        return sim
    inter_token_pairs = set(words_match(tokens1, tokens2, semi_match=semi_match))
    base1 = sum([weight_map1[t] for t in set(tokens1)])
    base2 = sum([weight_map2[t] for t in set(tokens2)])
    inter_base = sum( [ (weight_map1[t1] + weight_map2[t2])  for t1, t2 in inter_token_pairs]) / 2
    sim = round(inter_base / (base1 + base2 - inter_base), 2)
    return sim

def similarity(text1, text2, method="cosine", wtype="len", semi_match=False):
    tokens1 = _text_split(text1)
    tokens2 = _text_split(text2)
    weight_map1 = _get_weight(tokens1, wtype=wtype)
    weight_map2 = _get_weight(tokens2, wtype=wtype)
    if method in ["cosine", "jaccard"]:
        sim = globals()[method](tokens1, tokens2, weight_map1, weight_map2, semi_match=semi_match)
        return sim
    else:
        raise InvalidMehtod("invalid similarity method: "+ method)
    
def text_cosine(*args, **kwargs):
    return similarity(*args, **kwargs)




