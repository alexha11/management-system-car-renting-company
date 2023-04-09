import datetime 
from datetime import date
from datetime import datetime
from datetime import timedelta
import os 
import calendar

trans_action = ""
email_customer_temp = ""                 

def is_customer(name):  #THIS FUNCTION IS TO TEST WHETHER OR NOT THE CUSTOMER ALREADY EXITS IN THE FILE Customers.txt(IF yes return true, no return false)
	file_customers = open("Customers.txt", "r", encoding='UTF-8')
	while True:
		text = file_customers.readline()
		if text == '':
			break
		else:
			data = text.split(",")
			#print("TEST " + car + " " + data[0] + "\n") for testing this function works properly
			if name == str(data[1]): 				
				file_customers.close()
				return True
	file_customers.close()
	return False

def is_car_rented(register_number): #THIS FUNCTION IS TO TEST WHETHER OR NOT THE CAR IS RENTED(IF yes return true, no return false)
	file_rentedVehicles = open("rentedVehicles.txt", "r", encoding='UTF-8')
	while True:
		text = file_rentedVehicles.readline()
		if text == '':
			break
		else:
			data = text.split(",")
			#print("TEST " + car + " " + data[0] + "\n") for testing this function works properly
			if register_number == str(data[0]): 				
				file_rentedVehicles.close()
				return True
	file_rentedVehicles.close()
	return False

def validate_email(email_customer): #THIS FUNCTION IS TO VALIDATE EMAIL FROM CUSTOMER (EMAIL MUST CONTAIN "@" OR ".")
    global email_customer_temp
    if email_customer.find('.') == -1 or email_customer.find('@') == -1:
        print("Your email must contain symbol '@' and dot'.', please try again with a new one")
        email_customer = str(input("Enter your email:\n"))
        email_customer_temp = email_customer
        validate_email(email_customer)

def validate_age(birthday_user): #THIS FUNCTION IS TO VALIDATE AGE FROM CUSTOMER (CHECK THE AGE BELOW 100 AND AT LEAST 18)
    global rented_vehicles

    birthday = datetime.strptime(birthday_user,'%d/%m/%Y')
    current_time_tempt = date.today()
    current_time = current_time_tempt.strftime("%d/%m/%Y")
    time = datetime.strptime(current_time, "%d/%m/%Y")
    delta = abs(birthday - time)

    age = round(delta.days/365)
    if age < 18 or age > 100:
        print("Wrong age, your age must be below 100 years and at least 18 years")
        return False
    else:
        print(f"Your age is {age}, Acceptable")
        return True
        

def get_money_rented_car(register_number): #THIS FUNCTION IS TO GET DAILY COST OF THE RENT IN Vehicles.txt
	file_vehicles = open("Vehicles.txt", "r", encoding="UTF-8")
	while True:
		text = file_vehicles.readline()
		if text == '':
			break
		else: 
			data = text.split(",")
			if register_number == data[0]:
				file_vehicles.close()
				return data[2]
			

def get_time_and_remove_rented_car(register_number): #THIS FUNCTION IS TO GET THE TIME WHEN RENTING THE CAR IS RENTED AND REMOVE THE RENTED CAR IN FILE rentedVehicles.txt
    data_temp = ""
    global trans_action
    with open("rentedVehicles.txt", "r") as input:
        with open("temp.txt", "w") as output:
        # iterate all lines from file
            for line in input:
            # if text matches then don't write it
                data = line.split(",")
                if data[0] != register_number:
                    output.write(line)
                    #print(data[0] + " " + register_number + "\n")
                else:
                	data_temp = data[2]
                	trans_action = trans_action + line
    # replace file with original name
    os.replace('temp.txt', 'rentedVehicles.txt')
    return data_temp

def calculate_time(date_now ,date_rented):         # THIS FUNCTION IS TO CALCULATE HOW MANY DAYS DOES THE CUSTORMER RENTE THE CARE
	date_rented = date_rented.strip("\n")   
	data1 = datetime.strptime(date_rented, "%d/%m/%Y %H:%M")
	time_renting = date_now - data1
	return time_renting.days

def case1(): 
    file_vehicles = open("Vehicles.txt","r", encoding='UTF-8') 
    while True:
	    text = file_vehicles.readline()                           #basically way to get data from file Vehicles.txt 
	    if text == '':
		    break
	    else:
		    data = list(text.split(","))
		    if is_car_rented(str(data[0])) == False:            #check the car is rented
		        data[3] = data[3].strip("\n")   
		        print(f"* Reg. nr: {data[0]}, Model: {data[1]}, Price per day: {data[2]}")
		        sep = ", "
		        properties = sep.join(data[3:]).strip("\n")           #some small adjustment to have proper outputs
		        print(f"Properties: {properties}")

    file_vehicles.close()

