from src.domin.quiz import Quiz

class QuizGame:
    def __init__(self, ui, repository):
        self.ui = ui
        self.repository = repository
        self.is_running = True
        self.quiz_data = self.repository.load_state()

    def run(self):
        try:
            while self.is_running:
                choice = self.ui.display_menu()
                self._handle_choice(choice)
        except (KeyboardInterrupt, EOFError):
            self.ui.show_message("비정상 종료 요청이 감지되었습니다.")
            self.ui.show_message("데이터를 안전하게 저장하고 프로그램을 종료합니다.")
            self.repository.save_state(self.quiz_data)

    def _handle_choice(self, choice):
        if choice == 1:
            self.play_quiz() # 퀴즈 풀기 메서드 연결
        elif choice == 2:
            self.add_quiz()
        elif choice == 3:
            self.ui.show_message("퀴즈 목록 보기 기능을 준비 중입니다.")
        elif choice == 4:
            self.ui.show_message("최고 점수 확인 기능을 준비 중입니다.")
        elif choice == 5:
            self.ui.show_message("프로그램을 종료합니다. 이용해 주셔서 감사합니다!")
            self.repository.save_state(self.quiz_data)
            self.is_running = False

    # 1. 퀴즈 시작
    def play_quiz(self):
        """퀴즈 풀기 전체 비즈니스 로직을 담당합니다."""
        quizzes = self.quiz_data.get("quizzes", [])
        
        # 1. 퀴즈가 없는 경우 처리
        if not quizzes:
            self.ui.show_error("등록된 퀴즈가 없습니다. 퀴즈를 먼저 추가해 주세요.")
            return

        self.ui.show_message("퀴즈를 시작합니다! 화이팅! 🚀")
        score = 0
        total_quizzes = len(quizzes)

        # 2. 저장된 퀴즈 출제
        for i, quiz in enumerate(quizzes, 1):
            # 딕셔너리를 직접 뒤지는 대신, Quiz 객체에게 "예쁘게 포맷팅된 문자열을 줘!"라고 요청합니다.
            quiz_text = quiz.get_formatted_text(quiz_number=i)
            
            # 퀴즈 출력
            self.ui.show_message(quiz_text) 
            
            # UI를 통해 사용자 입력 받기
            user_answer = self.ui.get_valid_number("정답을 선택하세요: ", 1, len(quiz.options))

            # Service가 직접 answer == user_answer를 비교하지 않고, 객체에게 채점을 맡깁니다.
            if quiz.check_answer(user_answer):
                self.ui.show_message("정답입니다! 🎉\n")
                score += 1
            else:
                self.ui.show_error(f"틀렸습니다. 정답은 {quiz.answer}번입니다.\n")

        # 모든 문제를 풀면 결과 표시
        self.ui.show_message(f"퀴즈 종료! 총 {total_quizzes}문제 중 {score}문제를 맞히셨습니다.")
        
        # (보너스) 최고 점수 갱신 로직
        current_high_score = self.quiz_data.get("high_score", 0)
        if score > current_high_score:
            self.ui.show_message("🌟 최고 점수 갱신! 🌟")
            self.quiz_data["high_score"] = score
            self.repository.save_state(self.quiz_data)

    # 2. 퀴즈 추가
    def add_quiz(self):
        """새로운 퀴즈를 입력받아 데이터를 추가하고 저장합니다."""
        self.ui.show_message("\n=== 📝 새로운 퀴즈 추가 ===")

        # 1. 문제 입력 (빈칸 방지)
        question = input("추가할 질문을 입력하세요: ").strip()
        while not question:
            self.ui.show_message("질문은 빈칸일 수 없습니다.")
            question = input("추가할 질문을 입력하세요: ").strip()

        # 2. 보기 입력 (4개 고정)
        options = []
        for i in range(1, 5):
            option = input(f"보기 {i}번을 입력하세요: ").strip()
            while not option:
                self.ui.show_message("보기는 빈칸일 수 없습니다.")
                option = input(f"보기 {i}번을 입력하세요: ").strip()
            options.append(option)

        # 3. 정답 입력 (ui 클래스의 메서드 활용)
        answer = self.ui.get_valid_number("정답 번호를 입력하세요 (1~4): ", 1, 4)

        # 4. 힌트 입력
        hint = input("힌트를 입력하세요 (없으면 엔터): ").strip()
        if not hint:
            hint = "제공된 힌트가 없습니다."

        # 5. 데이터 추가 (레파지토리 구조에 맞춰 Quiz 객체로 생성)
        new_quiz = Quiz(question, options, answer, hint)
        
        # 만약의 경우를 대비한 방어적 코드
        if "quizzes" not in self.quiz_data:
            self.quiz_data["quizzes"] = []
            
        # 딕셔너리가 아닌 Quiz 객체를 리스트에 추가합니다.
        self.quiz_data["quizzes"].append(new_quiz) 
        
        # 6. 저장 및 완료 메시지
        # repository.save_state가 퀴즈 객체 리스트를 알아서 to_dict()로 변환 후 저장합니다.
        self.repository.save_state(self.quiz_data)
        self.ui.show_message("\n새로운 퀴즈가 성공적으로 추가되었습니다! 🎉\n")