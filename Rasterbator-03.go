package main

import (
    "image"
    "image/color"
    "image/draw"
    "image/jpeg"
    "os"
    "log"
    "fyne.io/fyne/v2/app"
    "fyne.io/fyne/v2/canvas"
    "fyne.io/fyne/v2/container"
    "fyne.io/fyne/v2/widget"
    "github.com/jung-kurt/gofpdf"
)

func rasterbateImage(inputPath string, outputPath string, blockSize int) error {
    // Open the input image file
    inputFile, err := os.Open(inputPath)
    if err != nil {
        return err
    }
    defer inputFile.Close()

    // Decode the input image
    img, _, err := image.Decode(inputFile)
    if err != nil {
        return err
    }

    // Get the dimensions of the input image
    bounds := img.Bounds()
    width, height := bounds.Dx(), bounds.Dy()

    // Create a new blank image for rasterbated output
    outputImg := image.NewRGBA(image.Rect(0, 0, width*blockSize, height*blockSize))

    // Draw the rasterbated image
    for y := 0; y < height; y++ {
        for x := 0; x < width; x++ {
            // Get the color of the current pixel
            c := img.At(x, y)
            // Draw a block of the same color for each pixel in the input image
            for i := 0; i < blockSize; i++ {
                for j := 0; j < blockSize; j++ {
                    outputImg.Set(x*blockSize+i, y*blockSize+j, c)
                }
            }
        }
    }

    // Create a new file for the output image
    outputFile, err := os.Create(outputPath)
    if err != nil {
        return err
    }
    defer outputFile.Close()

    // Encode the output image as JPEG and save to the file
    err = jpeg.Encode(outputFile, outputImg, nil)
    if err != nil {
        return err
    }

    return nil
}

func exportToPDF(imagePaths []string, outputPath string) error {
    pdf := gofpdf.New("P", "mm", "A4", "")
    pdf.AddPage()

    for _, path := range imagePaths {
        pdf.ImageOptions(path, 0, 0, 210, 0, false, gofpdf.ImageOptions{ReadDpi: true}, 0, "")
    }

    return pdf.OutputFileAndClose(outputPath)
}

func main() {
    myApp := app.New()
    myWindow := myApp.NewWindow("Rasterbator")

    var imagePaths []string

    // Image Selection
    selectButton := widget.NewButton("Select Image", func() {
        dialog := myWindow.Canvas().FileDialog(widget.OpenFileChooser)
        dialog.SetFilter(storage.NewExtensionFileFilter([]string{".jpg", ".jpeg"}))
        dialog.SetDismissText("Cancel")
        dialog.Show()
        dialog.SetOnClosed(func() {
            if dialog.SelectedFiles() != nil && len(dialog.SelectedFiles()) > 0 {
                imagePath := dialog.SelectedFiles()[0]
                imagePaths = append(imagePaths, imagePath)
                image := canvas.NewImageFromFile(imagePath)
                myWindow.SetContent(container.NewBorder(nil, nil, nil, nil, image))
                myWindow.Resize(image.MinSize())
            }
        })
    })

    // Export to PDF
    exportButton := widget.NewButton("Export to PDF", func() {
        pdfPath := "output.pdf"
        err := exportToPDF(imagePaths, pdfPath)
        if err != nil {
            log.Fatal(err)
        }
        log.Println("PDF exported successfully to:", pdfPath)
    })

    myWindow.SetContent(container.NewVBox(
        selectButton,
        exportButton,
    ))

    myWindow.ShowAndRun()
}
