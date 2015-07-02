execfile("xlo365.py")
#sb = init_board("input_puzzles/more/9x9/9x9.5.sudoku")
sb = init_board("input_puzzles/easy/25_25.sudoku")
sb.print_board()
#print is_complete(sb)
fb = solve(sb, True, False, True, False)
fb.print_board()
# forward_checking, MRV, MCV, LCV



