class Animal():
    def __init__(self, name):
        self.name = name
        print('Running initializer')
    def __del__(self):
        print('Running deconstructor')
        print(f'The object "{self.name}" is completely cleaned up, and its memory space is released')

cat = Animal('Meow')
input('Waiting...')
# 仍在引用，暂不析构