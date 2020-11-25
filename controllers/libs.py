class Formatter:
    @staticmethod
    def image(name, idx=''):
        prefix = 'images/'
        postfix = '.png'
        return prefix + name + str(idx) + postfix
