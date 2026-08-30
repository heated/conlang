modes = {"h-u":"number","h-o":"date","h-i":"time","h-e":"spell","h-e-n":"phonetic(res)",
         "h-i-n":"coords(res)","h-a-s":"mode close","h-o-s":"close+checksum","h-a-n":"chunk sep"}
gram  = {"h-a":"and","h-a-n":"NEGATION","h-a-l":"to/for","h-e-s":"of/from","h-e-l":"that/which",
         "h-i-s":"with/by","h-o-l":"at/in/on","h-o-n":"past TAM","h-u-n":"or","h-u-s":"Y/N question",
         "h-u-l":"irrealis/future","h-i-l":"RESERVED"}
cells = [f"h-{v}" + (f"-{c}" if c else "") for v in "aeiou" for c in ["", "n", "s", "l"]]
print(f"{'cell':7} {'modes':16} {'grammar':16}")
clash, free = [], []
for c in cells:
    m, g = modes.get(c, ""), gram.get(c, "")
    if m and g:
        clash.append(c)
    if not m and not g:
        free.append(c)
    print(f"{c:7} {m:16} {g:16}")
print()
print("occupied:", len([c for c in cells if c in modes or c in gram]), "/ 20")
print("COLLISIONS:", clash)
print("genuinely free:", free)
