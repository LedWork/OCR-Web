
def mark_incorrect(data):
    data['correct'] = False
    print(data)


def mark_correct(data):
    data['correct'] = True
    print(data)
    print(f"Marked as correct: {data}")

