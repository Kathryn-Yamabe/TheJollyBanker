from queue import Queue
import tree

class bank():
    def __init__(self, text):
        self.text = text
        self.q = Queue()

    def readFile(self):
        #open file command
        text = open(self.text)
        for line in text:
            file = line.split()
        
            #open account
            if file[0] == "O":
                openAccount = transaction((file[0]), (file[3]), (file[1]), (file[2]))
                self.q.put(openAccount)


            elif file[0] == "T": 
                #Transfer money to different accounts

                transfer = transaction((file[0]), eval(file[1][0:4]), eval(file[1][4]), (file[2]), eval(file[3][0:4]), eval(file[3][4]))
                self.q.put(transfer)
            #checks history of the file
            elif file[0] == "H":
                if len(file[1]) == 4:
                    historyCheck = transaction(file[0], eval(file[1][0:4]))
                else:
                    historyCheck = transaction(file[0], eval(file[1][0:4]), eval(file[1][4]))
                self.q.put(historyCheck)
            #deposits or withdraws
            else:
            
                depositWithdraw = transaction((file[0]), eval(file[1][0:4]), eval(file[1][4]), (file[2]))
                self.q.put(depositWithdraw)

    def executeFile(self):
        #open accounts
        o = self.q.get()
        #open accounts
        if(o.getType() == "O"):
            c = client(o.getAmount(), o.getFund(), o.getAccount())
            ct = tree.BinarySearchTree()
            ct[int(o.getAccount())] = c

        while(self.q.empty() == False):
            trans = self.q.get()
            if(trans.getType() == "O"):
                c = client(trans.getAmount(), trans.getFund(), trans.getAccount())
                if ct.get(int(c.getID())) == None:
                    ct[int(trans.getAccount())] = c
                else:
                    print("ERROR: Account " + str(trans.getAccount()) + " is already open. Transaction denied.")
            #Transfer
            if(trans.getType() == "T"):
                #check which client
                #if the transaction account number does not match the client ID
                if(trans.getAccount() != int(c.getID())):
                    #we then set the new client to the ID of the transaction
                    c = ct[trans.getAccount()]
                    if c == None:
                        print("ERROR: Account " + str(trans.getAccount()) + " not found. Transfer refused")
                    elif trans.getFund() == 0:
                    #checks if there is enough money in the chosen fund
                        if int(trans.getAmount()) > c.moneyMarket.totalMoney:
                        #if not enough money an error message prints and the withdraw does not happen
                        #still adds to history but not added to the total amount
                            if int(trans.getAmount()) - c.moneyMarket.totalMoney > c.primeMoneyMarket.totalMoney:
                                c.moneyMarket.history.append("Withdraw for: " + (str(trans.amount)) + " (FAILED)")
                                print("ERROR: Not enough funds to withdraw " + str(trans.getAmount()) + " from " + c.getName() + " " + c.moneyMarket.fundName)
                            else:
                                mm = int(trans.getAmount()) - int(c.moneyMarket.totalMoney)
                                nn = int(trans.getAmount()) - mm
                                c.moneyMarket.treduceMoney(str(nn))
                                c.primeMoneyMarket.treduceMoney(str(mm))
                                c.moneyMarket.history.append("Over withdraw for: " + (str(trans.amount)) + "\n    Money Market insuficent funds. Using funds from Prime Money Market. Remaining balance: " + str(mm))
                                c.primeMoneyMarket.history.append("Insificient funds in Money Market. Remaining withdrawn from Prime Money Market: " + str(mm))

                        else:
                            c.moneyMarket.treduceMoney(trans.getAmount())
                    elif trans.getFund() == 1:
                        if int(trans.getAmount()) > c.primeMoneyMarket.totalMoney:
                            if int(trans.getAmount()) - c.primeMoneyMarket.totalMoney > c.moneyMarket.totalMoney:
                                c.primeMoneyMarket.history.append("Withdraw for: " + (str(trans.amount)) + " (FAILED)")
                                print("ERROR: Not enough funds to withdraw " + str(trans.getAmount()) + " from " + c.getName() + " " + c.primeMoneyMarket.fundName)
                            else:
                                mm = int(trans.getAmount()) - int(c.primeMoneyMarket.totalMoney)
                                nn = int(trans.getAmount()) - mm
                                c.primeMoneyMarket.treduceMoney(str(nn))
                                c.moneyMarket.treduceMoney(str(mm))
                                c.primeMoneyMarket.history.append("Over withdraw for: " + (str(trans.amount)) + "\n    Prime Money Market insuficent funds. Using funds from Money Market. Remaining balance: " + str(mm))
                                c.moneyMarket.history.append("Insificient funds in Prime Money Market. Remaining withdrawn from Money Market: " + str(mm))
                        
                        else:
                            c.primeMoneyMarket.treduceMoney(trans.getAmount())
                    elif trans.getFund() == 2:
                        if int(trans.getAmount()) > c.longTermBond.totalMoney:
                            if int(trans.getAmount()) - c.shortTermBond.totalMoney > c.longTermBond.totalMoney:
                                c.longTermBond.history.append("Withdraw for: " + (str(trans.amount)) + " (FAILED)")
                                print("ERROR: Not enough funds to withdraw " + str(trans.getAmount()) + " from " + c.getName() + " " + c.longTermBond.fundName)
                            else:
                                mm = int(trans.getAmount()) - int(c.longTermBond.totalMoney)
                                nn = int(trans.getAmount()) - mm
                                c.longTermBond.treduceMoney(str(nn))
                                c.shortTermBond.treduceMoney(str(mm))
                                c.longTermBond.history.append("Withdraw for: " + (str(trans.amount)) + "\n    Long Term Bond insuficent funds. Using funds from Money Market. Remaining balance: " + str(mm))
                                c.shortTermBond.history.append("Insificient funds in Long Term Bond. Remaining withdrawn from Short Term Bond: " + str(mm))

                        
                        else:
                            c.longTermBond.treduceMoney(trans.getAmount())
                    elif trans.getFund() == 3:
                        if int(trans.getAmount()) > shortTermBond.totalMoney:
                            if int(trans.getAmount()) - c.primeMoneyMarket.totalMoney > c.moneyMarket.totalMoney:
                                c.shortTermBond.history.append("Withdraw for: " + (str(trans.amount)) + " (FAILED)")
                                print("ERROR: Not enough funds to withdraw " + str(trans.getAmount()) + " from " + c.getName() + " " + c.shortTermBond.fundName)
                            else:
                                mm = int(trans.getAmount()) - int(c.shortTermBond.totalMoney)
                                nn = int(trans.getAmount()) - mm
                                c.shortTermBond.treduceMoney(str(nn))
                                c.longTermBond.treduceMoney(str(mm))
                                c.shortTermBond.history.append("Over withdraw for: " + (str(trans.amount)) + "\n    Short Term Bond insuficent funds. Using funds from Long Term Bond. Remaining balance: " + str(mm))
                                c.longTermBond.history.append("Insificient funds in Short Term Bond. Remaining withdrawn from Long Term Bond: " + str(mm))
                        
                        else:
                            c.shortTermBond.treduceMoney(trans.getAmount())
                    elif trans.getFund() == 4:
                        if int(trans.getAmount()) > c.fiveHundredIndexFund.totalMoney:
                            c.fiveHundredIndexFund.history.append("Withdraw for: " + (str(trans.amount)) + " (FAILED)")
                            print("ERROR: Not enough funds to withdraw " + str(trans.getAmount()) + " from " + c.getName() + " " + c.fiveHundredIndexFund.fundName)
                        else:
                            c.fiveHundredIndexFund.treduceMoney(trans.getAmount())
                    elif trans.getFund() == 5:
                        if int(trans.getAmount()) > c.capitalValueFund.totalMoney:
                            c.capitalValueFund.history.append("Withdraw for: " + (str(trans.amount)) + " (FAILED)")
                            print("ERROR: Not enough funds to withdraw " + str(trans.getAmount()) + " from " + c.getName() + " " + c.capitalValueFund.fundName)
                        else:
                            c.capitalValueFund.treduceMoney(trans.getAmount())
                    elif trans.getFund() == 6:
                        if int(trans.getAmount()) > c.growthEquityFund.totalMoney:
                            c.growthEquityFund.history.append("Withdraw for: " + (str(trans.amount)) + " (FAILED)")
                            print("ERROR: Not enough funds to withdraw " + str(trans.getAmount()) + " from " + c.getName() + " " + c.growthEquityFund.fundName)
                        else:
                            c.growthEquityFund.treduceMoney(trans.getAmount())
                    elif trans.getFund() == 7:
                        if int(trans.getAmount()) > c.growthIndexFund.totalMoney:
                            c.growthIndexFund.history.append("Withdraw for: " + (str(trans.amount)) + " (FAILED)")
                            print("ERROR: Not enough funds to withdraw " + str(trans.getAmount()) + " from " + c.getName() + " " + c.growthIndexFund.fundName)
                        else:
                            c.growthIndexFund.treduceMoney(trans.getAmount())
                    elif trans.getFund() == 8:
                        if int(trans.getAmount()) > c.valueFund.totalMoney:
                            c.valueFund.history.append("Withdraw for: " + (str(trans.amount)) + " (FAILED)")
                            print("ERROR: Not enough funds to withdraw " + str(trans.getAmount()) + " from " + c.getName() + " " + c.valueFund.fundName)
                        else:
                            c.valueFund.treduceMoney(trans.getAmount())
                    elif trans.getFund() == 9:
                        if int(trans.getAmount()) > c.valueStockIndex.totalMoney:
                            c.valueStockIndex.history.append("Withdraw for: " + (str(trans.amount)) + " (FAILED)")
                            print("ERROR: Not enough funds to withdraw " + str(trans.getAmount()) + " from " + c.getName() + " " + c.valueStockIndex.fundName)
                        else:
                            c.valueStockIndex.treduceMoney(trans.getAmount())
                else:
                    if trans.getFund() == 0:
                    #checks if there is enough money in the chosen fund
                        if int(trans.getAmount()) > c.moneyMarket.totalMoney:
                        #if not enough money an error message prints and the withdraw does not happen
                        #still adds to history but not added to the total amount
                            if int(trans.getAmount()) - c.moneyMarket.totalMoney > c.primeMoneyMarket.totalMoney:
                                c.moneyMarket.history.append("Withdraw for: " + (str(trans.amount)) + " (FAILED)")
                                print("ERROR: Not enough funds to withdraw " + str(trans.getAmount()) + " from " + c.getName() + " " + c.moneyMarket.fundName)
                            else:
                                mm = int(trans.getAmount()) - int(c.moneyMarket.totalMoney)
                                nn = int(trans.getAmount()) - mm
                                c.moneyMarket.treduceMoney(str(nn))
                                c.primeMoneyMarket.treduceMoney(str(mm))
                                c.moneyMarket.history.append("Over withdraw for: " + (str(trans.amount)) + "\n    Money Market insuficent funds. Using funds from Prime Money Market. Remaining balance: " + str(mm))
                                c.primeMoneyMarket.history.append("Insificient funds in Money Market. Remaining withdrawn from Prime Money Market: " + str(mm))

                        else:
                            c.moneyMarket.treduceMoney(trans.getAmount())
                    elif trans.getFund() == 1:
                        if int(trans.getAmount()) > c.primeMoneyMarket.totalMoney:
                            if int(trans.getAmount()) - c.primeMoneyMarket.totalMoney > c.moneyMarket.totalMoney:
                                c.primeMoneyMarket.history.append("Withdraw for: " + (str(trans.amount)) + " (FAILED)")
                                print("ERROR: Not enough funds to withdraw " + str(trans.getAmount()) + " from " + c.getName() + " " + c.primeMoneyMarket.fundName)
                            else:
                                mm = int(trans.getAmount()) - int(c.primeMoneyMarket.totalMoney)
                                nn = int(trans.getAmount()) - mm
                                c.primeMoneyMarket.treduceMoney(str(nn))
                                c.moneyMarket.treduceMoney(str(mm))
                                c.primeMoneyMarket.history.append("Over withdraw for: " + (str(trans.amount)) + "\n    Prime Money Market insuficent funds. Using funds from Money Market. Remaining balance: " + str(mm))
                                c.moneyMarket.history.append("Insificient funds in Prime Money Market. Remaining withdrawn from Money Market: " + str(mm))
                        
                        else:
                            c.primeMoneyMarket.treduceMoney(trans.getAmount())
                    elif trans.getFund() == 2:
                        if int(trans.getAmount()) > c.longTermBond.totalMoney:
                            if int(trans.getAmount()) - c.shortTermBond.totalMoney > c.longTermBond.totalMoney:
                                c.longTermBond.history.append("Withdraw for: " + (str(trans.amount)) + " (FAILED)")
                                print("ERROR: Not enough funds to withdraw " + str(trans.getAmount()) + " from " + c.getName() + " " + c.longTermBond.fundName)
                            else:
                                mm = int(trans.getAmount()) - int(c.longTermBond.totalMoney)
                                nn = int(trans.getAmount()) - mm
                                c.longTermBond.treduceMoney(str(nn))
                                c.shortTermBond.treduceMoney(str(mm))
                                c.longTermBond.history.append("Over withdraw for: " + (str(trans.amount)) + "\n    Long Term Bond insuficent funds. Using funds from Money Market. Remaining balance: " + str(mm))
                                c.shortTermBond.history.append("Insificient funds in Long Term Bond. Remaining withdrawn from Short Term Bond: " + str(mm))

                        
                        else:
                            c.longTermBond.treduceMoney(trans.getAmount())
                    elif trans.getFund() == 3:
                        if int(trans.getAmount()) > shortTermBond.totalMoney:
                            if int(trans.getAmount()) - c.primeMoneyMarket.totalMoney > c.moneyMarket.totalMoney:
                                c.shortTermBond.history.append("Withdraw for: " + (str(trans.amount)) + " (FAILED)")
                                print("ERROR: Not enough funds to withdraw " + str(trans.getAmount()) + " from " + c.getName() + " " + c.shortTermBond.fundName)
                            else:
                                mm = int(trans.getAmount()) - int(c.shortTermBond.totalMoney)
                                nn = int(trans.getAmount()) - mm
                                c.shortTermBond.treduceMoney(str(nn))
                                c.longTermBond.treduceMoney(str(mm))
                                c.shortTermBond.history.append("Over withdraw for: " + (str(trans.amount)) + "\n    Short Term Bond insuficent funds. Using funds from Long Term Bond. Remaining balance: " + str(mm))
                                c.longTermBond.history.append("Insificient funds in Short Term Bond. Remaining withdrawn from Long Term Bond: " + str(mm))
                        
                        else:
                            c.shortTermBond.treduceMoney(trans.getAmount())
                    elif trans.getFund() == 4:
                        if int(trans.getAmount()) > c.fiveHundredIndexFund.totalMoney:
                            c.fiveHundredIndexFund.history.append("Withdraw for: " + (str(trans.amount)) + " (FAILED)")
                            print("ERROR: Not enough funds to withdraw " + str(trans.getAmount()) + " from " + c.getName() + " " + c.fiveHundredIndexFund.fundName)
                        else:
                            c.fiveHundredIndexFund.treduceMoney(trans.getAmount())
                    elif trans.getFund() == 5:
                        if int(trans.getAmount()) > c.capitalValueFund.totalMoney:
                            c.capitalValueFund.history.append("Withdraw for: " + (str(trans.amount)) + " (FAILED)")
                            print("ERROR: Not enough funds to withdraw " + str(trans.getAmount()) + " from " + c.getName() + " " + c.capitalValueFund.fundName)
                        else:
                            c.capitalValueFund.treduceMoney(trans.getAmount())
                    elif trans.getFund() == 6:
                        if int(trans.getAmount()) > c.growthEquityFund.totalMoney:
                            c.growthEquityFund.history.append("Withdraw for: " + (str(trans.amount)) + " (FAILED)")
                            print("ERROR: Not enough funds to withdraw " + str(trans.getAmount()) + " from " + c.getName() + " " + c.growthEquityFund.fundName)
                        else:
                            c.growthEquityFund.treduceMoney(trans.getAmount())
                    elif trans.getFund() == 7:
                        if int(trans.getAmount()) > c.growthIndexFund.totalMoney:
                            c.growthIndexFund.history.append("Withdraw for: " + (str(trans.amount)) + " (FAILED)")
                            print("ERROR: Not enough funds to withdraw " + str(trans.getAmount()) + " from " + c.getName() + " " + c.growthIndexFund.fundName)
                        else:
                            c.growthIndexFund.treduceMoney(trans.getAmount())
                    elif trans.getFund() == 8:
                        if int(trans.getAmount()) > c.valueFund.totalMoney:
                            c.valueFund.history.append("Withdraw for: " + (str(trans.amount)) + " (FAILED)")
                            print("ERROR: Not enough funds to withdraw " + str(trans.getAmount()) + " from " + c.getName() + " " + c.valueFund.fundName)
                        else:
                            c.valueFund.treduceMoney(trans.getAmount())
                    elif trans.getFund() == 9:
                        if int(trans.getAmount()) > c.valueStockIndex.totalMoney:
                            c.valueStockIndex.history.append("Withdraw for: " + (str(trans.amount)) + " (FAILED)")
                            print("ERROR: Not enough funds to withdraw " + str(trans.getAmount()) + " from " + c.getName() + " " + c.valueStockIndex.fundName)
                        else:
                            c.valueStockIndex.treduceMoney(trans.getAmount())



                #print("")



                 #check which client
                #if the transaction account number does not match the client ID
                if(trans.getToAccount() != int(c.getID())):
                    #we then set the new client to the ID of the transaction
                    c = ct[trans.getToAccount()]
                    if c == None:
                        print("ERROR: Account " + str(trans.getToAccount()) + " not found. Transfer denied")
                    #checks which fund
                    elif trans.getToFund() == 0:
                        c.moneyMarket.taddMoney(trans.getAmount())
                    elif trans.getToFund() == 1:
                        c.primeMoneyMarket.taddMoney(trans.getAmount())
                    elif trans.getToFund() == 2:
                        c.longTermBond.taddMoney(trans.getAmount())
                    elif trans.getToFund() == 3:
                        c.shortTermBond.taddMoney(trans.getAmount())
                    elif trans.getToFund() == 4:
                        c.fiveHundredIndexFund.taddMoney(trans.getAmount())
                    elif trans.getToFund() == 5:
                        c.capitalValueFund.taddMoney(trans.getAmount())
                    elif trans.getToFund() == 6:
                        c.growthEquityFund.taddMoney(trans.getAmount())
                    elif trans.getToFund() == 7:
                        c.growthIndexFund.taddMoney(trans.getAmount())
                    elif trans.getToFund() == 8:
                        c.valueFund.taddMoney(trans.getAmount())
                    elif trans.getToFund() == 9:
                        c.valueStockIndex.taddMoney(trans.getAmount())
                #otherwise the transaction can carry on as normal
                else:

                    #checks which fund
                    if c == None:
                        print("ERROR: Account " + str(trans.getToAccount()) + " not found. Withdrawl refused")
                    elif trans.getToFund() == 0:
                        c.moneyMarket.taddMoney(trans.getAmount())
                    elif trans.getToFund() == 1:
                        c.primeMoneyMarket.taddMoney(trans.getAmount())
                    elif trans.getToFund() == 2:
                        c.longTermBond.taddMoney(trans.getAmount())
                    elif trans.getToFund() == 3:
                        c.shortTermBond.taddMoney(trans.getAmount())
                    elif trans.getToFund() == 4:
                        c.fiveHundredIndexFund.taddMoney(trans.getAmount())
                    elif trans.getToFund() == 5:
                        c.capitalValueFund.taddMoney(trans.getAmount())
                    elif trans.getToFund() == 6:
                        c.growthEquityFund.taddMoney(trans.getAmount())
                    elif trans.getToFund() == 7:
                        c.growthIndexFund.taddMoney(trans.getAmount())
                    elif trans.getToFund() == 8:
                        c.valueFund.taddMoney(trans.getAmount())
                    elif trans.getToFund() == 9:
                        c.valueStockIndex.taddMoney(trans.getAmount())

            elif(trans.getType() == "H"):
                c = ct[trans.getAccount()]
                if c == None:
                        print("ERROR: Account " + str(trans.getAccount()) + " not found. History print denied")
                elif trans.getFund() == -1:
                    c.printAllHistory()
                elif trans.getFund() == 1:
                    c.primeMoneyMarket.printHistory()
                elif trans.getFund() == 2:
                    c.longTermBond.printHistory()
                elif trans.getFund() == 3:
                    c.shortTermBond.printHistory()
                elif trans.getFund() == 4:
                    c.fiveHundredIndexFund.printHistory()
                elif trans.getFund() == 5:
                    c.capitalValueFund.printHistory()
                elif trans.getFund() == 6:
                    c.growthEquityFund.printHistory()
                elif trans.getFund() == 7:
                    c.growthIndexFund.printHistory()
                elif trans.getFund() == 8:
                    c.valueFund.printHistory()
                elif trans.getFund() == 9:
                    c.valueStockIndex.printHistory()
                elif trans.getFund() == 0:
                    c.moneyMarket.printHistory()
            #Deposit
            elif(trans.getType() == "D"):
                #check which client
                #if the transaction account number does not match the client ID
                if(trans.getAccount() != int(c.getID())):
                    #we then set the new client to the ID of the transaction
                    c = ct[trans.getAccount()]
                    if c == None:
                        print("ERROR: Account " + str(trans.getAccount()) + " not found. Deposit refused")
                    #checks which fund
                    elif trans.getFund() == 0:
                        c.moneyMarket.addMoney(trans.getAmount())
                    elif trans.getFund() == 1:
                        c.primeMoneyMarket.addMoney(trans.getAmount())
                    elif trans.getFund() == 2:
                        c.longTermBond.addMoney(trans.getAmount())
                    elif trans.getFund() == 3:
                        c.shortTermBond.addMoney(trans.getAmount())
                    elif trans.getFund() == 4:
                        c.fiveHundredIndexFund.addMoney(trans.getAmount())
                    elif trans.getFund() == 5:
                        c.capitalValueFund.addMoney(trans.getAmount())
                    elif trans.getFund() == 6:
                        c.growthEquityFund.addMoney(trans.getAmount())
                    elif trans.getFund() == 7:
                        c.growthIndexFund.addMoney(trans.getAmount())
                    elif trans.getFund() == 8:
                        c.valueFund.addMoney(trans.getAmount())
                    elif trans.getFund() == 9:
                        c.valueStockIndex.addMoney(trans.getAmount())
                #otherwise the transaction can carry on as normal
                else:

                    #checks which fund
                    if c == None:
                        print("ERROR: Account " + str(trans.getAccount()) + " not found. Withdrawl refused")
                    elif trans.getFund() == 0:
                        c.moneyMarket.addMoney(trans.getAmount())
                    elif trans.getFund() == 1:
                        c.primeMoneyMarket.addMoney(trans.getAmount())
                    elif trans.getFund() == 2:
                        c.longTermBond.addMoney(trans.getAmount())
                    elif trans.getFund() == 3:
                        c.shortTermBond.addMoney(trans.getAmount())
                    elif trans.getFund() == 4:
                        c.fiveHundredIndexFund.addMoney(trans.getAmount())
                    elif trans.getFund() == 5:
                        c.capitalValueFund.addMoney(trans.getAmount())
                    elif trans.getFund() == 6:
                        c.growthEquityFund.addMoney(trans.getAmount())
                    elif trans.getFund() == 7:
                        c.growthIndexFund.addMoney(trans.getAmount())
                    elif trans.getFund() == 8:
                        c.valueFund.addMoney(trans.getAmount())
                    elif trans.getFund() == 9:
                        c.valueStockIndex.addMoney(trans.getAmount())
            #withdraw
            elif(trans.getType() == "W"):
                #check which client
                #if the transaction account number does not match the client ID
                if(trans.getAccount() != int(c.getID())):
                    #we then set the new client to the ID of the transaction
                    c = ct[trans.getAccount()]
                    if c == None:
                        print("ERROR: Account " + str(trans.getAccount()) + " not found. Withdrawl refused")
                    elif trans.getFund() == 0:
                    #checks if there is enough money in the chosen fund
                        if int(trans.getAmount()) > c.moneyMarket.totalMoney:
                        #if not enough money an error message prints and the withdraw does not happen
                        #still adds to history but not added to the total amount
                            if int(trans.getAmount()) - c.moneyMarket.totalMoney > c.primeMoneyMarket.totalMoney:
                                c.moneyMarket.history.append("Withdraw for: " + (str(trans.amount)) + " (FAILED)")
                                print("ERROR: Not enough funds to withdraw " + str(trans.getAmount()) + " from " + c.getName() + " " + c.moneyMarket.fundName)
                            else:
                                mm = int(trans.getAmount()) - int(c.moneyMarket.totalMoney)
                                nn = int(trans.getAmount()) - mm
                                c.moneyMarket.reduceMoney(str(nn))
                                c.primeMoneyMarket.reduceMoney(str(mm))
                                c.moneyMarket.history.append("Over withdraw for: " + (str(trans.amount)) + "\n    Money Market insuficent funds. Using funds from Prime Money Market. Remaining balance: " + str(mm))
                                c.primeMoneyMarket.history.append("Insificient funds in Money Market. Remaining withdrawn from Prime Money Market: " + str(mm))

                        else:
                            c.moneyMarket.reduceMoney(trans.getAmount())
                    elif trans.getFund() == 1:
                        if int(trans.getAmount()) > c.primeMoneyMarket.totalMoney:
                            if int(trans.getAmount()) - c.primeMoneyMarket.totalMoney > c.moneyMarket.totalMoney:
                                c.primeMoneyMarket.history.append("Withdraw for: " + (str(trans.amount)) + " (FAILED)")
                                print("ERROR: Not enough funds to withdraw " + str(trans.getAmount()) + " from " + c.getName() + " " + c.primeMoneyMarket.fundName)
                            else:
                                mm = int(trans.getAmount()) - int(c.primeMoneyMarket.totalMoney)
                                nn = int(trans.getAmount()) - mm
                                c.primeMoneyMarket.reduceMoney(str(nn))
                                c.moneyMarket.reduceMoney(str(mm))
                                c.primeMoneyMarket.history.append("Over withdraw for: " + (str(trans.amount)) + "\n    Prime Money Market insuficent funds. Using funds from Money Market. Remaining balance: " + str(mm))
                                c.moneyMarket.history.append("Insificient funds in Prime Money Market. Remaining withdrawn from Money Market: " + str(mm))
                        
                        else:
                            c.primeMoneyMarket.reduceMoney(trans.getAmount())
                    elif trans.getFund() == 2:
                        if int(trans.getAmount()) > c.longTermBond.totalMoney:
                            if int(trans.getAmount()) - c.shortTermBond.totalMoney > c.longTermBond.totalMoney:
                                c.longTermBond.history.append("Withdraw for: " + (str(trans.amount)) + " (FAILED)")
                                print("ERROR: Not enough funds to withdraw " + str(trans.getAmount()) + " from " + c.getName() + " " + c.longTermBond.fundName)
                            else:
                                mm = int(trans.getAmount()) - int(c.longTermBond.totalMoney)
                                nn = int(trans.getAmount()) - mm
                                c.longTermBond.reduceMoney(str(nn))
                                c.shortTermBond.reduceMoney(str(mm))
                                c.longTermBond.history.append("Withdraw for: " + (str(trans.amount)) + "\n    Long Term Bond insuficent funds. Using funds from Money Market. Remaining balance: " + str(mm))
                                c.shortTermBond.history.append("Insificient funds in Long Term Bond. Remaining withdrawn from Short Term Bond: " + str(mm))

                        
                        else:
                            c.longTermBond.reduceMoney(trans.getAmount())
                    elif trans.getFund() == 3:
                        if int(trans.getAmount()) > shortTermBond.totalMoney:
                            if int(trans.getAmount()) - c.primeMoneyMarket.totalMoney > c.moneyMarket.totalMoney:
                                c.shortTermBond.history.append("Withdraw for: " + (str(trans.amount)) + " (FAILED)")
                                print("ERROR: Not enough funds to withdraw " + str(trans.getAmount()) + " from " + c.getName() + " " + c.shortTermBond.fundName)
                            else:
                                mm = int(trans.getAmount()) - int(c.shortTermBond.totalMoney)
                                nn = int(trans.getAmount()) - mm
                                c.shortTermBond.reduceMoney(str(nn))
                                c.longTermBond.reduceMoney(str(mm))
                                c.shortTermBond.history.append("Over withdraw for: " + (str(trans.amount)) + "\n    Short Term Bond insuficent funds. Using funds from Long Term Bond. Remaining balance: " + str(mm))
                                c.longTermBond.history.append("Insificient funds in Short Term Bond. Remaining withdrawn from Long Term Bond: " + str(mm))
                        
                        else:
                            c.shortTermBond.reduceMoney(trans.getAmount())
                    elif trans.getFund() == 4:
                        if int(trans.getAmount()) > c.fiveHundredIndexFund.totalMoney:
                            c.fiveHundredIndexFund.history.append("Withdraw for: " + (str(trans.amount)) + " (FAILED)")
                            print("ERROR: Not enough funds to withdraw " + str(trans.getAmount()) + " from " + c.getName() + " " + c.fiveHundredIndexFund.fundName)
                        else:
                            c.fiveHundredIndexFund.reduceMoney(trans.getAmount())
                    elif trans.getFund() == 5:
                        if int(trans.getAmount()) > c.capitalValueFund.totalMoney:
                            c.capitalValueFund.history.append("Withdraw for: " + (str(trans.amount)) + " (FAILED)")
                            print("ERROR: Not enough funds to withdraw " + str(trans.getAmount()) + " from " + c.getName() + " " + c.capitalValueFund.fundName)
                        else:
                            c.capitalValueFund.reduceMoney(trans.getAmount())
                    elif trans.getFund() == 6:
                        if int(trans.getAmount()) > c.growthEquityFund.totalMoney:
                            c.growthEquityFund.history.append("Withdraw for: " + (str(trans.amount)) + " (FAILED)")
                            print("ERROR: Not enough funds to withdraw " + str(trans.getAmount()) + " from " + c.getName() + " " + c.growthEquityFund.fundName)
                        else:
                            c.growthEquityFund.reduceMoney(trans.getAmount())
                    elif trans.getFund() == 7:
                        if int(trans.getAmount()) > c.growthIndexFund.totalMoney:
                            c.growthIndexFund.history.append("Withdraw for: " + (str(trans.amount)) + " (FAILED)")
                            print("ERROR: Not enough funds to withdraw " + str(trans.getAmount()) + " from " + c.getName() + " " + c.growthIndexFund.fundName)
                        else:
                            c.growthIndexFund.reduceMoney(trans.getAmount())
                    elif trans.getFund() == 8:
                        if int(trans.getAmount()) > c.valueFund.totalMoney:
                            c.valueFund.history.append("Withdraw for: " + (str(trans.amount)) + " (FAILED)")
                            print("ERROR: Not enough funds to withdraw " + str(trans.getAmount()) + " from " + c.getName() + " " + c.valueFund.fundName)
                        else:
                            c.valueFund.reduceMoney(trans.getAmount())
                    elif trans.getFund() == 9:
                        if int(trans.getAmount()) > c.valueStockIndex.totalMoney:
                            c.valueStockIndex.history.append("Withdraw for: " + (str(trans.amount)) + " (FAILED)")
                            print("ERROR: Not enough funds to withdraw " + str(trans.getAmount()) + " from " + c.getName() + " " + c.valueStockIndex.fundName)
                        else:
                            c.valueStockIndex.reduceMoney(trans.getAmount())
                else:
                    if trans.getFund() == 0:
                    #checks if there is enough money in the chosen fund
                        if int(trans.getAmount()) > c.moneyMarket.totalMoney:
                        #if not enough money an error message prints and the withdraw does not happen
                        #still adds to history but not added to the total amount
                            if int(trans.getAmount()) - c.moneyMarket.totalMoney > c.primeMoneyMarket.totalMoney:
                                c.moneyMarket.history.append("Withdraw for: " + (str(trans.amount)) + " (FAILED)")
                                print("ERROR: Not enough funds to withdraw " + str(trans.getAmount()) + " from " + c.getName() + " " + c.moneyMarket.fundName)
                            else:
                                mm = int(trans.getAmount()) - int(c.moneyMarket.totalMoney)
                                nn = int(trans.getAmount()) - mm
                                c.moneyMarket.reduceMoney(str(nn))
                                c.primeMoneyMarket.reduceMoney(str(mm))
                                c.moneyMarket.history.append("Over withdraw for: " + (str(trans.amount)) + "\n    Money Market insuficent funds. Using funds from Prime Money Market. Remaining balance: " + str(mm))
                                c.primeMoneyMarket.history.append("Insificient funds in Money Market. Remaining withdrawn from Prime Money Market: " + str(mm))

                        else:
                            c.moneyMarket.reduceMoney(trans.getAmount())
                    elif trans.getFund() == 1:
                        if int(trans.getAmount()) > c.primeMoneyMarket.totalMoney:
                            if int(trans.getAmount()) - c.primeMoneyMarket.totalMoney > c.moneyMarket.totalMoney:
                                c.primeMoneyMarket.history.append("Withdraw for: " + (str(trans.amount)) + " (FAILED)")
                                print("ERROR: Not enough funds to withdraw " + str(trans.getAmount()) + " from " + c.getName() + " " + c.primeMoneyMarket.fundName)
                            else:
                                mm = int(trans.getAmount()) - int(c.primeMoneyMarket.totalMoney)
                                nn = int(trans.getAmount()) - mm
                                c.primeMoneyMarket.reduceMoney(str(nn))
                                c.moneyMarket.reduceMoney(str(mm))
                                c.primeMoneyMarket.history.append("Over withdraw for: " + (str(trans.amount)) + "\n    Prime Money Market insuficent funds. Using funds from Money Market. Remaining balance: " + str(mm))
                                c.moneyMarket.history.append("Insificient funds in Prime Money Market. Remaining withdrawn from Money Market: " + str(mm))
                        
                        else:
                            c.primeMoneyMarket.reduceMoney(trans.getAmount())
                    elif trans.getFund() == 2:
                        if int(trans.getAmount()) > c.longTermBond.totalMoney:
                            if int(trans.getAmount()) - c.shortTermBond.totalMoney > c.longTermBond.totalMoney:
                                c.longTermBond.history.append("Withdraw for: " + (str(trans.amount)) + " (FAILED)")
                                print("ERROR: Not enough funds to withdraw " + str(trans.getAmount()) + " from " + c.getName() + " " + c.longTermBond.fundName)
                            else:
                                mm = int(trans.getAmount()) - int(c.longTermBond.totalMoney)
                                nn = int(trans.getAmount()) - mm
                                c.longTermBond.reduceMoney(str(nn))
                                c.shortTermBond.reduceMoney(str(mm))
                                c.longTermBond.history.append("Over withdraw for: " + (str(trans.amount)) + "\n    Long Term Bond insuficent funds. Using funds from Money Market. Remaining balance: " + str(mm))
                                c.shortTermBond.history.append("Insificient funds in Long Term Bond. Remaining withdrawn from Short Term Bond: " + str(mm))

                        
                        else:
                            c.longTermBond.reduceMoney(trans.getAmount())
                    elif trans.getFund() == 3:
                        if int(trans.getAmount()) > shortTermBond.totalMoney:
                            if int(trans.getAmount()) - c.primeMoneyMarket.totalMoney > c.moneyMarket.totalMoney:
                                c.shortTermBond.history.append("Withdraw for: " + (str(trans.amount)) + " (FAILED)")
                                print("ERROR: Not enough funds to withdraw " + str(trans.getAmount()) + " from " + c.getName() + " " + c.shortTermBond.fundName)
                            else:
                                mm = int(trans.getAmount()) - int(c.shortTermBond.totalMoney)
                                nn = int(trans.getAmount()) - mm
                                c.shortTermBond.reduceMoney(str(nn))
                                c.longTermBond.reduceMoney(str(mm))
                                c.shortTermBond.history.append("Over Withdraw for: " + (str(trans.amount)) + "\n    Short Term Bond insuficent funds. Using funds from Long Term Bond. Remaining balance: " + str(mm))
                                c.longTermBond.history.append("Insificient funds in Short Term Bond. Remaining withdrawn from Long Term Bond: " + str(mm))
                        
                        else:
                            c.shortTermBond.reduceMoney(trans.getAmount())
                    elif trans.getFund() == 4:
                        if int(trans.getAmount()) > c.fiveHundredIndexFund.totalMoney:
                            c.fiveHundredIndexFund.history.append("Withdraw for: " + (str(trans.amount)) + " (FAILED)")
                            print("ERROR: Not enough funds to withdraw " + str(trans.getAmount()) + " from " + c.getName() + " " + c.fiveHundredIndexFund.fundName)
                        else:
                            c.fiveHundredIndexFund.reduceMoney(trans.getAmount())
                    elif trans.getFund() == 5:
                        if int(trans.getAmount()) > c.capitalValueFund.totalMoney:
                            c.capitalValueFund.history.append("Withdraw for: " + (str(trans.amount)) + " (FAILED)")
                            print("ERROR: Not enough funds to withdraw " + str(trans.getAmount()) + " from " + c.getName() + " " + c.capitalValueFund.fundName)
                        else:
                            c.capitalValueFund.reduceMoney(trans.getAmount())
                    elif trans.getFund() == 6:
                        if int(trans.getAmount()) > c.growthEquityFund.totalMoney:
                            c.growthEquityFund.history.append("Withdraw for: " + (str(trans.amount)) + " (FAILED)")
                            print("ERROR: Not enough funds to withdraw " + str(trans.getAmount()) + " from " + c.getName() + " " + c.growthEquityFund.fundName)
                        else:
                            c.growthEquityFund.reduceMoney(trans.getAmount())
                    elif trans.getFund() == 7:
                        if int(trans.getAmount()) > c.growthIndexFund.totalMoney:
                            c.growthIndexFund.history.append("Withdraw for: " + (str(trans.amount)) + " (FAILED)")
                            print("ERROR: Not enough funds to withdraw " + str(trans.getAmount()) + " from " + c.getName() + " " + c.growthIndexFund.fundName)
                        else:
                            c.growthIndexFund.reduceMoney(trans.getAmount())
                    elif trans.getFund() == 8:
                        if int(trans.getAmount()) > c.valueFund.totalMoney:
                            c.valueFund.history.append("Withdraw for: " + (str(trans.amount)) + " (FAILED)")
                            print("ERROR: Not enough funds to withdraw " + str(trans.getAmount()) + " from " + c.getName() + " " + c.valueFund.fundName)
                        else:
                            c.valueFund.reduceMoney(trans.getAmount())
                    elif trans.getFund() == 9:
                        if int(trans.getAmount()) > c.valueStockIndex.totalMoney:
                            c.valueStockIndex.history.append("Withdraw for: " + (str(trans.amount)) + " (FAILED)")
                            print("ERROR: Not enough funds to withdraw " + str(trans.getAmount()) + " from " + c.getName() + " " + c.valueStockIndex.fundName)
                        else:
                            c.valueStockIndex.reduceMoney(trans.getAmount())

            #client(openAccount.type)
        print("Processing Done. Final Balances")    
        ct.printTree()
        return True

