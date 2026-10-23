import sqlite3

def add_tokens_to_stock(token_list, bot_type):
    conn = sqlite3.connect("bot_stock.db")
    cursor = conn.cursor()
    
    inserted_count = 0
    duplicate_count = 0
    
    for token in token_list:
        token = token.strip()
        if not token:
            continue
        try:
            cursor.execute(
                "INSERT INTO bots (token, bot_type, status) VALUES (?, ?, 'available')", 
                (token, bot_type)
            )
            inserted_count += 1
        except sqlite3.IntegrityError:
            duplicate_count += 1
            
    conn.commit()
    conn.close()
    
    print(f"📦 Stock Update Results for [{bot_type.upper()}] bots:")
    print(f"   Successfully added: {inserted_count} tokens")
    if duplicate_count > 0:
        print(f"   Skipped (already in database): {duplicate_count} tokens")

if __name__ == "__main__":
    print("--- 🤖 Discord Bot Stock Multi-Loader ---")
    print("Enter the Bot Type (online / offline / chat / vc):")
    b_type = input("> ").strip().lower()
    
    if b_type not in ['online', 'offline', 'chat', 'vc']:
        print("❌ Invalid type! Choose from online, offline, chat, or vc.")
    else:
        print("\nPaste your bot tokens below (one token per line).")
        print("When you are finished pasting, press Enter, then Ctrl+D to save:")
        
        import sys
        user_tokens = sys.stdin.read().splitlines()
        
        add_tokens_to_stock(user_tokens, b_type)
