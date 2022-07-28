def my_function(x):
  return list(dict.fromkeys(x))
if __name__ == '__main__':
    # fileold = open('stockxold.txt', 'r')
    # filenew = open('stockxnew.txt', 'r')
    filecompare = open('compareit.txt', 'r')
    #
    # old = fileold.read().split('\n')
    # old = [p for p in old if p]
    #
    # new = filenew.read().split('\n')
    # new = [p for p in new if p]
    #
    filecompare = filecompare.read().split('\n')
    filecompare = [p for p in filecompare if p]
    # count = 0
    # for sku in filecompare:
    #     if sku in old:
    #         print('sku: '+sku+' in OLD')
    #
    #     if sku in new:
    #         print('sku: '+sku+' in New')
    #
    #     if sku not in old and sku not in new:
    #         count +=1
    #         print('not in any')
    #
    # print(count)
    mylist = my_function(filecompare)

    print(mylist)
    filecomparewrite = open('compareit.txt', 'w')
    for lst in mylist:
        filecomparewrite.write(lst+'\n')




