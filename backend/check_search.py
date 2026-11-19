from retrieval import find_chunks

# 질문을 직접 입력합니다. 예: git commit, chmod 권한
# CI/CD 파이프라인, 오늘 날씨도 입력해 보세요.
while True:
    question = input("질문 입력 (끝내려면 종료): ")
    if question == "종료":
        break  # 반복문을 끝냅니다.
    matches = find_chunks(question)
    print("찾은 문단 수: ", len(matches))

    # 검색 결과가 없을 때
    if not matches:
        print("자료에서 관련 내용을 찾지 못했습니다.\n")

    for match in matches:
        print(f"파일 : {match['source']}")
        print(f"내용 앞부분 : {match['text'][:80]}\n")
