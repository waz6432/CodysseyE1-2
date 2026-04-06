from src.ui.console_ui import ConsoleUI
from src.service.quiz_game import QuizGame

def main():
    # 의존성 주입(DI) 느낌으로 UI 객체를 넘겨줍니다.
    ui = ConsoleUI()
    game = QuizGame(ui)
    
    # 게임 시작!
    game.run()

if __name__ == "__main__":
    main()