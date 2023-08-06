import random
def is_error(obj):
    try:
        obj.ie()
        return True
    except:
        return False
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
            i+=1
        Ro_NameError(l,"Нет имени "+n+'!',s,p=list(s).index(n))
    def value_re_with_id(self,i,v): pass
    def id_re_with_name(self,n,i): pass
    def name_re_with_id(self,i,n): pass
    def value_re_with_name(self,n,v): pass
    def type_re_with_id(self,i,t): pass
    def type_re_with_name(self,n,t): pass
    def find_value_with_name(self,n,line,string):
        i=0
        while i<len(self.date):
            if self.date[i][1]==n:
                return self.date[i][3]
            i+=1
        Ro_NameError(line,"Нет имени "+n+'!',string,p=list(string).index(n))
    def add_object(self,obj):
        self.date+=[obj]
    
class Robin:
    def __init__(self):
        self.data=data()
    def load(self,ert):
        self.eexece(ert)
    def eexece(self,code):
        self.exec(code)
    def error(self,e):
        e.out()
    def exex(self,ex,l,string):
        sc=string
        exc=ex
        for c in list('+-*/%1234567890'):
            try:
                exc=exc.replace(c," ")
            except: pass
        exc=exc.split()
        for nm in exc:
            ex=ex.replace(nm,str(self.data.find_value_with_name(nm,l,sc)))
        return ex
    def exec(self,codepart):
        codepartlist=list(codepart.split("\n"))
        i=0
        while i<len(codepartlist):
            if "=" in codepartlist[i]:
                string=codepartlist[i]
                strlist=string.split("=")
                #if(True):
                try:
                    es=eval(self.exex(strlist[1],i+1,string))
                    self.new_object(strlist[0],'int',es,i+1,string)
                except: Ro_SintaxError(i+1,'',string)
            if ' ' in codepartlist[i]:
                string=codepartlist[i]
                oper=string.split()[0]
                if oper=='строка':
                    try:
                        i=int(string[1])-1
                    except:
                        Ro_SintaxError(i+1,'Должно быть число',string)
                if oper=='печать':
                    if True:
                    #try:
                        print(eval(self.exex(string.split()[1],i+1,string)))
                    #except:
                        #Ro_SintaxError(i+1,'',string)
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
