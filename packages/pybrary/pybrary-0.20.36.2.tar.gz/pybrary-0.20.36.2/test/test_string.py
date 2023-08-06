from pybrary.string import rm_ansi_codes, oct_mod


def test_s_oct_mod():
    assert oct_mod('r--r--r--') == '444'


def test_s_rm_ansi():
    esc, color, txt = chr(27), 33, 'OK'
    colored = f'{esc}[1;{color}m{txt}{esc}[0m'

    assert rm_ansi_codes(colored) == 'OK'


if __name__=='__main__': test_s_rm_ansi()
