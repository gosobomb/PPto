print("1. 입력한 수식 계산  2. 두 수 사이의 합계")
a = int(input("번호를 선택하세요: "))

if a == 1:
    expr = input("*** 수식을 입력하세요: ")
    result = eval(expr)  # eval()을 사용하여 수식 계산
    print(f"{expr} 결과는 {result}입니다.")
    
elif a == 2:
    n = int(input("*** 첫 번째 숫자를 입력하세요: "))
    m = int(input("*** 두 번째 숫자를 입력하세요: "))
    S = ((n+m) * (m-n+1)/2) 
    print(f"{n} + ... + {m}는 {S}입니다.")
    
else:
    print("잘못된 선택입니다.")