import os, sys
print(__file__)
#sys.path.insert(0, 'src')
print(os.getcwd())
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))