import fortune


def get_maxim(fortune_file):
    """return a fortune cookie"""
    return fortune.get_random_fortune(fortune_file)
