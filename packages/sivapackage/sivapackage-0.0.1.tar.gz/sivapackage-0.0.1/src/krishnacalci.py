"""calc
 
Usage:
    calc.py square <num>
    calc.py cube  <num>
    calc.py (-h | --help)
 
Options:
    -h --help     Show this screen.
 
"""
from docopt import docopt 
 
 
def square(num):
  print(num**2) 
 
def cube(num):
  print(num**3)
 
 
if __name__ == '__main__':                                                                                                                              
  arguments = docopt(__doc__)
  if arguments['square']:
    square(int(arguments['<num>']))
  elif arguments['cube']:
    cube(int(arguments['<num>']))
