import numpy as np

SIZE = 1000
matrix = np.ones((SIZE, SIZE), dtype=int)  # Start with free space

# Draw border
matrix[0, :] = 3
matrix[-1, :] = 3
matrix[:, 0] = 3
matrix[:, -1] = 3

def place_square(matrix, cx, cy, sz):
    half = sz // 2
    x1, x2 = max(0, cx-half), min(SIZE, cx+half)
    y1, y2 = max(0, cy-half), min(SIZE, cy+half)
    matrix[y1:y2, x1:x2] = 0

# Place cubes (2.5cm ≈ 50px, 5cm ≈ 100px)
place_square(matrix, 150, 150, 50)   # Black cube (top-left)
place_square(matrix, 230, 750, 50)   # Green cube (bottom-left)
place_square(matrix, 350, 850, 50)   # Blue cube (bottom mid-left)
place_square(matrix, 610, 240, 50)   # Gray cube (upper, center-right)
place_square(matrix, 820, 200, 50)   # Gray cube (upper, right)
place_square(matrix, 720, 320, 100)  # Gray cube (big, right-middle)
place_square(matrix, 870, 120, 50)   # Red cube (top-right)

# Big gray rectangle (center-right)
rect_cx, rect_cy = 760, 560
rect_w, rect_h = 250, 230
x1, x2 = rect_cx - rect_w // 2, rect_cx + rect_w // 2
y1, y2 = rect_cy - rect_h // 2, rect_cy + rect_h // 2
matrix[max(0,y1):min(SIZE,y2), max(0,x1):min(SIZE,x2)] = 0

# Black bar (middle)
bar_cx, bar_cy = 450, 500
bar_w, bar_h = 80, 20
x1, x2 = bar_cx - bar_w // 2, bar_cx + bar_w // 2
y1, y2 = bar_cy - bar_h // 2, bar_cy + bar_h // 2
matrix[max(0,y1):min(SIZE,y2), max(0,x1):min(SIZE,x2)] = 0

# === Ask for error percentage and insert random errors ===
while True:
    try:
        percent_str = input("Enter error percentage (0–100): ")
        percent = float(percent_str)
        if 0 <= percent <= 100:
            break
        print("Please enter a value between 0 and 100.")
    except Exception:
        print("Invalid input. Please enter a number.")

num_errors = int(SIZE * SIZE * (percent / 100.0))
print(f"Inserting {num_errors} plausible errors...")

np.random.seed(43)
for _ in range(num_errors):
    y = np.random.randint(1, SIZE-1)
    x = np.random.randint(1, SIZE-1)
    old_val = matrix[y, x]
    # Only allow values 0, 1, or 3 (so no "illegal" values)
    new_val = np.random.choice([v for v in (0, 1, 3) if v != old_val])
    matrix[y, x] = new_val

np.savetxt("map_matrix_big_obstacle.txt", matrix, fmt='%d', delimiter=' ')
print("map_matrix_big_obstacle.txt saved! Now run your cleaning/reconstruction code.")
