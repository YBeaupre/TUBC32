import math
import sys

def bitsToNum(bits, size):
	result = 0
	for i in range(size):
		index = (size - 1) - i
		if(bits[index] == 1):
			result += (2 ** i)
	
	return result

def hexStreamToBits(num, size):
	result = []
	for i in range(int(size/4)):
		value = int(num[i], 16)
		
		bit4 = value % 2
		value = math.floor(value/2)
		
		bit3 = value % 2
		value = math.floor(value/2)
		
		bit2 = value % 2
		value = math.floor(value/2)
		
		bit1 = value % 2
		value = math.floor(value/2)
		
		result.append(bit1)
		result.append(bit2)
		result.append(bit3)
		result.append(bit4)
		
	return result
    
def num2bits(num, bitlength):
	bits = []
	for i in range(bitlength):
		bits.append(num & 1)
		num >>= 1
	
	result = []
	for i in range(bitlength): 
		result.append(bits[bitlength - i - 1])
	
	return result
	
def enc(plaintext, long_key, showWork):
	
	#BitString to array of bits
	text = []
	for i in range(32):
		text.append(int(plaintext[i]))
		
	key = hexStreamToBits(long_key, 3584)
	
	#Repeat for 56 rounds
	for roundNum in range(56):
		if(showWork):
			print(roundNum+1)
		
		#Prepare both sub keys needed
		XORKeyStart = 56*roundNum
		permKeyStart = (56*roundNum)+32
		
		
		#key xor
		for i in range(32):
			text[i] = text[i] ^ key[XORKeyStart + i]
	
		if(showWork):
			print(bitsToNum(text, 32))
	
		#Fixed permutation
		state = [None] * 32
		for i in range(32):
			state[(3 * i) % 32] = text[i]
		
		text = state
		
		if(showWork):
			print(bitsToNum(text, 32))
		
		for i in range(8):
			c0 = 4*i 
			c1 = 4*i + 1 
			c2 = 4*i + 2
			c3 = 4*i + 3
			a0 = (3*i) + permKeyStart
			a1 = (3*i + 1) + permKeyStart
			a2 = (3*i + 2) + permKeyStart
			
			#Keyed permutation
			if(key[a0] == 0) and (key[a1] == 0) and (key[a2] == 0):
				#Do nothing (python requires there be something here)
				c0 = c0
			elif(key[a0] == 0) and (key[a1] == 0) and (key[a2] == 1):
				c0Bit = text[c0]
				c1Bit = text[c1]
				c2Bit = text[c2]
				c3Bit = text[c3]
				
				text[c0] = c1Bit
				text[c1] = c0Bit
				text[c2] = c3Bit
				text[c3] = c2Bit
			elif(key[a0] == 0) and (key[a1] == 1) and (key[a2] == 0):
				c0Bit = text[c0]
				c1Bit = text[c1]
				c2Bit = text[c2]
				c3Bit = text[c3]
				
				text[c0] = c2Bit
				text[c1] = c3Bit
				text[c2] = c0Bit
				text[c3] = c1Bit
			elif(key[a0] == 1) and (key[a1] == 0) and (key[a2] == 0):
				c0Bit = text[c0]
				c1Bit = text[c1]
				c2Bit = text[c2]
				c3Bit = text[c3]
				
				text[c0] = c3Bit
				text[c1] = c2Bit
				text[c2] = c1Bit
				text[c3] = c0Bit
			elif(key[a0] == 0) and (key[a1] == 1) and (key[a2] == 1):
				c0Bit = text[c0]
				c1Bit = text[c1]
				c2Bit = text[c2]
				c3Bit = text[c3]
				
				text[c0] = c1Bit
				text[c1] = c0Bit
				text[c2] = c2Bit
				text[c3] = c3Bit
			elif(key[a0] == 1) and (key[a1] == 0) and (key[a2] == 1):
				c0Bit = text[c0]
				c1Bit = text[c1]
				c2Bit = text[c2]
				c3Bit = text[c3]
				
				text[c0] = c2Bit
				text[c1] = c1Bit
				text[c2] = c0Bit
				text[c3] = c3Bit
			elif(key[a0] == 1) and (key[a1] == 1) and (key[a2] == 0):
				c0Bit = text[c0]
				c1Bit = text[c1]
				c2Bit = text[c2]
				c3Bit = text[c3]
				
				text[c0] = c3Bit
				text[c1] = c1Bit
				text[c2] = c2Bit
				text[c3] = c0Bit
			elif(key[a0] == 1) and (key[a1] == 1) and (key[a2] == 1):
				c0Bit = text[c0]
				c1Bit = text[c1]
				c2Bit = text[c2]
				c3Bit = text[c3]
				
				text[c0] = c0Bit
				text[c1] = c2Bit
				text[c2] = c1Bit
				text[c3] = c3Bit
		
			#Fixed substitution
			W = 0
			if (text[c0] == 1):
				W += 8
			if (text[c1] == 1):
				W += 4
			if (text[c2] == 1):
				W += 2
			if (text[c3] == 1):
				W += 1

			if(W == 1):
				text[c0] = 1
				text[c1] = 0
				text[c2] = 1
				text[c3] = 0
			elif(W == 2):
				text[c0] = 0
				text[c1] = 1
				text[c2] = 1
				text[c3] = 1
			elif(W == 3):
				text[c0] = 1
				text[c1] = 1
				text[c2] = 1
				text[c3] = 0
			elif(W == 4):
				text[c0] = 0
				text[c1] = 1
				text[c2] = 0
				text[c3] = 1
			elif(W == 5):
				text[c0] = 0
				text[c1] = 0
				text[c2] = 1
				text[c3] = 0
			elif(W == 6):
				text[c0] = 1
				text[c1] = 1
				text[c2] = 0
				text[c3] = 0
			elif(W == 7):
				text[c0] = 1
				text[c1] = 1
				text[c2] = 1
				text[c3] = 1
			elif(W == 8):
				text[c0] = 0
				text[c1] = 1
				text[c2] = 1
				text[c3] = 0
			elif(W == 9):
				text[c0] = 1
				text[c1] = 0
				text[c2] = 1
				text[c3] = 1
			elif(W == 10):
				text[c0] = 0
				text[c1] = 0
				text[c2] = 1
				text[c3] = 1
			elif(W == 11):
				text[c0] = 1
				text[c1] = 0
				text[c2] = 0
				text[c3] = 0
			elif(W == 12):
				text[c0] = 1
				text[c1] = 1
				text[c2] = 0
				text[c3] = 1
			elif(W == 13):
				text[c0] = 0
				text[c1] = 0
				text[c2] = 0
				text[c3] = 1
			elif(W == 14):
				text[c0] = 0
				text[c1] = 1
				text[c2] = 0
				text[c3] = 0
			elif(W == 15):
				text[c0] = 1
				text[c1] = 0
				text[c2] = 0
				text[c3] = 1
				
		if(showWork):
			print(bitsToNum(text, 32))
			print()
	
	return bitsToNum(text, 32)

