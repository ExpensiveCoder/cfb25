import sqlite3
import os


class TeamProfile:
    def __init__(self, team_name, grades):
        self.team_name = team_name
        self.grades = {
            "Playing Time": None,
            "Playing Style": None,
            "Championship Contender": None,
            "Program Tradition": None,
            "Campus Lifestyle": None,
            "Stadium Atmosphere": None,
            "Pro Potential": None,
            "Brand Exposure": None,
            "Academic Prestige": None,
            "Conference Prestige": None,
            "Coach Prestige": None,
            "Coach Stability": None,
            "Athletic Facilites": None,
            "Proximity to Home": None
        }
    
    # get_grade() - returns the grade for x motivation
    def get_grade(self, motivation):
        return self.grades.get(motivation, None)
    
    # update_grade() - updates the letter number grade for x motiovation
    def update_grade(self, motivation, grade):
        self.grades[motivation] = grade
        
    # display_team() - prints all the motivations and their letter grade for current team
    def display_team(self):
        print(f"Team Name: {self.team_name}")
        print("Motivation Grades:")
        for motivation, grade in self.grades.items():
            print(f"  {motivation}: {grade}")

# Set-up database
def setup_database():
    conn = sqlite3.connect('recruiting.db')
    c = conn.cursor()
    # Creates database for recruits (has name, interested and disinterested motivations) (needs position and archtype)
    c.execute('''CREATE TABLE IF NOT EXISTS recruits (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    position TEXT NOT NULL,
                    archetype TEXT NOT NULL,
                    known_motivations TEXT,
                    disinterested_motivations TEXT,
                    determined_pitch TEXT,
                    log TEXT
            )''')
    # Create database for Team Profiles(has name, recruiting year, motivation grades, weekly hours, weekly log)
    c.execute('''CREATE TABLE IF NOT EXISTS team_profile (
                    id INTEGER PRIMARY KEY,
                    team_name TEXT NOT NULL,
                    recruiting_year INTEGER NOT NULL,
                    motivation_grades TEXT NOT NULL,
                    weekly_hours INTEGER NOT NULL,
                    weekly_log TEXT
            )''')
    
    conn.commit()
    conn.close()

# add_recruit() - adds a new recruit
def add_recruit():
    name = input("Enter recruit name: ")
    position = input("Enter recruit position: ")
    archetype = input("Enter recruit archetype: ")
    known_motivations = input("Enter interested motivations (comma-separated, optional): ")
    disinterested_motivations = input("Enter disinterested motivations (comma-separated, optional): ")
    
    conn = sqlite3.connect('recruiting.db')
    c = conn.cursor()
    c.execute('''INSERT INTO recruits (name, position, archetype, known_motivations, disinterested_motivations)
                VALUES (?, ?, ?, ?, ?)''',
                (name, position, archetype, known_motivations, disinterested_motivations))
    conn.commit()
    conn.close()
    print(f"Recruit '{name}' added successfully.")
    
# add_team_profile() - adds a new team profile
def add_team_profile():
    team_name = input("Enter the team name: ")
    recruiting_year = int(input("Enter the recruiting class year: "))
    weekly_hours = int(input("Enter your recruiting hours: "))
    
    motivations = []
    for i in range(1, 15):
        motivation = input(f"Enter the letter grade for Motivation {i} (A-F): ")
        motivations.append(motivation)
        
    motivation_grades = ','.join(motivations)
    
    conn = sqlite3.connect('recruiting.db')
    c = conn.cursor()
    
    c.execute('''INSERT INTO team_profile (team_name, recruiting_year, recruiting_hours, motivation_grades)
              VALUES (?, ?, ?, ?)''', (team_name, recruiting_year, recruiting_hours, motivation_grades))
    
    conn.commit()
    conn.close()
    
    print(f"Team profile for {team_name} (Year: {recruiting_year}) added successfully.")

# update_recruit(recruit_id, known_motivations, disinterested_motivations)
def update_recruit():
    name = input("Enter recruit name to update: ")
    
    
    conn = sqlite3.connect('recruiting.db')
    c = conn.cursor()
    
    c.execute('SELECT id, known_motivations, disinterested_motivations, determined_pitch FROM recruits WHERE name = ?', (name,))
    recruit = c.fetchone()
    
    if not recruit:
        print(f"No recruit found with the name '{name}'.")
        conn.close()
        return
    
    recruit_id, current_known_motivations, current_disinterested_motivations, current_determined_pitch = recruit
    
    new_known_motivations = input("Enter new interested motivations (comma-separated, optional)")
    new_disinterested_motivations = input("Enter new disinterested motivations (comma-separated, optional)")
    
    # Only update motivations if provided an update
    if new_known_motivations:
        known_motivations = new_known_motivations
    else:
        known_motivations = current_known_motivations
        
    if new_disinterested_motivations:
        disinterested_motivations = new_disinterested_motivations
    else:
        disinterested_motivations = current_disinterested_motivations
        
    # Find Pitch if possible
    #determine_pitch = determine_pitch(known_motivations, disinterested_motivations)
        
    # Update recruit's record
    c.execute('''UPDATE recruits
              SET known_motivations = ?, disinterested_motivations = ?
              WHERE id = ?''',
              (known_motivations, disinterested_motivations, recruit_id))
    
    conn.commit()
    conn.close()
    print(f"Recruit '{name}' updated successfully")

