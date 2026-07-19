import pygame, asyncio

pygame.init()

def name(char):#Returns full name of piece based on character
    colour = ""
    
    if char == char.lower():
        colour = "Black"
    
    else:
        colour = "White"
        
    if char.lower() == "p":
        return f"{colour} pawn"
    
    elif char.lower() == "n":
        return f"{colour} knight"
    
    elif char.lower() == "b":
        return f"{colour} bishop"
    
    elif char.lower() == "r":
        return f"{colour} rook"
    
    elif char.lower() == "q":
        return f"{colour} queen"
    
    elif char.lower() == "k":
        return f"{colour} king"
    
    else:
        return None

def number(char):#Returns True if char is a number and False otherwise
    
    for num in range(1,9):
        
        if char == str(num):
            return True
    
    return False

def colour(piece):#Returns the colour of the piece
    
    if not number(piece):
    
        if piece == piece.lower():
            return "b"
        
        return "w"
    
    return None

def colNum(piece):
    
    if piece == piece.upper():
        return 1
    
    return -1

def position(file, rank, fen):
    key = rank + 1
    val_dex = 0
    file_match = 0
    
    for char in fen[key]:
        
        if file_match + 1 > file:
            break
        
        elif number(char):
            
            if file_match + int(char) > file:
                break
            
            else:
                file_match += int(char)
        
        else:
            file_match += 1
        
        val_dex += 1
    
    return key, val_dex

def coordinate(key, val_dex, fen):
    rank = key - 1
    file = 0
    
    if val_dex == 0:
        return file, rank
    
    else:
        
        for char in fen[key][:val_dex]:
            
            if number(char):
                file += int(char)
            
            else:
                file += 1
    
    return file, rank

def pseudoLegal(start_file, start_rank, end_file, end_rank, fen):
    key, val_dex = position(start_file, start_rank, fen)
    piece = fen[key][val_dex]
    key, val_dex = position(end_file, end_rank, fen)
    other_piece = fen[key][val_dex]
    
    if colour(piece) == colour(other_piece):
        return False
    
    if piece.lower() == "p":
        
        if start_file == end_file:
            
            if ((end_rank - start_rank) * colNum(piece) == 1 or (start_rank == -2.5 * colNum(piece) + 3.5 and (end_rank - start_rank) * colNum(piece) == 2)) and number(other_piece):
                return True
            
            return False
        
        if abs(end_file - start_file) == 1 and end_rank - start_rank == colNum(piece):
            
            if not number(other_piece) or f"{files[end_file]}{end_rank + 1}" == fen["en passant"]:
                return True
        
        return False
    
    if piece.lower() == "r":
        
        if start_file == end_file:
            
            for rank in range(start_rank, end_rank, int((end_rank - start_rank)/abs(end_rank - start_rank))):
                
                if rank != start_rank:
                    key, val_dex = position(end_file, rank, fen)
                    
                    if not number(fen[key][val_dex]):
                        return False
            
            return True
        
        if start_rank == end_rank:
            
            for file in range(start_file, end_file, int((end_file - start_file)/abs(end_file - start_file))):
                
                if file != start_file:
                    key, val_dex = position(file, end_rank, fen)
                    
                    if not number(fen[key][val_dex]):
                        return False
            
            return True
        
        return False
    
    if piece.lower() == "n":
        
        if (abs(end_rank - start_rank) == 2 and abs(end_file - start_file) == 1) or (abs(end_file - start_file) == 2 and abs(end_rank - start_rank) == 1):
            return True
        
        return False
    
    if piece.lower() == "b":
        
        if abs(end_file - start_file) == abs(end_rank - start_rank) and not start_file == end_file:
            
            for square in range(1, abs(end_file - start_file)):
                key, val_dex = position(start_file + square * ((end_file - start_file)/abs(end_file - start_file)), start_rank + square * ((end_rank - start_rank)/abs(end_rank - start_rank)), fen)
                
                if not number(fen[key][val_dex]):
                    return False
            
            return True
        
        return False
    
    if piece.lower() == "q":
        
        if start_file == end_file:
            
            for rank in range(start_rank, end_rank, int((end_rank - start_rank)/abs(end_rank - start_rank))):
                
                if rank != start_rank:
                    key, val_dex = position(end_file, rank, fen)
                    
                    if not number(fen[key][val_dex]):
                        return False
            
            return True
        
        if start_rank == end_rank:
            
            for file in range(start_file, end_file, int((end_file - start_file)/abs(end_file - start_file))):
                
                if file != start_file:
                    key, val_dex = position(file, end_rank, fen)
                    
                    if not number(fen[key][val_dex]):
                        return False
            
            return True
        
        if abs(end_file - start_file) == abs(end_rank - start_rank):
            
            for square in range(1, abs(end_file - start_file)):
                key, val_dex = position(start_file + square * ((end_file - start_file)/abs(end_file - start_file)), start_rank + square * ((end_rank - start_rank)/abs(end_rank - start_rank)), fen)
                
                if not number(fen[key][val_dex]):
                    return False
            
            return True
        
        return False
    
    if piece.lower() == "k":
        
        for file in range(start_file - 1, start_file + 2):
            
            for rank in range(start_rank - 1, start_rank + 2):
                
                if file == end_file and rank == end_rank and not (start_file == end_file and start_rank == end_rank):
                    return True
        
        return False
    
    return True

