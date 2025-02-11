# Background-Remover-Advance

Background Remover is a Python-based GUI application that removes backgrounds from images using the `rembg` library. It provides both single image processing and batch processing capabilities with a user-friendly interface built using Tkinter.

## Features
- **Single Image Processing**: Remove the background from a single image and save the output.
- **Batch Processing**: Process multiple images in a directory and save the results automatically.
- **Preview Support** (Planned): Display input and output images before and after processing.
- **Progress Tracking**: Real-time progress bar and log updates for batch processing.
- **Multi-threaded Logging**: Ensures a responsive GUI while processing images.

## Requirements
Before running the application, make sure you have the following dependencies installed:

```bash
pip install tkinter rembg pillow
```

## Installation & Usage
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/background-remover.git
   cd background-remover
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python background_remover.py
   ```

## How to Use
### Single Image Mode
1. Click on the **Single Image** tab.
2. Select an input image file.
3. Choose the output file location.
4. Click **Remove Background** to process the image.

### Batch Processing Mode
1. Click on the **Batch Processing** tab.
2. Select the input directory containing images.
3. Select the output directory for processed images.
4. Click **Remove Backgrounds** to start processing.

## Contributing
Contributions are welcome! If you find a bug or have a feature request, please open an issue or submit a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Author
Developed by [Your Name](https://github.com/mutassimalzeem).

