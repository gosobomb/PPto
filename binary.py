# 사용자가 입력할 진법 선택 (16진수, 10진수, 8진수, 2진수)
base = int(input("입력 진수 결정(16/10/8/2) : "))
value = input("값 입력 : ")

# 입력된 값을 주어진 진법으로 변환하여 10진수 정수로 변환
num = int(value, base)

# 변환된 값을 다양한 진법으로 출력
print(f"16진수 ==> {hex(num)}")
print(f"10진수 ==> {num}")
print(f"8진수 ==> {oct(num)}")
print(f"2진수 ==> {bin(num)}") 