def inCheck(fen):
    
    found_king = False
    for key in range(1, 9):
        
        if found_king:
            break
        
        for val_dex in range(len(fen[key])):
            
            if fen[key][val_dex].lower() == "k" and colour(fen[key][val_dex]) == fen["turn"]:
                k_file, k_rank = coordinate(key, val_dex, fen)
                found_king = True
                break
    
    for key in range(1, 9):
        
        for val_dex in range(len(fen[key])):
            
            if not number(fen[key][val_dex]) and colour(fen[key][val_dex]) != fen["turn"]:
                p_file, p_rank = coordinate(key, val_dex, fen)
                
                if pseudoLegal(p_file, p_rank, k_file, k_rank, fen):
                    return True
    
    return False

def legal(start_file, start_rank, end_file, end_rank, fen):
    key, val_dex = position(start_file, start_rank, fen)
    piece = fen[key][val_dex]
        
    if piece.lower() == "k":
        
        if abs(end_file - start_file) == 2 and start_rank == end_rank:
            rights = False
    
            if end_file > start_file:
                
                for char in fen["castling"]:
                    
                    if char == piece:
                        rights = True
                        break
        
                if rights:
                    clear = True
                    
                    for file in range(5, 7):
                        key, val_dex = position(file, start_rank, fen)
                        
                        if not number(fen[key][val_dex]):
                            clear = False
                            break
                    
                    if clear and not inCheck(fen):
                        test = fen.copy()
                        test[start_rank + 1] = f"{fen[start_rank + 1][:fen[start_rank + 1].index(piece)]}1{piece}1{fen[start_rank + 1][-1]}"
                        
                        for file in range(8):
                            
                            for rank in range(8):
                                key, val_dex = position(file, rank, test)
                                
                                if not number(test[key][val_dex]):
                                    
                                    if colour(test[key][val_dex]) != colour(piece) and pseudoLegal(file, rank, start_file + 1, start_rank, test):
                                        return False
                        
                        test[start_rank + 1] = f"{fen[start_rank + 1][:fen[start_rank + 1].index(piece)]}2{piece}{fen[start_rank + 1][-1]}"
                        
                        for file in range(8):
                            
                            for rank in range(8):
                                key, val_dex = position(file, rank, test)
                                
                                if not number(test[key][val_dex]):
                                    
                                    if colour(test[key][val_dex]) != colour(piece) and pseudoLegal(file, rank, start_file + 2, start_rank, test):
                                        return False
                    
                        return True
                    
                    return False
                
                return False
                
            else:
                
                for char in fen["castling"]:
                    
                    if char.lower() == "q" and colour(char) == colour(piece):
                        rights = True
                        break
                
                if rights:
                    clear = True
                    
                    for file in range(1,4):
                        key, val_dex = position(file, start_rank, fen)
                        
                        if not number(fen[key][val_dex]):
                            clear = False
                            break
                    
                    if clear and not inCheck(fen):
                        test = fen.copy()
                        test[start_rank + 1] = f"{fen[start_rank + 1][0]}2{piece}1{fen[start_rank + 1][fen[start_rank + 1].index(piece) + 1:]}"
                        
                        if inCheck(test):
                            return False
                        
                        test[start_rank + 1] = f"{fen[start_rank + 1][0]}1{piece}2{fen[start_rank + 1][fen[start_rank + 1].index(piece) + 1:]}"
                        
                        if inCheck(test):
                            return False
                        
                        return True
                        
                    return False
                    
                return False
    
    test = fen.copy()
    makeMove(start_file, start_rank, end_file, end_rank, test)
    test["turn"] = oppCol(test["turn"])
    
    if pseudoLegal(start_file, start_rank, end_file, end_rank, fen) and not inCheck(test):
        return True
    
    return False

