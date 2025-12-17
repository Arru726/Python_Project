import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

plt.style.use("ggplot")  # optional styling



#                 PLAYER CLASS

class Player:
    def __init__(self, name, filepath):
        self.name = name
        self.filepath = filepath
        self.data = None

    # ----- ENTER MANUAL DATA -----
    def enter_manual_data(self):
        manual_entries = []

        print("\nDo you want to add NEW matches to this player?")
        ans = input("Type yes or no: ").lower()

        if ans != "yes":
            return pd.DataFrame()

        print("\nHow many matches do you want to add?")
        try:
            count = int(input("Enter number: "))
        except ValueError:
            print("Invalid number.")
            return pd.DataFrame()

        for i in range(count):
            print(f"\nEnter data for match {i+1}:")
            try:
                match_id = int(input("Match ID: "))
                runs = int(input("Runs: "))
                balls = int(input("Balls: "))
                fours = int(input("Fours: "))
                sixes = int(input("Sixes: "))
                dismissal = input("Dismissal type: ")
                overs = int(input("Overs bowled: "))
                runs_conceded = int(input("Runs conceded: "))
                wickets = int(input("Wickets taken: "))

                manual_entries.append([
                    match_id, runs, balls, fours, sixes,
                    dismissal, overs, runs_conceded, wickets
                ])

            except ValueError:
                print("Invalid input. Skipping...")
                continue

        cols = ["match_id","runs","balls","fours","sixes",
                "dismissal","overs","runs_conceded","wickets"]

        return pd.DataFrame(manual_entries, columns=cols)

    # ----- LOAD + MERGE CSV -----
    def load_data(self):
        try:
            df_csv = pd.read_csv(self.filepath)
        except FileNotFoundError:
            print("CSV file not found.")
            return

        df_manual = self.enter_manual_data()

        # Merge old + new
        self.data = pd.concat([df_csv, df_manual], ignore_index=True)

        # Save updated CSV
        self.data.to_csv(self.filepath, index=False)

        print(f"\nData loaded for {self.name}.")
        print(f"Total matches: {len(self.data)} (saved to CSV)\n")


    #                 STATS
   
    def batting_stats(self):
        runs = self.data["runs"].sum()
        innings = len(self.data)
        balls = self.data["balls"].sum()

        highest = self.data["runs"].max()
        avg = runs / innings
        sr = (runs / balls) * 100 if balls else 0

        fifties = np.sum(self.data["runs"] >= 50)
        hundreds = np.sum(self.data["runs"] >= 100)

        print("\n----- Batting Stats -----")
        print("Total Runs:", runs)
        print("Highest:", highest)
        print("Average:", round(avg, 2))
        print("Strike Rate:", round(sr, 2))
        print("50s:", fifties)
        print("100s:", hundreds)

    def bowling_stats(self):
        wkts = self.data["wickets"].sum()
        rc = self.data["runs_conceded"].sum()
        overs = self.data["overs"].sum()

        eco = rc / overs if overs else 0
        avg = rc / wkts if wkts else 0
        best = self.data["wickets"].max()

        print("\n----- Bowling Stats -----")
        print("Total Wickets:", wkts)
        print("Best Figure:", best)
        print("Economy:", round(eco, 2))
        print("Bowling Avg:", round(avg, 2))


    #                 GRAPHS
    def plot_runs(self):
        plt.figure(figsize=(9,5))
        plt.plot(self.data["match_id"], self.data["runs"], marker='o')
        plt.title(f"Runs per Match - {self.name}", fontsize=14, fontweight="bold")
        plt.xlabel("Match ID")
        plt.ylabel("Runs")
        plt.grid(True, linestyle="--", alpha=0.5)
        plt.tight_layout()
        plt.show()

    def plot_wickets(self):
        plt.figure(figsize=(9,5))
        plt.plot(self.data["match_id"], self.data["wickets"], color="#c0392b", marker='s')
        plt.title(f"Wickets per Match - {self.name}", fontsize=14, fontweight="bold")
        plt.xlabel("Match ID")
        plt.ylabel("Wickets")
        plt.grid(True, linestyle="--", alpha=0.5)
        plt.tight_layout()
        plt.show()

    def plot_boundaries(self):
        fours = self.data["fours"].sum()
        sixes = self.data["sixes"].sum()

        plt.figure(figsize=(7,5))
        plt.bar(["Fours", "Sixes"], [fours, sixes], 
                color=["#2980b9", "#8e44ad"])
        plt.title(f"Boundaries - {self.name}", fontsize=14, fontweight="bold")
        plt.grid(axis="y", linestyle="--", alpha=0.5)
        plt.tight_layout()
        plt.show()

    def plot_batting_average(self):
        df = self.data.sort_values("match_id")
        avg = df["runs"].cumsum() / np.arange(1, len(df)+1)

        plt.figure(figsize=(9,5))
        plt.plot(df["match_id"], avg, marker='o', color="#16a085")
        plt.title(f"Batting Average Progression - {self.name}", fontsize=14, fontweight="bold")
        plt.xlabel("Match ID")
        plt.ylabel("Average")
        plt.grid(True, linestyle="--", alpha=0.5)
        plt.tight_layout()
        plt.show()

    def plot_bowling_average(self):
        df = self.data.sort_values("match_id")
        bowling_avg = []

        for i in range(len(df)):
            total_runs = df["runs_conceded"][:i+1].sum()
            total_wkts = df["wickets"][:i+1].sum()

            bowling_avg.append(total_runs / total_wkts if total_wkts else None)

        plt.figure(figsize=(9,5))
        plt.plot(df["match_id"], bowling_avg, marker='o', color="#d35400")
        plt.title(f"Bowling Average Progression - {self.name}", fontsize=14, fontweight="bold")
        plt.xlabel("Match ID")
        plt.ylabel("Bowling Average")
        plt.grid(True, linestyle="--", alpha=0.5)
        plt.tight_layout()
        plt.show()



