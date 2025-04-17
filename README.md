game-project-directory-creator:
Creates a template directory structure for game development.

directory_svg_generator:
Creates directory visual tree html file

![directory_svg_generator](directory_svg_generator.jpg)


# Game Project Directory Creator

A comprehensive Python tool to generate a standardized, production-ready directory structure for game development projects. This tool creates an organized framework aligned with game development best practices, supporting various engines and platforms.

## Features

- **Complete Project Structure**: Creates a professional directory structure for all phases of game development.
- **Production Pipeline Organization**: Includes dedicated folders for Pre-Production, Production, and Post-Production phases.
- **Multiple Engine Support**: Built-in templates for Unity, Unreal, Godot, and custom engines.
- **Cross-Platform**: Configure builds for multiple target platforms (Windows, MacOS, Linux, consoles, mobile, web).
- **Documentation**: Automatically generates description files for all directories explaining their purpose.
- **Temporary File Management**: Includes comprehensive tmp directory structure with cleanup scripts.
- **Source Organization**: Well-structured folders for code, assets, tests, and third-party dependencies.
- **Version Control Ready**: Includes basic .gitignore configuration.

## Installation

```bash
# Clone the repository
git clone https://github.com/kursatturkay/game-project-directory-creator.git

# Navigate to the directory
cd game-project-directory-creator

# Make the script executable (Linux/Mac)
chmod +x game-project-directory-creator.py
```

## Usage

### Basic Usage (Interactive Mode)

```bash
python game-project-directory-creator.py
```

Follow the interactive prompts to specify your game name, directory location, engine, and platforms.

### Command-Line Arguments

```bash
python game-project-directory-creator.py --game-name "My Awesome Game" --root-dir "/path/to/projects" --engine Unity --platforms Windows,MacOS,Linux
```

### Available Options

- `--game-name`: Name of your game project
- `--root-dir`: Root directory where the game structure will be created
- `--engine`: Game engine to use (Custom, Unity, Unreal, Godot)
- `--platforms`: Comma-separated list of target platforms
- `--examples`: Show usage examples and exit

### Available Engines

- Custom (generic structure)
- Unity
- Unreal
- Godot

### Available Platforms

- Windows
- MacOS
- Linux
- Android
- iOS
- PlayStation
- Xbox
- Nintendo
- Web

## Directory Structure Overview

The generated project structure includes:

### Production Pipeline

- **Pre-Production**: Idea, Story, Characters, Art Direction, Storyboard, Product Planning, Marketing, etc.
- **Production**: Layout, Modeling, Texturing, Rigging, Animation, Lighting, VFX, Sound, Music, etc.
- **Post-Production**: Compositing, 2D VFX, Color Correction, Final Output, etc.

### Development Framework

- **Documentation**: Design documents, technical specifications, API references
- **Source**: Core game systems, gameplay code, engine components, development tools
- **Assets**: Models, textures, animations, audio, shaders, UI elements
- **Build**: Platform-specific build outputs
- **Tests**: Unit tests and integration tests
- **ThirdParty**: External libraries and tools
- **Scripts**: Build, deployment, and utility scripts
- **Config**: Engine and game configuration
- **Versions**: Version tracking
- **Releases**: Organized release builds for different distribution channels
- **tmp**: Temporary files, builds, caches, and logs

### Engine-Specific Structure

The tool generates additional directories based on the selected game engine:

- **Unity**: Assets/Prefabs, Assets/Materials, Assets/Scenes, etc.
- **Unreal**: Content/Blueprints, Content/Materials, Content/Levels, etc.
- **Godot**: scenes, scripts, assets, addons, etc.

## Temporary File Management

The generated project includes a comprehensive `tmp` directory structure with:

- Multiple categorized temporary directories (Builds, Cache, Logs, etc.)
- Dedicated media subdirectories (Images, Audio, Video, Textures)
- Workflow directories (Prototypes, Staging, Review, Processing, etc.)
- Python cleanup script for managing temporary files

```bash
# Run the cleanup script to delete tmp files older than 7 days
python Scripts/Tools/cleanup_tmp.py

# Specify age in days for cleanup
python Scripts/Tools/cleanup_tmp.py --age 30

# Dry run (shows what would be deleted without actually deleting)
python Scripts/Tools/cleanup_tmp.py --dry-run
```

## Blender Integration

The structure includes special directories for Blender workflows:

- **Source/Tools/BlenderAddons**: For custom Blender add-ons
- **Assets/Models/Sources**: For original .blend files
- **Assets/Models/Exported**: For game-ready exported models
- **Scripts/Pipeline**: For asset pipeline automation (Blender to game engine)

## Examples

### Basic Example
```bash
python game-project-directory-creator.py --game-name "Space Adventure"
```

### Unity Project with Multiple Platforms
```bash
python game-project-directory-creator.py --game-name "Puzzle Quest" --engine Unity --platforms Windows,Android,iOS
```

### Unreal Project for Console Development
```bash
python game-project-directory-creator.py --game-name "Epic RPG" --engine Unreal --platforms Windows,PlayStation,Xbox
```

### View All Available Examples
```bash
python game-project-directory-creator.py --examples
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
