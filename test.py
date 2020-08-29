inp_w = "ば"

if inp_w == "ば":
    inp_w = [l.replace("ば", "は") for l in inp_w]
    inp_w.append("゙")

print(inp_w)