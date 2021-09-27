# -*- coding: utf-8 -*-
"""
Created on Sun Sep 26 18:47:19 2021

@author: sefunmi

MIPS Decoder Class

default constructor

convert_to_asm(string Instruct_32bit) -> String cmd_r0_r1_r2 
cmd_r0_r1_r2 = None if Error Occur

getCmd(self, String opcode, String func) -> String cmd_asm, String cmd_type

getSyntax_hex_asm(string Instruct_32bit, string cmd)-> String cmd_r0_r1_r2



"""
class MyClass:
    """converts 32bit hex instructions to MIPS Assembly code wiht Error Check"""
    def __init__(self):
        self.rd = None
        self.rs = None
        self.rt = None
        self.shamt = None
        self.immediate = None
        self.Hex_char_set = { "0","1","2","3","4","5","6","7","8","9","A","B","C","D","E","F"}
        self.cmd_hashmap = {#Opcode_func/X : (asm,cmdtype)
            1:(0,0)}
        
        
    def convert_to_asm(self, String instruct_32bit):
        """error chec:
            length
            hex char
            cmd/opcode_func exist
        """ 
        if len(instruct_32bit) != 8:
            return None
        
        for value in instruct_32bit:
            if Value not in self.Hex_char_set:
                return None 
        # TODO: opcode and func index
        opcode = instruct_32bit[:] + ""
        func = instruct_32bit[:] + ""
        
        (cmd_asm, cmd_type) = self.getCmd(opcode,func)
        (r0,r1,r2) = self.getSyntax_hex_asm(cmd_asm, cmd_type)
        
        asm = ""
        if r2 != None:
            asm = cmd_asm + " " + r0 +", "+r1 +", "r2
        else:
            asm = cmd_asm + " " + r0 +", "+r1
        
        return asm
    
            
    def getCmd(self, String opcode, String func):  
        cmd_hex = opcode+"_X"
        if opcode == "00":
            cmd_hex = opcode+"_"+func
            
        (cmd_asm, cmd_type) = self.cmd_hashmap[cmd_hex]
        
        self.rs = instruct_32bit[:]# TODO: rs index
        self.rt =instruct_32bit[:]# TODO: rt index
        if self.cmd_type == "I":
            self.rd = instruct_32bit[:] # TODO: rd index
            self.shamt = instruct_32bit[:]  # TODO: shamt index
        else:
            self.immediate = instruct_32bit[:] # TODO:  immediate index
        
        return (cmd_asm, cmd_type)
        
    def getSyntax_hex_asm(self,cmd_asm, cmd_type):
        
        r0 = None
        r1 = None
        r2 = None
        
        if cmd_type == "I":
			r0 = self.rt
			if cmd_asm in {24 ,25 ,30 ,23 ,28 ,38, 29}:
				# TODO:  signextendedImm
                r1 = self.immediate + "(" + self.rs +")" 
            elif cmd_asm == f:
				r1 = self.immediate #16 bit
            else:
				r1 = self.rs
				if cmd_asm in {4, 5}: //branch
					# TODO: Addr_#### relative offset (0004/line) index
                    r2 = "Addr_" + self.immediate
                elif cmd_asm in {c, d}:
                    # TODO: zeroextendedImm 
					r2  = self.immediate
				else:
                    # TODO: signextendedImm 
					r2  = self.immediate
		elif cmd_type == "R":
			r0 = self.rd
			if cmd_asm in {"0/00","0/02"}:
				r1 = self.rt
				r2 = self.shamt
			else:
				r1 = self.rs
				r2 = self.rt
                
		return (r0,r1,r2) #r2 can equal NONe
        