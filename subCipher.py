import copy
import math
import random
import string

# generate bigrams dictionary with probabilities
# returns count and bigrams dict
def createBigrams(filename):
    file = open(filename,'r').read()
    # process corpus text to remove non-alphabetic/non-whitespace
    # generate bigrams dictionary
    bigrams = {}
    for i in range(0,len(file)-1):
        bigram = file[i]+file[i+1]
        if bigram in bigrams:
            bigrams[bigram] += 1.
        else:
            bigrams[bigram] = 1.

    count = 0
      
    for i in bigrams:
        count += bigrams[i]
    #

    # compute bigram probabilities, altered to deal with bigrams that
    # occur once (bigrams that don't occur are handled in function plf)
    count+=2
    for i in bigrams:
        bigrams[i] = (bigrams[i]+1)/count
    return (count, bigrams)

# do decryption on cipher text with guess
# return f(C) as string
def tryKey(key,cipher):
    decodedCipher = ""
    i = 0
    while i < len(cipher):
        c = cipher[i]
        if c in key:
            decodedCipher+= key[c]
        else:
            decodedCipher+= c
        i+=1
    return decodedCipher

# calculate plausibility of key
# returns ln(Pl(f))
def plf(key,cipher,corpusBigrams,corpusCount):    
    decodedCipher = tryKey(key,cipher) #applies f to cipher
    pl = 0

    for i in range(0,len(decodedCipher)-1):
        bigram = decodedCipher[i]+decodedCipher[i+1]
        if bigram in corpusBigrams:
            pl += math.log(corpusBigrams[bigram])
        elif bigram == '  ':
            pl += 0
        else:
            pl -= math.log(corpusCount) # const = 1/corpusCount
    return pl

# swaps random characters
def transpose(key):
    newkey = copy.deepcopy(key)
    chars = random.sample(string.ascii_lowercase, 2) 
    temp = newkey[chars[0]]
    newkey[chars[0]] = newkey[chars[1]]
    newkey[chars[1]] = temp
    return newkey
    
# random walk - take better pl, or take worse pl with small probability
def keyLoop(key,cipher, corpusBigrams,corpusCount):

    curr = plf(key,cipher,corpusBigrams,corpusCount)
    p = random.random() #initialize bernoulli
    newkey = key #initialize newkey
    
    for i in range(3000):
        newkey = transpose(key)
        ###
        fol = plf(newkey,cipher,corpusBigrams,corpusCount)
        # fol is pl(f*), named fol because next is reserved
        # if pl(f*) > pl(f)

        if fol > curr:
            key = newkey
            curr = fol
        # else accept f* with probability p
        else:
            ### bernoulli trial
            p = random.random()
            if p < math.exp(fol-curr):
                key = newkey
                curr = fol

    print(tryKey(key,cipher))
    return key

def main():
    # generate bigrams and frequencies as well as a count of bigrams

    corpusFile = "war-and-peace.txt"
    cipherFile = "cipher.txt"

    corpusData = createBigrams(corpusFile)
    corpusCount = corpusData[0]
    corpusBigrams = corpusData[1]

    # initial guess, implemented with dictionary
    key = {}
    sigma = list(string.lowercase)
    random.shuffle(sigma)
    
    for i in range(0,26):
        x = 'a'
        key[chr(ord(x)+i)] = sigma[i]
    #

    #string preprocessing on cipher text to remove non-alphabetic/non-whitespace
    cipher = open(cipherFile,'r').read()
    keyLoop(key,cipher,corpusBigrams,corpusCount)

main()