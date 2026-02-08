import json
from collections import Counter
from datetime import datetime

def analyze_json_structure(data, path="root", depth=0, max_depth=3):
    """
    Recursively analyzes and prints the structure of a JSON object.
    """
    indent = "  " * depth
    if depth > max_depth:
        print(f"{indent}...")
        return

    if isinstance(data, dict):
        print(f"{indent}Dict with {len(data)} keys: {list(data.keys())[:5]}{'...' if len(data)>5 else ''}")
        for key, value in list(data.items())[:3]: # Show first 3 keys for brevity in deep structures
            print(f"{indent}- {key}: {type(value).__name__}")
            if isinstance(value, (dict, list)):
                analyze_json_structure(value, path=f"{path}.{key}", depth=depth + 1, max_depth=max_depth)
    elif isinstance(data, list):
        print(f"{indent}List of length {len(data)}")
        if data:
            print(f"{indent}Sample item structure:")
            analyze_json_structure(data[0], path=f"{path}[]", depth=depth + 1, max_depth=max_depth)

def analyze_conversations_content(data):
    """
    Specific analysis for ChatGPT conversations.json format.
    """
    print("\n\n=== Content Statistics ===")
    print(f"Total Conversations: {len(data)}")
    
    user_msg_count = 0
    assistant_msg_count = 0
    timestamps = []
    
    for conv in data:
        mapping = conv.get('mapping', {})
        for msg_data in mapping.values():
            message = msg_data.get('message')
            if message:
                role = message.get('author', {}).get('role')
                if role == 'user':
                    user_msg_count += 1
                elif role == 'assistant':
                    assistant_msg_count += 1
                
                create_time = message.get('create_time')
                if create_time:
                    timestamps.append(create_time)

    print(f"Total User Messages: {user_msg_count}")
    print(f"Total Assistant Messages: {assistant_msg_count}")
    
    if timestamps:
        min_ts = min(timestamps)
        max_ts = max(timestamps)
        print(f"Date Range: {datetime.fromtimestamp(min_ts)} to {datetime.fromtimestamp(max_ts)}")

def main():
    file_path = 'conversations.json'
    try:
        print(f"Loading {file_path}...")
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print("\n=== JSON Structure Analysis ===")
        analyze_json_structure(data)
        
        if isinstance(data, list) and len(data) > 0 and 'mapping' in data[0]:
             analyze_conversations_content(data)
        else:
            print("\nNote: File does not appear to be a standard ChatGPT conversations export.")

    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON from {file_path}.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
