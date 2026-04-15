import random
from datetime import datetime

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
            self.show_quiz_list()
        elif choice == 4:
            self.show_high_score()
        elif choice == 5:
            self.delete_quiz()
        elif choice == 6:
            self.show_score_history()
        elif choice == 7:
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

        question_count = self.ui.get_valid_number(
            f"몇 문제를 풀까요? (1~{len(quizzes)}): ",
            1,
            len(quizzes)
        )
        selected_quizzes = random.sample(quizzes, question_count)

        self.ui.show_message("퀴즈를 시작합니다! 화이팅! 🚀")
        score = 0
        total_quizzes = len(selected_quizzes)

        # 2. 저장된 퀴즈를 랜덤 순서로 출제
        for i, quiz in enumerate(selected_quizzes, 1):
            # 딕셔너리를 직접 뒤지는 대신, Quiz 객체에게 "예쁘게 포맷팅된 문자열을 줘!"라고 요청합니다.
            quiz_text = quiz.get_formatted_text(quiz_number=i)
            
            # 퀴즈 출력
            self.ui.show_message(quiz_text) 

            # 힌트는 문제당 1번만 허용하며, 사용 시 해당 문제 점수 1점 차감
            hint_used = False
            while True:
                user_answer = self.ui.get_valid_number(
                    f"정답을 선택하세요 (1~{len(quiz.options)}, 힌트: 0): ",
                    0,
                    len(quiz.options)
                )

                if user_answer != 0:
                    break

                if hint_used:
                    self.ui.show_error("이 문제에서는 이미 힌트를 사용했습니다.")
                    continue

                if quiz.hint:
                    self.ui.show_message(f"💡 힌트: {quiz.hint}")
                    hint_used = True
                else:
                    self.ui.show_message("이 문제에는 등록된 힌트가 없습니다.")

            # Service가 직접 answer == user_answer를 비교하지 않고, 객체에게 채점을 맡깁니다.
            if quiz.check_answer(user_answer):
                earned_score = 0 if hint_used else 1
                score += earned_score

                if hint_used:
                    self.ui.show_message("정답입니다! (힌트 사용으로 0점)\n")
                else:
                    self.ui.show_message("정답입니다! 🎉\n")
            else:
                self.ui.show_error(f"틀렸습니다. 정답은 {quiz.answer}번입니다.\n")

        # 모든 문제를 풀면 결과 표시
        self.ui.show_message(f"퀴즈 종료! 총 {total_quizzes}문제 중 {score}문제를 맞히셨습니다.")
        
        # 최고 점수 비교 후 필요 시 갱신
        current_high_score = self.quiz_data.get("high_score", 0)
        if score > current_high_score:
            self.ui.show_message("🌟 최고 점수 갱신! 🌟")
            self.quiz_data["high_score"] = score

        # 플레이 이력 저장 (아직 퀴즈를 풀지 않은 경우 판단에 사용)
        if "history" not in self.quiz_data or not isinstance(self.quiz_data["history"], list):
            self.quiz_data["history"] = []
        played_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.quiz_data["history"].append({
            "played_at": played_at,
            "question_count": total_quizzes,
            "score": score,
            "total": total_quizzes
        })

        # 파일에 최신 상태를 저장
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

    # 3. 퀴즈 목록 보기
    def show_quiz_list(self):
        """저장된 퀴즈 목록을 출력합니다."""
        quizzes = self.quiz_data.get("quizzes", [])

        # 1. 퀴즈가 없는 경우 처리
        if not quizzes:
            self.ui.show_error("저장된 퀴즈가 없습니다. 먼저 퀴즈를 추가해 주세요.")
            return

        # 2. 저장된 퀴즈 목록 확인
        self.ui.show_message("\n=== 📚 저장된 퀴즈 목록 ===")
        for index, quiz in enumerate(quizzes, 1):
            self.ui.show_message(f"{index}. {quiz.question}")

    # 5. 퀴즈 삭제
    def delete_quiz(self):
        """등록된 퀴즈를 선택해 삭제합니다."""
        quizzes = self.quiz_data.get("quizzes", [])

        if not quizzes:
            self.ui.show_error("삭제할 퀴즈가 없습니다.")
            return

        self.ui.show_message("\n=== 🗑️ 퀴즈 삭제 ===")
        for index, quiz in enumerate(quizzes, 1):
            self.ui.show_message(f"{index}. {quiz.question}")

        choice = self.ui.get_valid_number(
            f"삭제할 퀴즈 번호를 선택하세요 (취소: 0, 1~{len(quizzes)}): ",
            0,
            len(quizzes)
        )

        if choice == 0:
            self.ui.show_message("퀴즈 삭제를 취소했습니다.")
            return

        removed_quiz = quizzes.pop(choice - 1)
        self.repository.save_state(self.quiz_data)
        self.ui.show_message(f"'{removed_quiz.question}' 퀴즈를 삭제했습니다.")

    # 4. 최고 점수 확인
    def show_high_score(self):
        """최고 점수를 출력합니다."""
        history = self.quiz_data.get("history", [])

        # 1. 아직 퀴즈를 풀지 않은 경우 처리
        if not history:
            self.ui.show_message("아직 퀴즈를 푼 기록이 없습니다. 먼저 퀴즈를 풀어보세요!")
            return

        # 2. 최고 점수 확인
        high_score = self.quiz_data.get("high_score", 0)
        self.ui.show_message(f"현재 최고 점수는 {high_score}점입니다.")

    # 6. 점수 기록 히스토리 보기
    def show_score_history(self):
        """모든 게임 점수 기록을 최신순으로 출력합니다."""
        history = self.quiz_data.get("history", [])

        if not history:
            self.ui.show_message("아직 저장된 점수 기록이 없습니다.")
            return

        self.ui.show_message("\n=== 📈 점수 기록 히스토리 ===")
        for index, record in enumerate(reversed(history), 1):
            played_at = record.get("played_at", "기록 시간 없음")
            question_count = record.get("question_count", record.get("total", 0))
            score = record.get("score", 0)
            self.ui.show_message(
                f"{index}. {played_at} | 문제 수: {question_count} | 점수: {score}"
            )