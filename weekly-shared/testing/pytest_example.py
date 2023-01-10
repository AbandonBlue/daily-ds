"""
    簡短的pytest範例，之後都可以透過 function 自建 unit test。
    參考自(CS50): https://www.youtube.com/watch?v=tIrcxwLqzjQ

    記得 function 必須要 test_開頭
"""
def square(x):
    return x ** 2

# 要test開頭才會被pytest辨識。
def test_positive():
    assert square(9) > 0
    assert square(-1) > 0
    # assert -1 > 0

def test_negative():
    assert square(-1) < 0
    assert square(9) < 0
    assert square(9) < 0

def test_zero():
    assert square(0) == 0
    assert square(0.1) == 0


# $ pytest pytest_example.py