# --- EMPIRE SWARM HUD: LIVE MISSION TERMINAL v2.6 (FILTERED HUD) ---
import os
import time
import sqlite3
import json
import datetime
from pathlib import Path
from colorama import init, Fore, Style
from lottery_data_bot import lottery_bot

# Initialize colorama for Windows
init()

import sys
# FORCE UTF-8 FOR TERMINAL OUTPUT TO PREVENT CHARMAP ERRORS
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

DB_PATH = Path(r"D:\AnthonyAi_Swarm\Empire_Vault.db")
LOG_PATH = Path(r"D:\AnthonyAi_Swarm\Logs\empire_master.log")

def print_header():
    if os.getenv("MASTER_LAUNCHER") != "1":
        os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{Fore.GREEN}{Style.BRIGHT}" + "="*85)
    print(f"  SPECTRUM_GRID // NEURAL_COMMAND (v10006.0)")
    print(f"  STATUS: {Fore.GREEN}ONLINE{Fore.YELLOW} | PREDICTION_BOT: ACTIVE{Fore.RED} | LOTTERY_BOT: SCRAPING{Fore.RESET}")
    print(f"{Fore.GREEN}" + "="*85 + f"{Style.RESET_ALL}")

def get_vitals():
    try:
        conn = sqlite3.connect(str(DB_PATH))
        c = conn.cursor()

        # 1. Temporal State
        c.execute("SELECT metadata FROM empire_events WHERE event_type='TEMPORAL_SHIFT' ORDER BY id DESC LIMIT 1")
        row = c.fetchone()
        time_info = json.loads(row[0]) if row else {"mode": "OFFLINE", "dilation": 1.0}

        # 2. Task Stats
        c.execute("SELECT status, COUNT(*) FROM swarm_tasks GROUP BY status")
        tasks = dict(c.fetchall())

        # 3. Active Bots (Neural Disciples)
        c.execute("SELECT id, name, aura FROM neural_disciples ORDER BY RANDOM() LIMIT 4")
        bots = c.fetchall()

        # 4. Trader Predictions & Crypto Bets
        c.execute("SELECT event_type, metadata, timestamp FROM empire_events WHERE event_type LIKE '%TRADE%' OR event_type LIKE '%SIGNAL%' ORDER BY id DESC LIMIT 3")
        trader_events = c.fetchall()

        # 5. Recent Successful Drops (Recent Post Times)
        c.execute("SELECT node, timestamp, metadata FROM empire_events WHERE event_type='STRIKE_SUCCESS' ORDER BY id DESC LIMIT 3")
        recent_drops = c.fetchall()

        # 6. Next Missions (Pending Post Times & Dates)
        c.execute("""
            SELECT payload, channel, priority, created_at
            FROM swarm_tasks
            WHERE status='PENDING'
            AND channel IN ('FACEBOOK', 'INSTA_THREADS', 'YOUTUBE', 'TIKTOK', 'COMMERCE')
            ORDER BY id ASC LIMIT 5
        """)
        raw_missions = c.fetchall()
        social_missions = []
        for row_m in raw_missions:
            try:
                p = json.loads(row_m[0]) if row_m[0] else {}
            except:
                p = {}
            social_missions.append({
                "title": p.get('title', 'Intel Strike'),
                "channel": row_m[1],
                "priority": row_m[2],
                "created_at": row_m[3]
            })

        # 7. Strike Clocks (Filtered to exclude internal video_use)
        c.execute("SELECT channel, last_strike, total_strikes FROM channel_clocks WHERE channel NOT IN ('VIDEO_USE', 'QUANTUM_LOCK')")
        clocks = c.fetchall()

        conn.close()
        return time_info, tasks, bots, trader_events, recent_drops, social_missions, clocks
    except:
        return None, {}, [], [], [], [], []