def oppCol(colour):#Returns the opposite colour of the input
    
    if colour == "w":
        return "b"
    
    return "w"

def makeMove(start_file, start_rank, end_file, end_rank, fen, castling = False):
    key, val_dex = position(start_file, start_rank, fen)
    piece = fen[key][val_dex]
    
    if len(fen[key]) == 2:
        fen[key] = "8"
    
    elif val_dex == 0:
        
        if number(fen[key][1]):
            fen[key] = f"{int(fen[key][1]) + 1}{fen[key][2:]}"
        
        else:
            fen[key] = f"1{fen[key][1:]}"
    
    elif val_dex == len(fen[key]) - 1:
        
        if number(fen[key][-2]):
            fen[key] = f"{fen[key][:-2]}{int(fen[key][-2]) + 1}"
        
        else:
            fen[key] = f"{fen[key][:-1]}1"
    
    elif number(fen[key][val_dex - 1]) and number(fen[key][val_dex + 1]):
        
        if val_dex == len(fen[key]) - 2:
            fen[key] = f"{fen[key][:-3]}{int(fen[key][-3]) + int(fen[key][-1]) + 1}"
        
        else:
            fen[key] = f"{fen[key][:val_dex - 1]}{int(fen[key][val_dex - 1]) + int(fen[key][val_dex + 1]) + 1}{fen[key][val_dex + 2:]}"
    
    elif number(fen[key][val_dex - 1]):
        fen[key] = f"{fen[key][:val_dex - 1]}{int(fen[key][val_dex - 1]) + 1}{fen[key][val_dex + 1:]}"
    
    elif number(fen[key][val_dex + 1]):
        
        if val_dex == len(fen[key]) - 2:
            fen[key] = f"{fen[key][:-2]}{int(fen[key][-1]) + 1}"
        
        else:
            fen[key] = f"{fen[key][:val_dex]}{int(fen[key][val_dex + 1]) + 1}{fen[key][val_dex + 2:]}"
    
    else:
        fen[key] = f"{fen[key][:val_dex]}1{fen[key][val_dex + 1:]}"
    
    key, val_dex = position(end_file, end_rank, fen)
    
    if not number(fen[key][val_dex]):
        
        if val_dex == len(fen[key]) - 1:
            fen[key] = f"{fen[key][:-1]}{piece}"
        
        else:
            fen[key] = f"{fen[key][:val_dex]}{piece}{fen[key][val_dex + 1:]}"
    
    elif fen[key] == "8":
        
        if end_file == 0:
            fen[key] = f"{piece}7"
        
        elif end_file == 7:
            fen[key] = f"7{piece}"
        
        else:
            fen[key] = f"{end_file}{piece}{7 - end_file}"
    
    elif int(fen[key][val_dex]) == 1:
        
        if val_dex == 0:
            fen[key] = f"{piece}{fen[key][1:]}"
        
        elif val_dex == len(fen[key]) - 1:
            fen[key] = f"{fen[key][:-1]}{piece}"
        
        else:
            fen[key] = f"{fen[key][:val_dex]}{piece}{fen[key][val_dex + 1:]}"
    
    elif val_dex == 0:
        
        if end_file == 0:
            fen[key] = f"{piece}{int(fen[key][0]) - 1}{fen[key][1:]}"
        
        elif end_file + 1 == int(fen[key][0]):
            fen[key] = f"{int(fen[key][0]) - 1}{piece}{fen[key][1:]}"
        
        else:
            fen[key] = f"{end_file}{piece}{int(fen[key][0]) - end_file - 1}{fen[key][1:]}"
    
    elif val_dex == len(fen[key]) - 1:
        
        if end_file == 8 - int(fen[key][val_dex]):
            fen[key] = f"{fen[key][:-1]}{piece}{int(fen[key][-1]) - 1}"
        
        elif end_file == 7:
            fen[key] = f"{fen[key][:-1]}{int(fen[key][-1]) - 1}{piece}"
        
        else:
            file_prev, rank_prev = coordinate(key, val_dex - 1, fen)
            fen[key] = f"{fen[key][:-1]}{end_file - file_prev - 1}{piece}{7 - end_file}"
    
    else:
        file_prev, rank_prev = coordinate(key, val_dex - 1, fen)
        file_aft, rank_aft = coordinate(key, val_dex + 1, fen)
        
        if end_file == file_prev + 1:
            fen[key] = f"{fen[key][:val_dex]}{piece}{int(fen[key][val_dex]) - 1}{fen[key][val_dex + 1:]}"
        
        elif end_file == file_aft - 1:
            fen[key] = f"{fen[key][:val_dex]}{int(fen[key][val_dex]) - 1}{piece}{fen[key][val_dex + 1:]}"
        
        else:
            fen[key] = f"{fen[key][:val_dex]}{end_file - file_prev - 1}{piece}{file_aft - end_file - 1}{fen[key][val_dex + 1:]}"
    
    if piece == "R" or end_rank == 0:
        
        if (start_file == 0 or end_file == 0) and fen["castling"].find("Q") != -1:
            
            if fen["castling"].find("Q") == len(fen["castling"]) - 1:
                fen["castling"] = f"{fen['castling'][:-1]}"
            
            else:
                fen["castling"] = f"{fen['castling'][:fen['castling'].find('Q')]}{fen['castling'][fen['castling'].find('Q') + 1:]}"
        
        elif (start_file == 7 or end_file == 7) and fen["castling"].find("K") != -1:
            
            if fen["castling"] == "K":
                fen["castling"] = "-"
            
            else:
                fen["castling"] = f"{fen['castling'][1:]}"
    
    elif piece == "r" or end_rank == 7:
        
        if (start_file == 0 or end_file == 0) and fen["castling"].find("q") != -1:
            fen["castling"] = f"{fen['castling'][:-1]}"
        
        elif (start_file == 7 or end_file == 7) and fen["castling"].find("k") != -1:
            
            if fen["castling"].find("k") == len(fen["castling"]) - 1:
                fen["castling"] = f"{fen['castling'][:fen['castling'].find('k')]}"
            
            else:
                fen["castling"] = f"{fen['castling'][:fen['castling'].find('k')]}q"
    
    if piece == "K":
        
        for char in fen["castling"]:
            
            if char == char.upper():
                
                if fen["castling"].find(char) == len(fen["castling"]) - 1:
                    fen["castling"] = f"{fen['castling'][:-1]}"
                
                else:
                    fen["castling"] = f"{fen['castling'][:fen['castling'].find(char)]}{fen['castling'][fen['castling'].find(char) + 1:]}"
    
    elif piece == "k":
        
        for char in fen["castling"]:
            
            if char == char.lower():
                
                if fen["castling"].find(char) == len(fen["castling"]) - 1:
                    fen["castling"] = f"{fen['castling'][:-1]}"
                
                else:
                    fen["castling"] = f"{fen['castling'][:fen['castling'].find(char)]}{fen['castling'][fen['castling'].find(char) + 1:]}"
    
    if fen["castling"] == "":
        fen["castling"] = "-"
    
    if piece.lower() == "p" and fen["en passant"] == f"{files[end_file]}{end_rank + 1}":
        key, val_dex = position(end_file, end_rank - 1, fen)
        
        if len(fen[key]) == 2:
            fen[key] = "8"
        
        elif val_dex == 0:
            
            if number(fen[key][1]):
                fen[key] = f"{int(fen[key][1]) + 1}{fen[key][2:]}"
            
            else:
                fen[key] = f"1{fen[key][1:]}"
        
        elif val_dex == len(fen[key]) - 1:
            
            if number(fen[key][-2]):
                fen[key] = f"{fen[key][:-2]}{int(fen[key][-2]) + 1}"
            
            else:
                fen[key] = f"{fen[key][:-1]}1"
        
        elif number(fen[key][val_dex - 1]) and number(fen[key][val_dex + 1]):
            
            if val_dex == len(fen[key]) - 2:
                fen[key] = f"{fen[key][:-3]}{int(fen[key][-3]) + int(fen[key][-1]) + 1}"
            
            else:
                fen[key] = f"{fen[key][:val_dex - 1]}{int(fen[key][val_dex - 1]) + int(fen[key][val_dex + 1]) + 1}{fen[key][val_dex + 2:]}"
        
        elif number(fen[key][val_dex - 1]):
            fen[key] = f"{fen[key][:val_dex - 1]}{int(fen[key][val_dex - 1]) + 1}{fen[key][val_dex + 1:]}"
        
        elif number(fen[key][val_dex + 1]):
            
            if val_dex == len(fen[key]) - 2:
                fen[key] = f"{fen[key][:-2]}{int(fen[key][-1]) + 1}"
            
            else:
                fen[key] = f"{fen[key][:val_dex]}{int(fen[key][val_dex + 1]) + 1}{fen[key][val_dex + 2:]}"
        
        else:
            fen[key] = f"{fen[key][:val_dex]}1{fen[key][val_dex + 1:]}"
        
    if piece.lower() == "p" and abs(end_rank - start_rank) == 2:
        fen["en passant"] = f"{files[end_file]}{3 * end_rank - 6}"
    
    else:
        fen["en passant"] = "-"
    
    if not castling:
        
        if piece.lower() == "p" or not number(fen[key][val_dex]):
            fen["halfmoves"] = 0
        
        else:
            fen["halfmoves"] += 1
        
        if fen["turn"] == "b":
            fen["fullmoves"] += 1
        
        fen["turn"] = oppCol(fen["turn"])
    
    if piece.lower() == "k" and abs(end_file - start_file) == 2:
        
        if end_file > start_file:
            makeMove(7, end_rank, 5, end_rank, fen, True)
        
        else:
            makeMove(0, end_rank, 3, end_rank, fen, True)
    
    return fen

