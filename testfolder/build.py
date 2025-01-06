import sys

sys.path.append(r"C:\Users\User5\Documents\OLD DATA\2dEngine")

from r2d import building

building.build_all_files(sys.argv[2:], sys.argv[1])