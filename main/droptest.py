import random

# Function to determine card droprate
def droprate():
    random_number = random.randint(1, 10000)

    if random_number > 9899:  # 0.1% for LR
        return "LR"
    elif random_number > 9798:  # 1.01% for UR
        return "UR"
    elif random_number > 8998:  # 8% for SSR
        return "SSR"
    elif random_number > 7998:  # 10% for SR
        return "SR"
    elif random_number > 4998:  # 30% for R
        return "R"
    else:  # 50% for N
        return "N"

# Cards in each rarity
card_pool = {
    'N': ['SideCharacter (N)', 'SideCharacter2 (N)'],
    'R': ['PyroStark (R)', 'Rukironii (R)', 'Branakuya (R)'],
    'SR': ['Lensu (SR)', 'Munozaki (SR)'],
    'SSR': ['TomKuna (SSR)', 'Shinrago (SSR)', 'GrimDrago (SSR)'],
    'UR': ['YachiTuan (UR)'],
    'LR': ['Diddy Force (LR)']
}

# Getting the rarity to choose which pool
def card_drop():
    cardRarity = droprate()
    card = random.choice(card_pool[cardRarity])
    return cardRarity, card

# Simulate 100 drops to test the percentages
drop_results = {"N": 0, "R": 0, "SR": 0, "SSR": 0, "UR": 0, "LR": 0}

# Run 100 trials to test the drop rates
for _ in range(100):
    rarity, _ = card_drop()
    drop_results[rarity] += 1

# Display the results
print("Results from 100 trials:")
for rarity, count in drop_results.items():
    print(f"{rarity}: {count} drops")
