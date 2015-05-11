import equation_builder


t,l,u = readData()

functions = parseFunFile(funFile)

model = model_tseries(t,functions)

