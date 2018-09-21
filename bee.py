#!/bin/env python

import random,time

with open("scrabble.txt") as f:
    wds = [x.strip().lower() for x in f.readlines()[2:] if len(x) > 4]

vowels = set(list("aeiou"))

f = set(list("oohioo"))

candidates = [x for x in wds if len(set(list(x))) == 7 and len(set(list(x)).intersection(vowels)) == 2]

def check_entry(entry,pangram,report=True):
    if entry.lower() not in wds:
        if report: print("Not a word.")
        return 0
    elif special not in entry:
        if report: print("Missing",special)
        return(0)
    s = set(list(entry))
    all = set(list(pangram))
    if s.issubset(all):

        if s == all:
            if report: print("Pangram!")
            return 2*len(entry)
        elif len(entry) == 4:
            return 1
        else:
            return len(entry)
    else:
        if report: print("Not Valid.")
        return(0)



if __name__ == "__main__":
    pgram = random.choice(candidates)
    letters = set(pgram)
    special = random.choice(list(letters))
    others = list(letters.copy())
    others.remove(special)
    random.shuffle(others)

    score = 0
    found = set([])

    solve = {x:check_entry(x,pgram,False) for x in wds if set(list(x)).issubset(set(list(pgram)))}

    tot = sum(solve.values())

    # print(tot,"\n",pgram,"\n",list(solve.keys())[:10])

    while score < tot/5:
        print(score, tot,"\n")
        print(" " + others[0].upper() + " " + others[1].upper())
        print(others[2].upper() + " " + special.upper() + " " + others[3].upper())
        print(" " + others[4].upper() + " " + others[5].upper())
        try:
            entry = input("Watcha got? ")
        except EOFError:
            foundlist = list(found)
            foundlist.sort()
            print("You found",", ".join(foundlist))
        print(chr(27) + "[2J")
        if entry not in found:
            n = check_entry(entry,pgram)
            if n > 0:
                score += n
                found.add(entry)
        else:
            print("Already found.")
        # time.sleep(.7)
