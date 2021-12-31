# short-truth
A simple Python script(s) that calculates an approximate number of shares still short using FINRA data.

This data goes back until August of 2009.

How to use:
- Download the code.
- Install httpx: ```python3 -m pip install httpx```.
- Run the file for your desired exchange(s) with the desired ticker.
- E.x. ```python3 short-truth-NNE.py TSLA``` << Case insensitive/

This code does not take into account off-exchange trades or pre/post market trades so the real volume could be less. However, this assumes all non shorted shares are being used to cover so the real volume could be higher. 