class client():
    def __init__(self, firstName, lastName, clientID):
        self.firstName = firstName
        self.lastName = lastName
        self.clientID = clientID
        self.moneyMarket = fund("Money Market")
        self.primeMoneyMarket = fund("Prime Money Market")
        self.longTermBond = fund("Long Term Bond")
        self.shortTermBond = fund("Short Term Bond")
        self.fiveHundredIndexFund = fund("500 Money Market")
        self.capitalValueFund = fund("Capital Value Fund")
        self.growthEquityFund = fund("Growth Equity Fund")
        self.growthIndexFund = fund("Growth Index Fund")
        self.valueFund = fund("Value Fund")
        self.valueStockIndex = fund("Value Stock Index")



    def __str__(self):
        return self.firstName + " " + self.lastName + "\n"\
            + "Money Market: $" + str(self.moneyMarket.totalMoney) + "\n"\
            + "Prime Money Market: $" + str(self.primeMoneyMarket.totalMoney) + "\n"\
            + "Long Term Bond: $" + str(self.longTermBond.totalMoney) + "\n"\
            + "Short Term Bond: $" + str(self.shortTermBond.totalMoney) + "\n"\
            + "500 Money Market: $" + str(self.fiveHundredIndexFund.totalMoney) + "\n"\
            + "Capital Value Fund: $" + str(self.capitalValueFund.totalMoney) + "\n"\
            + "Growth Equity Fund: $" + str(self.growthEquityFund.totalMoney) + "\n"\
            + "Growth Index Fund: $" + str(self.growthIndexFund.totalMoney) + "\n"\
            + "Value Fund: $" + str(self.valueFund.totalMoney) + "\n"\
            + "Value Stock Index: $" + str(self.valueStockIndex.totalMoney)

    def printAllHistory(self):
        print("Transaction Hisory for " + self.firstName + " " + self.lastName + " " + str(self.clientID) + " by fund.\n"\
            + "Money Market: $" + str(self.moneyMarket.totalMoney) + "\n"\
            + "    " + str(self.moneyMarket) + "\n"\
            + "Prime Money Market: $" + str(self.primeMoneyMarket.totalMoney) + "\n"\
            + "    " + str(self.primeMoneyMarket) + "\n"\
            + "Long Term Bond: $" + str(self.longTermBond.totalMoney) + "\n"\
            + "    " + str(self.longTermBond) + "\n"\
            + "Short Term Bond: $" + str(self.shortTermBond.totalMoney) + "\n"\
            + "    " + str(self.shortTermBond) + "\n"\
            + "500 Money Market: $" + str(self.fiveHundredIndexFund.totalMoney) + "\n"\
            + "    " + str(self.fiveHundredIndexFund) + "\n"\
            + "Capital Value Fund: $" + str(self.capitalValueFund.totalMoney) + "\n"\
            + "    " + str(self.capitalValueFund) + "\n"\
            + "Growth Equity Fund: $" + str(self.growthEquityFund.totalMoney) + "\n"\
            + "    " + str(self.growthEquityFund) + "\n"\
            + "Growth Index Fund: $" + str(self.growthIndexFund.totalMoney) + "\n"\
            + "    " + str(self.growthIndexFund) + "\n"\
            + "Value Fund: $" + str(self.valueFund.totalMoney) + "\n"\
            + "    " + str(self.valueFund) + "\n"\
            + "Value Stock Index: $" + str(self.valueStockIndex.totalMoney) + "\n"\
            + "    " + str(self.valueStockIndex))


    def getName(self):
        return self.firstName + " " + self.lastName
    def getID(self):
        return self.clientID

