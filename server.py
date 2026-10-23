from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

@app.route("/sellauth-webhook", methods=["POST"])
def handle_payment():
    payload = request.get_json()
    if not payload or payload.get("event") != "order.completed":
        return jsonify({"status": "ignored"}), 200
        
    data = payload.get("data", {})
    custom_fields = data.get("custom_fields", {})
    
    guild_id = custom_fields.get("Guild ID")
    
    # Gracefully handle optional Channel IDs (fallback to '-' if empty or missing)
    channel_id = custom_fields.get("Channel ID")
    if not channel_id or str(channel_id).strip() == "":
        channel_id = "-"
        
    bot_type = custom_fields.get("Bot Type")
    quantity = int(custom_fields.get("Quantity", 1))
    
    print(f"\n📦 New Order Received! Type: {bot_type} | Qty: {quantity} | Server: {guild_id} | Channel: {channel_id}")
    
    conn = sqlite3.connect("bot_stock.db")
    cursor = conn.cursor()
    cursor.execute("SELECT token FROM bots WHERE bot_type = ? AND status = 'available' LIMIT ?", (bot_type, quantity))
    tokens_found = cursor.fetchall()
    
    for (token,) in tokens_found:
        cursor.execute("UPDATE bots SET status = 'active', assigned_guild = ?, target_channel = ? WHERE token = ?", (guild_id, channel_id, token))
        
    conn.commit()
    conn.close()
    
    print(f"🚀 Successfully reserved {len(tokens_found)} tokens for deployment.")
    return jsonify({"status": "processed", "reserved_count": len(tokens_found)}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
