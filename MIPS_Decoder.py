# -*- coding: utf-8 -*-
"""
Created on Sun Sep 26 18:47:19 2021

@author: sefunmi

MIPS Decoder Class

default constructor

convert_to_asm(string Instruct_32bit_binary) -> String cmd_r0_r1_r2 
cmd_r0_r1_r2 = None if Error Occur

getCmd(self, String opcode, String func) -> String cmd_asm, String cmd_type

getSyntax_hex_asm(string Instruct_32bit_binary, string cmd)-> String cmd_r0_r1_r2

getConstant(self, String immediate_base2, bool isSigned) -> String un/signed_constant_base10

storeJumpAddress(String immediate_base2) -> bool isStored [stores jump address hashset]
checks if jump is out of bounds

renderJumpLabels(string filename(.asm)) -> void [writes in the labels at the expected line using the jump address hashset]

invert()
add()

"""
class MIPSDecoder:
    """converts 32bit hex instructions to MIPS Assembly code wiht Error Check"""
    def __init__(self, filename,num_program_lines):
        self.filename = filename
        self.num_program_lines = num_program_lines
        
        self.Hex_char_set = { "0","1","2","3","4","5","6","7","8","9","A","B","C","D","E","F"}
        self.jump_Addr = {} #(outputline addr[0xaddr%0x0004])
        self.instruction = {
            "opcode" : None,
            "func" : None,
            "rd" : None,
            "rs" = None,
            "rt" = None,
            "shamt" = None,
            "immediate" = None
            }
        self.cmd_hashmap = {#Opcode[0:6]_func[26:] /X : (asm,cmdtype)
            "000000_100000":("add","R"), #hex 0_20 == b 0..._0010 0000 
            "001000_X":("addi","I"), #hex 8 == b 0000 1000 
            "001001_X":("addiu","I"),#hex 9 == b 0000 1001 
            "000000_100001":("addu","R"), #hex 0_21 == b 0..._0010 0001 
            "000000_100100":("and","R"),  #hex 0_24 == b 0..._0010 0100 
            "001100_X":("andi","I"), #hex C == b 0000 1100
            "000100_X":("beq","I"),#hex 4 == b 0000 0100 
            "000101_X":("bne","I"),#hex 5 == b 0000 0101
            "100100_X":("lbu","I"),#hex 24 == b 0010 0100
            "100101_X":("lhu","I"),#hex 25 == b 0010 0101
            "110000_X":("ll","I"),#hex 30 == b 0011 0000
            "001111_X":("lui","I"),#hex F == b 0000 1111
            "100011_X":("lw","I"),#hex 23 == b 0010 0011
            "000000_100111":("nor","R"),#hex 0_27 == b 0..._0010 0111 
            "000000_100101":("or","R"),#hex 0_25 == b 0..._0010 0101 
            "001101_X":("ori","I"),#hex D == b 0000 1101
            "000000_101010":("slt","R"),#hex 0_2a == b 0..._0010 1010 
            "001010_X":("slti","I"),#hex A == b 0000 1010
            "001011_X":("sltiu","I"),#hex B == b 0000 1011
            "000000_101011":("sltu","R"),#hex 0_2b == b 0..._0010 1011
            "000000_000000":("sll","R"),#hex 0_00 == b 0..._0000 0000 
            "000000_000010":("srl","R"),#hex 0_02 == b 0..._0000 0010 
            "000000_100100":("sb","I"),#hex 28 == b 0010 0100
            "000000_110100":("sc","I"),#hex 38 == b 0011 0100
            "101001_X":("sh","I"),#hex 29 == b 0010 1001
            "101011_X":("sw","I"),#hex 2b == b 0010 1011
            "100010 _X":("sub","R"),#hex 0_22 == b 0..._0010 0010 
            "100011_X":("subu","R"),#hex 0_23 == b 0..._0010 0011 
            }
        
        
    def convert_to_asm(self, instruct_32bit):
        """error check:
            length
            hex char
            cmd/opcode_func exist
        """ 
        if len(instruct_32bit) != 32:
            return None
        
        for value in instruct_32bit:
            if value not in self.Hex_char_set:
                return None 
        
        self.instruction["opcode"] = instruct_32bit[0:6] + ""
        self.instruction["func"]  = instruct_32bit[26:] + ""
        
        (cmd_asm, cmd_type) = self.getCmd(self.instruction["opcode"],self.instruction["func"] )
        
        self.instruction["rs"] = instruct_32bit[:]# TODO: rs index
        self.instruction["rt"] = instruct_32bit[:]# TODO: rt index
        if cmd_type == "I":
            self.instruction["rd"] = instruct_32bit[:] # TODO: rd index
            self.instruction["shamt"] = instruct_32bit[:]  # TODO: shamt index
        else:
            self.instruction["immediate"] = instruct_32bit[:] # TODO:  immediate index
            
        (r0,r1,r2) = self.getSyntax_hex_asm(cmd_asm, cmd_type)
        
        asm = ""
        if r2 != None:
            asm = cmd_asm + " " + r0 +", "+r1 +", "r2
        else:
            asm = cmd_asm + " " + r0 +", "+r1
            
        return asm
    
            
    def getCmd(self, opcode,func):  
        cmd_hex = opcode+"_X"
        if opcode == "000000":
            cmd_hex = opcode+"_"+func
        (cmd_asm, cmd_type) = self.cmd_hashmap[cmd_hex]
        return (cmd_asm, cmd_type)
        
    
    def getSyntax_hex_asm(self,cmd_asm, cmd_type):
        r0 = None
        r1 = None
        r2 = None
        
        if (cmd_type == 'I'):
            r0 = self.instruction["rt"]
            if cmd_asm in {"lbu" ,"lhu" ,"ll" ,"lw" ,"sb" ,"sc", "sh"}:
                #signextendedImm
                r1 = self.getConstant(self.instruction["immediate"], isSigned = True) + "(" + self.instruction["rs"]+")" 
            elif cmd_asm == f:
                r1 = self.instruction["immediate"] #16 bit
            else:
                r1 = self.instruction["rs"]
                if cmd_asm in {"beq", "bne"}: #branch
                    # TODO: Addr_#### relative offset (0004/line) index capture addresses another function to render adress
                    r2 = "Addr_" + self.instruction["immediate"] #TODO: check if address is out of bounds
                elif cmd_asm in {"andi", "ori"}: #logical immediate
                    #zeroextendedImm 
                    r2  = self.getConstant(self.instruction["immediate"], isSigned = False)
				else:
                    #signextendedImm 
                    r2  =  self.getConstant(self.instruction["immediate"], isSigned = True)   
        elif (cmd_type == "R"):
            r0 = self.instruction["rd"]
            if cmd_asm in {"sll","srl"}:
				r1 = self.instruction["rt"]
				r2 = self.instruction["shamt"]
			else:
				r1 = self.instruction["rs"]
				r2 = self.instruction["rt"]
                
		return (r0,r1,r2) #r2 can equal NONE
        
    def getConstant(self, immediate_base2, isSigned):
        sign = ''
        base10 = ""
        if isSigned:
            if immediate_base2[0] == '1':
                sign = '-'
            invert = BinaryStrOp.invert(immediate_base2)
            twoComp = BinaryStrOp.add(invert)
            base10 = str(int(twoComp,2))
        else:
            base10 = str(int(immediate_base2,2))
            
        return sign + base10
            
class BinaryStrOp:   
           
    def invert(self, base2):
        b_num = list(base2)
        value = list(base2)

        for i in range(len(b_num)):
        	digit = b_num.pop()
        	if digit == '1':
        		value[i] = '0'
            else:
                value[i] = '1'
                
        return "".join(value)
        
    
    def add(self, base2):
        b_num = list(base2)
        value = 0

        for i in range(len(b_num)):
        	digit = b_num.pop()
        	if digit == '1':
        		value = value + pow(2, i)
                
        return value
        
        
        