from src.ui.console_ui import ConsoleUI
from src.service.quiz_game import QuizGame
from src.repository.quiz_repository import QuizRepository

def main():
    # 1. 사용할 객체들을 생성합니다.
    ui = ConsoleUI()
    repository = QuizRepository()
    
    # 2. 의존성 주입(DI)으로 Service에 필요한 부품들을 조립합니다.
    game = QuizGame(ui, repository)
    
    # 3. 게임 시작!
    game.run()

if __name__ == "__main__":
    main()