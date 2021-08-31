from tic_tac_toe import TicTacToeGame


def main():
    game = TicTacToeGame()
    game.show_logo()
    return game.play_game()


if __name__ == "__main__":
    # results = []
    # for i in range(1000):
    #     results.append(main())
    # for i in [-1,0,1]:
    #     print(f"The number of {i} is: {results.count(i)}")
    main()