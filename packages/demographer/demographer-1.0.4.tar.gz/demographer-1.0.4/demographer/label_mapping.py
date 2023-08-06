race_label_mapping = {
    "white": 0, "black": 1, "asian": 3, "latin": 2, "latinx": 2,
    None: None,
    "White": 0, "Black": 1, "Asian": 3, "Hispanic": 2,
    'black/african american': 1, 'latino/hispanic': 2}
race_back_mapping = {0: "W", 1: "B", 2: "H/L", 3: "A"}
race_bert_back_mapping = {1: "B", 2: "H/L", 3: "A", 4: "W"}
vocab_mapping = {0: "White", 1: "Black", 2: "Hispanic", 3: "Asian"}

gender_label_mapping = {"Man": 1, "Woman": 0}
gender_back_mapping = {1: "Man", 0: "Woman"}
