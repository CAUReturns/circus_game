class Formatter:
    @staticmethod
    def image(name, idx=''):
        return 'images/' + name + Formatter.concat_idx(idx) + '.png'

    @staticmethod
    def sound(name, idx=''):
        return 'sound/' + name + Formatter.concat_idx(idx) + '.wav'

    @staticmethod
    def concat_idx(idx=''):
        return '' if idx == '' else '/'+str(idx)
