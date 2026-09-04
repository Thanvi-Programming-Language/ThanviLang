from dataclasses import dataclass
KEYWORDS={"set","show","check","otherwise","repeat","define","give","end","finish","true","false","and","or","not"}
@dataclass
class Token: kind:str; value:object; line:int; col:int
def lex(source):
    out=[];i=0;line=1;col=1
    while i<len(source):
        c=source[i]
        if c in ' \t\r': i+=1;col+=1;continue
        if c=='\n': i+=1;line+=1;col=1;continue
        if c=='#' or (c=='/' and i+1<len(source) and source[i+1]=='/'):
            while i<len(source) and source[i]!='\n': i+=1;col+=1
            continue
        ln,cl=line,col
        if c=='"':
            i+=1;col+=1;b=[]
            while i<len(source) and source[i]!='"':
                if source[i]=='\\' and i+1<len(source):
                    e=source[i+1];b.append({'n':'\n','t':'\t','r':'\r'}.get(e,e));i+=2;col+=2
                else:b.append(source[i]);i+=1;col+=1
            if i>=len(source): raise SyntaxError(f'Line {ln}: unclosed string')
            i+=1;col+=1;out.append(Token('STRING',''.join(b),ln,cl));continue
        if c.isdigit() or (c=='.' and i+1<len(source) and source[i+1].isdigit()):
            j=i
            while j<len(source) and (source[j].isdigit() or source[j]=='.'):j+=1
            raw=source[i:j]
            if raw.count('.')>1:raise SyntaxError(f'Line {ln}: invalid number {raw}')
            out.append(Token('NUMBER',float(raw) if '.' in raw else int(raw),ln,cl));col+=j-i;i=j;continue
        if c.isalpha() or c=='_':
            j=i+1
            while j<len(source) and (source[j].isalnum() or source[j]=='_'):j+=1
            w=source[i:j];out.append(Token('KW' if w in KEYWORDS else 'IDENT',w,ln,cl));col+=j-i;i=j;continue
        two=source[i:i+2]
        if two in ('==','!=','<=','>=','=>'):out.append(Token('OP',two,ln,cl));i+=2;col+=2;continue
        if c in '+-*/%()[],=<>':out.append(Token('OP',c,ln,cl));i+=1;col+=1;continue
        raise SyntaxError(f'Line {ln}, col {cl}: unexpected character {c!r}')
    out.append(Token('EOF','',line,col));return out
