#!/bin/env python

import random,time
import curses
from math import ceil

with open("scrabble.txt") as f:
    wds = [x.strip().lower() for x in f.readlines()[2:] if len(x) > 4]

vowels = set(list("aeiou"))

candidates = [x for x in wds if len(set(list(x))) == 7 and len(set(list(x)).intersection(vowels)) == 2]

def check_entry(entry,pangram,special,scr,report=True):
    if entry.lower() not in wds:
        if report: scr.addstr("Not a word.")
        return 0
    elif special not in entry:
        if report: scr.addstr("Missing " + special.upper())
        return 0
    s = set(list(entry))
    all = set(list(pangram))
    if s.issubset(all):

        if s == all:
            if report: scr.addstr("Pangram!")
            return 2*len(entry)
        elif len(entry) == 4:
            return 1
        else:
            return len(entry)
    else:
        if report: scr.addstr("Not Valid.")
        return(0)

def printfound(found,scr):
    fwds = list(found)
    fwds.sort()
    m = (curses.COLS - 22) // 15
    # m=3
    n = ceil(len(fwds) / m)
    if n > curses.LINES - 2:
        print("Too many words.")
    else:
        for j in range(m):
            for i,w in enumerate(fwds[n*j:n*j + n]):
                scr.addstr(2+i,22+15*j,w)
                scr.clrtoeol()
            # for i,w in enumerate(fwds[n:2*n]):
            #     scr.addstr(4+i,37,w)
            #     scr.clrtoeol()
            # for i,w in enumerate(fwds[2*n:]):
            #     scr.addstr(4+i,52,w)
            #     scr.clrtoeol()
        
def main(stdscr):
    stdscr.clear()
    curses.curs_set(0)

    pgram = random.choice(candidates)
    letters = set(pgram)
    special = random.choice(list(letters))
    others = list(letters.copy())
    others.remove(special)
    random.shuffle(others)

    score = 0
    found = set([])

    solve = {x:check_entry(x,pgram,special,stdscr,False) for x in wds if set(list(x)).issubset(set(list(pgram)))}

    tot = sum(solve.values())

    # print(tot,"\n",pgram,"\n",list(solve.keys())[:10])
    stdscr.addstr(4,3,"    " + others[0].upper() + "     " + others[1].upper())
    stdscr.addstr(6,3," " + others[2].upper() + "          " + " " + others[3].upper())
    stdscr.addstr(8,3,"    " + others[4].upper() + "     " + others[5].upper())
    stdscr.addstr(6,10,special.upper(),curses.A_BOLD)

    while score < tot:
        stdscr.addstr(0,9,"{} of {}".format(score, tot))
        for n in range(2,curses.LINES):
            stdscr.addstr(n,20,"|")
        printfound(found,stdscr)
        entry = ""
        stdscr.addstr(2,max(12 - len(entry)//2,0),entry.upper())
        c = stdscr.getch()
        while c != ord("\n"):
            if c == 127:
                entry = entry[:-1]
                stdscr.move(2,0)
                stdscr.clrtoeol()
            else:
                # print("---",c,curses.KEY_DL)
                entry += chr(c)
            stdscr.addstr(2,max(10 - len(entry)//2,0),entry.upper())
            stdscr.move(12,0)
            c = stdscr.getch()

        entry = entry.strip()

        if entry == "0":
            # stdscr.addstr(12,0,"Quit? (y/N) ")
            # if chr(stdscr.getch()).upper() == 'Y': 
            foundlist = list(found)
            foundlist.sort()
            print("You found:",", ".join(foundlist))
            time.sleep(.5)
            quit()

        stdscr.move(12,0)
        stdscr.clrtoeol()

        # except EOFError:
        # print(chr(27) + "[2J")
        # stdscr.clear()
        if entry not in found:
            n = check_entry(entry,pgram,special,stdscr)
            if n > 0:
                score += n
                found.add(entry)
        else:
            stdscr.addstr("Already found.")
        time.sleep(.1)
        stdscr.move(2,0)
        stdscr.clrtoeol()

    stdscr.move(12,0)
    stdscr.clrtoeol()
    stdscr.addstr("Queen Bee!")
    stdscr.getch()

curses.wrapper(main)