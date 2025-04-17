import random
# Ask for the user's name
name = input("What is your name? ")

# Display a greeting using the entered name
print(f"Hello, {name}! Nice to meet you.Welcome to the World of StockQuest. You have stocks you can sell them, not sell them, or buy them. Depnding on how much money your stocks make will depend on how fast you can upgrade your kingdom.")


class Kingdom:
    def __init__(self):
        self.money = 1000
        self.level = 1
        self.walls = 1  # Number of walls protecting the kingdom
        self.crops = 10  # Initial crop yield
        self.soldiers = 10  # Number of soldiers in the kingdom
        self.transportation = 1  # Transportation efficiency
        self.materials = 1  # Material production efficiency
        self.irrigation = 1  # Irrigation effectiveness
        self.land = 10  # Amount of land owned by the kingdom

    def upgrade_kingdom(self, cost):
        if self.money >= cost:
            self.money -= cost
            self.level += 1
            print(f"Kingdom upgraded to level {self.level}")
        else:
            print("Not enough money for the upgrade!")

    def build_wall(self, cost):
        if self.money >= cost:
            self.money -= cost
            self.walls += 1
            print(f"Built a new wall! Walls: {self.walls}")
        else:
            print("Not enough money to build a wall!")

    def invest_in_crops(self, cost):
        if self.money >= cost:
            self.money -= cost
            self.crops += 5  # Increase crop yield
            print(f"Invested in crops! Crop yield: {self.crops}")
        else:
            print("Not enough money to invest in crops!")

    def recruit_soldiers(self, cost):
        if self.money >= cost:
            self.money -= cost
            self.soldiers += 5  # Recruit more soldiers
            print(f"Recruited new soldiers! Soldiers: {self.soldiers}")
        else:
            print("Not enough money to recruit soldiers!")

    def improve_transportation(self, cost):
        if self.money >= cost:
            self.money -= cost
            self.transportation += 1  # Improve transportation efficiency
            print(f"Improved transportation! Transportation level: {self.transportation}")
        else:
            print("Not enough money to improve transportation!")

    def import_materials(self, cost):
        if self.money >= cost:
            self.money -= cost
            self.materials += 1  # Increase material production efficiency
            print(f"Imported materials! Materials level: {self.materials}")
        else:
            print("Not enough money to import materials!")

    def enhance_irrigation(self, cost):
        if self.money >= cost:
            self.money -= cost
            self.irrigation += 1  # Enhance irrigation effectiveness
            print(f"Enhanced irrigation! Irrigation level: {self.irrigation}")
        else:
            print("Not enough money to enhance irrigation!")

    def claim_more_land(self, cost):
        if self.money >= cost:
            self.money -= cost
            self.land += 10  # Claim more land
            print(f"Claimed more land! Total land: {self.land}")
        else:
            print("Not enough money to claim more land!")

    def handle_disaster(self):
        disaster_cost = 50 * self.crops
        self.money -= disaster_cost
        print(f"Oh no! A natural disaster occurred. Lost {disaster_cost} money!")

class Stock:
    def __init__(self, name, initial_price):
        self.name = name
        self.price = initial_price

    def update_price(self):
        # Simulate random price fluctuations
        self.price += random.uniform(-5, 5)

class Game:
    def __init__(self):
        self.kingdom = Kingdom()
        self.stocks = [Stock("WAT", 50), Stock("TSLA", 300)]

    def play_day(self):
        # Update stock prices
        for stock in self.stocks:
            stock.update_price()

        # Simulate natural disasters (10% chance each day)
        if random.random() < 0.1:
            self.kingdom.handle_disaster()

        # Allow the player to buy/sell stocks
        self.handle_stock_transactions()

        # Calculate daily income based on stock investments
        daily_income = sum(stock.price for stock in self.stocks)
        self.kingdom.money += daily_income

        # Upgrade the kingdom
        upgrade_cost = 200 * self.kingdom.level
        self.kingdom.upgrade_kingdom(upgrade_cost)

    def handle_stock_transactions(self):
        for stock in self.stocks:
            action = input(f"Do you want to buy or sell {stock.name} stocks? (b/s/n): ").lower()
            if action == 'b':
                quantity = int(input(f"How many {stock.name} stocks do you want to buy? "))
                cost = stock.price * quantity
                if cost <= self.kingdom.money:
                    self.kingdom.money -= cost
                    print(f"Bought {quantity} {stock.name} stocks for ${cost:.2f}")
                else:
                    print("Not enough money to buy stocks!")
            elif action == 's':
                quantity = int(input(f"How many {stock.name} stocks do you want to sell? "))
                earnings = stock.price * quantity
                self.kingdom.money += earnings
                print(f"Sold {quantity} {stock.name} stocks for ${earnings:.2f}")

    def handle_upgrades(self):
        print("\nUpgrade Options:")
        print("1. Build a new wall")
        print("2. Invest in crops")
        print("3. Recruit new soldiers")
        print("4. Improve transportation")
        print("5. Import materials")
        print("6. Enhance irrigation")
        print("7. Claim more land")
        upgrade_choice = input("Choose an upgrade option (1-7/n): ").lower()
        if upgrade_choice == '1':
            wall_cost = 50 * self.kingdom.walls
            self.kingdom.build_wall(wall_cost)
        elif upgrade_choice == '2':
            crop_investment_cost = 100
            self.kingdom.invest_in_crops(crop_investment_cost)
        elif upgrade_choice == '3':
            recruit_cost = 150
            self.kingdom.recruit_soldiers(recruit_cost)
        elif upgrade_choice == '4':
            transportation_cost = 120
            self.kingdom.improve_transportation(transportation_cost)
        elif upgrade_choice == '5':
            materials_cost = 130
            self.kingdom.import_materials(materials_cost)
        elif upgrade_choice == '6':
            irrigation_cost = 110
            self.kingdom.enhance_irrigation(irrigation_cost)
        elif upgrade_choice == '7':
            land_claim_cost = 200
            self.kingdom.claim_more_land(land_claim_cost)

        # Check if all upgrades are done to advance to level 2
        if (
            self.kingdom.walls > 1 and
            self.kingdom.crops > 10 and
            self.kingdom.soldiers > 10 and
            self.kingdom.transportation > 1 and
            self.kingdom.materials > 1 and
            self.kingdom.irrigation > 1 and
            self.kingdom.land > 10
        ):
            print("Congratulations! Your kingdom has reached level 2!")
            exit()

    def run_game(self):
        while True:
            print(f"\nDay {self.kingdom.level}")
            self.play_day()
            self.handle_upgrades()

if __name__ == "__main__":
    game = Game()
    game.run_game()
