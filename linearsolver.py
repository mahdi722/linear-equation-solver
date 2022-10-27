import numpy as np
from scipy.sparse import csc_matrix

from scipy.sparse.linalg import spsolve

class SparseMatrixSystem:
    def __init__(self, numofvar, nonzeroes, RHS):
        self.numofvar = numofvar
        self.nonzeroes = nonzeroes
        self.RHS = RHS
        self.numofeq = len(RHS)
        self.answers = []
        #self.row = self.generator(numofvar,self.numofeq,nonzeroes)
    def sparsity(self, numofvar, numofeq, nonzeroes):
        if    -len(nonzeroes) >=  -(numofvar+numofeq) :
            return True
        return False
    def sparsity2(self, rows):
        n = 0
        for item in rows:
            for element in item:
                if element != 0:
                    n += 1
        numofvar = len(rows[0])
        numofeq = len(rows)
        if    -n >=  -(numofvar+numofeq) :
            return True
        return False
    def addressofnz(self, nonzeroes):
        address = []
        for node in nonzeroes:
            address.append([node[0],node[1]])
        return address
    def generator(self, numofvar, numofeq, nonzeroes):
        address = self.addressofnz(nonzeroes)
        rows = []
        for i in range(numofeq):
            tempolist = []
            for j in range(numofvar):
                if [i,j] in address:
                    for node in nonzeroes:
                        if i == node[0] and j == node[1]:
                            tempolist.append(node[2])
                else:
                    tempolist.append(0)
            rows.append(tempolist)
        return rows
    def rowgenerator(self, rows, RHS):
        newrows = rows
        newRHS = RHS
######################### making rows
        for item in rows:
            if len(set(item)) == 1 and item[0]==0:
                if newRHS[rows.index(item)] == 0:
                    newRHS.pop(rows.index(item))
                    newrows.pop(rows.index(item))
                else: 
                    print(" 0 = n  n!= 0")
                    return False
        return rows
##########################
        rows = newrows
        RHS = newRHS
        newrows = rows
        newRHS = RHS
    def relocator(self,rows, RHS):
        newrows = rows
        newRHS = RHS
######################### making rows
        for item in rows:
            if len(set(item)) == 1 and item[0]==0:
                if newRHS[rows.index(item)] == [0,0]:
                    newRHS.pop(rows.index(item))
                    newrows.pop(rows.index(item))
                else: 
                    print(" 0 = n  n != 0")
                    return False
##########################
        rows = newrows
        RHS = newRHS
        newrows = rows
        newRHS = RHS
        columns = []
################## making col
        if len(rows) >= 1:
            for j in range(len(rows[0])):
                col = []
                for i in rows:
                    col.append(i[j])
                columns.append(col)
########################################### eliminating the columns
        eliminates = []
        for i in range(len(columns)):
            if len(set(columns[i])) == 1 and columns[i][0] == 0:
                eliminates.append(i)
        for i in range(len(rows)):
            for eliminate in eliminates:
                rows[i][eliminate] = "#"
        if len(rows)>= 1:
            n = rows[0].count("#")
            for i in range(len(rows)):
                for j in range(n):
                    rows[i].remove("#")
###########################################                
        return [rows,RHS]
    def counter(self, rows):
        
        nums = []
        for i in rows:
            n = 0
            for j in i:
                if j != 0:
                    n += 1
            nums.append(n)
        return nums
    def rowcounter(self, row):
        n = 0
        for i in row:
            if i != 0:
                n += 1
                ind = row.index(i)
        return [n,ind]
    
    def idea1(self, rows, RHS):
        while 1 in self.counter(rows) and len(rows)>=1:
            for row in rows:
                if self.rowcounter(row)[0] == 1:
                    index = self.rowcounter(row)[1]
                    RHS[rows.index(row)][0] = RHS[rows.index(row)][0] / row[index]
                    self.answers.append(RHS[rows.index(row)][0])
                    
                    for i in range(len(RHS)):
                        RHS[i][0] -= rows[i][index]*RHS[rows.index(row)][0] 
                            
                        rows[i][index] = 0
                    RHS[rows.index(row)][0] = 0
                    rows = self.relocator(rows,RHS)[0]
                    RHS = self.relocator(rows,RHS)[1]
        if len(rows) > 1:
            return [rows,RHS,0]
        else:
            
            return [rows,RHS,1]
######################################
    def sparse(self, rows, RHS):
        A = csc_matrix(np.array(rows), dtype=float)

        B = csc_matrix(np.array(RHS), dtype=float)

        x = spsolve(A, B)

        ans = np.allclose(A.dot(x).todense(), B.todense())
        self.anserws.append(x)      
    def solve(self):
        rows = self.generator(self.numofvar, self.numofeq, self.nonzeroes)
        rHS = self.relocator(rows, self.RHS)
 
        if rHS != False:
            rows,RHS = rHS[0],rHS[1]
            if 1 in self.counter(rows):
                rows = self.idea1(rows,RHS)
                RHS = rows[1]
                rows = rows[0]
            if rows[1] != 0:
                if 1 not in self.counter(rows) and len(rows) >= 1:
                    try:
                        self.sparse(rows, RHS)
                    except:
                        for item in rows:
                            print(item, "  " ,"[{}]".format(RHS[rows.index(item)][0]))
                        return "not solvable"
                    
        return self.answers
sparsematrix = SparseMatrixSystem(3,[[0,0,1],[0,2,1],[1,1,2],[2,0,1],[2,2,1]],[[2,0],[2,0],[2,0]])
print(sparsematrix.solve())
