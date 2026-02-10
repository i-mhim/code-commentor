def calc(x, y):
    # No comments, vague names
    res = (x * 0.1) + y
    return res / 2

class Handler:
    def __init__(self, data):
        self.d = data
    
    def proc(self):
        return [i for i in self.d if i > 10]