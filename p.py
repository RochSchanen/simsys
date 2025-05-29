
# S = "ABCDEF"
# print("".join([S[i] for i in subset]))

# dico = {1:"A", 2:"B"}
# for k in dico: print(k)

# def _ns(l, n):
#     nc, ns = 0, f"{n}"
#     while ns in l.keys():
#         ns = f"{n}{nc}"
#         nc += 1
#     return ns

# l = {}
# for i in range(5):
# 	ns = _ns(l, "Q")
# 	l[ns] = "X"
# print(l)


### SYMBOLS
EOL, SPC, NUL, TAB = "\n", " ", "", "\t"

def S():
	return """
	this is a line
	another line
	"""

L = [f"-{l.lstrip()}-" for l in S().split(EOL)]

print(EOL.join(L[1:-1]))
