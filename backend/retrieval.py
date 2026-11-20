"""Supabase가 허용한 현재 사용자의 문서에서 문단을 검색합니다."""


def load_chunks(documents):
    chunks = []
    for document in documents:
        for paragraph in document["content"].split("\n\n"):
            paragraph = paragraph.strip()
            if paragraph:
                chunks.append(
                    {"source": document["filename"], "text": paragraph}
                )
    return chunks


def make_words(text):
    cleaned = text.lower()
    for mark in "?!,./:()-":
        cleaned = cleaned.replace(mark, " ")
    return cleaned.split()


# Filler words that carry no topic information.
STOP_WORDS = {"대해", "대해서", "알려줘", "설명해줘", "알려주세요", "설명해주세요", "뭐야", "무엇인가요"}


def find_chunks(question, documents):
    question_text = question.lower()
    # Documents whose file name is written in the question.
    mentioned = set()
    cleaned_question = question_text
    for document in documents:
        name = document["filename"].lower()
        stem = name.rsplit(".", 1)[0]
        if name in question_text or stem in question_text:
            mentioned.add(document["filename"])
            # Remove the file name so it does not count as a topic word.
            cleaned_question = cleaned_question.replace(name, " ").replace(stem, " ")

    question_words = [
        w for w in make_words(cleaned_question) if len(w) > 1 and w not in STOP_WORDS
    ]
    scored = []
    for chunk in load_chunks(documents):
        content_words = make_words(chunk["text"])
        # Count question words that appear in this paragraph.
        # A word also matches when one contains the other.
        score = sum(
            1
            for word in question_words
            if any(c in word or word in c for c in content_words if len(c) > 1)
        )
        # A named file puts its paragraphs first, in file order.
        if chunk["source"] in mentioned:
            score += 100
        if score > 0:
            scored.append((score, chunk))
    # Highest score first (stable sort keeps file order on ties), keep the best 3.
    scored.sort(key=lambda item: item[0], reverse=True)
    return [chunk for score, chunk in scored[:3]]
