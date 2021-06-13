import itertools,sys,re,math,time,subprocess

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



def shorten(num):
    power=re.sub(r".*\+","",str(num))
    actnum=re.sub(r"e.*","",str(num))
    if power[0]=="0":
        if power[1::] in list([k for k in SUFFIXES.keys()]):return f"{actnum} {SUFFIXES[str(power[1::])]}"
        return "{:,}".format(int(int(re.sub(r"\..*","",str(actnum)))*math.pow(10,int(power[1::]))))
    else:
        if power in list([k for k in SUFFIXES.keys()]):return f"{actnum} {SUFFIXES[str(power)]}"
        return "{:,}".format(int(int(re.sub(r"\..*","",str(actnum)))*math.pow(10,int(power[0::]))))

def countX(lst, x):return lst.count(x)


def equal_ignore_order(a, b):
    unmatched=list(b)
    for element in a:
        try:unmatched.remove(element)
        except ValueError:return False
    return not unmatched


def change(amt, req=False):
    lstf = []
    if not req:
        amtpen = re.sub(r"\..*", "", str(amt))
        for x in range(2, int(amtpen) + int(sys.argv[1])):
            lst2itr=["Penny", "Nickel", "Dime", "Quarter"]
            [lst2itr.append(str(asd2)) for asd2 in list([asd for asd in [1,5,10,20,50,100] if asd < amt])]

            print(f"Working on Combinations with Length {x}")
            tic = time.perf_counter()
            lstcombs = list([list(g) for g in list(itertools.product(lst2itr,repeat=x))])
            for ps6 in ["Penny", "Nickel", "Dime", "Quarter",1,5,10,20,50,100]:lstcombs.append([str(ps6)])
            toc = time.perf_counter()
            print(f"Finished Generating",shorten("{:.2e}".format(len(lstcombs))),f"Combinations for Length {x} in {toc - tic:0.4f}s")
            itmsumlist = []
            for itml in lstcombs:
                numf = 0
                for rng in range(len(itml)):
                    if itml[rng] == "Penny":
                        numf += 0.01
                        continue
                    elif itml[rng] == "Nickel":
                        numf += 0.05
                        continue
                    elif itml[rng] == "Dime":
                        numf += 0.1
                        continue
                    elif itml[rng] == "Quarter":
                        numf += 0.25
                        continue
                    numf += int(itml[rng])
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
            print(f"Determined Combatible Combinations for Length {x} in {toc - tic:0.4f}s")



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
for gg in range(len(sys.argv)):
    gg=str(sys.argv[gg])
    if "amt" in gg:
        inthere=True
        break
    else:
        inthere=False
if inthere:change(float(re.sub(r".*\:","",gg)), req=False)
else:change(5,req=False)
