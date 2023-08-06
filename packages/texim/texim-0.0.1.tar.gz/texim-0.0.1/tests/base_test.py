from texim.base import words_match, similarity

def base_check(func, items):
    for args, kwargs, y in items:
        out = func(*args, **kwargs)
        assert out == y, "Input: {args} {kwargs} \nOutput: {out}\nExpect: {y}".format(
            args=args, kwargs=kwargs, y=y, out=out)

word_match_items = [
    [ 
        [["vandesompele","j"], ["jo", "vandesompele"]], {"semi_match": False}, 
        [("vandesompele", "vandesompele")]
    ],
    [
        [["vandesompele","j"], ["jo", "vandesompele"]], {"semi_match": True}, 
        [("vandesompele", "vandesompele"), ("j", "jo")]
    ],
    [
        [["chemical", "reviews"], ["chem", "rev"]], {"semi_match": False},
        []
    ],
    [
        [["chemical", "reviews"], ["chem", "rev"]], {"semi_match": True},
        [("chemical", "chem"), ("reviews", "rev")]
    ],    
    [
        [[], []], {"semi_match": False},
        []
    ],
    [
        [[], []], {"semi_match": True},
        []
    ]
]

def test_words_match():
    base_check(words_match, word_match_items)

text_cosine_items = [
    [["vandesompele j", "jo vandesompele"], {"semi_match": False, "wtype":"len"}, 0.98],
    [["vandesompele j", "jo vandesompele"], {"semi_match": True, "wtype":"len"}, 1.0],
    [["vandesompele j", "jo vandesompele"], {"semi_match": False, "wtype":"tf"}, 0.5],
    [["a b b b v", "a b b c"], {"semi_match": False, "wtype":"tf"}, 0.86],
    [["a b b b v", "a b b c"], {"semi_match": False, "wtype":"1"}, 0.67],
    [["a b v", "a b c"], {"semi_match": False}, 0.67],
    [["a b j", "a b c"], {"semi_match": True}, 0.67],
    [["abc def", "abc def cde"], {"semi_match": False}, 0.82],
    [["abc def", "abc defghh cde"], {"semi_match": True}, 0.87],
    [["", ""], {"semi_match": False}, 0.0],
    [["", ""], {"semi_match": True}, 0.0],
]

def test_text_cosine():
    base_check(similarity, text_cosine_items)

text_jaccard_items = [
    [["vandesompele", "vandesompele"], {"semi_match": False, "method":"jaccard"}, 1.0],
    [["vandesompele", "vande"], {"semi_match": True, "method":"jaccard"}, 1.0],
    [["vandesompele j", "jo vandesompele"], {"semi_match": False, "method":"jaccard", "wtype":"tf"}, 0.33],
    [["vandesompele j", "jo vandesompele"], {"semi_match": False, "method":"jaccard", "wtype":"len"}, 0.8],
    [["vandesompele j", "jo vandesompele"], {"semi_match": True, "method":"jaccard", "wtype":"len"}, 1.0],
    [["a b b b v", "a b b c"], {"semi_match": False, "method":"jaccard", "wtype":"tf"}, 0.64],
    [["a b b b v", "a b b c"], {"semi_match": False, "method":"jaccard", "wtype":"1"}, 0.5],
    [["", ""], {"semi_match": False, "method":"jaccard"}, 0.0],
    [["", ""], {"semi_match": True, "method":"jaccard"}, 0.0],
    [["abc", ""], {"semi_match": True}, 0.0],
]

def test_text_jaccard():
    base_check(similarity, text_jaccard_items)