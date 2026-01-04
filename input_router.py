import re

def route_user_input(user_input):
    """
    Analyzes the raw input string to decide which tool to use.
    Returns a dictionary with 'type' and 'content'.
    """
    print(f"\n--- 📡 Input Router Receiving: '{user_input[:20]}...' ---")

    # Check 1: Is it a Website Link?
    # (Regex to look for http/https)
    url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    
    if url_pattern.match(user_input):
        return {
            "type": "URL",
            "action": "Needs Web Scraper Tool",
            "content": user_input
        }

    # Check 2: Is it an Image? 
    # (In terminal, we check for file extensions like .jpg or .png)
    if user_input.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
         return {
            "type": "IMAGE",
            "action": "Needs Vision/OCR Tool",
            "content": user_input
        }
    
    # Default: It is Manual Text
    return {
        "type": "TEXT",
        "action": "Direct Processing",
        "content": user_input
    }

# --- TEST ZONE ---
if __name__ == "__main__":
    print(route_user_input("https://www.bigbasket.com/pd/10000/cookies"))
    print(route_user_input("my_snack_photo.jpg"))
    print(route_user_input("Sugar, Maida, Salt"))