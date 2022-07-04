# Computing-Chess
Play chess against against a smart ai!

## Setting up:
1. Clone it `git clone https://github.com/ihammadasghar/computing-chess.git`
2. `cd computing-chess`
3. Make a virtual environment `python -m venv venv`
4. Activate it `venv\scripts\activate`
5. Download requirements `pip install -r requirements.txt`
6. Run Path Finder: `python app.py`

NOTE: If the python/pip commands don't work for you try `python3` and `pip3` or `py` (python version issues)

## Intructions:
- Click the piece you want to select and click the destination and hit make move (click again to deselect)
- Click "Compute move" to get the AI's response.

## About this project:
Python being a higher level language sometimes lacks in speed for certain tasks & as it requires minimax to compute chess boards which is a recursive algorithmn & can take time to compute, so the main motivation behind this project was how fast can I make it go & in the process discovering the best python practices/data structures to get the best speeds possible.
By the end of the project I was able to increase the speed 30x from what I had initially, discovering how certain functions of python, data structures & project architecture affect execution time in the process.
