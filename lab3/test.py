def foo():
    global y
    y = 10
    x = 10
    print(x)

x = 0
print(x)
foo()
print(x)
print(y)