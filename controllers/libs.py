class Formatter:
    @staticmethod
    def image(name, idx=''):
        prefix = 'images/'
        postfix = '' if idx == '' else '/'+str(idx)
        postfix += '.png'
        return prefix + name + postfix
