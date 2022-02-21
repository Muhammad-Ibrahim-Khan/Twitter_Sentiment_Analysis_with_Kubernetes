import string
import re

def cleaning_text(text):
    text = re.sub(r'((www.\S+)|(https?://\S+))',r' ',text)
    text = re.sub(r'[0-9]\S+', r'', text)
    text = re.sub(r'(@\S+) | (#\S+)', r'', text)
    
    translator = str.maketrans('', '', string.punctuation)
    return text.translate(translator)

