import itertools,sys,re,math,time,subprocess,datetime
from pprint import pprint

global tic,toc

VALUES = {
    "Penny": 0.01,
    "Nickel": 0.05,
    "Dime": 0.1,
    "Quarter": 0.25,
    "Bills": ["1", "5", "10", "20", "50", "100"]
}



SUFFIXES = {
    "6":"M",
    "7":"x 10M",
    "8":"x 100M",
    "9":"B",
    "10":"x 10B",
    "11":"x 100B",
    "12":"T",
    "13":"x 10T",
    "14":"x 100T"
}

# Return The Json Values (Useful for If You are Adding Custom Coins / Bills)

try:subprocess.call(f"echo {VALUES} | underscore print | jq",shell=True)
except ValueError:pprint(VALUES)


# Takes in a Number in Scientific Notation, and will break it up into powers of ten,
# then convert it into Shortened Form if the Provided Suffix is Available.
# For Example, shorten("7.64e+6") will return "7.64 B"
def shorten(num):
    power=re.sub(r".*\+","",str(num))
    actnum=re.sub(r"e.*","",str(num))
    if power[0]=="0":
        if power[1::] in list([k for k in SUFFIXES.keys()]):return f"{actnum} {SUFFIXES[str(power[1::])]}"
        return "{:,}".format(int(int(re.sub(r"\..*","",str(actnum)))*math.pow(10,int(power[1::]))))
    else:
        if power in list([k for k in SUFFIXES.keys()]):return f"{actnum} {SUFFIXES[str(power)]}"
        return "{:,}".format(int(int(re.sub(r"\..*","",str(actnum)))*math.pow(10,int(power[0::]))))


# Count the amount of times that "x" appears in list "lst"
def countX(lst, x):return lst.count(x)



# Return Whether or Not Two Lists are the Same.
# For example, equal_ignore_order([1,2,3,4,5],[5,1,4,2,3]) will return True
def equal_ignore_order(a, b):
    unmatched=list(b)
    for element in a:
        try:unmatched.remove(element)
        except ValueError:return False
    return not unmatched


def change(amt,req=False,maximum=100000):
    lstf = []
    if not req:
        amtpen = re.sub(r"\..*", "", str(amt))

        # This For Loop ranges from two up until the first system argument plus amt without the decimal point because
        # for some reason itertools doesn't understand that you can have just one thing in a combination, which gets added
        # with the line that has "for ps6..."
        for x in range(2, int(amtpen) + int(sys.argv[1])):
            lst2itr=["Penny", "Nickel", "Dime", "Quarter"]
            [lst2itr.append(str(asd2)) for asd2 in list([asd for asd in [1,5,10,20,50,100] if asd < amt])]

            # Generates all the combinations with itertools, and returns it to the user.
            print(f"Working on Combinations with Length {x}")
            tic = time.perf_counter()
            lstcombs = list([list(g) for g in list(itertools.product(lst2itr,repeat=x))])
            for ps6 in ["Penny", "Nickel", "Dime", "Quarter",1,5,10,20,50,100]:lstcombs.append([str(ps6)])
            toc = time.perf_counter()

            timeinsec = float(f"{toc - tic:0.4f}")
            if timeinsec > 60:time2=f"{datetime.timedelta(seconds=timeinsec)}"
            else:time2=f"{toc - tic:0.4f}s"

            print(f"Finished Generating",shorten("{:.2e}".format(len(lstcombs))),f"Combinations for Length {x} in {time2}")

            itmsumlist = []
            # Converts the Coins (Called their actual names) to their corresponding value in the dictionary
            for itml in lstcombs:
                numf = 0
                for rng2 in range(len(itml)):numf += VALUES[str(itml[rng2])] if itml[rng2] in list([k1 for k1 in VALUES.keys()]) else int(itml[rng2])
                itmsumlist.append(numf)



            tic = time.perf_counter()

            for sm in range(len(itmsumlist)):
                if str(sm)[-1]=="0" and "-p" in sys.argv:
                    sys.stdout.write('Percent Done: {}\r'.format(re.sub(r"\..*","",str(sm*(1/len(itmsumlist))*100))))
                    sys.stdout.flush()
                alreadyinlist = False
                if str(itmsumlist[sm]) == str(amt):
                    if len(lstf) != 0:
                        alreadyinlist = [True for ps in lstf if equal_ignore_order(lstcombs[sm], ps)]
                        if not alreadyinlist:
                            lstf.append(lstcombs[sm])
                            print(f"\n[DEV] Found Combination {lstcombs[sm]}\n")
                    else:
                        lstf.append(lstcombs[sm])
                        print(f"\n[DEV]Found Combination {lstcombs[sm]}\n")
            toc = time.perf_counter()

            timeinsec = float(f"{toc - tic:0.4f}")
            if timeinsec > 60:print(f"Determined Combatible Combinations for Length {x} in {datetime.timedelta(seconds=timeinsec)}")
            else:print(f"Determined Combatible Combinations for Length {x} in {toc - tic:0.4f}s")
            if len(lstf)==maximum:
                break



        print("\n")
        for ps5 in lstf:
            res=[]
            print(f"\n\tPossibility {lstf.index(ps5)+1}")
            [res.append(gc) for gc in ps5 if gc not in res]
            for ps5itm in res:
                amtofnum = int(countX(ps5,ps5itm))
                if amtofnum == 1:
                    if str(ps5itm) in VALUES["Bills"]:print(f"\t{amtofnum} ${ps5itm} Bill")
                    else:print(f"\t{amtofnum} {ps5itm}")
                elif amtofnum > 1:
                    if ps5itm in VALUES["Bills"]:print(f"\t{amtofnum} ${ps5itm} Bills")
                    else:print(f"\t{amtofnum} Pennies") if ps5itm == "Penny" else (print(f"\t{amtofnum} {ps5itm}s") if ps5itm != "Penny" else None)
        print("\n")

inthere=False
intheremax=False
for gg in range(len(sys.argv)):
    gg2=str(sys.argv[gg])
    if "amt:" in gg2:
        inthere=True
        amt2use=float(re.sub(r".*\:","",str(sys.argv[gg])))
    elif "max:" in gg2:
        intheremax=True
        max2use=int(re.sub(r"[^1-9]*","",str(sys.argv[gg])))

amt1=amt2use if inthere else 5
max2usev=max2use if intheremax else 100000

change(amt1,maximum=max2usev,req=False)
