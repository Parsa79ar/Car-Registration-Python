import random

class CarLotterySystem:
    def __init__(self):
        self.users = {}
        self.cars = []

    def load_cars_from_file(self, filename="cars.txt"):
        with open(filename, "r") as file:
            lines = file.read().strip().split('\n')
            
            for line in lines:
                parts = line.split('-')
                if len(parts) >= 5:
                    company = parts[0].strip()
                    country = parts[1].strip()
                    model = parts[2].strip()
                    year = parts[3].strip()
                    price = parts[4].strip()

                    car_info = f"{company} {model} ({year}) - {price}"
                    self.cars.append(car_info)
                else:
                    print(f"Invalid data in line: {line}. Skipping.")

    def register_user(self, name, family, national_code):
        user_id = str(national_code)
        if user_id not in self.users:
            self.users[user_id] = {"name": name, "family": family, "cars_registered": []}
        return user_id

    def show_available_cars(self):
        return self.cars

    def register_car_for_user(self, user_id, car_index):
        if str(user_id) not in self.users:
            return "User not registered. Please register first."

        user = self.users[str(user_id)]
        if 0 <= car_index < len(self.cars):
            car = self.cars[car_index]
            user["cars_registered"].append(car)
            return f"Car registered successfully for the lottery: {car}"
        else:
            return "Invalid car index."

    def show_winners(self, filename="lottery_results.txt"):
        result = []
        try:
            with open(filename, "r") as file:
                lines = file.readlines()
                for line in lines:
                    result.append(line.strip())
        except FileNotFoundError:
            return "No winners found."
        return result
    
    def draw_random_winners(self):
        total_users = len(self.users)
        num_winners = max(1, int(total_users * 0.05)) 
        winners = []
        for _ in range(num_winners):
            user_id = random.choice(list(self.users.keys()))
            user = self.users[user_id]
            
            if user["cars_registered"]:
                winner_car = random.choice(user["cars_registered"])
                winners.append({"user_id": user_id, "winner_car": winner_car})

        with open("lottery_results.txt", "w") as file:
            for winner in winners:
                file.write(f"{winner['user_id']} won the car: {winner['winner_car']}\n")
        return winners

def main():
    lottery_system = CarLotterySystem()
    lottery_system.load_cars_from_file()

    while True:
        print("\n1. Register/Login\n2. Show Available Cars\n3. Register Car for User\n4. Show Winners\n5. Lottery (5% of total users)\n6. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter your name: ")
            family = input("Enter your family name: ")
            national_code = input("Enter your national code: ")

            user_id = lottery_system.register_user(name, family, national_code)
            print(f"User registered successfully. Your user ID: {user_id}")

        elif choice == "2":
            available_cars = lottery_system.show_available_cars()
            print("Available Cars:")
            for i, car in enumerate(available_cars, 1):
                print(f"{i}. {car}")

        elif choice == "3":
            national_code = input("Enter your national code: ")
            if user_id:
                available_cars = lottery_system.show_available_cars()
                print("Available Cars:")
                for i, car in enumerate(available_cars, 1):
                    print(f"{i}. {car}")
                
                car_index = int(input("Enter the index of the car you want to register for the lottery: ")) - 1
                result = lottery_system.register_car_for_user(national_code, car_index)
                print(result)
            else:
                print("User not found. Please register or log in.")

        elif choice == "4":
            winners = lottery_system.show_winners()
            print("List of Winners:")
            for winner in winners:
                print(winner.strip())

        elif choice == "5":
            winners = lottery_system.draw_random_winners()
            print(f"\nRandom Winners (5% of total users):")
            for winner in winners:
                print(f"{winner['user_id']} won the car: {winner['winner_car']}")

        elif choice == "6":
            print("Lottery results saved. Exiting the program.")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
