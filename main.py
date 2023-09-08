import numpy as np
from fractions import Fraction
"""Outputs the equation of an inputted polynomial or geometric sequence as well as the value for the inputted term number
"""
def seqSolver(seqList, termnum=1):
    diffList = [j-i for i, j in zip(seqList[:-1], seqList[1:])] #creates a list of the differences between the items in the list
    ratioList = []
    if 0 not in seqList: #to avoid divide by 0 error
      ratioList = [j/i for i, j in zip(seqList[:-1], seqList[1:])] #creates a list of the ratios between the items in the list
    degCount = 1 #to count the number of iterations needed to find a common difference (called degCount because the depth value is the same as the highest degree in the polynomial)
    if all(ratio == ratioList[0] for ratio in ratioList):
        if len(ratioList)<=1: #If there are one or fewer ratios, it's not enough items to make a pattern
            print("Not enough items inputted\n")
        else:
            print(geometricSolver(ratioList, seqList[0], termnum))
        return
    while not all(diff == diffList[0] for diff in diffList): #makes a list of differences of the differences list until the list only has common differences. The degree variable is also incremented for each iteration
        diffList = [j-i for i, j in zip(diffList[:-1], diffList[1:])]
        degCount+=1
    if len(seqList)< degCount+2: #checks that there are enough items inputted for the polynomial sequence
        print("Not enough items inputted\n")
        return
    coefmatrix = [] #initializes a coefficient matrix
    loadMatrices(seqList, coefmatrix, degCount) #loads the coefmatrix with the proper values
    varmatrix = [item for item in seqList[:degCount+1]] #sets the variable matrix to be the items in the sequence list up to the degree position
    varmatrix = np.array(varmatrix).reshape(len(varmatrix), 1) #Need to make it a vertical array to be able to use matmul (Otherwise you can't do the product since the dimensions dont match)
    invcoef = np.linalg.inv(coefmatrix) #inversing 
    solmatrix = np.matmul(invcoef, varmatrix)
    #Solmatrix is the "final" matrix, which we make from multiplying the inverse of the coef matrix with the var matrix. Basically it has the coefficents for the final equation.
    termval = findvalueofseq(solmatrix, termnum) #stores the value at the term number as termval
    equation = equationMaker(solmatrix, degCount) #stores the equation string as equation
    print(f"Equation: {equation}\nValue at {termnum}: {termval}\n") #displays equation and value for term number

def loadMatrices(seqList, coefmatrix, degCount): #iterates through values from 1 to the degree count+1 and makes a matrix with the rows being the value to the power of the highest degree to 0. 
    for i in range(1, degCount+2):
        numlist = []
        for j in range(degCount, -1, -1):
            numlist.append(i**j) 
        coefmatrix.append(numlist)
    coefmatrix = np.array(coefmatrix) #turns the matrix into a 2d numpy array so that the matrix functions can be applied to it

def equationMaker(varMatrix, highDeg): #Uses variable matrix to form the equation
    equatString = ""
    for deg in range(highDeg, -1, -1): #Goes through each degree from highest to 0
        coef_as_float = round(varMatrix.item(highDeg-deg), 2) #Selects a coefficient and rounds it to 2 places, storing it as a float
        coef = str(Fraction.from_float(varMatrix.item(highDeg-deg)).limit_denominator(100)) #Selects a coefficient and stores it as a Fraction object, but when turned to a string it shows as the numerator/denominator like "4/5". For integers, it will store it as a normal integer string like "1"
        if coef_as_float%1!=0: #checking whether the coefficient is a fraction, not an integer float
            coef = f"({coef})" 
            coef+="*" #adding parentheses and an asterisk with the fraction coef to make it more readable in the equation
        varStr = ""
        """
        Rules for coefficients stated through if statements:
        1: If coefficient is 0, don't bother writing it (not having 0x for exp.)
        2: If the coefficient is 1, but the degree is not 0, don't write the coefficient (not having the 1 in 1x, for exp.)
        3: If degree is not the highest degree and the coefficient is positive, add a + sign in front of it and turn the coefficient into a string (+ 2.5 for exp.)
        4: If the degree is negative or the degree is the highest, add a negative and a space before the number (-0.5 becomes - 0.5).  
        """
        if coef_as_float != 0: 
            if coef_as_float!=1 or deg == 0:
                if deg!=highDeg and coef_as_float > 0:
                    varStr = f"+ {coef}"
                elif coef_as_float < 0:
                    varStr = f"- {coef[1:]}" 
                else:
                    varStr = str(coef)
            # If the degree is greater than 1, then follow the coefficient with the string "x^degree". Else, if the degree is 1, just print the coefficient followed by "x". Finally, if the degree is 0, just make the coefficient what you print out. 
            if deg > 1:
                equatString += f"{varStr}x^{deg} "
            elif deg == 1:
                equatString += f"{varStr}x "
            else:
                equatString += varStr
    return equatString

def findvalueofseq(pattern, termnum): #uses the term number and the solution matrix to find the value of the sequence at the term number
    value = 0
    for pos, item in enumerate(pattern):
        coef = item[0] #needed because the matrix is 2d, so the coefficient is the 1st (and only) element in each row
        power = len(pattern)-pos-1
        value+=coef*(termnum**power) #plugs in term number into equation (number is the "x")
    return round(value, 2) #rounds the value to 2 decimal places

def geometricSolver(ratioList, firstTerm, termnum): #used to solve for the equation and value if the sequence is geometric
    ratio = Fraction.from_float(ratioList[0]).limit_denominator(100) #like the coefficient, it turns a decimal into a fraction and keeps integers like 1.0 as they are
    firstStr = ""
    if firstTerm!=1: #checks that the number isn't 1 because 1x = x
        firstStr = str(firstTerm)
    equationstr = f"{firstStr}({str(ratio)})^(x-1)" 
    termval = firstTerm*(float(ratio)**(termnum-1)) #plugs in the ratio and term number into the equation to get the value
    return f"Equation: {equationstr}\nValue at {termnum}: {termval}\n" #displays geometric equation and value at the term number
       
#Input your sequences here (The ones below are examples, feel free to remove them.)
#seqSolver([1, 4, 9, 16])
#seqSolver([1, 3, 5, 7], 6)
seqSolver([6, 11, 18, 27], 5)
#seqSolver([1, 4, 27, 256, 3125], 6)
#seqSolver([12, 20, 24, 24, 20, 12, 0, -16, -36, -60], 5)