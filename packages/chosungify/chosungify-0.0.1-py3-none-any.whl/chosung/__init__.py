''''
Author: Joon-Won Choi (SHUcream00)
License: MIT
Short snippet that maps Korean character to its initial consonant (chosung)

'''

def chosungify(text):
    '''
    iterates the given text and returns chosung-ified text.
    '''
    if not text:
        return ""

    return "".join(get_consonent(char) for char in text)

def get_consonent(chr_):
    try:
        codemap = {1: 12593, 2: 12594, 3: 12596, 4: 12599, 5: 12600, 6: 12601, 7: 12609, 8: 12610, 9: 12611, 10: 12613,
                    11: 12614, 12: 12615, 13: 12616, 14: 12617, 15: 12618, 16: 12619, 17: 12620, 18: 12621, 19: 12622}
        codepoint = ord(chr_)
        if 44032 <= codepoint <= 55203:
            return chr(codemap[((codepoint - 44032) // 588) + 1])
        else:
            return chr_

    except TypeError as e: 
        print("get_consonent error: ", e)
