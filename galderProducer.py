import enchant
from enchant.tokenize import get_tokenizer

def main():
    extraWords = open("extraWords.txt")
    extraNames = open("names.txt")
    dict = enchant.Dict("en_US")
    for dropChar1 in range(97, 123):
        dict.remove(chr(dropChar1))
        for dropChar2 in range(97, 123):
            dict.remove(chr(dropChar1)+chr(dropChar2))
    for wordToAdd in extraWords:
        print(wordToAdd)
        dict.add(wordToAdd)
    for nameToAdd in extraNames:
        print(nameToAdd)
        dict.add(nameToAdd)
    tknzr = get_tokenizer("en_US")

    for i in range(10):
        doTheThing(dict,tknzr,i)
    
    extraNames.close()
    extraWords.close()
    


def doTheThing(dict, tknzr, level):
    #open spells
    input = open("inputs/lvl"+str(level)+"in.txt", "r")
    output = open("outputs/lvl"+str(level)+"out.txt", "w")

    #loop through each spell
    listOfValidSpells = []
    for spell in input:
        permutations = makeNewSpellNames(spell.lower())
        listOfValidSpells.extend(filterPermutations(permutations, dict, tknzr))
        #print(permutations)
    for validSpell in listOfValidSpells:
        output.write(validSpell)

    input.close()
    output.close()

def makeNewSpellNames(spell):
    returnList = []
    # print(spell)
    for index, char in enumerate(spell):
        #Transforming characters
        for insertChar in range(97, 123):
            if(chr(insertChar) != spell[index-1]):
                newSpell = spell[:index-1] + chr(insertChar-32) + spell[index:]
                # print(newSpell)
            returnList.append(newSpell)
        #Adding characters
        for insertChar in range(97, 123):
            newSpell = spell[:index] + chr(insertChar-32) + spell[index:]
            returnList.append(newSpell)
        # dropping characters
        if((ord(char) < 124 and ord(char) > 96) or (ord(char) < 92 and ord(char) > 64)):
            returnList.append((spell[:index] + spell[index+1:]).strip() + "\n")
    return returnList

def filterPermutations(permutations, dict, tknzr):
    validPermutations = []
    for permutation in permutations:
            isGood = True
            for word in tknzr(permutation):
                #print(word)
                if((dict.check(word[0].strip().lower())) == False):
                    isGood = False
            if(isGood):
                validPermutations.append(permutation)
    return validPermutations

main()