def algebraic(start_file, start_rank, end_file, end_rank, fen):
    key, val_dex = position(start_file, start_rank, fen)
    piece = fen[key][val_dex]
    key, val_dex = position(end_file, end_rank, fen)
    other_piece = fen[key][val_dex]
    move = ""
    check = False
    
    if piece.upper() != "P":
        move = piece.upper()
    
    move = f"{move}{files[end_file]}{end_rank + 1}"
    
    if not number(other_piece) or (piece.upper() == "P" and f"{files[end_file]}{end_rank + 1}" == fen["en passant"]):
        
        if piece.upper() == "P":
            move = f"{files[start_file]}x{move}"
        
        else:
            move = f"{move[0]}x{move[1:]}"
    
    if piece.upper() == "K":
        
        if end_file - start_file == 2:
            move = "0-0"
        
        if end_file - start_file == -2:
            move = "0-0-0"
    
    test = fen.copy()
    makeMove(start_file, start_rank, end_file, end_rank, test)
    
    if inCheck(test):
        move = f"{move}+"
        check = True
    
    if check:
        mate = True
        
        for s_file in range(8):
            
            if not mate:
                break
            
            for s_rank in range(8):
                
                if not mate:
                    break
                
                key, val_dex = position(s_file, s_rank, test)
                
                if colour(test[key][val_dex]) == test["turn"] and not number(test[key][val_dex]):
                
                    for e_file in range(8):
                        
                        if not mate:
                            break
                        
                        for e_rank in range(8):
                            
                            if pseudoLegal(s_file, s_rank, e_file, e_rank, test) and (s_file != e_file or s_rank != e_rank):
                                save = test.copy()
                                makeMove(s_file, s_rank, e_file, e_rank, test)
                                test["turn"] = oppCol(test["turn"])
                                
                                if not inCheck(test):
                                    mate = False
                                    break
                                
                                test = save
        
        if mate:
            move = f"{move[:-1]}#"
    
    for file in range(8):
        
        for rank in range(8):
            key, val_dex = position(file, rank, fen)
            
            if fen[key][val_dex] == piece and legal(file, rank, end_file, end_rank, fen):
                
                if rank != start_rank:
                
                    if piece.upper() == "P":
                        move = f"{files[start_file]}{move}"
                    
                    else:
                        move = f"{move[0]}{files[start_file]}{move[1:]}"
                
                elif file != start_file:
                    
                    if piece.upper() == "P":
                        move = f"{start_rank + 1}{move}"
                    
                    else:
                        move = f"{move[0]}{start_rank + 1}{move[1:]}"
    
    if piece.upper() == "P" and (end_rank == 0 or end_rank == 7):
        move = [f"{files[end_file]}{end_rank + 1}=N", f"{files[end_file]}{end_rank + 1}=B", f"{files[end_file]}{end_rank + 1}=R", f"{files[end_file]}{end_rank + 1}=Q"]
    
    return move

