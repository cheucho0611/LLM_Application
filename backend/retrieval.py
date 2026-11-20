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


def find_chunks(question, documents):
    question_words = [w for w in make_words(question) if len(w) > 1]
    scored = []
    for chunk in load_chunks(documents):
        content_words = make_words(chunk["text"])
        # Count question words that appear in this paragraph.
        # A word also matches when one contains the other (e.g. "commit" and "commit-particle").
        score = sum(
            1
            for word in question_words
            if any(c in word or word in c for c in content_words if len(c) > 1)
        )
        if score > 0:
            scored.append((score, chunk))
    # Highest score first, keep the best 3 paragraphs.
    scored.sort(key=lambda item: item[0], reverse=True)
    return [chunk for score, chunk in scored[:3]]
