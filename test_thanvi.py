from parser import parse
from runtime import run

def test_parser():
    assert len(parse("let x = 1;").statements) == 1

def test_arithmetic_and_print(capsys):
    run("print 2 + 3 * 4;")
    assert capsys.readouterr().out.strip() == "14"

def test_condition(capsys):
    run('if (2 < 3) { print "yes"; } else { print "no"; }')
    assert capsys.readouterr().out.strip() == "yes"

def test_function(capsys):
    run("fn add(a,b) { return a+b; } print add(2,3);")
    assert capsys.readouterr().out.strip() == "5"
