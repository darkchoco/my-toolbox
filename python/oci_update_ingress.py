import json
import sys
from requests import get


def update_source_in_json(file_path, new_source_ip):
    # JSON 파일 읽기
    with open(file_path, 'r') as f:
        data = json.load(f)

    # 'description'이 'HomeOffice'인 항목의 'source' 업데이트
    for item in data:
        if item.get("description") == "HomeOffice":
            item["source"] = new_source_ip

    # 변경된 내용을 같은 파일에 다시 저장
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)


if __name__ == "__main__":
    # 스크립트 실행 시 인자로 JSON 파일 경로와 새로운 소스 값을 받음
    if len(sys.argv) < 2:
        print("Usage: python update_json.py <json_file_path> <new_source>")
        sys.exit(1)

    json_file_path = sys.argv[1]
    if len(sys.argv) == 2:
        new_source = get('https://ident.me').text + "/32"
    else:
        new_source = sys.argv[2]

    update_source_in_json(json_file_path, new_source)
    print(f"Updated 'source' to '{new_source}' for 'description' == 'HomeOffice'")
