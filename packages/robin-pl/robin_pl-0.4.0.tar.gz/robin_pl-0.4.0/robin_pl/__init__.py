"""FotonPC
Robin Interpter
example:
    x=1
    y=x*3+2
    печать y+x
print - печать
goto - строка
if - если

exaple:
    i=0
    печать i
    i=i+1
    если (i<101):строка 2
    x=13;печать x*y
result:
    1
    2
    3
    4
    5
    6
    7
    8
    9
    10
    11
    12
    13
    ...
    99
    100"""
import random
def is_error(obj):
    try:
        obj.ie()
        return True
    except:
        return False
def supereval(value):
    res=value
    while True:
        #try:
        res=eval(res)
        #except: break
    return res
def superindex(it,value):
    res=[]
    for i in range(len(it)):
        if it[i]==value:
            res+=[i]
    return res
class Ro_Error:
    def __init__(self,line,text,string,p=0):
        self.line=line
        self.info=text
        self.string=string
        self.out(p)
        exit(1)
    def ie(self): pass
    def out(self,p):
        print(" В строке",str(self.line)+':',"\n "+self.string,"\n"+self.pos(p),'\n',self.name()+':',self.info)
    def name(self):
        return "Базовая ошибка"
    def pos(self,p):
        return ' '*(p+1)+"^"
class Ro_NameError(Ro_Error):
    def name(self):
        return 'Ошибка имени переменной'
class Ro_SintaxError(Ro_Error):
    def name(self):
        return 'Ошибка синтаксиса'
class data:
    def __init__(self):
        self.date=[]
    def __getitem__(self,i):
        return self.date[i]
    def names(self,b=0):
        return [a[1] for a in self.date]
    def ids(self):
        return [a[0] for a in self.date]
    def types(self):
        return [a[2] for a in self.date]
    def values(self):
        return [a[3] for a in self.date]  
    def value_re_with_name(self,n,v,l,s):
        i=0
        while i<len(self.date):
            if self.date[i][1]==n:
                self.date[i][3]=v
                return None
            i+=1
        Ro_NameError(l,"Нет имени "+n+'!',s,p=list(s).index(n))
    def value_re_with_id(self,i,v): pass
    def id_re_with_name(self,n,i): pass
    def name_re_with_id(self,i,n): pass
    def type_re_with_id(self,i,t): pass
    def type_re_with_name(self,n,t): pass
    def find_value_with_name(self,n,line,string):
        i=0
        while i<len(self.date):
            if self.date[i][1]==n:
                return self.date[i][3]
            i+=1
        Ro_NameError(line,"Нет имени "+n+'!',string,p=list(string.replace(n,'p')).index('p'))
    def add_object(self,obj):
        self.date+=[obj]
    def __str__(self):
        return str(self.date)
    
class Robin:
    def __init__(self,lang='RUS'):
        self.data=data()
        self.lang=lang
        self.idnumber=1
        if lang=="EN":
            self.new_object("True",'bool',True,None,None)
            self.new_object("False",'bool',False,None,None)
        if lang=='RUS':
            self.new_object("Истина",'bool',True,None,None)
            self.new_object("Ложь",'bool',False,None,None)
    def load(self,ert):
        self.eexece(ert)
    def eexece(self,code):
        code=code.replace(';','\n')
        self.exec(code)
    def error(self,e):
        e.out()
    def str_re(self,bex,l,s):
        stri=superindex(bex,'"')
        if len(stri)%2==1:
            Ro_SintaxError(l,'Неожиданный маркер "',s,pos=max(stri))
        for i in range(0,len(stri)//2,2):
            self.new_object("|"+'s'*self.idnumber,'str',"'"+bex[stri[i]+1:stri[i+1]:]+"'",l,s)
            bex=bex.replace(bex[stri[i]:stri[i+1]+1:],"|"+'s'*self.idnumber)
            self.idnumber+=1
        return bex
    def boolexex(self,bex,l,string):
        sc=string
        exc=bex
        stri=superindex(bex,'"')
        for c in list('.+-*/%1234567890>=<!'):
            try:
                exc=exc.replace(c," ")
            except: pass
        exc=exc.split()
        bex=bex.replace('не','not')
        bex=bex.replace('и','and')
        bex=bex.replace('или','or')
        for nm in exc:
            bex=bex.replace(nm,str(self.data.find_value_with_name(nm,l,sc)))
        return bex
    def exec(self,codepart,line=0,lines=None):
        codepartlist=list(codepart.split("\n"))
        i=line
        if(lines==None):
            lines=len(codepartlist)
        while i<lines:
            string=codepartlist[i]
            string=self.str_re(string,i+1,codepartlist[i])
            if ' ' in string:
                oper=string.split()[0]
                if oper=='строка':
                    try:
                        i=eval(boolexec(string.split()[1]))-2
                    except:
                        Ro_SintaxError(i+1,'Должно быть число',string)
                if oper=='печать':
                    #if True:
                    try:
                        print(eval(self.boolexex(string.split()[1],i+1,string)))
                    except: Ro_SintaxError(i+1,'',string) 
                if oper=='если':
                    n=string.index(':')
                    s1=string.index('(')
                    s2=string.index(')')
                    #if True:
                    try:
                        if(bool(eval(self.boolexex(string[s1+1:s2:],i+1,string)))):
                            strin=string[n+1::]
                            if ' ' in strin:
                                oper=strin.split()[0]
                                if oper=='строка':
                                    try:
                                        i=int(strin.split()[1])-2
                                    except:
                                        Ro_SintaxError(i+1,'Должно быть число',strin)
                                if oper=='печать':
                                    #if True:
                                    try:
                                        print(eval(self.boolexex(strin.split()[1],i+1,strin)))
                                    except:
                                        Ro_SintaxError(i+1,'',strin) 
                            if "=" in strin:
                                strlist=strin.split("=")
                                #if(True):
                                try:
                                    es=eval(self.boolexex(strlist[1],i+1,strin))
                                    self.new_object(strlist[0],'int',es,i+1,strin)
                                except: Ro_SintaxError(i+1,'',strin)
                    except:
                        Ro_SintaxError(i+1,'',string)
                i+=1
                continue
            if "=" in string:
                strlist=string.split("=")
                #if(True):
                try:
                    es=eval(self.boolexex(strlist[1],i+1,string))
                    if type(es)==type(''):
                        es="'"+es+"'"
                    self.new_object(strlist[0],str(type(es)),es,i+1,string)
                except: Ro_SintaxError(i+1,'',string)
            
            i+=1
    def new_object(self, name,typeo,value,line,string):
        if name in self.data.names():
            self.data.value_re_with_name(name,value,line,string)
            return None
        id_o=random.randint(0,1000000000000)
        id_o=str(id_o)
        id_o="0"*(13-len(id_o))+id_o
        self.data.add_object([id_o,name,typeo,value])
def exec_robin(code):
    robin_inter=Robin()
    robin_inter.load(code)
if(__name__=="__main__"):
    while True:
        try: exec_robin(input())
        except SystemExit: pass

