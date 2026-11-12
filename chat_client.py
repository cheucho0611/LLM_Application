from chat_service import answer_question

sum = 0
#          ____조건____ 연속된 숫자를 세는 함수 / for 반복문의 하나의 블럭
for num in range(1,11):
     sum += num
     print(sum)
     if sum == 21:
        break

print(sum)
print(f"1부터10까지의 총 합: {sum}")

total = 0
number = 1
while (number <= 10): # 참(Ture)일때에만 while 반복문이 실행)
    total += number
    number = number + 1
    #print(total)

print(f"1부터10까지의 총 합: {total}")

while True:

   question = input("질문(종료:q): ").strip()
   if question == "q":
      print("대화를 종료합니다.")
      break
   if not question:
      print("질문을 입력 해주세요 : ")
      continue

   answer = answer_question(question)
   print("답변:", answer)
   print() #가독성을 해서 추가한것 뿐이다.(가독성 좋다ㅁ)

#question = input("질문: ")
#answer = answer_question(question)
#print("답변:", answer)

#반복문 추가