def case2():
	global email_customer_temp
	last_name_customer = ""

	while True: 
		register_number = input("Give the register number of the car your want to rent:\n")
		if is_car_rented(register_number) == True:
			print("this car is not available")      									#check is car rented (if not allow customer to rent, yes announce and require custome type new register number of the car)
		else:
			print("this car is available")
			break
	birthday_user = input("Please enter you birthday in the form DD/MM/YYYY:\n")

	while True:
		try: 
			data_object = datetime.strptime(birthday_user, "%d/%m/%Y")                    #check is birthday of user correct
			break
		except ValueError:
			print("Wrong")
			birthday_user = str(input("Please type your birthday with the form 'DD/MM/YYYY'\n"))
	if validate_age(birthday_user) == False:
		return
	name_customer = str(input("Enter the customer's name:\n"))                  #check is age of customer 18-100

	if is_customer(name_customer) == True:
		print("The customer has already had an account!")          #check does customer have an account 
		return
	else:
		print("The customer has not had an account, let make a new one")				
		last_name_customer = str(input("Enter your last name\n"))
		email_address = str(input("Enter your email\n"))                        #if the customer doesn't have an account, requiring custumer type their last name, their email
		email_customer_temp = email_address
		validate_email(email_address)  #check does email contain symbol "." or "@" 

	file_customers = open("Customers.txt", "a", encoding="UTF-8")
	file_customers.write(f'{birthday_user},{name_customer},{last_name_customer},{email_customer_temp}\n')     #the data of a new customer is appended to the file Customers.txt
	file_customers.close()

	current_time = datetime.now()
	current_time = current_time.strftime("%d/%m/%Y %H:%M")

	file_rentedVehicles = open("rentedVehicles.txt", "a", encoding="UTF-8")
	file_rentedVehicles.write(f"{register_number},{birthday_user},{current_time}\n")        #the data of a new register number car is appended to the file rentedVehicles.txt
	file_rentedVehicles.close()

	print(f'Hello {name_customer}')
	print(f'You rented the car {register_number}')       #display the confirmation of the rent to the screen
	

def case3(register_number):
	global trans_action
	if is_car_rented(register_number) == True:
		time_renting = str(get_time_and_remove_rented_car(register_number))        #find the time when reting the car, at the same time revome the rented car from the file rentedVehicles.txt
		money_per_hour = int(get_money_rented_car(register_number))       #find the daily cost of the rent

		time = calculate_time(datetime.now(), time_renting) + 1                 # computes the number of the days
		print(f"The rent lasted {time} days and the cost is {time * money_per_hour}.00 euros")       #computes the cost of renting

		trans_action = trans_action.strip("\n")   
		now = datetime.now()
		trans_action = trans_action + "," + str(now.strftime("%d/%m/%Y %H:%M")) + "," + str(time) + "," + str(time * money_per_hour) + ".00" + "\n"              #display the number of days and the cost to the screen for customer
 
		file_transActions = open("transActions.txt", "a", encoding="UTF-8")
		file_transActions.write(trans_action)                                  #data of renting is appended to the file transActions.txt
		file_transActions.close()
		trans_action = ""

	else:
		print("The car with this register number does not exist or is not rented")


def case4():
    file_transActions = open("transActions.txt","r", encoding='UTF-8')
    sum_money = 0.00
    while True:
	    text = file_transActions.readline()
	    if text == '':
		    break
	    else:
		    data = text.split(",") 
		    data[5] = data[5].strip("\n") 
		    
		    sum_money = sum_money + float(data[5])                                   #calculate the earned money 
    file_transActions.close()
    return format(sum_money, "0.2f")

while True:
	print("You may select one of the following:\n" + "1) List available cars\n" + "2) Rent a car\n" + "3) Return a car\n" + "4) Count the money\n" + "0) Exit")
	#printing the menu
	number_selection = int(input("What is your selection?\n"))
	if number_selection < 0 or number_selection > 4:
		print("Please select again (the number should be 0-4)")
	if number_selection == 1:
		print("The following cars are available:")
		case1()
	if number_selection == 2:															#dividing the program into functions
		case2()
	if number_selection == 3:
	    register_number = input("Give the register number of the car your want to return:\n")
	    case3(register_number)
	if number_selection == 4:
		print(f"The total amount of money is {case4()} euros")
	if number_selection == 0:
		break











