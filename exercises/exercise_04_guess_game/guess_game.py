"""练习 4：猜数字游戏（实现我，然后写测试）"""

import random


def guess_number(max_attempts: int = 5, low: int = 1, high: int = 100) -> dict:
    """
    猜数字游戏纯逻辑版本。
    返回 {"win": bool, "attempts": int, "answer": int}
    """
    answer = random.randint(low, high)
    used = 0
    while used < max_attempts:
        while True:
            raw = input(f"请输入 {low}~{high} 之间的数字：")
            # TODO: 非数字输入 continue（不消耗次数）
            if raw.isdigit():
                break
            else:
                continue
        guess = int(raw)
        used += 1
        # TODO: 猜对返回 win=True
        if guess == answer:
            return {"win": True, "attempts": used, "answer": answer}
        # TODO: 给出大小提示（返回结构里可加 hint，或直接进入下一轮）
    # TODO: 次数用尽返回 win=False
    return {"win": False, "attempts": used, "answer": answer}
