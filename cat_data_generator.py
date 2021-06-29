import uuid
import random
import pandas as pd
from datetime import datetime, timedelta

cat_names = [
        "peanut butter",
        "idget",
        "biscuit",
        "dr pepper",
        "sammy",
        "mio",
        ]

good_outcomes = [
        "Cat cuddled with me",
        "Cat cuddled with dog",
        "Cat cuddled with partner",
        "Cat did something adorable",
        ]

bad_outcomes = [
        "Cat bit me",
        "Cat attacked dog",
        "Cat scratched partner",
        "Cat scratched me",
        "Cat scratched something",
        ]

def gen_random_event(years):
    seconds_limit = 31557600 * years
    action = random.choice(["good", "bad"])

    if action == "good":
        comment = random.choice(good_outcomes)
    else:
        comment = random.choice(bad_outcomes)

    date_time = datetime.now() - timedelta(seconds=random.randint(0, seconds_limit))

    return {
            "_id":  uuid.uuid4(),
            "date": date_time.isoformat(),
            "action": action,
            "comment": comment,
            "cat": random.choice(cat_names),
            }

cat = pd.DataFrame([gen_random_event(15) for _ in
    range(400000)]).set_index('_id')
cat.to_csv('cat_data.csv')
