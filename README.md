# subCipher
Implementation to break substitution cipher using Diaconis' algorithm

# Contents
* war-and-peace.txt - the corpus text; used to calculate bigram frequencies of the English language
* cipher.txt - the encoded cipher text (a poem); the text to be decrypted by the algorithm
* subCipher.py - the implementation of Diaconis' algorithm

# How subCipher works
1. Calculates bigram frequencies using the corpus text (should be representative of the language)
2. Choose a random key over the same alphabet (in this case sigma = the lowercase English character)
3. Loop to calculate the Plausibility of the key (~2000 - 3000 iterations should be sufficient)
  * swap two random characters in the key
  * recalculate plausibility for the new key
  * if the new plausibility is better, keep the new key
  * else if the new plausibility is worse, keep the new key with some probability
4. return the decoded cipher text at the end of the iterations (~90% convergence)

In this implementation, we use ln(Pl(f)) (where Pl is the plausibility, and f is the key) because the bigram frequencies are so small (in Diaconis' algorith, he takes the product of frequencies). It is also notable that we sometimes take plausibilities that are worse to prevent getting stuck in local maxima. As the plausibility grows, the probability that we take a lower plausibility decreases.