#       CREATE NEW PLAYER (AUTO SAVE)

def create_player_file():
    print("\n--- Create a New Player ---")
    name = input("Enter player name: ")

    file_name = name.lower().replace(" ", "_") + ".csv"
    file_path = "players/" + file_name

    print(f"Creating file: {file_path}")

    print("\nHow many matches to enter?")
    try:
        count = int(input("Number: "))
    except ValueError:
        print("Invalid number.")
        return

    data = {
        "match_id": [],
        "runs": [],
        "balls": [],
        "fours": [],
        "sixes": [],
        "dismissal": [],
        "overs": [],
        "runs_conceded": [],
        "wickets": []
    }

    for i in range(count):
        print(f"\nMatch {i+1}:")
        try:
            data["match_id"].append(int(input("Match ID: ")))
            data["runs"].append(int(input("Runs: ")))
            data["balls"].append(int(input("Balls: ")))
            data["fours"].append(int(input("Fours: ")))
            data["sixes"].append(int(input("Sixes: ")))
            data["dismissal"].append(input("Dismissal: "))
            data["overs"].append(int(input("Overs: ")))
            data["runs_conceded"].append(int(input("Runs conceded: ")))
            data["wickets"].append(int(input("Wickets: ")))
        except:
            print("Invalid input. Skipping…")

    df = pd.DataFrame(data)
    df.to_csv(file_path, index=False)

    print(f"\nPlayer created successfully! File saved as {file_path}\n")


#                    MAIN

def main():
    print("---- Cricket Scorecard Analyzer ----")

    while True:
        print("\nMAIN MENU")
        print("1. Load Player & View Stats")
        print("2. Create New Player")
        print("3. Exit")

        main_choice = input("Enter choice: ")

        if main_choice == "1":
            file_path = input("Enter CSV path (example: players/player1.csv): ")
            name = input("Enter player name: ")

            p = Player(name, file_path)
            p.load_data()

            # Player submenu
            while True:
                print("\n--- Player Menu ---")
                print("1. Show Batting Stats")
                print("2. Show Bowling Stats")
                print("3. Plot Runs")
                print("4. Plot Boundaries")
                print("5. Plot Wickets")
                print("6. Plot Batting Average")
                print("7. Plot Bowling Average")
                print("8. Back to Main Menu")

                c = input("Enter choice: ")

                if c == "1": p.batting_stats()
                elif c == "2": p.bowling_stats()
                elif c == "3": p.plot_runs()
                elif c == "4": p.plot_boundaries()
                elif c == "5": p.plot_wickets()
                elif c == "6": p.plot_batting_average()
                elif c == "7": p.plot_bowling_average()
                elif c == "8": break
                else: print("Invalid choice.")

        elif main_choice == "2":
            create_player_file()

        elif main_choice == "3":
            print("Exiting...")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
