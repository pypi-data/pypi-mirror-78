from datefactory import *

def test_isFriday_true():
    assert isFriday(createDatetimeObj(28,8,2020)) == True
