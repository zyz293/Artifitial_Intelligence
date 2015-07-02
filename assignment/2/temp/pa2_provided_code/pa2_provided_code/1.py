execfile("MancalaGUI.py")

player1 = Player(1, Player.ABPRUNE)
player2 = Player(2, Player.CUSTOM, 10)
startGame(player1, player2)