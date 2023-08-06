import pickle
import re
def save_obj(obj, name ):
    with open('./resource/' + name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
def load_obj(name):
    with open('./resource/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)
PCA = load_obj("PCA")
PC = load_obj("PC")
PA = load_obj("PA")
CA = load_obj("CA")
P = load_obj("P")
C = load_obj("C")
A = load_obj("A")
PCA_re = load_obj("PCA_re")
PC_re = load_obj("PC_re")
PA_re = load_obj("PA_re")
CA_re = load_obj("CA_re")
P_re = load_obj("P_re")
C_re = load_obj("C_re")
A_re = load_obj("A_re")
def extract(sentence):
    res = []
    s = sentence
    #PCA---1 
    for i in re.finditer(PCA_re,s):
        first = s[:i.span()[1]]
        second = s[i.span()[1]:]
        entity = i.group()
        location = PCA[entity]
        first = re.sub(entity, "*"*len(entity), first)
        s = first + second
        res.append({
            "entity":entity,
            "loc_begin":int(i.span()[0]),
            "loc_end":int(i.span()[1]),
            "location":location,
            "status":'1'
        })
    #PC---2    
    for i in re.finditer(PC_re,s):
        first = s[:i.span()[1]]
        second = s[i.span()[1]:]
        entity = i.group()
        location = PC[entity]
        first = re.sub(entity, "*"*len(entity), first)
        s = first + second
        res.append({
            "entity":entity,
            "loc_begin":int(i.span()[0]),
            "loc_end":int(i.span()[1]),
            "location":location,
            "status":'2'
        })
    #PA---3 
    for i in re.finditer(PA_re,s):
        first = s[:i.span()[1]]
        second = s[i.span()[1]:]
        entity = i.group()
        location = PA[entity]
        first = re.sub(entity, "*"*len(entity), first)
        s = first + second
        res.append({
            "entity":entity,
            "loc_begin":int(i.span()[0]),
            "loc_end":int(i.span()[1]),
            "location":location,
            "status":'3'
        })
    #CA---4
    for i in re.finditer(CA_re,s):
        first = s[:i.span()[1]]
        second = s[i.span()[1]:]
        entity = i.group()
        location = CA[entity]
        first = re.sub(entity, "*"*len(entity), first)
        s = first + second
        res.append({
            "entity":entity,
            "loc_begin":int(i.span()[0]),
            "loc_end":int(i.span()[1]),
            "location":location,
            "status":'4'
        })
        
    #P---5
    for i in re.finditer(P_re,s):
        first = s[:i.span()[1]]
        second = s[i.span()[1]:]
        entity = i.group()
        location = P[entity]
        first = re.sub(entity, "*"*len(entity), first)
        s = first + second
        res.append({
            "entity":entity,
            "loc_begin":int(i.span()[0]),
            "loc_end":int(i.span()[1]),
            "location":location,
            "status":'5'
        })
    #C---6
    for i in re.finditer(C_re,s):
        entity = i.group()
        if str(entity) == "朝阳":
            continue
        first = s[:i.span()[1]]
        second = s[i.span()[1]:]
        location = C[entity]
        first = re.sub(entity, "*"*len(entity), first)
        s = first + second
        res.append({
            "entity":entity,
            "loc_begin":int(i.span()[0]),
            "loc_end":int(i.span()[1]),
            "location":location,
            "status":'6'
        })
    #A---7
    for i in re.finditer(A_re,s):
        first = s[:i.span()[1]]
        second = s[i.span()[1]:]
        entity = i.group()
        location = A[entity]
        first = re.sub(entity, "*"*len(entity), first)
        s = first + second
        res.append({
            "entity":entity,
            "loc_begin":int(i.span()[0]),
            "loc_end":int(i.span()[1]),
            "location":location[0],
            "status":'7'
        })
    res.sort(key = lambda x:x["loc_begin"])
    return res