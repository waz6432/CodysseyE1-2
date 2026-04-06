class ConsoleUI:
    @staticmethod
    def display_menu():
        """프로그램 메인 메뉴를 출력합니다."""
        print("\n" + "="*30)
        print("      🚀 QUIZ CHALLENGE")
        print("="*30)
        print(" 1. 퀴즈 풀기")
        print(" 2. 퀴즈 추가")
        print(" 3. 퀴즈 목록 보기")
        print(" 4. 최고 점수 확인")
        print(" 5. 프로그램 종료")
        print("="*30)
        return input("번호를 선택하세요: ")

    @staticmethod
    def show_message(message):
        """알림 메시지를 출력합니다."""
        print(f"\n[알림] {message}")

    @staticmethod
    def show_error(message):
        """에러 메시지를 출력합니다."""
        print(f"\n❌ [오류] {message}")