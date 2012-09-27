simple-list-interpreter
=======================

A simple interpreter to explore the compiler principles.
It is implemented by LL(1) and processes a small list language. The grammar is:  

statlist: stat+  
stat: ID '=' expr  | 'print' expr (, expr)*  
expr: multipart ('+' multipart)*  | STR  
multipart: primary ('*' primary)*  
primary: INT  | ID  | '[' expr (',', expr)* ']'  
INT: (1..9)(0..9)*  
ID: (a..z | A..Z)*  
STR: (\".*\") | (\'.*\')  

Here is a example that demonstrate the operations of the language:  

source code:  
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

output:  
veca: [1, 2, 3]  
veca * 2: [2, 4, 6]  
veca + 2: [1, 2, 3, 2]  
veca + vecb: [1, 2, 3, 2, 4, 5, 6]  
veca + [11, 12]: [1, 2, 3, 2, 11, 12]  
veca * vecb: [4, 5, 6, 8, 10, 12, 12, 15, 18, 8, 10, 12]  
veca: [1, 2, 3, 2]  
vecb: [4, 5, 6]  

More information can be found in [my blog](http://blog.csdn.net/chosen0ne/article/details/8024176)


