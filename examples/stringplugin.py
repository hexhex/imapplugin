import dlvhex

def concat(strs):
  print("called", strs)
  needquote = any(['"' in str(s) for s in strs])
  unquoted = [str(s).strip('"') for s in strs]
  print(unquoted)
  result = ''.join(unquoted)
  if needquote:
    result = '"'+result+'"'
  dlvhex.output((result,))

def register():
	prop = dlvhex.ExtSourceProperties()
	prop.addFiniteOutputDomain(0)
	dlvhex.addAtom("concat", (dlvhex.TUPLE,), 1, prop)