window = pygame.display.set_mode((490,490))
pygame.display.set_caption("Beat_Will_Bot_1000")

game_state = {
    8: "rnbqkbnr",
    7: "pppppppp",
    6: "8",
    5: "8",
    4: "8",
    3: "8",
    2: "PPPPPPPP",
    1: "RNBQKBNR",
    "turn": "w",
    "castling": "KQkq",
    "en passant": "-",
    "halfmoves": 0,
    "fullmoves": 0}
files = ["a","b","c","d","e","f","g","h"]

async def main():
    m_file = 0
    m_rank = 0
    select = None
    promote = None
    
    running = True
    while running:
        
        if promote is not None:
            
            pygame.event.pump()
            for events in pygame.event.get():
                
                if events.type == pygame.MOUSEBUTTONUP and events.button == 1:
                
                    for col in range(8):
                                
                        if pygame.mouse.get_pos()[0] >= 5 + 60 * col and pygame.mouse.get_pos()[0] < 5 + 60 * (col + 1):
                            m_file = col
                            break
                    
                    for row in range(8):
                        
                        if pygame.mouse.get_pos()[1] >= 5 + 60 * (7 - row) and pygame.mouse.get_pos()[1] < 5 + 60 * (8 - row):
                            m_rank = row
                            break
                    
                    selected = False
                    while not selected:
                        key, val_dex = position(promote[0], promote[1], game_state)
                        piece = game_state[key][val_dex]
                        
                        if m_file == promote[0]:
                                    
                            if m_rank == promote[1]:
                                
                                if colour(piece) == "w":
                                
                                    if val_dex == len(game_state[key]) - 1:
                                        game_state[key] = f"{game_state[key][:-1]}Q"
                                    
                                    else:
                                        game_state[key] = f"{game_state[key][:val_dex]}Q{game_state[key][val_dex + 1:]}"
                                
                                else:
                                    
                                    if val_dex == len(game_state[key]) - 1:
                                        game_state[key] = f"{game_state[key][:-1]}q"
                                    
                                    else:
                                        game_state[key] = f"{game_state[key][:val_dex]}q{game_state[key][val_dex + 1:]}"
                                        
                                promote = None
                                selected = True
                            
                            elif m_rank == promote[1] - colNum(piece):
                                
                                if colour(piece) == "w":
                                
                                    if val_dex == len(game_state[key]) - 1:
                                        game_state[key] = f"{game_state[key][:-1]}R"
                                    
                                    else:
                                        game_state[key] = f"{game_state[key][:val_dex]}R{game_state[key][val_dex + 1:]}"
                                
                                else:
                                    
                                    if val_dex == len(game_state[key]) - 1:
                                        game_state[key] = f"{game_state[key][:-1]}r"
                                    
                                    else:
                                        game_state[key] = f"{game_state[key][:val_dex]}r{game_state[key][val_dex + 1:]}"
                                        
                                promote = None
                                selected = True
                            
                            elif m_rank == promote[1] - colNum(piece) * 2:
                                
                                if colour(piece) == "w":
                                
                                    if val_dex == len(game_state[key]) - 1:
                                        game_state[key] = f"{game_state[key][:-1]}B"
                                    
                                    else:
                                        game_state[key] = f"{game_state[key][:val_dex]}B{game_state[key][val_dex + 1:]}"
                                
                                else:
                                    
                                    if val_dex == len(game_state[key]) - 1:
                                        game_state[key] = f"{game_state[key][:-1]}b"
                                    
                                    else:
                                        game_state[key] = f"{game_state[key][:val_dex]}b{game_state[key][val_dex + 1:]}"
                                        
                                promote = None
                                selected = True
                            
                            elif m_rank == promote[1] - colNum(piece) * 3:
                                
                                if colour(piece) == "w":
                                
                                    if val_dex == len(game_state[key]) - 1:
                                        game_state[key] = f"{game_state[key][:-1]}N"
                                    
                                    else:
                                        game_state[key] = f"{game_state[key][:val_dex]}N{game_state[key][val_dex + 1:]}"
                                
                                else:
                                    
                                    if val_dex == len(game_state[key]) - 1:
                                        game_state[key] = f"{game_state[key][:-1]}n"
                                    
                                    else:
                                        game_state[key] = f"{game_state[key][:val_dex]}n{game_state[key][val_dex + 1:]}"
                                        
                                promote = None
                                selected = True
        
        pygame.event.pump()
        for events in pygame.event.get():
            
            if events.type == pygame.MOUSEBUTTONUP and events.button == 1:
                
                for col in range(8):
                            
                    if pygame.mouse.get_pos()[0] >= 5 + 60 * col and pygame.mouse.get_pos()[0] < 5 + 60 * (col + 1):
                        m_file = col
                        break
                
                for row in range(8):
                    
                    if pygame.mouse.get_pos()[1] >= 5 + 60 * (7 - row) and pygame.mouse.get_pos()[1] < 5 + 60 * (8 - row):
                        m_rank = row
                        break
                
                if select == None:
                    key, val_dex = position(m_file, m_rank, game_state)
                    
                    if not number(game_state[key][val_dex]) and colour(game_state[key][val_dex]) == game_state["turn"]:
                        select = [m_file, m_rank]
                
                elif select[0] == m_file and select[1] == m_rank:
                    select = None
                
                elif legal(select[0], select[1], m_file, m_rank, game_state):
                    print(algebraic(select[0], select[1], m_file, m_rank, game_state))
                    makeMove(select[0], select[1], m_file, m_rank, game_state)
                    select = None
                    key, val_dex = position(m_file, m_rank, game_state)
                    
                    if game_state[key][val_dex].lower() == "p" and (m_rank == 0 or m_rank == 7):
                        promote = [m_file, m_rank]
            
            if events.type == pygame.QUIT:
                running = False
            
        #Board rendering
        for row in range(0, 480, 60):
            
            for square in range(5, 480, 60):
        
                if ((square - 5) % 120 == 0 and row % 120 == 60) or ((square - 5) % 120 == 60 and row % 120 == 0):
                    pygame.draw.rect(window, (179,152,79), [square, row + 5, 60, 60])
                            
                else:
                    pygame.draw.rect(window, (117, 99, 50), [square, row + 5, 60, 60])

        if select != None:
            pygame.draw.rect(window, (255, 255, 0), [select[0] * 60 + 5, 60 * (7 - select[1]) + 5, 60, 60])
        
        #Piece rendering
        for col in range(8):
            
            for row in range(8):
                key, val_dex = position(col, row, game_state)
                
                if not number(game_state[key][val_dex]):
                    window.blit(pygame.image.load(f"Chess PNG's/{name(game_state[key][val_dex])}.png"), (5 + 60 * col, 5 + 60 * (7 - row)))
        
        if promote is not None:
            key, val_dex = position(promote[0], promote[1], game_state)
            
            if colour(game_state[key][val_dex]) == "w":
                pygame.draw.rect(window, (184, 184, 184), [4 + 60 * promote[0], 5, 62, 242])
                window.blit(pygame.image.load(f"Chess PNG's/White queen.png"), (5 + 60 * promote[0], 5))
                window.blit(pygame.image.load(f"Chess PNG's/White rook.png"), (5 + 60 * promote[0], 5 + 60))
                window.blit(pygame.image.load(f"Chess PNG's/White bishop.png"), (5 + 60 * promote[0], 5 + 60 * 2))
                window.blit(pygame.image.load(f"Chess PNG's/White knight.png"), (5 + 60 * promote[0], 5 + 60 * 3))
            
            else:
                pygame.draw.rect(window, (184, 184, 184), [4 + 60 * promote[0], 3 + 60 * 4, 62, 242])
                window.blit(pygame.image.load(f"Chess PNG's/Black queen.png"), (5 + 60 * promote[0], 5 + 60 * 7))
                window.blit(pygame.image.load(f"Chess PNG's/Black rook.png"), (5 + 60 * promote[0], 5 + 60 * 6))
                window.blit(pygame.image.load(f"Chess PNG's/Black bishop.png"), (5 + 60 * promote[0], 5 + 60 * 5))
                window.blit(pygame.image.load(f"Chess PNG's/Black knight.png"), (5 + 60 * promote[0], 5 + 60 * 4))
        
        pygame.display.flip()
        await asyncio.sleep(0)

asyncio.run(main())
pygame.quit()