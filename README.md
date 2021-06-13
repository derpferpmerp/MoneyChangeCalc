# MoneyChangeCalc
This was created so that you could get the amount of items you needed to give back for change (ie at a restaurant).
How to Run:
The Second Value is the amount added onto the rounded down number that you supply for the amount.

For example:

```assembly
python3 pyworksolver.py 6 -p amt:4.5 max:3
```

Would be running pyworksolver, with a maximum amount of 10 combinations, output the percent (-p, exclude if you want for performance), and
the total to sum to of 4.5, with a maximum of 3 combinations until exiting

PARAMS:
```cs
PARAMS: {
      NumPlus: |REQUIRED| => "Fixed First Param, Required",
           -p: |OPTIONAL| => "Show Percent Done, might cause worse performance (+/- 0.1% second delay)",
      amt:NUM: |OPTIONAL| => "Sum up to Number NUM, if not supplied will default to 5",
      max:VAL: |OPTIONAL| => "Allow up to VAL number of combinations to be calculated before exiting"
}

```

Running that command will output:
```assembly
Possibility 1
2 Quarters
4 $1 Bills

Possibility 2
1 Nickel
2 Dimes
1 Quarter
4 $1 Bills

Possibility 3
3 Nickels
1 Dime
1 Quarter
4 $1 Bills

Possibility 4
5 Dimes
4 $1 Bills

Possibility 5
6 Quarters
3 $1 Bills
```

Have Fun!
