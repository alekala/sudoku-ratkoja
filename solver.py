# -*- coding: utf-8 -*-

from random import randint

board = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9],
]

"""
Ratkaiseen pelilaudan `bo`
takapakki (backtracking)
algoritmin avulla
"""
def solve(bo):
    emptyFound = findEmptyCell(bo)
    if emptyFound:
        x, y = emptyFound
    else:
        return True

    for digit in range(1, 10):
        safe = checkConflict((x, y), bo, digit)
        if safe:
            bo[y][x] = digit
            if solve(bo):
                return True
            bo[y][x] = 0

    return False

"""
Etsii annetulta pelilaudalta
`bo` tyhjän solun
"""
def findEmptyCell(bo):
    for y in range(len(bo)):
        for x in range(len(bo[0])):
            if bo[y][x] is 0:
                return x, y
    return None

"""
Tarkastaa onko samassa rivissä,
sarakkeessa tai 3x3 ruudussa
vielä samaa numeroa
"""
def checkConflict(pos, bo, num):
    # Tarkista rivi
    for index, x in enumerate(bo[pos[1]]):
        if x is num and pos[0] is not index:
            return False
    
    # Tarkista sarake
    for index, y in enumerate(bo):
        if y[pos[0]] is num and pos[0] is not index:
            return False
    
    # Tarkista ruutu
    groupX = pos[0] // 3
    groupY = pos[1] // 3

    for y in range(groupY * 3, groupY * 3 + 3):
        for x in range(groupX * 3, groupX * 3 + 3):
            if bo[y][x] is num and (x, y) is not pos:
                return False
    
    return True
            
"""
Tulostaa pelilaudan `bo`
hyvän näköisenä konsoliin
"""
def printBoard(bo):
    for row in range(0, 9):
        print(bo[row])

if __name__ == "__main__":
    solve(board)
    printBoard(board)
