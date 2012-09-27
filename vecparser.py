'''
A simple parser of a small vector language.

statlist: stat+
stat: ID '=' expr
    | 'print' expr (, expr)*
expr: multipart ('+' multipart)*
    | STR
multipart: primary ('*' primary)*
primary: INT
    | ID
    | '[' expr (',', expr)* ']'
INT: (1..9)(0..9)*
ID: (a..z | A..Z)*
STR: (\".*\") | (\'.*\')

example:
veca = [1, 2, 3]
vecb = veca + 4    # vecb: [1, 2, 3, 4]
vecc = veca * 3    # vecc: 

Created on 2012-9-26

@author: bjzllou
'''
import veclexer

class Vecparser:
    '''
    LL(1) parser.
    '''
    
    def __init__(self, lexer):
        self.lexer = lexer
        
        # lookahead token. Based on the lookahead token to choose the parse option.
        self.cur_token = lexer.next_token()
        
        # similar to symbol table, here it's only used to store variables' value
        self.symtab = {}
        
    def statlist(self):
        while self.lexer.has_next():
            self.stat()
    
    def stat(self):
        token_type, token_val = self.cur_token
        
        # Asignment
        if token_type == veclexer.ID:
            self.consume()
            
            # For the terminal token, it only needs to match and consume.
            # If it's not matched, it means that is a syntax error.
            self.match(veclexer.EQUAL)
            
            # Store the value to symbol table.
            self.symtab[token_val] = self.expr()
            
        # print statement
        elif token_type == veclexer.PRINT:
            self.consume()
            v = str(self.expr())
            while self.cur_token[0] == veclexer.COMMA:
                self.match(veclexer.COMMA)
                v += ' ' + str(self.expr())
            print v
        else:
            raise Exception('not support token %s', token_type)
        
    def expr(self):
        token_type, token_val = self.cur_token
        if token_type == veclexer.STR:
            self.consume()
            return token_val
        else:
            v = self.multipart()
            while self.cur_token[0] == veclexer.ADD:
                self.consume()
                v1 = self.multipart()
                if type(v1) == int:
                    v.append(v1)
                elif type(v1) == list:
                    v = v + v1
            
            return v         
    
    def multipart(self):
        v = self.primary()
        while self.cur_token[0] == veclexer.TIMES:
            self.consume()
            v1 = self.primary()
            if type(v1) == int:
                v = [x*v1 for x in v]
            elif type(v1) == list:
                v = [x*y for x in v for y in v1]
                
        return v
                
    def primary(self):
        token_type = self.cur_token[0]
        token_val = self.cur_token[1]
        
        # int
        if token_type == veclexer.INT:
            self.consume()
            return token_val
        
        # variables reference
        elif token_type == veclexer.ID:
            self.consume()
            if token_val in self.symtab:
                return self.symtab[token_val]
            else:
                raise Exception('undefined variable %s' % token_val)
        
        # parse list
        elif token_type == veclexer.LBRACK:
            self.match(veclexer.LBRACK)
            v = [self.expr()]
            while self.cur_token[0] == veclexer.COMMA:
                self.match(veclexer.COMMA)
                v.append(self.expr())
            self.match(veclexer.RBRACK)
            
            return v
        
    
    def consume(self):
        self.cur_token = self.lexer.next_token()
    
    def match(self, token_type):
        if self.cur_token[0] == token_type:
            self.consume()
            return True
        raise Exception('expecting %s; found %s' % (token_type, self.cur_token[0]))
       
if __name__ == '__main__':
    prog = '''
        veca = [1, 2, 3]
        vecb = [4, 5, 6]
        print 'veca:', veca
        print 'veca * 2:', veca * 2
        print 'veca + 2:', veca + 2
        print 'veca + vecb:', veca + vecb
        print 'veca + [11, 12]:', veca + [11, 12]
        print 'veca * vecb:', veca * vecb
        print 'veca:', veca
        print 'vecb:', vecb
        
    '''
    lex = veclexer.Veclexer(prog)
    parser = Vecparser(lex)
    parser.statlist()




 
        