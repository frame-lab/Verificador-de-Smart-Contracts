import random
from program.converter_nuxmv.converter import MyNuxmvConverter

def make_blockchain(files, options):
    module = []
    converter = MyNuxmvConverter()
    if files:
        for file in files:
            module.append(converter.make_conversion(file, options))

    if options["autogen"]:
        random.seed(options['seeds'])
        if "nodes" in options:
            numNodes = random.randint(2, options["nodes"])
        else:
            numNodes = random.randint(2, 20)
    else:
        if "nodes" in options:
            top = max(options["nodes"], options["nodes_quantity"])
            numNodes = top
        else:
            numNodes = options["nodes_quantity"]

    nodes = []
    for i in range(1, numNodes+1):
        nodes.append("node{} : createNode({});".format(i, i))

    users = []
    if options["autogen"]:
        random.seed(options['seeds'])
        if "users" in options:
            numUsers = random.randint(2, options["users"])
        else:
            numUsers = random.randint(2, 25)
        for i in range(1, numUsers+1):
            if "balance" in options:
                balance = random.randint(0, options["balance"])
            else:
                balance = random.randint(0, 100)
            users.append("user{} : createUser(self,{});".format(i, balance))
    else:
        if "users" in options:
            top = max(options["users"], options["users_quantity"])
            numUsers = top
        else:
            numUsers = options["users_quantity"]
        if numUsers >= 2:
            file = options['balance_file']
            for i in range(1, numUsers+1):
                balance = int(file.readline())
                if 'balance' in options:
                    bottom = min(balance, options['balance'])
                    users.append(
                        "user{} : createUser(self,{});".format(i, bottom))
                else:
                    users.append(
                        "user{} : createUser(self,{});".format(i, balance))
            file.close()
        else:
            print("You must create at least 2 users")

    userList = []
    for i in range(1, numUsers+1):
        userList.append("user{}".format(i))

    transactions = []
    userTxns = dict()

    for i in range(1, len(users)+1):
        userTxns["user{}".format(i)] = []

    if options["autogen"]:
        random.seed(options['seeds'])
        if "transactions" in options:
            countTxn = random.randint(0, options["transactions"])
        else:
            countTxn = random.randint(2, 60)
        for i in range(1, countTxn+1):
            userTxn = []
            random.seed(options['seeds'])
            ufrom = random.choice(userList)
            random.seed(options['seeds'])
            uto = random.choice(userList)
            random.seed(options['seeds'])
            amount = random.randint(1, 20)
            transactions.append(
                "tx{} : createTransaction(self,{},{},{});".format(i, ufrom, uto, amount))
            if ufrom == uto:
                userTxns[ufrom].append("tx{}".format(i))
            else:
                userTxns[ufrom].append("tx{}".format(i))
                userTxns[uto].append("tx{}".format(i))
    else:
        file = options['transactions_file']
        countTxn = 1
        if options['program'] > 0:
            for line in file:
                lineArr = line.split(" ")
                ufrom = lineArr[0]
                uto = lineArr[1]
                amount = lineArr[2]
                program = lineArr[3]
                transactions.append("tx{} : createTransaction(self,{},{},{},{});".format(
                    countTxn, ufrom, uto, amount, program))
                countTxn += 1
        else:
            for line in file:
                lineArr = line.split(" ")
                ufrom = lineArr[0]
                uto = lineArr[1]
                amount = lineArr[2]
                transactions.append("tx{} : createTransaction(self,{},{},{});".format(
                    countTxn, ufrom, uto, amount))
                countTxn += 1
        file.close()

    txnList = []
    for i in range(1, countTxn+1):
        txnList.append("tx{}".format(i))

    blocks = []
    if options["autogen"]:
        random.seed(options['seeds'])
        if "block" in options:
            countBlock = random.randint(0, options["block"])
        else:
            countBlock = random.randint(1, int(countTxn/2))
        for i in range(1, countBlock+1):
            random.seed(options['seeds'])
            txa = random.choice(txnList)
            txnList.remove(txa)
            random.seed(options['seeds'])
            txb = random.choice(txnList)
            blocks.append(
                "block{} : createBlock({},{},{});".format(i, i, txa, txb))
    else:
        file = options['block_file']
        countBlock = 1
        for line in file:
            lineArr = line.split(" ")
            txa = lineArr[0]
            txb = lineArr[1]
            blocks.append("block{} : createBlock({},{},{});".format(
                countBlock, countBlock, txa, txb))
            countBlock += 1
        file.close()
    program = options['program']
    if program == 0:
        base = open("./program/blockchain/blockchain_model.smv", "r")
    else:
        base = open("./program/blockchain/blockchain_model_program.smv", "r")
    model = base.readlines()
    f = open("./results/blockchain.smv", "w+")
    f.writelines(module)
    f.writelines(model)
    base.close()
    f.write("MODULE main" + "\n\n\tVAR")
    for i in range(0, len(nodes)):
        f.write("\n\t\t" + nodes[i])
    f.write("\n")
    for j in range(0, len(users)):
        f.write("\n\t\t" + users[j])
    f.write("\n")
    for k in range(0, len(transactions)):
        f.write("\n\t\t" + transactions[k])
    f.write("\n")
    for s in range(0, len(blocks)):
        f.write("\n\t\t" + blocks[s])
    f.write("\n")
    f.write("\n\tASSIGN")
    for i in range(1, int((len(users)))):
        f.write("\n\t\tinit(user{}.busy) := TRUE;".format(i))
    f.write("\n")
    f.write("\n\tDEFINE")

    for i in range(1, len(users)+1):
        userTxn = userTxns["user{}".format(i)]
        string_update = "\n\t\tuser{}.update := ".format(i)
        if len(userTxn) != 0:
            for i in range(0, len(userTxn)):
                if i != len(userTxn) - 1:
                    string_update = string_update + \
                        (userTxn[i]+".validTransaction | ")
                else:
                    string_update = string_update + \
                        (userTxn[i]+".validTransaction;")
        else:
            string_update = string_update + "FALSE;"
        f.write(string_update)

    f.write("\n")
    f.write("\n\t\tblock1.previousBlock := block1.validBlock ? 0 : -1;")
    for i in range(2, len(blocks)+1):
        f.write("\n\t\tblock{}.previousBlock := case".format(i))
        f.write("\n\t\t\tblock{}.validBlock : case".format(i))
        j = i - 1
        while(j > 0):
            f.write(
                "\n\t\t\t\tblock{}.validBlock : block{}.id;".format(j, j))
            j = j - 1
        f.write("\n\t\t\t\tesac;")
        f.write("\n\t\t\tTRUE : -1;")
        f.write("\n\t\t\tesac;")

    f.close()
