# src/repository/quiz_repository.py
import json
import os
from pathlib import Path
from src.domin.quiz import Quiz

class QuizRepository:
    def __init__(self):
        # 루트 경로의 state.json
        self.file_path = Path(__file__).resolve().parent.parent.parent / "state.json"
        
        # [기본 데이터 정의] 파일이 없거나 손상되었을 때 사용할 비상용 데이터
        self.default_quizzes = [
            Quiz("C#에서 값 타입(Value Type)에 해당하는 것은?", ["string", "object", "class", "int"], 4, "구조체(struct)와 기본 숫자 데이터 타입은 값 타입입니다."),
            Quiz("ASP.NET MVC 패턴에서 사용자의 요청을 제어하는 역할은?", ["Model", "View", "Controller", "ViewModel"], 3, "라우팅을 통해 가장 먼저 호출되는 곳입니다."),
            Quiz(".NET에서 메모리를 자동으로 관리하는 시스템은?", ["JIT 컴파일러", "Garbage Collector", "CLR", "MSIL"], 2, "사용하지 않는 객체를 알아서 해제해줍니다."),
            Quiz("MSSQL에서 기존 데이터를 수정하는 명령어는?", ["SELECT", "INSERT", "UPDATE", "DELETE"], 3, "WHERE 조건과 함께 주로 사용됩니다."),
            Quiz("C#에서 상속이나 인터페이스 구현 시 사용하는 기호는?", [":", "::", "->", "=>"], 1, "클래스 이름 뒤에 붙여서 사용합니다.")
        ]

    def load_state(self):
        """파일 상태를 체크하여 적절한 데이터를 Quiz 객체 리스트로 반환합니다."""
        
        # 1. 파일이 아예 없는 경우
        if not self.file_path.exists():
            print("\n[안내] 데이터 파일(state.json)이 존재하지 않아 기본 퀴즈 데이터를 로드합니다.")
            return self._get_default_state()

        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                
                # 데이터가 비어있거나 잘못된 구조일 경우를 위한 방어
                quizzes_data = data.get("quizzes", [])
                if not quizzes_data:
                    return self._get_default_state()

                # 성공적으로 읽어온 경우 Quiz 객체로 변환
                data["quizzes"] = [Quiz.from_dict(q) for q in quizzes_data]
                return data

        # 2. 파일이 손상된 경우 (JSON 파싱 에러)
        except json.JSONDecodeError:
            print("\n❌ [오류] 데이터 파일이 손상되었습니다. 기본 데이터로 복구(초기화)합니다.")
            default_state = self._get_default_state()
            # 손상된 파일을 기본 데이터로 덮어씌워 복구
            self.save_state(default_state)
            return default_state
            
        except Exception as e:
            print(f"\n[오류] 알 수 없는 문제가 발생했습니다: {e}")
            return self._get_default_state()

    def _get_default_state(self):
        """기본 구조를 가진 딕셔너리를 반환하는 헬퍼 메서드"""
        return {
            "quizzes": self.default_quizzes,
            "high_score": 0,
            "history": []
        }

    def save_state(self, state):
        """Quiz 객체를 딕셔너리로 변환하여 안전하게 저장합니다."""
        try:
            state_to_save = {
                "quizzes": [quiz.to_dict() for quiz in state.get("quizzes", [])],
                "high_score": state.get("high_score", 0),
                "history": state.get("history", [])
            }
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(state_to_save, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"\n[오류] 파일 저장 중 문제가 발생했습니다: {e}")