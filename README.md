# 💡 Python 콘솔 퀴즈 게임

계층형 아키텍처(Layered Architecture)를 적용한 콘솔 기반 퀴즈 게임입니다.
사용자는 퀴즈를 풀고/추가하고/삭제할 수 있으며, 점수와 플레이 이력은 파일에 저장됩니다.

## 1. 프로젝트 개요

- Python 표준 라이브러리만 사용 (외부 패키지 설치 불필요)
- `state.json` 기반 영속 저장
- 메뉴 중심 콘솔 인터페이스

## 2. 실행 방법 (Windows / iMac(macOS))

프로젝트 루트에서 실행하세요.

1) 저장소 클론

```bash
git clone <저장소_URL>
cd CodysseyE1-2
```

2) 실행 명령

- Windows (PowerShell/CMD)

```bash
python -m src.main
```

- iMac/macOS (Terminal)

```bash
python3 -m src.main
```

### 실행이 안 될 때 체크 포인트

- 명령은 반드시 프로젝트 루트(`README.md`, `src/`, `state.json`이 있는 위치)에서 실행
- `ModuleNotFoundError: No module named 'src'` 발생 시:
  - 현재 경로를 다시 확인

## 3. 현재 기능

- 메뉴 인터페이스
- 퀴즈 풀기
  - 문제 수 선택
  - 랜덤 출제
  - 힌트 사용(문제당 1회, 사용 시 해당 문제 점수 0점 처리)
- 퀴즈 추가
- 퀴즈 목록 보기
- 퀴즈 삭제
- 최고 점수 확인
- 점수 기록 히스토리 보기(최신순)
- 비정상 종료(Ctrl+C, EOF) 시 데이터 저장

## 4. 데이터 관리 (`state.json`)

`state.json` 파일에 아래 정보가 저장됩니다.

- `quizzes`: 문제/보기/정답/힌트
- `high_score`: 최고 점수
- `history`: 플레이 기록
  - `played_at`: 날짜/시간
  - `question_count`: 푼 문제 수
  - `score`: 점수
  - `total`: 총 문제 수(호환성용)

## 5. 파일 구조 (현재 기준)

```text
.
├── README.md
├── .gitignore
├── state.json
└── src/
    ├── __init__.py
    ├── main.py
    ├── domain/
    │   ├── __init__.py
    │   └── quiz.py                  # Quiz 도메인 모델
    ├── repository/
    │   ├── __init__.py
    │   └── quiz_repository.py       # state.json 로드/저장
    ├── service/
    │   ├── __init__.py
    │   └── quiz_game.py             # 게임 핵심 로직
    └── ui/
        ├── __init__.py
        ├── console_ui.py            # 콘솔 입출력
        └── input_handler.py         # 입력 유틸(보조)
```
