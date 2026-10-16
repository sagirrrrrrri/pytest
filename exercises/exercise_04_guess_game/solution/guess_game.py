"""练习 4 参考答案：guess_game 完整实现"""
import random


def guess_number(max_attempts: int = 5, low: int = 1, high: int = 100) -> dict:
    answer = random.randint(low, high)
    used = 0
    last_hint = ""
    while used < max_attempts:
        raw = input(f"请输入 {low}~{high} 之间的数字：")
        try:
            guess = int(raw)
        except ValueError:
            continue  # 非数字不计次数
        used += 1
        if guess == answer:
            return {"win": True, "attempts": used, "answer": answer}
        last_hint = "猜小了" if guess < answer else "猜大了"
    return {"win": False, "attempts": max_attempts, "answer": answer, "hint": last_hint}
