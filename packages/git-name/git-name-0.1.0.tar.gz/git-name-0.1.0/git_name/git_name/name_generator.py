import os
import csv
from string import ascii_letters
from collections import OrderedDict
from itertools import compress
import inflect

class NameGenerator:
    def __init__(self):
        self.inflect = inflect.engine()
        self.letters = set(ascii_letters)
        self.local = os.path.dirname(os.path.abspath(__file__))
        self.corpus = {}
        
        with open(os.path.join(self.local, "determiners.txt")) as f:
            self.corpus["determiners"] = f.read().split("\n")

        with open(os.path.join(self.local, "plural_determiners.txt")) as f:
            self.corpus["plural_determiners"] = f.read().split("\n")
        
        with open(os.path.join(self.local, "adjectives.txt")) as f:
            self.corpus["adjectives"] = f.read().split("\n")

        with open(os.path.join(self.local, "nouns.txt")) as f:
            self.corpus["nouns"] = f.read().split("\n")

        with open(os.path.join(self.local, "adverbs.txt")) as f:
            self.corpus["adverbs"] = f.read().split("\n")

        with open(os.path.join(self.local, "auxiliary_verbs.txt")) as f:
            self.corpus["aux_verbs"] = f.read().split("\n")

        with open(os.path.join(self.local, "verbs.txt")) as f:
            self.corpus["verbs"] = f.read().split("\n")
            

        
        word_dump = set()
        
        for word_type, words in self.corpus.items():
            temp=set()
            for word in words:
                word = self.__clean_word(word, word_type)
                if word and not word in word_dump:
                    word_dump.add(word)
                    temp.add(word)
            
            self.corpus[word_type]=sorted(temp)
        self.word_dump=word_dump
        self.corpus["determiners"]+=self.corpus["plural_determiners"]
        
        self.counts = {
            "determiners": len(self.corpus["determiners"]),
            "adjectives": len(self.corpus["adjectives"]),
            "nouns": len(self.corpus["nouns"]),
            "adverbs": len(self.corpus["adverbs"]),
            "aux_verbs": len(self.corpus["aux_verbs"]),
            "verbs": len(self.corpus["verbs"]),
        }

        self.counts_ordered = [
            i[0]
            for i in sorted(
                zip(self.counts.keys(), self.counts.values()),
                key=lambda x: x[1],
                reverse=True,
            )
        ]

        self.mapper = OrderedDict()
        with open(os.path.join(self.local,"mapper.csv"), newline="") as csvfile:
            mapreader = csv.reader(csvfile, delimiter=",")
            for row in mapreader:
                self.mapper[row[0]] = [int(i) * self.counts[row[0]] for i in row[1:]]
                
        self.word_order = list(self.mapper.keys())
        self.poss_combos=[[vv>0 for vv in v] for v in self.mapper.values()]

        self.poss_combos=[tuple(compress(self.word_order, [l[i] for l in self.poss_combos])) for i in range(len(self.poss_combos[0]))]
        
        self.tot = []
        for v in self.mapper.values():
            for i, vv in enumerate(v):
                vv = max(vv, 1)
                try:
                    self.tot[i] *= vv
                except IndexError:
                    self.tot.append(vv)
                    
        for i in range(len(self.tot)):
            if i:
                self.tot[i]+=self.tot[i-1]
        self.tot.insert(0,0)
        
    
    def __clean_word(self, word, type):
        word=[" " if not (c in self.letters or c=="-") else c.lower() for c in word.strip()]
        
        word="".join(word)
        if type in ("nouns", "verbs"):
            word = word.replace(" ", "-")
            if type == "nouns" and word[-2:]!="ss":
                singular=self.inflect.singular_noun(word)
                if singular:
                    return singular
                else:
                    return word
        elif not "determiners" in type and " " in word:
            return False
        
        return word
    
    def generate_name_from_hash(self, hash, n:int=4)->str:
        hash = hash[:n]
        try:
            num = int("0x"+hash, 16)
        except ValueError:
            raise ValueError("Argument of `{}` could not not be understood as a hash.".format(hash))
        return self.generate_name(num)
    
    def generate_name(self, num: int)->str:
        """
        given a hash, return an english "sentence"/"name" based on the first n digits of the hash
        lower hash => more concise "name" so lower n => more concise "name"
        """
        
        if num<0:
            raise ValueError("Hash cannot be negative.")
            
        if num >= self.tot[-1]:
            raise OverflowError("Unfortunately, this hash {} (hex) = {} (decimal) is larger than our corpus can handle {} (hex) = {} (decimal). You requested the first {} digits be used. Try less.".format(hash, num,  hex(sum(self.tot)), sum(self.tot), n))

        choices = {}
        for i, t in enumerate(self.tot):
            if num<t:
                i-=1
                num-=self.tot[i]
                
                break

        remainder = 0
        dividend = num
        for w in self.counts_ordered:
            if self.mapper[w][i] > 0:
                remainder = dividend % self.counts[w]
                choices[w] = remainder
                dividend -= remainder
                dividend //= self.counts[w]

        for w, v in choices.items():
            choices[w]=self.corpus[w][v]
        if "determiners" in choices.keys() and "nouns" in choices.keys():
            if choices["determiners"] in self.corpus["plural_determiners"]:
                choices["nouns"] = self.inflect.plural_noun(choices["nouns"])
        return (" ".join([choices[w] for w in self.word_order if w in choices.keys()]).replace("_", " ")).strip()

    def __check_word(self, word, list):
        try:
            return list.index(word)+1
        except ValueError:
            return False
        
    def generate_num(self, name: str)->int:
        
        name=" ".join(name.split())
        orig=name
        assignments=OrderedDict()
        deciphered=[]
        for i in range(len(name)):
            temp=name[:(i+1)]
            checked_det = self.__check_word(temp, self.corpus['determiners'])
            if checked_det:
                assignments["determiners"]=(checked_det-1, temp)
                if not deciphered:
                    deciphered.append(temp)
                else:
                    deciphered[0]=temp
        if deciphered:
            name=name[len(deciphered[0]):]
        name=name.split()
        
        for token in name:
            for words in self.word_order:
                if words in assignments.keys():
                    continue
                #we are in the process of checking if the token is a noun
                #the token is not in nouns but could be plural
                if words == "nouns" and not token in self.corpus["nouns"]:
                    #get the possible singular form
                    singular = self.inflect.singular_noun(token)
                    #and check if it is a noun
                    checked_singular = self.__check_word(singular, self.corpus["nouns"])
                    
                    #if the token does not end in ss, its singular form does not match the token
                    #and we found it in the nouns then it must be a singular noun made plural
                    if token[-2:]!="ss" and singular != token and checked_singular:
                        #but if we found a determiner already and it is not a plural determiner then this cannot yield a valid hash
                        if "determiners" in assignments.keys():
                            det=assignments["determiners"][1]
                            if not det in self.corpus["plural_determiners"]:
                                raise ValueError("The name `{}` contains a determiner `{}` this application will not pair with a plural noun `{}`. Consider checking your grammar and spelling.".format(orig, det, token))
                        assignments["nouns"]=(checked_singular-1, token)
                        deciphered.append(token)
                else:
                    checked_word = self.__check_word(token, self.corpus[words])
                    if checked_word:
                        if words == "nouns" and "determiners" in assignments.keys():
                            
                            singular = self.inflect.singular_noun(token)
                            
                            if not singular:
                                det=assignments["determiners"][1]
                                if det in self.corpus["plural_determiners"]:
                                    raise ValueError("The name `{}` contains a determiner `{}` this application will not pair with a singular noun `{}`. Consider checking your grammar and spelling.".format(orig, det, token))
                        assignments[words]=(checked_word-1, token)
                        deciphered.append(token)

        if orig!=" ".join(deciphered):
            raise ValueError("The name `{}` could not be deciphered for the given corpus. Consider checking your grammar and spelling.".format(orig))
        if not tuple(assignments.keys()) in self.poss_combos:
            raise ValueError("The name `{}` is of an invalid word pattern {}. Consider checking your grammar and spelling.".format(orig, tuple(assignments.keys())))
       
        rel_counts_ordered = [w for w in reversed(self.counts_ordered) if w in assignments.keys()]

        dividend=0
        for words in rel_counts_ordered:
            remainder, token = assignments[words]
            dividend = self.counts[words] * dividend + remainder
        dividend+=self.tot[self.poss_combos.index(tuple(assignments.keys()))]

        return dividend
    
    def generate_hash_from_name(self, name: str, n:int=4)->str:
        num=self.generate_num(name)
        ret = hex(num)[2:][:n]
        return ret.zfill(n-len(ret))