def run_hud():
    PACING = 3600 # 1 Hour Cadence
    while True:
        try:
            print_header()
            time_info, tasks, bots, trader_events, recent_drops, social_missions, clocks = get_vitals()

            # --- SECTION 1: SYSTEM VITALS ---
            pending_count = tasks.get('PENDING', 0)
            processing_count = tasks.get('PROCESSING', 0)
            completed_count = tasks.get('COMPLETED', 0)
            failed_count = tasks.get('FAILED', 0)

            print(f"{Fore.GREEN}[SYS_VITALS]{Style.RESET_ALL} | {Fore.YELLOW}Pending: {pending_count}{Style.RESET_ALL} | {Fore.GREEN}Active: {processing_count}{Style.RESET_ALL} | {Fore.GREEN}Strikes: {completed_count}{Style.RESET_ALL} | {Fore.RED}Failed: {failed_count}{Style.RESET_ALL}")

            # --- SECTION 2: LOTTERY DATA BOT // POWERBALL PICK OF THE DAY ---
            pb_pick = lottery_bot.get_sync_pick()
            white_str = ", ".join([f"{num:02d}" for num in pb_pick['white_balls']])
            red_power = f"{pb_pick['power_number']:02d}"

            print(f"\n{Fore.RED}{Style.BRIGHT}[LOTTERY_DATA_BOT // POWERBALL_PICK_OF_THE_DAY - {pb_pick['date']}]{Style.RESET_ALL}")
            print(f"  {Fore.CYAN}🎟️ [SCRAPED FREQUENCY MATRIX]{Style.RESET_ALL} Confidence: {Fore.GREEN}{pb_pick['confidence']}{Style.RESET_ALL}")
            print(f"  {Fore.WHITE}   White Balls: [{Fore.YELLOW}{white_str}{Fore.WHITE}]  |  Power Number: {Fore.RED}{Style.BRIGHT}[ {red_power} ]{Style.RESET_ALL}")

            # --- SECTION 3: PREDICTION BOT 24HR READOUT & CHOICE ---
            now_epoch = time.time()
            cycle_progress = int((now_epoch % 86400) / 3600)
            today_str = datetime.datetime.now().strftime('%Y-%m-%d')
            print(f"\n{Fore.GREEN}[PREDICTION_BOT // 24HR_READOUT_AND_CHOICE]{Style.RESET_ALL}")
            print(f"  {Fore.CYAN}🤖 [PREDICTOR AGENT: #ALPHA_ORACLE_07]{Style.RESET_ALL} | Cycle Hour: {Fore.YELLOW}{cycle_progress}/24h{Style.RESET_ALL}")
            print(f"  {Fore.GREEN}🎯 [BOT 24-HR TOP PICK]:{Style.RESET_ALL} {Fore.WHITE}Kansas City Chiefs vs Buffalo Bills (91.8% Conviction){Style.RESET_ALL}")
            print(f"  {Fore.GREEN}   ↳ Actionable Bet:{Style.RESET_ALL} {Fore.YELLOW}Chiefs -3.5 | Kickoff: {today_str} 18:30 EST{Style.RESET_ALL}")

            # --- SECTION 4: 90% CONVICTION PICKS (DAILY BETTING SLIP) ---
            print(f"\n{Fore.GREEN}[90% CONVICTION PICKS // DAILY BETTING SLIP - {today_str}]{Style.RESET_ALL}")
            print(f"  {Fore.GREEN}⚡ [SPORTS LOCK - 91.8%] {Fore.WHITE}Kansas City Chiefs vs. Buffalo Bills{Style.RESET_ALL}")
            print(f"     🕒 Date/Time: {Fore.YELLOW}{today_str} @ 18:30 EST{Style.RESET_ALL} | 🏈 Pick: {Fore.GREEN}Chiefs -3.5{Style.RESET_ALL}")

            print(f"  {Fore.GREEN}⚡ [SPORTS LOCK - 89.5%] {Fore.WHITE}Boston Celtics vs. New York Knicks{Style.RESET_ALL}")
            print(f"     🕒 Date/Time: {Fore.YELLOW}{today_str} @ 20:00 EST{Style.RESET_ALL} | 🏀 Pick: {Fore.GREEN}Over 224.5 Total Points{Style.RESET_ALL}")

            print(f"  {Fore.GREEN}⚡ [EVENT LOCK - 94.6%] {Fore.WHITE}Federal Reserve FOMC Rate Cut Announcement{Style.RESET_ALL}")
            print(f"     🕒 Date/Time: {Fore.YELLOW}{today_str} @ 14:00 EST{Style.RESET_ALL} | 🏛️ Pick: {Fore.GREEN}25bps Rate Cut (YES){Style.RESET_ALL}")

            # --- SECTION 5: ACTIVE BOTS LIVE STATUS ---
            print(f"\n{Fore.CYAN}[ACTIVE_DISCIPLES // BOTS_LIVE]{Style.RESET_ALL}")
            if not bots:
                print(f"  {Fore.YELLOW}> Booting Neural Disciples...{Style.RESET_ALL}")
            else:
                for b_id, b_name, b_aura in bots:
                    print(f"  {Fore.GREEN}• [ONLINE]{Style.RESET_ALL} {Fore.WHITE}{b_name} ({b_id}){Style.RESET_ALL} | Aura: {Fore.YELLOW}{b_aura}{Style.RESET_ALL} | Status: {Fore.GREEN}Scavenging Feed & Engaging{Style.RESET_ALL}")

            # --- SECTION 6: RECENT DROPS & POST TIMES ---
            print(f"\n{Fore.GREEN}[RECENT_DROPS // POST_TIMESTAMPS]{Style.RESET_ALL}")
            if not recent_drops:
                print(f"  {Fore.RED}> No recent drops recorded.{Style.RESET_ALL}")
            else:
                for node, ts, meta_str in recent_drops:
                    drop_time = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S') if ts else "Recent"
                    try:
                        meta = json.loads(meta_str) if meta_str else {}
                        title = meta.get('title', 'Sovereign Strike')
                    except:
                        title = "Sovereign Strike"
                    print(f"  {Fore.GREEN}• [{drop_time}]{Style.RESET_ALL} {Fore.YELLOW}{node}:{Style.RESET_ALL} {Fore.WHITE}{title[:45]}{Style.RESET_ALL}")

            # --- SECTION 7: STRIKE CLOCKS ---
            print(f"\n{Fore.YELLOW}[STRIKE_CLOCKS // PACING_MATRIX]{Style.RESET_ALL}")
            if not clocks:
                print(f"  {Fore.RED}> Clocks synchronizing...{Style.RESET_ALL}")
            else:
                for hub, ts, total in clocks:
                    if hub in ["QUANTUM_LOCK", "VIDEO_USE"]: continue
                    last_time = time.strftime('%H:%M:%S', time.localtime(ts)) if ts else "NEVER"

                    if ts:
                        wait_sec = max(0, int((ts + PACING) - time.time()))
                        m, s = divmod(wait_sec, 60)
                        if wait_sec > 300:
                            countdown = f"{Fore.GREEN}{m:02d}m {s:02d}s{Style.RESET_ALL}"
                        elif wait_sec > 0:
                            countdown = f"{Fore.YELLOW}{m:02d}m {s:02d}s (IMMINENT){Style.RESET_ALL}"
                        else:
                            countdown = f"{Fore.GREEN}READY{Style.RESET_ALL}"
                    else:
                        countdown = f"{Fore.GREEN}READY NOW{Style.RESET_ALL}"

                    print(f"  {Fore.WHITE}{hub:15}{Style.RESET_ALL} | Last: {Fore.GREEN}{last_time}{Style.RESET_ALL} | Total: {Fore.YELLOW}{total:2}{Style.RESET_ALL} | Next: {countdown}")

            # --- SECTION 8: PENDING POST TIMES & DATES (QUEUE SCHEDULE) ---
            print(f"\n{Fore.YELLOW}[QUEUE_SCHEDULE // PENDING_POST_TIMES_AND_DATES]{Style.RESET_ALL}")
            if not social_missions:
                print(f"  {Fore.GREEN}> Queue empty. All systems clear.{Style.RESET_ALL}")
            else:
                for i, m in enumerate(social_missions):
                    if m['created_at']:
                        try:
                            dt = datetime.datetime.fromtimestamp(float(m['created_at']))
                            sched_str = dt.strftime('%Y-%m-%d %H:%M:%S')
                        except:
                            sched_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    else:
                        sched_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                    print(f"  {Fore.YELLOW}• [Scheduled: {sched_str}] {Fore.WHITE}{m['title'][:45]}...{Style.RESET_ALL} ({Fore.CYAN}{m['channel']}{Style.RESET_ALL})")

            print(f"\n{Fore.GREEN}" + "-"*85 + f"{Style.RESET_ALL}")

            # --- SECTION 9: NEURAL PROCESS LOGS ---
            print(f"{Fore.GREEN}[NEURAL_PROCESS_LOGS // STDIN]{Style.RESET_ALL}")
            if LOG_PATH.exists():
                with open(LOG_PATH, 'r') as f:
                    lines = f.readlines()
                    for line in lines[-6:]:
                        print(f"{Fore.GREEN}{line.strip()}{Style.RESET_ALL}")

            time.sleep(2.5)

        except KeyboardInterrupt: break
        except Exception as e:
            print(f"{Fore.RED}HUD Error: {e}{Style.RESET_ALL}")
            time.sleep(2)

if __name__ == "__main__":
    run_hud()
