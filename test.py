for n in range(404):
    if (0 != (n % 4)) or ((0 == (n % 100)) and (0 != (n % 400))):
        pass
    else:
        print("{0}年はうるう年です".format(n))
