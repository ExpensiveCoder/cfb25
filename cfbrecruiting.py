import sqlite3
import json
import os

def setup_database():
    conn = sqlite3.connect('playerDatabase.db')
    c = conn.cursor()
    
    # Database for players (player_id, name, position, archetype, team, recruit_year, current_year, current ratings, season ratings)
    c.execute('''CREATE TABLE IF NOT EXISTS player (
                    player_id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    position TEXT,
                    archetype TEXT,
                    team TEXT NOT NULL,
                    recruiting_year INTEGER NOT NULL,
                    curr_year INTEGER NOT NULL,
                    dev_trait TEXT,
                    ovr INTEGER,
                    spd INTEGER, acc INTEGER, agi INTEGER, cod INTEGER, str INTEGER, awr INTEGER, car INTEGER, bcv INTEGER, btk INTEGER,
                    trk INTEGER, sfa INTEGER, spm INTEGER, jkm INTEGER, cth INTEGER, cit INTEGER, spc INTEGER, srr INTEGER, mrr INTEGER, 
                    drr INTEGER, rls INTEGER, jmp INTEGER, thp INTEGER, sac INTEGER, mac INTEGER, dac INTEGER, run INTEGER, tup INTEGER,
                    bsk INTEGER, pac INTEGER, pbk INTEGER, pbp INTEGER, pbf INTEGER, rbk INTEGER, rbp INTEGER, rbf INTEGER, lbk INTEGER,
                    ibl INTEGER, prc INTEGER, tak INTEGER, pow INTEGER, bsh INTEGER, fmv INTEGER, pmv INTEGER, pur INTEGER, mcv INTEGER, 
                    zcv INTEGER, prs INTEGER, ret INTEGER, kpw INTEGER, kac INTEGER, sta INTEGER, tgh INTEGER, inj INTEGER,
                    rat_hist TEXT,
                    FOREIGN KEY (team) REFERENCES profiles (team)
            );
            ''')
    
    # Database for weekly stats (weekly_id, player_id, week_num, season_year, stats)
    c.execute('''CREATE TABLE IF NOT EXISTS weekly_stats (
                    weekly_id INTEGER PRIMARY KEY,
                    player_id INTEGER,
                    week_num INTEGER,
                    season_year INTEGER,
                    pass_yrd INTEGER, pass_comp INTEGER, pass_att INTEGER, pass_tds INTEGER, pass_int INTEGER, 
                    rush_carr INTEGER, rush_yrd INTEGER, rush_avg REAL, rush_tds INTEGER, rush_fmb INTEGER, rush_yac REAL, 
                    rec_recep INTEGER, rec_yrd INTEGER, rec_avg REAL, rec_td INTEGER, rec_rac INTEGER, rec_drops INTEGER,
                    block_sac INTEGER, 
                    def_solo INTEGER, def_assi INTEGER, def_tak INTEGER, def_tfl INTEGER, def_sack REAL, def_int INTEGER, def_defl INTEGER, def_ctha INTEGER, def_ff INTEGER, def_fr INTEGER, def_td INTEGER,
                    kick_fgm INTEGER, kick_fga INTEGER, kick_fgl INTEGER, kick_fgtb INTEGER, 
                    punt_pun INTEGER, punt_yrd INTEGER, punt_n20 INTEGER, punt_lng INTEGER, 
                    kr_ret INTEGER, kr_yrds INTEGER, kr_tds INTEGER,
                    pr_ret INTEGER, pr_yrds INTEGER, pr_tds INTEGER, pr_lng INTEGER,
                    gp INTEGER, dp INTEGER,
                    FOREIGN KEY (player_id) REFERENCES player (player_id)
            );
            ''')
    
    # Database for season stats (season_id, player_id, season_year, team, stats)
    c.execute('''CREATE TABLE IF NOT EXISTS season_stats (
                    season_id INTEGER PRIMARY KEY,
                    player_id INTEGER,
                    season_year INTEGER,
                    team TEXT NOT NULL,
                    pass_yrd INTEGER, pass_comp INTEGER, pass_att INTEGER, pass_tds INTEGER, pass_int INTEGER, 
                    rush_carr INTEGER, rush_yrd INTEGER, rush_avg REAL, rush_tds INTEGER, rush_fmb INTEGER, rush_yac REAL, 
                    rec_recep INTEGER, rec_yrd INTEGER, rec_avg REAL, rec_td INTEGER, rec_rac INTEGER, rec_drops INTEGER,
                    block_sac INTEGER, 
                    def_solo INTEGER, def_assi INTEGER, def_tak INTEGER, def_tfl INTEGER, def_sack REAL, def_int INTEGER, def_defl INTEGER, def_ctha INTEGER, def_ff INTEGER, def_fr INTEGER, def_td INTEGER,
                    kick_fgm INTEGER, kick_fga INTEGER, kick_fgl INTEGER, kick_fgtb INTEGER, 
                    punt_pun INTEGER, punt_yrd INTEGER, punt_n20 INTEGER, punt_lng INTEGER, 
                    kr_ret INTEGER, kr_yrds INTEGER, kr_tds INTEGER,
                    pr_ret INTEGER, pr_yrds INTEGER, pr_tds INTEGER, pr_lng INTEGER,
                    gp INTEGER, dp INTEGER,
                    FOREIGN KEY (player_id) REFERENCES player (player_id)
                    FOREIGN KEY (team) REFERENCES profiles (team)
            );
            ''')
    
    # Database for accolades earned by player (accolade_id, player_id, season_year, accolade)
    # Accolade = PoTW, PoTY, Heisman, All-American, 
    c.execute('''CREATE TABLE IF NOT EXISTS accolades (
                    accolade_id INTEGER PRIMARY KEY,
                    player_id INTEGER,
                    season_year INTEGER,
                    accolade TEXT
                    FOREIGN KEY (player_id) REFERENCES player (player_id)
            );
            ''')
    
    # Database for team (team_id, team, curr_year, motivation grades)
    c.execute('''CREATE TABLE IF NOT EXISTS teams (
                    team_id INTEGER PRIMARY KEY,
                    team TEXT NOT NULL,
                    curr_year INTEGER,
                    acad_pres TEXT,
                    ath_facil TEXT,
                    brand_exp TEXT,
                    campus_life TEXT,
                    champ_contender TEXT,
                    coach_stab TEXT,
                    coach_pres TEXT,
                    conf_pres TEXT,
                    play_time TEXT,
                    pro_poten TEXT,
                    play_style TEXT,
                    prox_to_home TEXT,
                    prog_trad TEXT,
                    stad_atmo TEXT
            );
            ''')
    

def menu():
    print("CFB Recruiting Database")
    print("-----------------------")
    print("1. View Teams")
    print("2. Exit")
    
    choice = input("Enter your Choice: ")
    return choice

def main():
    os.system('cls')
    setup_database()
    conn = sqlite3.connect('cfbrecruits.db')
    
    while True:
        choice = menu()
        
        if choice == "1":
            print("View Teams Not implemented")
        elif choice == "2":
            conn.close()
            print("Exiting Program")
            break
        else:
            print("Please input proper choice")
            
if __name__ == "__main__":
    main()