import random
from datetime import datetime

logged_user = ''
logged = False
users = []
option_letters = ['A', 'B', 'C', 'D']

def isValidPassword(password):
        if len(password) < 8:
            print("Password must be at least 8 characters.")
            return False

        hasSpecialChar = False
        for ch in password:
            if not ch.isalnum():
                hasSpecialChar = True
                break
        if not hasSpecialChar:
            print("Password must have special character")
            return False

        return True

def isValidEmail(email):
        if email.count('@') != 1:
            print("Email must contain exactly one '@' symbol.")
            return False
        if '.' not in email:
            print("Email must have .")
            return False
        if ' ' in email:
            print("Email must not have space")
            return False
        return True
    
def register():
    global logged_user, logged
    name = input("Enter username:")
    enrollment = input("Enter your Enrollment Number:")
    branch = input("Enter your Branch:")
    year = input("Enter your current Year:")
    contact = input("Enter your Contact Number:")

    while True:
        password = input("Create your password: ")
        if isValidPassword(password):
            break        
    
    while True:
        email = input("Enter your Email: ")
        if isValidEmail(email):
            print("Registered Successfully Yeee!")
            break

    users.append({'name':name, 'enrollment':enrollment, 'branch':branch, 'year':year, 'contact':contact, 'password':password, 'email':email, 'scores': {}})
    logged_user = name
    logged = True
    login()

def login():
    global logged_user, logged
    email = input("Enter your Email: ")
    password = input("Enter your password: ")

    for user in users:
        if (user['email'] == email and user['password'] == password):
            logged = True
            logged_user = user['name']
            print("Login Successfully")
            main()
            return
    print("Incorrect email or password.")
    choice = input("Try again (Try again/exit)?").lower()
    if choice == 'Try again':
        login()
    else:
        main()

def parse_ques(filepath):
    ques_list = []
    try:
        with open(filepath, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
                    ques = parts[0]
                    options = parts[1:5]
                    ans = parts[5]
                    ques_list.append({
                        "question" : ques,
                        "options" : options,
                        "answer" : ans
                        })
        return ques_list
    except FileNotFoundError:
        print("Not Found")
        return[]

def run_quiz(questions, category_name):
    global score, total_ques, logged_user, users

    random.shuffle(questions)
    quiz_questions = questions[:5]
    total = len(quiz_questions)
    score = 0
    
    for i, q_data in enumerate(quiz_questions):
        print(f"Question {i+1} : {q_data['question']}")
        option_map = {}

        for j,option in enumerate(q_data['options']):
            letter = option_letters[j]
            option_map[letter] = option
            print(f"{letter}. {option}")

        while True:
            user_input = input("Enter your choice (A, B, C or D):").strip().upper()
            if user_input in option_letters:
                user_choice_text = option_map[user_input]
                break
            else:
                print("Invalid input. Please enter A, B, C or D.")

        if user_choice_text == q_data['answer']:
            print("Correct!")
            score += 1
        else:
            print(f"Incorrect. The correct answer was: {q_data['answer']}")

    print(f"You scored {score} out of {total}.")

    for user in users:
        if user['name'] == logged_user:
            user['scores'][category_name] = []
        user['scores'][category_name].append({'marks':score, 'total_marks':total, 'datetime': datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
        
def dsa_ques():
    file_path = 'dsa_quiz.txt'
    questions = parse_ques(file_path)
    if questions:
        run_quiz(questions,'DSA')

def dbms_ques():
    file_path = 'dbms_quiz.txt'
    questions = parse_ques(file_path)
    if questions:
        run_quiz(questions,'DBMS')

def python_ques():
    file_path = 'python_quiz.txt'
    questions = parse_ques(file_path)
    if questions:
        run_quiz(questions,'Python')

def attempt_quiz():
    print("Quiz Categories")
    print("1. DSA")
    print("2. DBMS")
    print("3. Python")
    print("4. Back to Profile Menu")

    while True:
        choice = input("Select category (1-4)")
        if choice == '1':
            dsa_ques()
            main()
        elif choice == '2':
            dbms_ques()
            main()
        elif choice == '3':
            python_ques()
            main()
        elif choice == '4':
            main()
            break
        else:
            print("Invalid choice")
            main()
    
def show_profile():
    current_user = None
    for user in users:
        if user['name'] == logged_user:
            current_user = user
            break
    
    if logged == True:
        print("PROFILE")
        print(f"Name: {current_user.get('name')}")
        print(f"Enrollment: {current_user.get('enrollment')}")
        print(f"Email: {current_user.get('email')}")
        print(f"Branch: {current_user.get('branch')}")
        print(f"Year: {current_user.get('year')}")
        print(f"Contact: {current_user.get('contact')}")
    main()
        
def update_profile():
    global logged_user
    newName = input("Enter new username:")
    for user in users:
        if (user['name'] == logged_user):
            user['name'] = newName
            logged_user = newName
        newBranch = input(f"Enter new Branch (Current: {user['branch']}): ")
        if newBranch:
            user['branch'] = newBranch

        newYear = input(f"Enter new Year (Current: {user['year']}): ")
        if newYear:
            user['year'] = newYear

        newContact = input(f"Enter new Contact (Current: {user['contact']}): ")
        if newContact:
            user['contact'] = newContact
            
        print("Profile Updated Successfully")
    main()
    
def logout():
    global logged_user, logged
    logged_user = ''
    logged = False
    print("Logged out Successfully")
    main()
 
def terminate():
    exit()

def main():
    if logged == False:
        response = input("""
                         Choose option:
                         1. Registration
                         2. Login
                         3. Exit
                         select option 1/2/3:""")
        if response == '1':
            register()
        elif response == '2':
            login()
        elif response == '3':
            terminate()
        else:
            print("Please select correct option")
            main()

    else:
        response = input('''
                         Choose option:
                         1. Quiz
                         2. Profile
                         3. Update profile
                         4. Logout
                         5. Exit

            select option 1/2/3/4/5: ''')

    if response == '1':
        attempt_quiz()
    elif response == '2':
        show_profile()
    elif response == '3':
        update_profile()
    elif response == '4':
        logout()
    elif response == '5':
        terminate()
    else:
        print("Invalid Choice")
        main()
        
print("Welcome to LNCT")
main()













