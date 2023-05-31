from utils import multiple_grain_analysis

cases = multiple_grain_analysis()

for case in cases:
    print("\n ---- \n")
    print(case[0])
    print("   ")
    # print(case[1][0])
    print("Mean:", case[1][1][0])
    print("STD:", case[1][1][1])
    print("\n ---- \n")
