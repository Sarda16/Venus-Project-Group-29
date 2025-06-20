import numpy as np
import cv2
import matplotlib.pyplot as plt
from skimage.draw import polygon_perimeter, polygon

# === PARAMETERS ===
FILENAME = "map_matrix_big_obstacle.txt"
CLEANED_FILENAME = "map_matrix_big_obstacle_cleaned.txt"
RECONSTRUCTED_FILENAME = "map_matrix_reconstructed.txt"
MIN_OBSTACLE_SIZE = 1000
SIZE = 1000

def make_labeled_img(matrix):
    rgb_img = np.ones((SIZE, SIZE, 3), dtype=np.float32)
    rgb_img[matrix == 1] = [0, 0.8, 0.95]  # Free space (cyan)
    rgb_img[matrix == 3] = [0, 0, 0]       # Border (black)
    rgb_img[matrix == 0] = [0, 0, 0]       # Obstacles (black)

    # Copy for annotation
    img = rgb_img.copy()

    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats((matrix == 0).astype(np.uint8), connectivity=8)
    label_texts = []

    for label in range(1, num_labels):
        area = stats[label, cv2.CC_STAT_AREA]
        cx, cy = centroids[label]
        if 2100 < area < 2500:
            text = "2.5cm Cube"
        elif 8500 < area < 11000:
            text = "5cm Cube"
        elif 1200 < area < 2000:
            text = "Cliff"
        elif area > 30000:
            text = "Big Obstacle"
        else:
            text = "2.5cm Cube"
        label_texts.append((cx, cy - 30, text))
    return img, label_texts

# Load matrices
matrix_cleaned = np.loadtxt(CLEANED_FILENAME, dtype=np.int32)
matrix_recon = np.loadtxt(RECONSTRUCTED_FILENAME, dtype=np.int32)

# Make images and label positions
img1, labels1 = make_labeled_img(matrix_cleaned)
img2, labels2 = make_labeled_img(matrix_recon)

# === Plot side by side and SAVE ===
fig, axes = plt.subplots(1, 2, figsize=(18, 9))
for ax, img, labels, title in zip(axes, [img1, img2], [labels1, labels2],
                                  ["Cleaned Map (Before Reconstruction)", "Reconstructed Map (After Reconstruction)"]):
    ax.imshow(img, origin='upper')
    for x, y, text in labels:
        ax.text(x, y, text, color='red', fontsize=14, weight='bold', ha='center', va='bottom')
    ax.set_title(title)
    ax.axis('off')
plt.tight_layout()

# Save the combined figure
plt.savefig("comparison.png", bbox_inches='tight', dpi=300)
print("Saved comparison as 'comparison.png'.")

plt.show()
