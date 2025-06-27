# Python-Project
---
# _Typing Speed Test_

A Python-based typing speed test application inspired by Monkeytype, featuring real-time character checking, WPM calculation, accuracy tracking, and keypress sounds.

## Features

- **Real-time Character Checking**: Immediate visual feedback for correct/incorrect characters
- **Live Statistics**: WPM, accuracy, progress, and timer updated in real-time
- **Keypress Sounds**: Audio feedback for correct and incorrect keystrokes
- **Visual Highlighting**: Current character highlighting and color-coded feedback
- **Multiple Sample Texts**: Random selection from various typing passages
- **Results Screen**: Comprehensive test completion summary
- **Clean UI**: Monkeytype-inspired dark theme

## Installation

1. Install Python 3.7 or higher
2. Install required dependencies:
   ```
   pip install pygame
   ```

## Usage

Run the typing test:
```
python type.py
```

### Controls

- **Start typing** to begin the test
- **Backspace** to correct mistakes
- **Space** to restart after completion
- **Escape** to quit the application

## How It Works

1. **Character Checking**: Each keystroke is compared against the expected character
2. **WPM Calculation**: Words per minute based on standard 5-character word length
3. **Accuracy Tracking**: Percentage of correct characters typed
4. **Visual Feedback**: Color-coded text showing progress and errors

## Customization

You can easily customize:
- **Colors**: Modify the `COLORS` dictionary
- **Sample Texts**: Add new passages to the `SAMPLE_TEXTS` list
- **Fonts**: Change font sizes in the `__init__` method

## Technical Details

- Built with Pygame for cross-platform compatibility
- Real-time input handling with immediate feedback
- Efficient text rendering with character-level highlighting
- Responsive UI design with proper text wrapping
