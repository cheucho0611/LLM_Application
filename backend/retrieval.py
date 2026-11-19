from pathlib import Path

# 이 파일이 있는 backend 폴더 아래의 data 폴더
DATA_DIR = Path(__file__).resolve().parent / "data"


# 사용자 정의 함수 만들기
def load_chunks():
    chunks = []  # 문단을 담은 빈 목록
    # data 폴더의 TXT파일을 하나씩 읽습니다.
    for path in sorted(DATA_DIR.glob("*.txt")):
        text = path.read_text(encoding="utf-8")
        # 빈 줄을 기준으로 문단을 나눕니다.
        for paragraph in text.split("\n\n"):
            paragraph = paragraph.strip()  # 오류를 방지하기 위해서 공백을 제거
            if paragraph:  # 비어 있지 않은 문단만 저장
                chunks.append({
                    "source": path.name,  # 원본 파일명
                    "text": paragraph,  # 문단 내용
                })
    return chunks  # 모든 파일의 문단 목록


# 사용자 정의함수 추가
def make_words(text):
    # 대문자를 소문자로 통일합니다.
    cleaned = text.lower()
    # 문장부호를 공백으로 바꿉니다.
    for mark in "?!,./:()-_`'\"":
        cleaned = cleaned.replace(mark, " ")
    # 공백을 기준으로 단어 목록을 만듭니다.
    return cleaned.split()


def find_chunks(question, limit=3):
    # Turn the question into a word list (skip 1-letter words)
    question_words = [w for w in make_words(question) if len(w) > 1]
    scored = []
    for chunk in load_chunks():
        content_words = make_words(chunk["text"])
        source_words = make_words(chunk["source"])
        # Score = how many question words appear in this paragraph
        score = sum(1 for w in question_words if w in content_words)
        # Bonus when the question mentions this file name (e.g. git_basics.txt)
        score += sum(2 for w in question_words if w in source_words and w != "txt")
        if score > 0:
            scored.append((score, chunk))
    # Highest score first; ties keep the original order
    scored.sort(key=lambda item: item[0], reverse=True)
    return [chunk for score, chunk in scored[:limit]]
