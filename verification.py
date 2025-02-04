import os
from pprint import pprint

class Verficiation:

    def __init__(self, file, out):
        self.file = file
        self.out = out

    def read(self):

        with open(self.file, 'r') as f:
            lines = [line.strip() for line in f.readlines()]
        
        # Sort lines by length (longest first)
        lines.sort(key=lambda x: len(x), reverse=True)
        
        unique_paths = []
    
        for line in lines:
            if not any(line in path for path in unique_paths):
                unique_paths.append(line)
        
        with open(self.out, 'w') as f:
            f.write('\n'.join(unique_paths) + '\n')


if __name__ == '__main__':
    curr_dir = os.getcwd()
    file = os.path.join(curr_dir, 'output.txt')
    out = os.path.join(curr_dir, 'unique_output.txt')
    v = Verficiation(file, out)
    
    v.read()