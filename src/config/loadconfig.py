#./src/config/loadconfig.py
import json

def load_config(file_path):
    """
    Load the JSON configuration from the specified file path.
    """
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file: {file_path}")
        return None

def get_openai_keys(config):
    """
    Extract and return the OpenAI API keys from the configuration.
    """
    keys = []
    if config is not None:
        for entry in config:
            if "api_key" in entry:
                keys.append(entry["api_key"])
    return keys

def main():
    config_path = './src/config/OAI_CONFIG.json'
    config = load_config(config_path)
    
    if config is not None:
        openai_keys = get_openai_keys(config)
        if openai_keys:
            print("OpenAI API Keys found in the configuration:")
            for key in openai_keys:
                print(key)
        else:
            print("No OpenAI API keys found in the configuration.")
    else:
        print("Failed to load or parse the configuration.")

if __name__ == "__main__":
    main()
