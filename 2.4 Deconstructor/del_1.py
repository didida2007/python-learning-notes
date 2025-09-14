class Animal():
    def __init__(self, name):
        self.name = name
        print('Running initializer')
    def __del__(self):
        print('Running deconstructor')
        print(f'The object "{self.name}" is completely cleaned up, and its memory space is released')

cat = Animal('Meow')
# 引用完毕，启用析构