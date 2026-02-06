def print_header(title: str):
    print("\n" + "═" * 60)
    print(f"{title:^60}")
    print("═" * 60)

def print_kv(label: str, value: str):
    print(f"{label:<18} : {value}")