class fund():
    def __init__(self, choice):
        self.fundName = choice
        self.totalMoney = 0
        self.history = []

    def addMoney(self, money):
        self.totalMoney += int(money)
        self.history.append("Deposit for: " + money)
        

    def reduceMoney(self, money):
        self.totalMoney -= int(money)
        self.history.append("Withdrawl for: " + money)

    def treduceMoney(self, money):
        self.totalMoney -= int(money)
        self.history.append("Transfer from " + money)

    def taddMoney(self, money):
        self.totalMoney += int(money)
        self.history.append("Transfer to: " + money)

    def printHistory(self):
        print("\nHistory of " + self.fundName + ":")
        for i in self.history:
             print(str(i))
        
        

    #string function ends up printing the history from the list
    def __str__(self):
        #print ("\nHistory of " + self.fundName + ":")
        string = ""
        for i in self.history:
            string = string + (str(i)) + "\n" + "    "
        return string

class transaction():
    def __init__(self, type, account, fund = -1, amount = 0, toAccount = 0, toFund = 0):
        self.type = type
        self.account = account
        self.fund = fund
        self.amount = amount
        self.toAccount = toAccount
        self.toFund = toFund

    def getType(self):
        return self.type
    def getAccount(self):
        return self.account
    def getFund(self):
        return self.fund
    def getAmount(self):
        return self.amount
    def getToAccount(self):
        return self.toAccount
    def getToFund(self):
        return self.toFund

        if(self.type == "D"):
            self.type = "Deposit"
        elif(self.type == "W"):
            self.type = "Withdraw"
        elif(self.type == "T"):
            self.type = "Transfer"
        elif(self.type == "H"):
            self.type = "History"
        elif(self.type == "O"):
            self.type = "Open"
        else:
            self.type = "Invalid Type"

    def __str__(self):
        if (self.type == "Withdraw"):
            return "Type: " + self.type + "\nAccount " + str(self.account) + "\nFund: " + str(self.fund) + "\nAccount: " + str(self.amount)

        elif(self.type == "Deposit"):
            return "Type: " + self.type + "\nAccount " + str(self.account) + "\nFund: " + str(self.fund) + "\nAccount: " + str(self.amount)

        elif(self.type == "Transfer"):
            return "Type: " + self.type + "\nAccount " + str(self.account) + "\nFund: " + str(self.fund) + "\nAccount: " + str(self.amount) + "\nTransfer to: " + str(self.toAccount) + "\ninto: " + str(self.toFund)

        elif(self.type == "History"):
            return "History: " + str(fund(self.account))

        elif(self.type == "Open"):
            return "Open account for: " + self.amount + " " + self.fund  + "\nAccount #: " + self.account#+ client.getName() + str(client.getID())

        else:
            return ("")