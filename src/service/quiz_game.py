class QuizGame:
    def __init__(self, ui, repository):
        self.ui = ui
        self.repository = repository
        self.is_running = True
        
        # 프로그램 시작 시 데이터 로드
        self.quiz_data = self.repository.load_data()

    def run(self):
        """프로그램의 전체 실행 루프를 관리하고 강제 종료를 방어합니다."""
        try:
            while self.is_running:
                choice = self.ui.display_menu()
                self._handle_choice(choice)
                
        except (KeyboardInterrupt, EOFError):
            # 프로그램 실행 중 Ctrl+C 또는 입력 스트림 종료 발생 시
            self.ui.show_message("비정상 종료 요청이 감지되었습니다.")
            self.ui.show_message("데이터를 안전하게 저장하고 프로그램을 종료합니다.")
            self.repository.save_data(self.quiz_data)

    def _handle_choice(self, choice):
        """정수(int)형태로 들어온 사용자의 선택을 처리합니다."""
        if choice == 1:
            self.ui.show_message("퀴즈 풀기 기능을 준비 중입니다.")
        elif choice == 2:
            self.ui.show_message("퀴즈 추가 기능을 준비 중입니다.")
        elif choice == 3:
            self.ui.show_message("퀴즈 목록 보기 기능을 준비 중입니다.")
        elif choice == 4:
            self.ui.show_message("최고 점수 확인 기능을 준비 중입니다.")
        elif choice == 5:
            self.ui.show_message("프로그램을 종료합니다. 이용해 주셔서 감사합니다!")
            self.repository.save_data(self.quiz_data) # 정상 종료 시에도 저장
            self.is_running = False