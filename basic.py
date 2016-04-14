from sys import *

tokens = []
num_stack = []
symbols = {}

def open_file(filename):
	data = open(filename, "r").read()
	data += "<EOF>"
	return data

def lex(filecontents):
	tok = ""
	state = 0
	isexpr = 0
	varstarted = 0
	var = ""
	string = ""
	expr = ""
	n = ""
	filecontents = list(filecontents)
	for char in filecontents:
		tok += char
		if tok == " ": 
			 if state == 0:
			 	tok = ""
			 else:
			 	tok = " "
		elif tok =="\n" or tok == "<EOF>":   #DELIMITERS
			if expr !="" and isexpr == 1:    #Identifying b/w expressing and number
				tokens.append("EXPR:" + expr)
				expr = ""	
			elif expr != "" and isexpr == 0:	  #identfying NUMBER
				tokens.append("NUM:" + expr)
				expr = ""
			elif var != "":					#Parsing variable
				tokens.append("VAR:" + var)
				var = "" 
				varstarted = 0	
			tok = ""
		elif tok == "=" and state == 0:	#Reseting the variable group
			if expr != "" and isexpr == 0:	
				tokens.append("NUM:" + expr)
				expr = ""
			if var != "":		
				tokens.append("VAR:" + var)
				var = "" 
				varstarted = 0		#Finding where variable ends
			if tokens[-1] == "EQUALS"
				tokens[-1] = "EQEQ"
			else
				tokens.append("EQUALS")
			tok = ""		
		elif tok == "$" and state == 0:    #VARIABLES START WITH $
			varstarted = 1
			var += tok
			tok = ""
		elif varstarted == 1:
			if tok == "<" or tok ==">":
 				if var != "":					#Parsing variable
						tokens.append("VAR:"+var)
						var = "" 
						varstarted = 0	
			var += tok
			tok = ""
		elif tok == "PRINT" or tok == "print":
			tokens.append("PRINT")
			tok = ""
		elif tok == "IF" or tok == "if":
			tokens.append("IF")
			tok = ""
		elif tok == "THEN" or tok == "then":
			if expr != "" and isexpr == 0:	
				tokens.append("NUM:" + expr)
				expr = ""
			tokens.append("THEN")
			tok = ""
		elif tok == "INPUT" or tok == "input":
			tokens.append("INPUT")
			tok = ""
		elif tok == "0" or tok == "1" or tok == "2" or tok == "3" or tok == "4" or tok == "5" or tok == "6" or tok == "7" or tok == "8" or tok == "9":  # To identify numbers
			expr += tok
			tok = "" 
		elif tok == "+" or tok == "-" or tok == "/" or tok == "*" or tok == "(" or tok == ")":   # USING precedence, use brackets instead
			isexpr = 1
			expr += tok
			tok = ""
		elif tok == "\t":  #ignoring TAB SPACE
			tok = ""
		elif tok == "\"" or tok == " \"":
			if state == 0:
				state = 1
			elif state == 1:
				tokens.append("STRING:" + string + "\"")
				string = ""
				state = 0
				tok = ""
		elif state == 1:
			string += tok
			tok =""
	#print(tokens)

	return tokens

def evalExpression(expr):


	return eval(expr)   #helps with precedence

'''  # Evaluating manualy
	expr = "," + expr

	i = len(expr) - 1
	num = ""

	while i >= 0:
		if (expr[i] == "+" or expr[i] == "-" or expr[i] == "/" or expr[i] == "*" or expr[i] == "%"):
			num = num[::-1]
			num_stack.append(num)
			num_stack.append(expr[i])
			num = ""
		elif (expr[i] == ","):
			num = num[::-1]
			num_stack.append(num)
			num = ""
		else:
			num += expr[i]
		i-=1
	print(num_stack)
'''








def doPRINT(toPRINT):   # TO remove double quote from parsed string and STRING EXPR NUM
	if(toPRINT[0:6] == "STRING"):
		toPRINT = toPRINT[8:]
		toPRINT = toPRINT[:-1]
	elif(toPRINT[0:3] == "NUM"):
		toPRINT = toPRINT[4:]
	elif(toPRINT[0:4] == "EXPR"): 
		toPRINT = evalExpression(toPRINT[5:])
	print(toPRINT)

def doASSIGN(varname, varvalue):
	symbols[varname[4:]] = varvalue

def getVARIABLE(varname):
	varname = varname[4:]
	if varname in symbols:
		return symbols[varname]
	else:
		return "VARIABLE ERROR: Undefined VARIABLE"
		exit()

def getINPUT(string, varname):
	i = input(string[1:-1] + " ")
	symbols[varname] = "STRING:\"" + i + "\""

def parse(toks):
	i = 0;
	while (i < len(toks)):
		if toks[i] + " " + toks[i+1][0:6] == "PRINT STRING" or toks[i] + " " + toks[i+1][0:3] == "PRINT NUM" or toks[i] + " " + toks[i+1][0:4] == "PRINT EXPR" or toks[i] + " " + toks[i+1][0:3] == "PRINT VAR":    # 6 for STRING, 4 for EXPR, 3 for NUM
			if toks[i+1][0:6] == "STRING":  # To find which tokens
				doPRINT(toks[i+1])  # To remove STRING part and print rest
			elif toks[i+1][0:3] == "NUM":
				doPRINT(toks[i+1])  # To remove NUM part and print rest
			elif toks[i+1][0:4] == "EXPR":
				doPRINT(toks[i+1])  # To remove EXPR part and print rest
			elif toks[i+1][0:3] == "VAR":
				doPRINT(getVARIABLE(toks[i+1])) 
			i+=2
		elif toks[i][0:3] + " " + toks[i+1] + " " + toks[i+2][0:6] == "VAR EQUALS STRING" or toks[i][0:3] + " " + toks[i+1] + " " + toks[i+2][0:3] == "VAR EQUALS NUM" or toks[i][0:3] + " " + toks[i+1] + " " + toks[i+2][0:4] == "VAR EQUALS EXPR"  or toks[i][0:3] + " " + toks[i+1] + " " + toks[i+2][0:3] == "VAR EQUALS VAR":
			if toks[i+2][0:6] == "STRING":  # To find which tokens
				doASSIGN(toks[i], toks[i+2])  # To remove STRING part and print rest
			elif toks[i+2][0:3] == "NUM":
				doASSIGN(toks[i], toks[i+2])  # To remove NUM part and print rest
			elif toks[i+2][0:4] == "EXPR":
				doASSIGN(toks[i],"NUM:" + str(evalExpression(toks[i+2][5:])))   # To remove EXPR part and print rest
			elif toks[i+2][0:3] == "VAR":
				doASSIGN(toks[i],getVARIABLE(toks[i+2])) #get the second variable and return its value and assign to thhe first
			i+=3 #found three tokens, so passing by them
		elif toks[i] + " " + toks[i+1][0:6] + " " + toks[i+2][0:3] == "INPUT STRING VAR": # INPUT STRING: " " VAR: $VARNAME
			getINPUT(toks[i+1][7:], toks[i+2][4:]) #passing variable name to save input in
			i+=3
	#print(symbols)





def run():
	data = open_file(argv[1])
	toks = lex(data)
	parse(toks)
run()