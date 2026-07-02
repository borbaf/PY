alunos = [("Alice","2222-2222"), ("Bob","3333-3333"), ("Charlie","4444-4444")]
alunos2 = dict(alunos)
print(alunos2)    

alunos2["Lucas"] = "5555-5555"
print(alunos2)  

alunos2.pop("Alice")
print(alunos2)