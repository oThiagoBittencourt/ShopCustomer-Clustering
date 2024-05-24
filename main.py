from NewInstance import new_instance

def instance_inputs():
    gender = str
    while True:
        match int(input("\nGender:\n1.Male\n2.Female\n\nSelect an option above: ")):
            case 1:
                gender = "Male"
                break
            case 2:
                gender = "Female"
                break
    age = int(input("Age: "))
    annualIncome = int(input("Annual Income: "))
    spendingScore = int(input("Spending Score: "))
    profession = str
    while True:
        match int(input("\nProfession:\n1.Artist\n2.Doctor\n3.Engineer\n4.Entertainment\n5.Executive\n6.Healthcare\n7.Homemaker\n8.Lawyer\n9.Marketing\n\nSelect an option above: ")):
            case 1:
                profession = "Artist"
                break
            case 2:
                profession = "Doctor"
                break
            case 3:
                profession = "Engineer"
                break
            case 4:
                profession = "Entertainment"
                break
            case 5:
                profession = "Executive"
                break
            case 6:
                profession = "Healthcare"
                break
            case 7:
                profession = "Homemaker"
                break
            case 8:
                profession = "Lawyer"
                break
            case 9:
                profession = "Marketing"
                break
    workExperience = int(input("Work Experience: "))
    familySize = int(input("Family Size: "))
    return gender, age, annualIncome, spendingScore, profession, workExperience, familySize

while True:
    try:
        print("\n### SHOP CUSTOMER CLUSTER ###")
        print("\n1.Insert a new Instance\n2.Exit\n")
        match int(input("Select an option above: ")):
            case 1:
                gender, age, annualIncome, spendingScore, profession, workExperience, familySize = instance_inputs()
                new_instance(gender, age, annualIncome, spendingScore, profession, workExperience, familySize)
            case 2:
                break
    except:
        print("ERROR!")