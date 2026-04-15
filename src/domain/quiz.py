class Quiz:
    def __init__(self, question: str, options: list, answer: int, hint: str = ""):
        """
        퀴즈 도메인 객체입니다.
        :param question: 퀴즈 문제 (예: "파이썬의 창시자는?")
        :param options: 4지 선다 보기 리스트
        :param answer: 정답 번호 (1~4)
        :param hint: (선택) 문제 풀이 힌트
        """
        self.question = question
        self.options = options
        self.answer = answer
        self.hint = hint

    def check_answer(self, user_answer: int) -> bool:
        """
        사용자가 입력한 답이 정답인지 확인하여 True/False를 반환합니다.
        """
        return self.answer == user_answer

    def get_formatted_text(self, quiz_number: int = 1) -> str:
        """
        UI 계층에서 출력하기 쉽도록 퀴즈 문제와 보기를 하나의 문자열로 묶어서 반환합니다.
        """
        text = f"\nQ{quiz_number}. {self.question}\n"
        for i, option in enumerate(self.options, 1):
            text += f"  {i}) {option}\n"
        return text

    def to_dict(self) -> dict:
        """객체를 JSON 저장을 위한 딕셔너리로 변환합니다."""
        return {
            "question": self.question,
            "options": self.options,
            "answer": self.answer,
            "hint": self.hint
        }

    @classmethod
    def from_dict(cls, data: dict):
        """딕셔너리 데이터를 받아 Quiz 객체를 생성하는 팩토리 메서드입니다."""
        return cls(
            question=data["question"],
            options=data["options"],
            answer=data["answer"],
            hint=data.get("hint", "")  # 기존 데이터에 힌트가 없을 경우 빈 문자열 반환
        )