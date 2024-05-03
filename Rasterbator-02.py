import tkinter as tk
from tkinter import filedialog
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def rasterbate(image_path, output_prefix, tile_size=(100, 100), overlap=10):
    # Open the image
    img = Image.open(image_path)
    img_width, img_height = img.size

    # Calculate the number of tiles
    num_tiles_x = img_width // (tile_size[0] - overlap)
    num_tiles_y = img_height // (tile_size[1] - overlap)

    # Create PDF canvas
    pdf_width, pdf_height = letter
    c = canvas.Canvas(output_prefix + ".pdf", pagesize=letter)

    # Loop through each tile and draw it on the PDF canvas
    for y in range(num_tiles_y):
        for x in range(num_tiles_x):
            # Calculate coordinates for cropping
            left = x * (tile_size[0] - overlap)
            upper = y * (tile_size[1] - overlap)
            right = min(left + tile_size[0], img_width)
            lower = min(upper + tile_size[1], img_height)

            # Crop the tile
            tile = img.crop((left, upper, right, lower))

            # Draw tile on PDF canvas
            c.drawInlineImage(tile, 0, 0, width=pdf_width, height=pdf_height)

            # Add a new page for the next tile
            c.showPage()

    # Save the PDF file
    c.save()

def browse_image():
    filename = filedialog.askopenfilename(initialdir="/", title="Select Image", filetypes=(("Image files", "*.jpg;*.jpeg;*.png"), ("All files", "*.*")))
    entry_image.delete(0, tk.END)
    entry_image.insert(0, filename)

def rasterbate_image():
    image_path = entry_image.get()
    output_prefix = entry_prefix.get()
    tile_size = (int(entry_tile_width.get()), int(entry_tile_height.get()))
    overlap = int(entry_overlap.get())
    rasterbate(image_path, output_prefix, tile_size, overlap)
    status_label.config(text="Rasterbation completed.")

def export_pdf():
    output_prefix = entry_prefix.get()
    rasterbate_image()
    status_label.config(text="Exporting as PDF...")
    status_label.update()
    status_label.config(text="PDF export completed.")

# Create main window
root = tk.Tk()
root.title("Rasterbation GUI")

# Create widgets
label_image = tk.Label(root, text="Select Image:")
entry_image = tk.Entry(root, width=50)
button_browse = tk.Button(root, text="Browse", command=browse_image)

label_prefix = tk.Label(root, text="Output Prefix:")
entry_prefix = tk.Entry(root, width=50)

label_tile_size = tk.Label(root, text="Tile Size (Width x Height):")
entry_tile_width = tk.Entry(root, width=5)
entry_tile_height = tk.Entry(root, width=5)

label_overlap = tk.Label(root, text="Overlap:")
entry_overlap = tk.Entry(root, width=5)

button_rasterbate = tk.Button(root, text="Rasterbate", command=rasterbate_image)
button_export_pdf = tk.Button(root, text="Export as PDF", command=export_pdf)
status_label = tk.Label(root, text="")

# Layout widgets
label_image.grid(row=0, column=0, padx=5, pady=5)
entry_image.grid(row=0, column=1, columnspan=2, padx=5, pady=5)
button_browse.grid(row=0, column=3, padx=5, pady=5)

label_prefix.grid(row=1, column=0, padx=5, pady=5)
entry_prefix.grid(row=1, column=1, columnspan=3, padx=5, pady=5)

label_tile_size.grid(row=2, column=0, padx=5, pady=5)
entry_tile_width.grid(row=2, column=1, padx=5, pady=5)
entry_tile_height.grid(row=2, column=2, padx=5, pady=5)

label_overlap.grid(row=3, column=0, padx=5, pady=5)
entry_overlap.grid(row=3, column=1, padx=5, pady=5)

button_rasterbate.grid(row=4, column=0, columnspan=4, padx=5, pady=5)
button_export_pdf.grid(row=5, column=0, columnspan=4, padx=5, pady=5)
status_label.grid(row=6, column=0, columnspan=4)

# Start GUI event loop
root.mainloop()