# update_team_profile()
def update_team_profile():
    team_name = input("Enter the team name to update: ")
    recruiting_year = int(input("Enter the recruiting class year: "))
    
    conn = sqlite3.connect('recruiting.db')
    c = conn.cursor()
    
    c.execute('SELECT id, motivation_grades FROM team_profiles WHERE team_name = ? AND recruiting_year = ?', (team_name, recruiting_year))
    profile = c.fetchone()
    
    if not profile:
        print(f"No profile found for {team_name} (Year: {recruiting_year}).")
        conn.close()
        return
    
    profile_id, current_motivation_grades, current_weekly_hours = profile
    
    weekly_hours = int(input("Enter the new weekly hours"))
    motivations = []
    for i in range(1, 15):
        motivation = input(f"Enter the new letter grade for Motivation {i} (leave black to keep current grade): ")
        if motivation:
            motivations.append(motivation)
        else:
            motivations.append(current_motivation_grades.split(',')[i-1])
            
    motivation_grades = ','.join(motivations)
    
    c.execute('''UPDATE team_profile
                SET weekly_hours = ?
                SET motivation_grades = ?
                WHERE id = ?''', (weekly_hours, motivation_grades, profile_id))
    
    conn.commit()
    conn.close()
    
    print(f"Team profile for {team_name} (Year: {recruiting_year}) updated successfully.")

# view_recruits() - retrieves all recruits from database
def view_recruits():
    conn = sqlite3.connect('recruiting.db')
    c = conn.cursor()
    
    search_name = input("Enter recruit name to search (or press Enter to view all recruits): ")
    
    if search_name:
        c.execute('SELECT id, name, position, archetype, known_motivations, disinterested_motivations FROM recruits WHERE name = ?', (search_name,))
    else:
        c.execute('SELECT id, name, position, archetype, known_motivations, disinterested_motivations FROM recruits')
    
    recruits = c.fetchall()
    conn.close()
    
    if recruits:
        for recruit in recruits:
            print(f"ID: {recruit[0]}, Name: {recruit[1]}, Position: {recruit[2]}, Archetype: {recruit[3]}, "
                  f"Known Motivations: {recruit[4] if recruit[4] else 'None'}, Disinterested Motivations: {recruit[5] if recruit[5] else 'None'}")
    else:
        print("No recruits found.")
        
# view_team_profile() - prints all the team profiles in database
def view_team_profile():
    conn = sqlite3.connect('recruiting.db')
    c = conn.cursor()
    
    c.execute('SELECT id, team_name, recruiting_year, weekly_hours, motivation_grades FROM team_profile')
    profiles = c.fetchall()
    conn.close()
    
    if profiles:
        for profile in profiles:
            print(f"ID: {profile[0]}, Team: {profile[1]}, Year: {profile[2]}, Hours: {profile[3]}, Motivation Grades: {profile[4]}")
    else:
        print("No team profiles found.")

# delete_recruit() - removes recruit from database
def delete_recruit():
    name = input("Enter the recruit name you want to delete (first and last): ")
    
    conn = sqlite3.connect('recruiting.db')
    c = conn.cursor()
    c.execute('''DELETE FROM recruits WHERE name = ?''', (name,))
    conn.commit()
    conn.close()
    print(f"Recruit Name '{name}' was deleted successfully")

# TODO: delete_team_profile()
        
