def solveSudoku(board):
        empty =[]
        rows = [set() for _ in range(9)]
        cols = [set() for _ in range(9)]
        boxes = [set() for _ in range(9)]
        NUMS_STR = [str(i) for i in range(10)]

        for r in range(9):
            for c in range(9):
                val = board[r][c]
                if val == '.':
                    empty.append((r, c))

                else: 
                    rows[r].add(val)
                    cols[c].add(val)

                    box_idx = (r // 3) * 3 + (c // 3)
                    boxes[box_idx].add(val)

        index = 0
        while index < len(empty):
            r, c = empty[index]
            box_idx = (r // 3) * 3 + (c // 3)

            if board[r][c] == '.':
                start_num = 1

            else: 
                old_num = board[r][c]
                rows[r].remove(old_num)
                cols[c].remove(old_num)
                boxes[box_idx].remove(old_num)

                start_num = int(board[r][c])+1

            found_valid_num = False

            for guess in range(start_num, 10):
                guess_str = NUMS_STR[guess]

                if (guess_str not in rows[r]) and (guess_str not in cols[c]) and (guess_str not in boxes[box_idx]):
                    board[r][c] = guess_str
                    rows[r].add(guess_str)
                    cols[c].add(guess_str)
                    boxes[box_idx].add(guess_str) 

                    found_valid_num = True
                    break

            if found_valid_num:
                index +=1
            else:
                board[r][c] = '.'
                index -=1
      
