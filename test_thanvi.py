from parser import parse
from runtime import run


def test_parser():
    assert len(parse('set x = 1\nfinish').statements) == 2


def test_arithmetic_and_show(capsys):
    run('show 2 + 3 * 4\nfinish')
    assert capsys.readouterr().out.strip() == '14'


def test_condition(capsys):
    source = '''
set age = 20
check age >= 18 =>
    show "adult"
otherwise =>
    show "minor"
end
finish
'''
    run(source)
    assert capsys.readouterr().out.strip() == 'adult'


def test_function(capsys):
    source = '''
define add(a, b) =>
    give a + b
end
show add(2, 3)
finish
'''
    run(source)
    assert capsys.readouterr().out.strip() == '5'


def test_repeat(capsys):
    source = '''
set count = 1
repeat count <= 3 =>
    show count
    set count = count + 1
end
finish
'''
    run(source)
    assert capsys.readouterr().out.strip().splitlines() == ['1', '2', '3']
