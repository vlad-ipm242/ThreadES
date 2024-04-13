"""Машина логічного виведення для розширення Foam редактора VS Code.
Тріплети фактів бази знань (Subject, Property, Object) подаються як посилання, приблизно так, як це робиться в Semantic MediaWiki:
# Subject
[Property](Object.md)
де Subject - заголовок документу
"""

import os, re

def parse(filename, properties=[]):
    """Шукає усі посилання у файлі filename в форматі [property](object.md)
та додає в базу знань KB факт (filename, property, object)"""
    f=open(filename, "r")
    text=f.read()
    f.close()
    KB=set()
    for mo in re.finditer('\[(.*)\]\((.*\.md)\)', text):
        #print(mo.group(0))
        s=os.path.relpath(filename, path)
        p=mo.group(1)
        if p not in properties: continue
        o=mo.group(2)
        KB.add((s,p,o))
    return KB

def foam2KB(path, properties=[]):
    """Повертає множину фактів шляхом синтаксичного аналізу файлів .md каталогу path"""
    KB=set()
    for root, dirs, files in os.walk(path):
        for f in files:
            if os.path.splitext(f)[1]=='.md':
                #print(os.path.join(root, f))
                K=parse(os.path.join(root, f), properties)
                KB.update(K)
    return KB

def reasoner(KB, property='isCause'):
    """Найпростіша машина логічного виведення, для інверсної властивості property. Повертає множину виведених фактів"""
    K=set()
    for s,p,o in KB:
        if p==property:
            K.add((o,'isEffect',s))
    return K

def facts2foam(KB):
    """Дописує виведені факти в кінець відповідних файлів .md. Обережно!"""
    for s,p,o in KB:
        fn=os.path.join(path, s)
        f=open(fn, 'a')
        ref='\n['+p+']'+'('+o+')\n'
        f.write(ref)
        f.close()

def facts2mermaid(KB, properties=[]):
    """Створює у файлі .md Mermaid-граф з фактами KB. Граф може бути візуалізовано в VS Code, якщо установлені відповідні розширення"""
    tmp="""# Infered

```mermaid
graph TD;
%s
```
"""
    facts=""
    for s,p,o in KB:
        #print(s,p,o)
        if p not in properties: continue
        facts+="    "+s+"-->"+o+";\n"
    if not facts: return
    with open(os.path.join(path, 'Infered.md'), 'w') as f:
        f.write(tmp%facts)

if __name__=="__main__":
    path="c:\\FoamTest"
    KB=foam2KB(path, ['isCause', 'isEffect']) # отримати факти
    print(KB)
    K=reasoner(KB) # вивести нові факти
    print(K)
    #facts2foam({('1.md', 'isCause', '2.md')})
    facts2mermaid(K, properties=['isEffect']) # візуалізувати факти

    '''
    #Приклад використання зовнішньої машини виведення example3:
    import example3
    A=example3.reasoner(KB, [example3.rule1, example3.rule2], ('isCause',), ('isCause',))
    print(A)
    print(A-KB)
    '''