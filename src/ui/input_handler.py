import sys

def get_valid_number(prompt: str, min_val: int, max_val: int) -> int:
    """
    안전하게 숫자를 입력받는 공통 함수
    """
    while True:
        try:
            # 1. 입력 앞뒤 공백 제거 및 빈 입력 체크
            user_input = input(prompt).strip()
            
            if not user_input:
                print("안내: 값을 입력해주세요. (빈 입력)")
                continue
                
            # 2. 숫자 변환 시도
            number = int(user_input)
            
            # 3. 허용 범위 체크
            if not (min_val <= number <= max_val):
                print(f"안내: {min_val}에서 {max_val} 사이의 숫자를 입력해주세요.")
                continue
                
            return number
            
        except ValueError:
            # 숫자 변환 실패 (예: abc 입력)
            print("안내: 숫자로 변환할 수 없는 입력입니다. 올바른 숫자를 입력해주세요.")
            
        except (KeyboardInterrupt, EOFError):
            # 프로그램 실행 중 Ctrl+C 또는 EOF 발생 시 비정상 종료 방지
            print("\n\n안내: 프로그램 종료 요청이 감지되었습니다.")
            print("데이터를 안전하게 저장하고 프로그램을 종료합니다.")
            
            # TODO: 여기에 Service나 Repository를 호출하여 데이터 저장하는 로직 추가
            # 예: quiz_service.save_current_state()
            
            sys.exit(0) # 안전하게 정상 종료 처리