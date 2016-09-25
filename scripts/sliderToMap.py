start = 0
end = .5

firstDateIndex = int(start*len(x))
lastDateIndex = (int((end-start) * len(x)) + firstDateIndex - 1)


firstDate = datetime.date(*(int(s) for s in x[firstDateIndex]['purchase_date'].split("-")))
lastDate = datetime.date(*(int(s) for s in x[lastDateIndex]['purchase_date'].split("-")))

merchantDict = {}

for purchase in x:
    purchaseDate = datetime.date(*(int(s) for s in purchase['purchase_date'].split("-")))
    if purchaseDate >= firstDate and purchaseDate <= lastDate:
        merchant_id = purchase['merchant_id']
        print(merchant_id)
        print(merchantDict[merchant_id])
        if merchantDict[merchant_id] == None:
            print('hi')
            #merchantDict[purchase['merchant_id']] = purchase['amount']
        else:
            print('bye')
            #merchantDict[purchase['merchant_id']] = merchantDict[purchase['merchant_id']] + purchase['amount']

