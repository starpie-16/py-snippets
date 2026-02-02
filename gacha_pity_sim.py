import random

items = {
    "B Wheel": 90,
    "A Engine": 9.94,
    "SSR MAYBACH": 0.06
}

# Pity system
pity_count = 0
total_supplys = 0  # Total draw count

while True:
    # Draw 10 items
    draws = random.choices(list(items.keys()), weights=list(items.values()), k=10)

    # Check if SSR is obtained
    if "SSR MAYBACH" in draws:
        pity_count = 0  # Reset pity if SSR is won
    else:
        pity_count += 10  # Increase pity by 10

    # If pity reaches 90, guarantee an SSR
    if pity_count >= 90:
        draws[-1] = "SSR MAYBACH"  # Replace the last item with SSR
        pity_count = 0  # Reset pity

    total_supplys += 10  # Update total draw count

    # Count occurrences of each item
    result = {}
    for item in draws:
        result[item] = result.get(item, 0) + 1

    # Display information
    print(f"\n You have drawn {total_supplys} times!")
    print(" Results for this pull:")
    for item, count in result.items():
        print(f"  - {item}: {count} times")

    # Replay button (ask player if they want to continue)
    again = input("Pull again? (y/n): ").strip().lower()
    if again != 'y':
        break
