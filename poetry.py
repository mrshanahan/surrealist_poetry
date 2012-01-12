import sys, random, re

def list_parse(wl):
    dico = {}
    full_entries = re.findall('<[^>]*>.*?</[^>]*>', wl, re.S)
    for t in full_entries:
        m = re.search('<([^>]*)>(.*?)</', t, re.S)
        pos = m.group(1)
        entries = m.group(2).strip()
        dico[pos] = entries.split('\n')
    return dico

listfile = 'poetry_wordlist'
full_dict = list_parse(open(listfile).read())
line_formats = []
parse_map = {'A': 'adj', 'N': 'noun', 'V': 'verb', 'P': 'prep', 'D': 'adv', 
             'C': 'conj', 'U': 'punc', 'R': 'art', 'S': 'sim'}
default_pat = ['ANVPRANU','RANVSRANU','ANVDUNU','RANVPRAN']

# Stores a format statically; poem is variable

# FIX:
# - add more articles
# - initial "A" not turning to "An"
# - final period
# - need captalization following ending punctuation
class Format:
    def __init__(self, pat=default_pat):
        self.pattern = self.__parse(pat)
        self.poem = ''

    def fill(self):
        self.poem = ''
        for line in self.pattern:
            temp = []
            for i in range(len(line)):
                comp = line[i]
                next = random.choice(full_dict[comp])
                if comp == 'verb': next += 's'
                if i == 0: next = next.capitalize()
                if i < len(line)-1 and line[i+1] != 'punc': next += ' '                
                temp.append(next)
            for i in range(len(temp)):
                if i < len(temp)-1 and temp[i].strip().lower() == 'a' and \
                temp[i+1][0].lower() in 'aeiou':
                    temp[i] = temp[i][0] + 'n' + temp[i][1:]
                if i > 0 and temp[i-1].strip() in '.!?': temp[i] = temp[i].capitalize()
            self.poem += ''.join(temp) + '\n'
        self.poem = self.poem.strip() + '.'

    def new_poem(self):
        self.fill()
        return self.poem

    def __correct_a(c):
        if c == 'a':
            c += 'n'
        return c

    def __parse(self, pat):
        full_pat = []
        if not isinstance(pat, list): pat = map(lambda x: x.strip(), pat.split('\n'))
        for line in pat:
            full_pat.append(map(lambda x: parse_map[x], line))
            
        return full_pat

    def __str__(self):
        return self.pattern.__str__()

if __name__ == '__main__':
    if not sys.argv[1:]:
        f = Format()
    else:
        f = Format(sys.argv[1])
    print '\n' + f.new_poem() + '\n'
