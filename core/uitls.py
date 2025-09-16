import re

def parse_rules_file(filepath):
    groups = {}
    current_group = None

    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # Nhận diện tiêu đề nhóm
            if line.startswith("🔹 Nhóm hậu quả:"):
                current_group = line.replace("🔹 Nhóm hậu quả:", "").strip()
                groups[current_group] = []
                continue

            # Nhận diện luật
            if line.startswith("Hậu quả (consequents):"):
                rule = {}
            elif line.startswith("Các tác nhân (antecedents):"):
                rule["Các tác nhân"] = line.split(":", 1)[1].strip()
            elif line.startswith("Độ phổ biến"):
                rule["Support"] = float(re.findall(r"[-+]?\d*\.\d+|\d+", line)[0])
            elif line.startswith("Độ tin cậy"):
                rule["Confidence"] = float(re.findall(r"[-+]?\d*\.\d+|\d+", line)[0])
            elif line.startswith("Độ phụ thuộc"):
                rule["Lift"] = float(re.findall(r"[-+]?\d*\.\d+|\d+", line)[0])
                groups[current_group].append(rule)  # Kết thúc 1 luật

    return groups