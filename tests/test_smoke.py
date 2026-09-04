from runtime import run
def test_basic():assert run('show 10 + 20\nfinish')=='30'
def test_array():assert run('set x = [1,2,3]\nshow x[1]\nfinish')=='2'
def test_function():assert run('define add(a,b) =>\n give a+b\nend\nshow add(2,3)\nfinish')=='5'
