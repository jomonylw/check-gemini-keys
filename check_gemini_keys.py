import requests
import time
import json
import os

# --- 配置 ---
INPUT_FILENAME = "gemini_key.txt"
OUTPUT_FILENAME = "valid_key.txt"
# 使用一个成本较低、响应较快的模型进行测试
MODEL_NAME = "gemini-1.5-flash-latest"
API_ENDPOINT_TEMPLATE = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent"
HEADERS = {'Content-Type': 'application/json'}
# 一个非常简单的测试负载，减少消耗
TEST_PAYLOAD = json.dumps({"contents": [{"parts":[{"text": "Hi"}]}]})
# 请求超时时间（秒）
REQUEST_TIMEOUT = 10
# 每次请求之间的延迟（秒），防止触发速率限制
DELAY_BETWEEN_REQUESTS = 0.5 # 0.5秒延迟

# ANSI 颜色代码（用于控制台输出）
COLOR_GREEN = "\033[92m"
COLOR_RED = "\033[91m"
COLOR_YELLOW = "\033[93m"
COLOR_RESET = "\033[0m"
# --- 配置结束 ---

def check_gemini_key(api_key):
    """
    通过向 Gemini API 发送简单请求来检查 API 密钥的有效性。

    Args:
        api_key (str): 要测试的 Gemini API 密钥。

    Returns:
        tuple: (bool, str) - 第一个元素表示密钥是否有效，第二个元素是状态消息。
    """
    if not api_key:
        return False, "Empty key string provided"

    url = f"{API_ENDPOINT_TEMPLATE}?key={api_key}"
    try:
        response = requests.post(
            url,
            headers=HEADERS,
            data=TEST_PAYLOAD,
            timeout=REQUEST_TIMEOUT
        )

        # 检查 HTTP 状态码
        if response.status_code == 200:
            # 进一步检查响应内容是否有效（可选，但更可靠）
            try:
                response_json = response.json()
                if 'candidates' in response_json or 'promptFeedback' in response_json:
                     return True, f"{COLOR_GREEN}Valid{COLOR_RESET}"
                else:
                    # 状态码 200 但响应格式不对，可能是一个非 Gemini 的有效 Key 或者 API 行为变更
                    return False, f"{COLOR_YELLOW}Warning: Status 200 but unexpected response format{COLOR_RESET}"
            except json.JSONDecodeError:
                return False, f"{COLOR_YELLOW}Warning: Status 200 but response is not valid JSON{COLOR_RESET}"

        elif response.status_code == 400:
             error_message = f"Invalid Key or Request (HTTP {response.status_code})"
             try:
                 error_data = response.json()
                 error_message += f": {error_data.get('error', {}).get('message', 'No specific error message')}"
             except json.JSONDecodeError:
                 error_message += f": {response.text[:150]}" # 显示部分原始错误文本
             return False, f"{COLOR_RED}{error_message}{COLOR_RESET}"
        elif response.status_code == 403:
             return False, f"{COLOR_RED}Permission Denied (HTTP {response.status_code}). Check API enablement or restrictions.{COLOR_RESET}"
        elif response.status_code == 429:
            return False, f"{COLOR_YELLOW}Rate Limited (HTTP {response.status_code}). Try increasing DELAY_BETWEEN_REQUESTS.{COLOR_RESET}"
        else:
            return False, f"{COLOR_RED}Failed with HTTP {response.status_code}: {response.text[:100]}{COLOR_RESET}"

    except requests.exceptions.Timeout:
        return False, f"{COLOR_YELLOW}Request Timed Out ({REQUEST_TIMEOUT}s){COLOR_RESET}"
    except requests.exceptions.RequestException as e:
        return False, f"{COLOR_RED}Network or Request Error: {e}{COLOR_RESET}"
    except Exception as e:
        # 捕获其他意外错误
        return False, f"{COLOR_RED}An unexpected error occurred: {e}{COLOR_RESET}"

def main():
    """
    主函数，读取密钥文件，测试密钥，并将有效密钥写入输出文件。
    """
    print(f"--- Gemini API Key Checker ---")
    valid_keys = []
    keys_to_check = []

    # 检查输入文件是否存在
    if not os.path.exists(INPUT_FILENAME):
        print(f"{COLOR_RED}Error: Input file '{INPUT_FILENAME}' not found.{COLOR_RESET}")
        print(f"Please create '{INPUT_FILENAME}' and add your API keys, one per line.")
        return

    # 读取密钥
    try:
        with open(INPUT_FILENAME, 'r') as f_in:
            # Read all non-empty lines
            raw_keys_to_check = [line.strip() for line in f_in if line.strip()]
        original_key_count = len(raw_keys_to_check)
        # Deduplicate while preserving order (Python 3.7+)
        keys_to_check = list(dict.fromkeys(raw_keys_to_check))
        deduplicated_key_count = len(keys_to_check)
        print(f"Read {original_key_count} keys from '{INPUT_FILENAME}'. ", end="")
        if original_key_count > deduplicated_key_count:
            print(f"Found {deduplicated_key_count} unique keys after deduplication.")
        else:
            print(f"All {deduplicated_key_count} keys are unique.")
    except Exception as e:
        print(f"{COLOR_RED}Error reading input file '{INPUT_FILENAME}': {e}{COLOR_RESET}")
        return

    if not keys_to_check:
        print(f"{COLOR_YELLOW}No keys found in '{INPUT_FILENAME}'.{COLOR_RESET}")
        return

    print(f"Starting checks (Model: {MODEL_NAME}, Delay: {DELAY_BETWEEN_REQUESTS}s)...")
    print("-" * 30)

    # 逐个测试密钥
    for i, key in enumerate(keys_to_check):
        # 打印部分密钥以供识别，隐藏大部分内容
        key_display = f"...{key[-6:]}" if len(key) > 6 else key
        print(f"[{i+1}/{len(keys_to_check)}] Checking key ending in '{key_display}': ", end="")
        is_valid, status_message = check_gemini_key(key)

        print(status_message) # 打印来自 check_gemini_key 的带颜色消息

        if is_valid:
            valid_keys.append(key)

        # 在每次请求后暂停，避免速率限制
        if i < len(keys_to_check) - 1:
             time.sleep(DELAY_BETWEEN_REQUESTS)

    print("-" * 30)
    print(f"Check complete.")
    print(f"Found {COLOR_GREEN}{len(valid_keys)}{COLOR_RESET} valid keys out of {len(keys_to_check)} checked.")

    # 将有效密钥写入输出文件
    if valid_keys:
        try:
            with open(OUTPUT_FILENAME, 'w') as f_out:
                for key in valid_keys:
                    f_out.write(key + '\n')
            print(f"Valid keys saved to '{OUTPUT_FILENAME}'.")
        except Exception as e:
            print(f"{COLOR_RED}Error writing output file '{OUTPUT_FILENAME}': {e}{COLOR_RESET}")
    else:
        print(f"No valid keys found to save.")

if __name__ == "__main__":
    # 检查 requests 库是否安装
    try:
        import requests
    except ImportError:
        print(f"{COLOR_RED}Error: The 'requests' library is not installed.{COLOR_RESET}")
        print("Please install it by running: pip install requests")
        exit() # 退出脚本

    main()