# Part 2: Pitch logic
pitch_types = {
    "College Experience": ["Academic Prestige", "Campus Lifestyle", "Stadium Atmosphere"],
    "Team Player": ["Athletic Facilities", "Coach Stability", "Proximity to Home"],
    "Campus Personality": ["Academic Prestige", "Campus Lifestyle", "Proximity to Home"],
    "It's Game Time": ["Conference Prestige", "Playing Style", "Proximity to Home"],
    "Prestigious": ["Coach Prestige", "Conference Prestige", "Proximity to Home"],
    "Student of the Game": ["Academic Prestige", "Coach Prestige", "Proximity to Home"],
    "Hometown Hero": ["Campus Lifestyle", "Proximity to Home", "Program Tradition"],
    "Prove Yourself": ["Athletic Facilities", "Coach Prestige", "Conference Prestige"],
    "The Clutch": ["Pro Potential", "Playing Style", "Proximity to Home"],
    "TV Time": ["Brand Exposure", "Championship Contender", "Playing Time"],
    "Coach's Favorite": ["Athletic Facilities", "Coach Prestige", "Proximity to Home"],
    "Aspirational": ["Athletic Facilities", "Championship Contender", "Proximity to Home"],
    "To The House": ["Brand Exposure", "Championship Contender", "Coach Prestige"],
    "Football Influencer": ["Championship Contender", "Pro Potential", "Program Tradition"],
    "Time to Get to Work": ["Playing Time", "Playing Style", "Proximity to Home"],
    "Starter": ["Brand Exposure", "Playing Time", "Pro Potential"],
    "Grassroots": ["Pro Potential", "Proximity to Home", "Program Tradition"],
    "Conference Spotlight": ["Championship Contender", "Conference Prestige", "Proximity to Home"],
    "Sunday Bound": ["Championship Contender", "Conference Prestige", "Pro Potential"],
    "Work Horse": ["Athletic Facilities", "Brand Exposure", "Pro Potential"]
}
# determine_pitch(known_motivations, disinterested_motivations) - Use known motivations to determine Best Pitch type for each recruit
def determine_pitch(known_motivations, disinterested_motivations):
    known_set = set(known_motivations)
    disinterested_set = set(disinterested_motivations)
    possible_pitches = []
    
    for pitch, req_motivations in pitch_types.items():
        pitch_set = set(req_motivations)
        
        if known_set.issubset(pitch_set) and disinterested_set.isdisjoint(pitch_set):
            possible_pitches.append(pitch)
            
    return possible_pitches

def process_recruits(recruits):
    results = {}
    for recruit_id, recruit_name, position, archetype, known_motivations, disinterested_motivations in recruits:
        known_motivations = known_motivations.split(',') if known_motivations else []
        disinterested_motivations = disinterested_motivations.split(',') if disinterested_motivations else []
        
        possible_pitches = determine_pitch(known_motivations, disinterested_motivations)
        results[recruit_name] = possible_pitches
    
    return results

def clearScreen():
    os.system('cls')
    
# teamMenu() - Menu for Team Profile customization and updates
def teamMenu():
    
    while True:
        print("\nTeam Menu:")
        print("1. Change Active Profile")
        print("2. Update Team Profile")
        print("3. Delete Team Profile")
        print("4. View All Team Profiles")
        print("5. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            clearScreen()
            print("Change Team Not Implemented")
        elif choice == '2':
            clearScreen()
            print("Update team not implemented")
        elif choice == '3':
            clearScreen()
            print("Delete Teams not implemented")
        elif choice == '4':
            clearScreen()
            print("Viewing all team profiles not implemented")
        elif choice == '5':
            break
        else:
            print("invalid option try again.")
            
        
# recruitMenu() - Menu for recruits customization and updates
def recruitMenu():
    
    while True:
        print("\nRecruit Menu: ")
        print("1. Add Recruit")
        print("2. Update Recruit")
        print("3. Delete Recruit")
        print("4. View Recruits")
        print("5. Back")
        
        choice = input("Enter a choice: ")
        
        if choice == '1':
            clearScreen()
            print("Add Recruit not implemented")
        elif choice == '2':
            clearScreen()
            print("Update recruit not available")
        elif choice == '3':
            clearScreen()
            print("Delete recruit not implemented")
        elif choice == '4':
            clearScreen()
            print("Viewing recruits not implemented")
        elif choice == '5':
            break
        else:
            clearScreen()
            print("Invalid option try again")

# Menu for program
def menu():
    setup_database()
    
    while True:
        clearScreen()
        print("\nMenu:")
        print("1. Recruit Profiles")
        print("2. Update Recruit")
        print("3. Delete Recruit")
        print("4. View All Recruits")
        print("5. Team Profiles")
        print("6. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            recruitMenu()
        elif choice == '2':
            clearScreen()
            update_recruit()
        elif choice == '3':
            clearScreen()
            delete_recruit()
        elif choice == '4':
            clearScreen()
            view_recruits()
        elif choice == '5':
            teamMenu()
        elif choice == '6':
            break
        else:
            clearScreen()
            print("Invalid Choice. Try Again")

if __name__ == "__main__":
    menu()