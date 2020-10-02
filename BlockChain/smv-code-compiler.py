#!/usr/bin/env python
# coding: utf-8
 
import random
from random import seed
from random import choice
import datetime

print("--- Automatic blockchain SMV code generator. ---")
 
autoGen = input("Do you want to automatically generate a blockchain based on randomic parameters? (yes/no)")
 
 
 
if autoGen == "no":
    numNodes = int(input("How many nodes do you want in your P2P network?"))
else:
    seed(input("Type an integer number to be used as the seed of ramdomness: "))
    numNodes = 10 #random.randint(2,20)
 
 
nodes = []
for i in range(1,numNodes+1):
        nodes.append("node{} : createNode({});".format(i, i))      
 
 
#for i in range(0,len(nodes)):
   # print(nodes[i])
 
 
print("The {} requested nodes was sucessfully created.".format(len(nodes)))
print("You must create at least 2 users. The users are pairs like (id, balance).")
 
users = []
if autoGen == "no":
    numUsers = int(input("How many users do you want to create?"))
    if numUsers >= 2:
        for i in range(1,numUsers+1):
            balance = int(input("Please type the initial balance of the user{}:".format(i)))
            users.append("user{} : createUser(self,{});".format(i, balance))
    else:
        print("You must create at least 2 users")
else:
    numUsers = 30 #random.randint(2,25)
    for i in range(1,numUsers+1):
        balance = random.randint(0,100)
        users.append("user{} : createUser(self,{});".format(i, balance))
 
userList = []
for i in range(1, numUsers+1):
    userList.append("user{}".format(i))
#print(userList)
#for i in range(0,len(users)):
#    print(users[i])
 
 
print("Now you can create transactions. A transaction is a tuple like (from, to, balance)")
 
 
transactions = []
userTxns = dict()
 
for i in range(1,len(users)+1):
    userTxns["user{}".format(i)] = []
     
if autoGen == "no":
    anotherTxn = "yes"
    countTxn = 1
    while anotherTxn == "yes":
        ufrom = input("Please type the sender user:")
        uto = input("Please type the receiver user:")
        amount = int(input("Please type the amount transfered:"))
        transactions.append("tx{} : createTransaction(self,{},{},{});".format(countTxn,ufrom, uto, amount))
        anotherTxn = input("Do you want to create a new transaction? (yes/no)")
        if anotherTxn == "yes":
            countTxn += 1
else:
    countTxn = 17 #random.randint(2,60)
    for i in range(1,countTxn+1):
        userTxn = []
        ufrom = random.choice(userList)
        uto = random.choice(userList)
        amount = random.randint(1,20)
        transactions.append("tx{} : createTransaction(self,{},{},{});".format(i,ufrom, uto, amount))
        if ufrom == uto :
            userTxns[ufrom].append("tx{}".format(i))
        else:
            userTxns[ufrom].append("tx{}".format(i))
            userTxns[uto].append("tx{}".format(i))
 
print("{} transactions created.".format(countTxn))
#print(userTxns)
 
 
txnList = []
for i in range(1,countTxn+1):
    txnList.append("tx{}".format(i))
#for i in range(0, len(transactions)):
#    print(transactions[i])
 
 
print("Now it's time to create blocks")
 
 
blocks = []
if autoGen == "no":
    anotherBlock = "yes"
    countBlock = 1
    while anotherBlock == "yes":
        txa = input("Which transaction do you include in this block?")
        txb = input("Which other transaction do you include in this block?")
        blocks.append("block{} : createBlock({},{},{});".format(countBlock, countBlock,txa,txb))
        anotherBlock = input("Do you want to create a block? (yes/no)")
        if anotherBlock == "yes":
            countBlock += 1
else:
    countBlock = 6 #random.randint(1,int(countTxn/2))
    for i in range(1,countBlock+1):
        txa = random.choice(txnList)
        txnList.remove(txa)
        txb = random.choice(txnList)
        blocks.append("block{} : createBlock({},{},{});".format(i, i,txa,txb))
 
print("{} blocks created.".format(countBlock))
 
#for s in range(0,len(blocks)):
#    print(blocks[s])
 
print("")
print("The blockchain generated has the below parameters:")
print("--> {} nodes;".format(len(nodes)))
print("--> {} users;".format(len(users)))
print("--> {} transactions;".format(len(transactions)))
print("--> {} blocks;".format(len(blocks))) 
print("")
print("--- Copy all the below code and paste it at the end of the file blockchain.smv ---")
print("")
print("")
base = open("blockchain-model.smv", "r")
model = base.readlines()
f = open("blockchain.smv", "w+")
f.writelines(model)
f.write("MODULE main" + "\nVAR" + "\n")
("\n")
for i in range(0,len(nodes)):
    f.write("\n   " + nodes[i])
f.write("\n")
for j in range(0,len(users)):
    f.write("\n   " + users[j])
f.write("\n")
for k in range(0,len(transactions)):
    f.write("\n   " + transactions[k])
f.write("\n")    
for s in range(0,len(blocks)):
    f.write("\n   " + blocks[s])
f.write("\n")
f.write("\nASSIGN")
for i in range(1,int((len(users)))):
    f.write("\n init(user{}.busy) := TRUE;".format(i))
f.write("\n")
f.write("\nDEFINE")
 
for i in range(1,len(users)+1):
    userTxn = userTxns["user{}".format(i)]
    string_update = "\n   user{}.update := ".format(i)
    if len(userTxn) != 0:
        for i in range(0, len(userTxn)):
            if i != len(userTxn) - 1:
                string_update = string_update + (userTxn[i]+".validTransaction | ")
            else:
                string_update = string_update + (userTxn[i]+".validTransaction;")
    else:
        string_update = string_update + "FALSE;"
    f.write(string_update)
     
f.write("\n")
f.write("\nblock1.previousBlock := block1.validBlock ? 0 : -1;")
for i in range(2,len(blocks)+1):
    f.write("\nblock{}.previousBlock := case".format(i))
    f.write("\n                               block{}.validBlock : case".format(i))
    j = i - 1
    while(j > 0):
        f.write("\n                                                      block{}.validBlock : block{}.id;".format(j,j))
        j = j - 1
    f.write("\n                                                    esac;")
    f.write("\n                               TRUE : -1;")
    f.write("\n                            esac;")

f.close()
