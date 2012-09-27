'''
A simple lexer of a small vector language.

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

Created on 2012-9-26

@author: bjzllou
'''

EOF = -1

# token type
COMMA = 'COMMA'
EQUAL = 'EQUAL'
LBRACK = 'LBRACK'
RBRACK = 'RBRACK'
TIMES = 'TIMES'
ADD = 'ADD'
PRINT = 'print'
ID = 'ID'
INT = 'INT'
STR = 'STR'

class Veclexer:
    '''
    LL(1) lexer. 
    It uses only one lookahead char to determine which is next token.
    For each non-terminal token, it has a rule to handle it.
    LL(1) is a quit weak parser, it isn't appropriate for the grammar which is 
    left-recursive or ambiguity. For example, the rule 'T: T r' is left recursive.
    However, it's rather simple and has high performance, and fits simple grammar.
    '''
    
    def __init__(self, input):
        self.input = input
        
        # current index of the input stream.
        self.idx = 1
        
        # lookahead char.
        self.cur_c = input[0]
        
    def next_token(self):
        while self.cur_c != EOF:
            c = self.cur_c
            
            if c.isspace():
                self.consume()
            elif c == '[':
                self.consume()
                return (LBRACK, c)
            elif c == ']':
                self.consume()
                return (RBRACK, c)
            elif c == ',':
                self.consume()
                return (COMMA, c)
            elif c == '=':
                self.consume()
                return (EQUAL, c)
            elif c == '*':
                self.consume()
                return (TIMES, c)
            elif c == '+':
                self.consume()
                return (ADD, c)
            elif c == '\'' or c == '"':
                return self._string()
            elif c.isdigit():
                return self._int()
            elif c.isalpha():
                t = self._print()
                return t if t else self._id()
            else:
                raise Exception('not support token')
        
        return (EOF, 'EOF')
           
    def has_next(self):
        return self.cur_c != EOF     
    
    def _id(self):
        n = self.cur_c
        self.consume()
        while self.cur_c.isalpha():
            n += self.cur_c
            self.consume()
            
        return (ID, n)
    
    def _int(self):
        n = self.cur_c
        self.consume()
        while self.cur_c.isdigit():
            n += self.cur_c
            self.consume()
            
        return (INT, int(n))
    
    def _print(self):
        n = self.input[self.idx - 1 : self.idx + 4]
        if n == 'print':
            self.idx += 4
            self.cur_c = self.input[self.idx]
            
            return (PRINT, n)
        
        return None
    
    def _string(self):
        quotes_type = self.cur_c
        self.consume()
        s = ''
        while self.cur_c != '\n' and self.cur_c != quotes_type:
            s += self.cur_c
            self.consume()
        if self.cur_c != quotes_type:
            raise Exception('string quotes is not matched. excepted %s' % quotes_type)
        
        self.consume()
        
        return (STR, s)
           
    def consume(self):
        if self.idx >= len(self.input):
            self.cur_c = EOF
            return
        self.cur_c = self.input[self.idx]
        self.idx += 1   
        
        
if __name__ == '__main__':
    exp = '''
        veca = [1, 2, 3]
        print 'veca:', veca
        print 'veca * 2:', veca * 2
        print 'veca + 2:', veca + 2
    '''
    lex = Veclexer(exp)
    t = lex.next_token()
    
    while t[0] != EOF:
        print t
        t = lex.next_token()
    