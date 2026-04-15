class ConsoleUI:
    def get_valid_number(self, prompt, min_val, max_val):
        """숫자 입력 시 발생할 수 있는 모든 예외를 처리하는 공통 메서드"""
        while True:
            # Ctrl+C, EOFError는 여기서 잡지 않고 상위(Service)로 던집니다.
            user_input = input(prompt).strip() # 1. 앞뒤 공백 제거
            
            if not user_input: # 2. 빈 입력 체크
                self.show_error("값을 입력해주세요. (빈 입력)")
                continue
                
            try:
                number = int(user_input) # 3. 숫자 변환 시도
                
                if not (min_val <= number <= max_val): # 4. 허용 범위 체크
                    self.show_error(f"허용 범위 밖 숫자입니다. {min_val}~{max_val} 사이를 입력해주세요.")
                    continue
                    
                return number
                
            except ValueError:
                self.show_error("숫자로 변환할 수 없는 입력입니다. 올바른 숫자를 입력해주세요.")

    def display_menu(self):
        """프로그램 메인 메뉴를 출력하고 안전한 입력을 받습니다."""
        print("\n" + "="*30)
        print("      🚀 QUIZ CHALLENGE")
        print("="*30)
        print(" 1. 퀴즈 풀기")
        print(" 2. 퀴즈 추가")
        print(" 3. 퀴즈 목록 보기")
        print(" 4. 최고 점수 확인")
        print(" 5. 퀴즈 삭제")
        print(" 6. 점수 기록 히스토리 보기")
        print(" 7. 프로그램 종료")
        print("="*30)
        
        # 문자열 리턴 대신, 공통 입력 함수를 사용해 1~7 사이의 정수를 리턴받음
        return self.get_valid_number("번호를 선택하세요: ", 1, 7)

    def show_message(self, message):
        print(f"\n[알림] {message}")

    def show_error(self, message):
        print(f"\n❌ [오류] {message}")