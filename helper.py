import sys
import os
from dotenv import load_dotenv

def check_api_keys():
    load_dotenv()
    print("\n--- Running System Check ---")
    keys_to_check=["OPENAI_API_KEY","SERPER_API_KEY","NVIDIA_API_KEY"]
    missing_keys = [] # Let's keep a list of anything that fails
    for key in keys_to_check:
        value = os.getenv(key)
        if value:
            print(f"✅ {key} found! (Starts with: {value[:5]}...)")
        else:
            print(f"❌ Error: {key} is MISSING. Check your .env file.")
            missing_keys.append(key)
            print("----------------------------\n")
    
    if missing_keys:
        print(f"""
            CRITICAL ERROR: Cannot start pipeline. Please add the following keys to your .env file: {missing_keys}
        """)
        sys.exit(1) # '1' tells the terminal that the program crashed due to an error