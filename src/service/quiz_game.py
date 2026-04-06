class QuizGame:
    def __init__(self, ui):
        self.ui = ui
        self.is_running = True

    def run(self):
        """프로그램의 전체 실행 루프를 관리합니다."""
        while self.is_running:
            choice = self.ui.display_menu()
            self._handle_choice(choice)

    def _handle_choice(self, choice):
        """사용자의 선택에 따라 적절한 메서드를 호출합니다."""
        if choice == '1':
            self.ui.show_message("퀴즈 풀기 기능을 준비 중입니다.")
        elif choice == '2':
            self.ui.show_message("퀴즈 추가 기능을 준비 중입니다.")
        elif choice == '3':
            self.ui.show_message("퀴즈 목록 보기 기능을 준비 중입니다.")
        elif choice == '4':
            self.ui.show_message("최고 점수 확인 기능을 준비 중입니다.")
        elif choice == '5':
            self.ui.show_message("프로그램을 종료합니다. 이용해 주셔서 감사합니다!")
            self.is_running = False
        else:
            self.ui.show_error("잘못된 입력입니다. 1~5 사이의 숫자를 입력해 주세요.")