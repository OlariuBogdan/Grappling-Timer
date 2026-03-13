# BJJ Grappling Timer Pro

A professional-grade interval timer application designed specifically for Brazilian Jiu-Jitsu (BJJ) training sessions. Features a touch-friendly interface, customizable presets, integrated music player, and comprehensive sound feedback.

## Features

### 🕐 Timer Functionality
- **Preset Training Modes**: Adult Gi (8min/10min), No-Gi (10min), Competition, Submission Only, Training
- **Customizable Settings**: Adjust work time, rest time, and number of rounds
- **Preparation Phase**: 12-second preparation countdown before training begins
- **Visual Indicators**: Color-coded phases (Yellow=Prepare, Green=Work, Red=Rest, Blue=Finished)
- **Warning System**: 10-second warning before round transitions

### 🎵 Music Player
- **USB Music Support**: Load music folders from external drives
- **Auto-Advance**: Automatically plays next track when current song ends
- **Volume Control**: Adjustable volume slider
- **Track Navigation**: Previous/Next track controls
- **Compact Display**: Shows current track name with truncation for long filenames

### 🔊 Sound System
- **Event-Based Audio**: Different sounds for preparation, work start, rest, warnings, and completion
- **Fallback System**: Uses Windows system beeps if audio files are unavailable
- **Pygame Integration**: High-quality audio playback with low latency

### 🎯 User Interface
- **Fullscreen Mode**: Optimized for touchscreens and projection
- **Touch-Friendly**: Large buttons and high-contrast colors
- **Keyboard Shortcuts**: F11 for fullscreen, Escape to exit fullscreen
- **Status Display**: Real-time status updates and round information
- **Responsive Design**: Adapts to different screen sizes

### ⚙️ Advanced Features
- **Pause/Resume**: Pause training at any time and resume later
- **Reset Functionality**: Reset timer to initial state
- **Round Tracking**: Displays current round and total rounds
- **Time Display**: Large, easy-to-read digital clock font

## Installation

### Prerequisites
- Python 3.8 or higher
- Windows operating system (uses winsound for fallback)

### Setup
1. Clone or download the project
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Place audio files in the `sounds/` directory
4. Run the application:
   ```bash
   python timer.py
   ```

## Audio Files

Place the following audio files in the `sounds/` directory:

- `pregatire.mp3` - Preparation phase sound
- `start 2.mp3` - Work round start sound
- `final.mp3` - Rest phase start sound
- `start.wav` - 10-second warning sound
- `final 2.mp3` - Training completion sound

## Usage

### Basic Operation
1. **Select Preset**: Choose from predefined training modes or customize settings
2. **Adjust Settings**: Use +/- buttons to modify work time, rest time, and rounds
3. **Start Training**: Press the green START button
4. **Control Playback**: Use PAUSE to temporarily stop, RESET to restart

### Music Player
1. **Load Music**: Click "FOLDER" button and select a directory containing MP3/WAV files
2. **Playback Control**: Use play/pause, previous/next buttons
3. **Volume**: Adjust volume using the slider

### Fullscreen Mode
- Press F11 to toggle fullscreen
- Press Escape to exit fullscreen

## Configuration

The application automatically saves your last used settings and restores them on startup.

## Technical Details

- **GUI Framework**: Tkinter with custom styling
- **Audio Engine**: Pygame mixer with winsound fallback
- **File Formats**: Supports MP3 and WAV audio files
- **Display**: Optimized for 1080p+ resolutions
- **Performance**: Low CPU usage, real-time updates

## Troubleshooting

### Audio Issues
- Ensure audio files are in the correct format (MP3/WAV)
- Check file permissions and paths
- Pygame will fallback to system beeps if audio fails

### Display Issues
- The application is designed for fullscreen use
- Ensure your display supports the requested resolution
- Font sizes are optimized for touch interfaces

### Performance
- Close other applications for best performance
- The timer runs on a 1-second update cycle
- Music playback is handled asynchronously

## Development

### Project Structure
```
├── timer.py              # Main application
├── sound_manager.py      # Audio management
├── sounds/               # Audio files directory
│   ├── README.txt        # Audio file documentation
│   └── *.mp3/*.wav       # Sound files
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

### Code Style
- Object-oriented design
- Comprehensive error handling
- Modular sound management
- Event-driven UI updates

## License

This project is open source. Feel free to modify and distribute.

## Contributing

Contributions are welcome! Please ensure code quality and maintain the touch-friendly design philosophy.

## Support

For issues or feature requests, please check the troubleshooting section or create an issue in the repository.