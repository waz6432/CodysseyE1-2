import json
import os
from pathlib import Path

class QuizRepository:
    def __init__(self):
        # 프로젝트 루트 경로 기준 data.json
        self.file_path = Path(__file__).resolve().parent.parent.parent / "state.json"
        
        # 파일이 없거나 손상되었을 때 사용할 기본 데이터
        self.default_data = [
            {
                "question": "파이썬의 창시자는?", 
                "options": ["귀도 반 로섬", "제임스 고슬링", "데니스 리치", "리누스 토발즈"], 
                "answer": 1
            }
        ]

    def load_data(self):
        """데이터를 불러오고, 문제 발생 시 예외 처리를 수행합니다."""
        if not os.path.exists(self.file_path):
            print("\n[안내] 데이터 파일이 없습니다. 기본 퀴즈 데이터를 사용합니다.")
            return self.default_data

        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)
            
        except json.JSONDecodeError:
            print("\n[오류] 데이터 파일이 손상되었습니다. 기본 퀴즈 데이터로 복구(초기화)합니다.")
            self.save_data(self.default_data)
            return self.default_data
        
        except Exception as e:
            print(f"\n[오류] 알 수 없는 오류로 기본 데이터를 사용합니다: {e}")
            return self.default_data

    def save_data(self, data):
        """데이터를 JSON 파일로 안전하게 저장합니다."""
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
                
        except Exception as e:
            print(f"\n[오류] 데이터 저장에 실패했습니다: {e}")