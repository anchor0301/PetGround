name= input("본인의 이름과 학번을 입력하세요 : ")
kor = int(input("국어 점수를 입력하세요"))
mat = int(input("수학 점수를 입력하세요"))
eng = int(input("영어 점수를 입력하세요"))
sum = kor + mat+ eng
ave = float(sum/3)
print(name+f"님의 성적은\n총합 {sum}점, 평균 {ave}점 입니다.")