from parser import decode

print("----- STRING -----")
print(decode(b"4:spam"))

print("\n----- INTEGER -----")
print(decode(b"i42e"))

print("\n----- LIST -----")
print(decode(b"l4:spam4:eggse"))

print("\n----- DICTIONARY -----")
print(decode(b"d3:cow3:moo4:spam4:eggse"))