def dec(ciphertext, long_key, showWork):
	text = num2bits(ciphertext, 32)
	key = hexStreamToBits(long_key, 3584)
	
	#Repeat for 56 rounds
	for count in range(56):
		roundNum = 55 - count
		if(showWork):
			print(roundNum+1)
		
		#Prepare both sub keys needed
		XORKeyStart = 56*roundNum
		permKeyStart = (56*roundNum)+32
		
		for i in range(8):
			c0 = 4*i 
			c1 = 4*i + 1 
			c2 = 4*i + 2
			c3 = 4*i + 3
			a0 = (3*i) + permKeyStart
			a1 = (3*i + 1) + permKeyStart
			a2 = (3*i + 2) + permKeyStart
			
			#Fixed substitution
			W = 0
			if (text[c0] == 1):
				W += 8
			if (text[c1] == 1):
				W += 4
			if (text[c2] == 1):
				W += 2
			if (text[c3] == 1):
				W += 1

			if(W == 1):
				text[c0] = 1
				text[c1] = 1
				text[c2] = 0
				text[c3] = 1
			elif(W == 2):
				text[c0] = 0
				text[c1] = 1
				text[c2] = 0
				text[c3] = 1
			elif(W == 3):
				text[c0] = 1
				text[c1] = 0
				text[c2] = 1
				text[c3] = 0
			elif(W == 4):
				text[c0] = 1
				text[c1] = 1
				text[c2] = 1
				text[c3] = 0
			elif(W == 5):
				text[c0] = 0
				text[c1] = 1
				text[c2] = 0
				text[c3] = 0
			elif(W == 6):
				text[c0] = 1
				text[c1] = 0
				text[c2] = 0
				text[c3] = 0
			elif(W == 7):
				text[c0] = 0
				text[c1] = 0
				text[c2] = 1
				text[c3] = 0
			elif(W == 8):
				text[c0] = 1
				text[c1] = 0
				text[c2] = 1
				text[c3] = 1
			elif(W == 9):
				text[c0] = 1
				text[c1] = 1
				text[c2] = 1
				text[c3] = 1
			elif(W == 10):
				text[c0] = 0
				text[c1] = 0
				text[c2] = 0
				text[c3] = 1
			elif(W == 11):
				text[c0] = 1
				text[c1] = 0
				text[c2] = 0
				text[c3] = 1
			elif(W == 12):
				text[c0] = 0
				text[c1] = 1
				text[c2] = 1
				text[c3] = 0
			elif(W == 13):
				text[c0] = 1
				text[c1] = 1
				text[c2] = 0
				text[c3] = 0
			elif(W == 14):
				text[c0] = 0
				text[c1] = 0
				text[c2] = 1
				text[c3] = 1
			elif(W == 15):
				text[c0] = 0
				text[c1] = 1
				text[c2] = 1
				text[c3] = 1
	
			#Keyed permutation
			if(key[a0] == 0) and (key[a1] == 0) and (key[a2] == 0):
				#Do nothing (python requires there be something here)
				c0 = c0
			elif(key[a0] == 0) and (key[a1] == 0) and (key[a2] == 1):
				c0Bit = text[c0]
				c1Bit = text[c1]
				c2Bit = text[c2]
				c3Bit = text[c3]
				
				text[c0] = c1Bit
				text[c1] = c0Bit
				text[c2] = c3Bit
				text[c3] = c2Bit
			elif(key[a0] == 0) and (key[a1] == 1) and (key[a2] == 0):
				c0Bit = text[c0]
				c1Bit = text[c1]
				c2Bit = text[c2]
				c3Bit = text[c3]
				
				text[c0] = c2Bit
				text[c1] = c3Bit
				text[c2] = c0Bit
				text[c3] = c1Bit
			elif(key[a0] == 1) and (key[a1] == 0) and (key[a2] == 0):
				c0Bit = text[c0]
				c1Bit = text[c1]
				c2Bit = text[c2]
				c3Bit = text[c3]
				
				text[c0] = c3Bit
				text[c1] = c2Bit
				text[c2] = c1Bit
				text[c3] = c0Bit
			elif(key[a0] == 0) and (key[a1] == 1) and (key[a2] == 1):
				c0Bit = text[c0]
				c1Bit = text[c1]
				c2Bit = text[c2]
				c3Bit = text[c3]
				
				text[c0] = c1Bit
				text[c1] = c0Bit
				text[c2] = c2Bit
				text[c3] = c3Bit
			elif(key[a0] == 1) and (key[a1] == 0) and (key[a2] == 1):
				c0Bit = text[c0]
				c1Bit = text[c1]
				c2Bit = text[c2]
				c3Bit = text[c3]
				
				text[c0] = c2Bit
				text[c1] = c1Bit
				text[c2] = c0Bit
				text[c3] = c3Bit
			elif(key[a0] == 1) and (key[a1] == 1) and (key[a2] == 0):
				c0Bit = text[c0]
				c1Bit = text[c1]
				c2Bit = text[c2]
				c3Bit = text[c3]
				
				text[c0] = c3Bit
				text[c1] = c1Bit
				text[c2] = c2Bit
				text[c3] = c0Bit
			elif(key[a0] == 1) and (key[a1] == 1) and (key[a2] == 1):
				c0Bit = text[c0]
				c1Bit = text[c1]
				c2Bit = text[c2]
				c3Bit = text[c3]
				
				text[c0] = c0Bit
				text[c1] = c2Bit
				text[c2] = c1Bit
				text[c3] = c3Bit
		
		if(showWork):
			print(bitsToNum(text, 32))
			
		#Fixed permutation
		state = [None] * 32
		for i in range(32):
			state[(11 * i) % 32] = text[i]
		
		text = state
		
		if(showWork):
			print(bitsToNum(text, 32))
	
		#key xor
		for i in range(32):
			text[i] = text[i] ^ key[XORKeyStart + i]
	
		if(showWork):
			print(bitsToNum(text, 32))
			print()
	
	return bitsToNum(text, 32)
	
#Handling command line arguments
showWork = False
if(len(sys.argv) > 1):
	if (sys.argv[1] == "t"):
		showWork = True
		
