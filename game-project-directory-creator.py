#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import shutil
import datetime
import argparse

# Define production phases
PRE_PRODUCTION = "Pre-Production"
PRODUCTION = "Production"
POST_PRODUCTION = "Post-Production"

def create_game_directory_structure(game_name, root_directory, engine="Custom", platforms=None):
    """
    Creates a template directory structure for game development
    
    Args:
        game_name (str): Name of the game
        root_directory (str): Root directory where the game structure will be created
        engine (str): Game engine to be used (default: "Custom")
        platforms (list): Target platforms (default: ["Windows", "MacOS", "Linux"])
    
    Returns:
        str: Path to the created game directory
    """
    if platforms is None:
        platforms = ["Windows", "MacOS", "Linux"]
    
    # Create the full path for the game directory
    game_dir = os.path.join(root_directory, game_name.replace(" ", ""))
    
    # Define directory structure with descriptions
    directory_descriptions = {
        # Production Pipeline Organization
        f"{PRE_PRODUCTION}/Idea": "Contains initial game concept documents and brainstorming materials.",
        f"{PRE_PRODUCTION}/Story": "Contains narrative structure, plot outlines, and story development documents.",
        f"{PRE_PRODUCTION}/Characters": "Contains character designs, backstories, and development.",
        f"{PRE_PRODUCTION}/ArtDirection": "Contains art style guides, mood boards, and visual direction documents.",
        f"{PRE_PRODUCTION}/Storyboard": "Contains storyboards for cutscenes and key game moments.",
        f"{PRE_PRODUCTION}/ProductPlanning": "Contains project schedules, milestone planning, and production roadmaps.",
        f"{PRE_PRODUCTION}/Marketing": "Contains early marketing plans, target audience analysis, and promotional strategy.",
        f"{PRE_PRODUCTION}/VocalTracks": "Contains voice acting scripts, audition materials, and placeholder recordings.",
        f"{PRE_PRODUCTION}/StoryReel": "Contains animatics and early visualization of game sequences.",
        f"{PRE_PRODUCTION}/RnD": "Contains research and development materials for new gameplay features or technologies.",
        
        f"{PRODUCTION}/Layout": "Contains scene layout files and environment blocking.",
        f"{PRODUCTION}/Modeling": "Contains 3D modeling files and assets in production.",
        f"{PRODUCTION}/Texturing": "Contains texturing work files and materials in development.",
        f"{PRODUCTION}/Rigging": "Contains character and object rig files and setups.",
        f"{PRODUCTION}/Animation": "Contains animation work in progress and animation systems.",
        f"{PRODUCTION}/Lighting": "Contains lighting setups and environment illumination assets.",
        f"{PRODUCTION}/VFX": "Contains visual effects work and particle systems in development.",
        f"{PRODUCTION}/SoundFX": "Contains sound effects work files and mixing in progress.",
        f"{PRODUCTION}/Music": "Contains musical score work and soundtrack development.",
        f"{PRODUCTION}/Rendering": "Contains rendering outputs and material previews.",
        f"{PRODUCTION}/TitleCredits": "Contains title screen and credits sequence development.",
        f"{PRODUCTION}/CharSetup": "Contains character finalization and implementation.",
        
        f"{POST_PRODUCTION}/Compositing": "Contains scene composition work and final visual integration.",
        f"{POST_PRODUCTION}/2DVFX": "Contains 2D visual effects and motion graphics elements.",
        f"{POST_PRODUCTION}/ColorCorrection": "Contains color grading and final visual polish.",
        f"{POST_PRODUCTION}/FinalOutput": "Contains finalized game scenes ready for implementation.",
        
        "Documentation/Design": "Contains game design documents, concept art, and gameplay specifications.",
        "Documentation/Technical": "Contains technical documentation, architecture diagrams, and implementation details.",
        "Documentation/API": "Contains API reference documentation for the game's programming interfaces.",
        
        "Source/Core": "Contains core game engine systems and fundamental components.",
        "Source/Game": "Contains game-specific code, gameplay mechanics, and game logic.",
        "Source/Engine": "Contains engine components, rendering systems, physics, and other subsystems.",
        "Source/Tools": "Contains development tools and utilities for the game development process.",
        "Source/Tools/BlenderAddons": "Contains custom Blender add-ons for the game development pipeline.",
        
        "Assets/Models/Sources": "Contains original Blender (.blend) model files.",
        "Assets/Models/Exported": "Contains exported game-ready models in engine-compatible formats.",
        "Assets/Textures": "Contains texture files, materials, and surface descriptions.",
        "Assets/Animations": "Contains character and object animations.",
        "Assets/Audio": "Contains sound effects, music, and voice recordings.",
        "Assets/Shaders": "Contains shader programs for visual effects and rendering techniques.",
        "Assets/UI": "Contains user interface assets, icons, and UI-specific graphics.",
        "Assets/3DAnimate": "Contains 3D animation files and rigs for game characters and objects.",
        
        "tmp/Builds": "Contains temporary build files and intermediate compilation results.",
        "tmp/Cache": "Contains cached data for faster loading and processing.",
        "tmp/Logs": "Contains log files generated during development and testing.",
        "tmp/Backups": "Contains automatic backups of project files.",
        "tmp/Renders": "Contains temporary rendering outputs and previews.",
        "tmp/Debug": "Contains debug information and crash dumps.",
        "tmp/Testing": "Contains temporary files generated during testing.",
        "tmp/Artifacts": "Contains build artifacts and intermediate files.",
        "tmp/AutoSave": "Contains auto-saved versions of project files.",
        "tmp/Exports": "Contains temporary exported files before final placement.",
        "tmp/Media/Images": "Contains temporary images, screenshots, and visual assets used during development.",
        "tmp/Media/Audio": "Contains temporary audio files, voice recordings, and sound effects for testing.",
        "tmp/Media/Video": "Contains temporary video files, cutscenes, and animations for review.",
        "tmp/Media/Textures": "Contains in-progress and temporary textures before final implementation.",
        "tmp/Prototypes": "Contains prototype assets and code for experimental features.",
        "tmp/Staging": "Contains assets staged for review before moving to production assets.",
        "tmp/Review": "Contains assets under review by team members or clients.",
        "tmp/Processing": "Contains assets currently being processed or converted.",
        "tmp/Import": "Contains recently imported assets pending proper organization.",
        "tmp/Outsourced": "Contains temporary storage for assets from external partners or contractors.",
        
        "Tests/Unit": "Contains unit tests for individual components and systems.",
        "Tests/Integration": "Contains integration tests for testing how components work together.",
        
        "ThirdParty/Libraries": "Contains third-party libraries and dependencies used by the game.",
        "ThirdParty/Tools": "Contains third-party tools used in the game development process.",
        
        "Scripts/Build": "Contains scripts for automating the build process.",
        "Scripts/Deploy": "Contains scripts for deploying the game to various platforms.",
        "Scripts/Tools": "Contains utility scripts for development workflow automation.",
        "Scripts/Pipeline": "Contains scripts for asset pipeline automation, particularly for Blender to game engine exports.",
        "Scripts/CI": "Contains continuous integration scripts for automated testing, building, and deployment in CI/CD workflows.",
        
        "Config/Engine": "Contains configuration files for the game engine.",
        "Config/Game": "Contains game-specific configuration files.",
        
        "Versions/Current": "Contains or links to the current active development version.",
        "Releases/Internal": "Contains builds for internal testing and development.",
        "Releases/External": "Contains builds for external testing and beta releases.",
        "Releases/Public": "Contains public release builds and distribution packages."
    }
    
    # Create each directory in the structure and add description.txt
    print(f"Creating directory structure for {game_name} at {game_dir}...")
    
    # Create root directory description
    root_desc_path = os.path.join(game_dir, "description.txt")
    os.makedirs(game_dir, exist_ok=True)
    with open(root_desc_path, "w") as f:
        f.write(f"# {game_name} Project Root\n\n")
        f.write("This is the main project directory for the game. It contains all source code, assets, and documentation.\n")
        f.write("The directory structure follows game development best practices and is organized by function.\n")
        f.write("Each subdirectory contains a description.txt file explaining its purpose.\n")
        f.write(f"Game Engine: {engine}\n")
        f.write(f"Target Platforms: {', '.join(platforms)}\n")
    
    # Create platform-specific build directories
    build_dirs = {}
    for platform in platforms:
        build_dirs[f"Build/{platform}"] = f"Contains build outputs and packages for {platform} platform."
    
    # Update the directory_descriptions with platform-specific build directories
    for key, value in build_dirs.items():
        directory_descriptions[key] = value
    
    # Remove build directories that are not in platforms
    for key in list(directory_descriptions.keys()):
        if key.startswith("Build/") and not any(key == f"Build/{platform}" for platform in platforms):
            if key not in build_dirs:
                directory_descriptions.pop(key, None)
    
    # Create directories with descriptions
    for directory, description in directory_descriptions.items():
        dir_path = os.path.join(game_dir, directory)
        os.makedirs(dir_path, exist_ok=True)
        
        # Create a description.txt file in each directory
        desc_path = os.path.join(dir_path, "description.txt")
        with open(desc_path, "w") as f:
            f.write(f"# {directory}\n\n")
            f.write(f"{description}\n")
        
        print(f"Created: {dir_path} (with description.txt)")
    
    # Create description files for top-level directories that might not have been covered
    top_level_dirs = {
        "Documentation": "Contains all project documentation, including design documents, technical specifications, and API references.",
        "Source": "Contains all source code for the game, including core systems, gameplay code, and development tools.",
        "Assets": "Contains all game assets such as models, textures, animations, audio, and other resources.",
        "Build": f"Contains build outputs and distribution packages for {', '.join(platforms)}.",
        "Tests": "Contains all testing code, including unit tests and integration tests.",
        "ThirdParty": "Contains third-party libraries, tools, and dependencies.",
        "Scripts": "Contains automation scripts for building, deployment, and development workflows.",
        "Config": "Contains configuration files for both the game engine and game-specific settings.",
        "Versions": "Contains or tracks different versions of the game during development.",
        "Releases": "Contains organized release builds for different distribution channels.",
        "tmp": "Contains all temporary files, caches, logs, and intermediate build artifacts.",
        PRE_PRODUCTION: "Contains all pre-production materials including concept, story, design, and planning.",
        PRODUCTION: "Contains all production phase materials including asset creation, animation, and implementation.",
        POST_PRODUCTION: "Contains all post-production materials including compositing, effects, and final polishing."
    }
    
    for directory, description in top_level_dirs.items():
        dir_path = os.path.join(game_dir, directory)
        if os.path.exists(dir_path):
            desc_path = os.path.join(dir_path, "description.txt")
            if not os.path.exists(desc_path):
                with open(desc_path, "w") as f:
                    f.write(f"# {directory}\n\n")
                    f.write(f"{description}\n")
    
    # Create engine-specific folders based on the engine parameter
    if engine != "Custom":
        engine_folders = create_engine_specific_structure(engine, game_dir)
        print(f"Created engine-specific folders for {engine}")
    
    # Create a README file
    readme_path = os.path.join(game_dir, "README.md")
    with open(readme_path, "w") as f:
        f.write(f"# {game_name}\n\n")
        f.write(f"Game development project created on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"## Game Engine\n\n{engine}\n\n")
        f.write(f"## Target Platforms\n\n{', '.join(platforms)}\n\n")
        f.write("## Directory Structure\n\n")
        f.write("### Production Pipeline\n\n")
        f.write(f"- **{PRE_PRODUCTION}**: Pre-production materials (concept, story, design, planning)\n")
        f.write(f"- **{PRODUCTION}**: Production phase materials (asset creation, animation, implementation)\n")
        f.write(f"- **{POST_PRODUCTION}**: Post-production materials (compositing, effects, final polishing)\n\n")
        f.write("### Development Structure\n\n")
        f.write("- **Documentation**: Design documents, technical specifications, and API references\n")
        f.write("- **Source**: Source code for the game and engine\n")
        f.write("- **Assets**: Game assets including models, textures, animations, audio, etc.\n")
        f.write("- **Build**: Build files for different platforms\n")
        f.write("- **Tests**: Test code including unit tests and integration tests\n")
        f.write("- **ThirdParty**: Third-party libraries and tools\n")
        f.write("- **Scripts**: Automation and utility scripts\n")
        f.write("- **Config**: Configuration files\n")
        f.write("- **Versions**: Version management\n")
        f.write("- **Releases**: Release builds for different distribution channels\n")
        f.write("- **tmp**: Temporary files, builds, caches, and logs\n")
    
    print(f"Created README file: {readme_path}")
    
    # Create a README file for the tmp directory
    tmp_readme_path = os.path.join(game_dir, "tmp", "README.md")
    with open(tmp_readme_path, "w") as f:
        f.write("# Temporary Files Directory\n\n")
        f.write("This directory contains all temporary files used during the development process. Files in this directory are not intended for version control and may be deleted by cleanup scripts.\n\n")
        f.write("## Directory Structure\n\n")
        f.write("- **Builds**: Temporary build files and intermediate compilation results\n")
        f.write("- **Cache**: Cached data for faster loading and processing\n")
        f.write("- **Logs**: Log files generated during development and testing\n")
        f.write("- **Backups**: Automatic backups of project files\n")
        f.write("- **Renders**: Temporary rendering outputs and previews\n")
        f.write("- **Debug**: Debug information and crash dumps\n")
        f.write("- **Testing**: Temporary files generated during testing\n")
        f.write("- **Artifacts**: Build artifacts and intermediate files\n")
        f.write("- **AutoSave**: Auto-saved versions of project files\n")
        f.write("- **Exports**: Temporary exported files before final placement\n")
        f.write("- **Media**: Temporary media assets\n")
        f.write("  - **Images**: Temporary images, screenshots, and visual assets\n")
        f.write("  - **Audio**: Temporary audio files, voice recordings, and sound effects\n")
        f.write("  - **Video**: Temporary video files, cutscenes, and animations\n")
        f.write("  - **Textures**: In-progress and temporary textures\n")
        f.write("- **Prototypes**: Prototype assets and code for experimental features\n")
        f.write("- **Staging**: Assets staged for review before production\n")
        f.write("- **Review**: Assets under review by team members or clients\n")
        f.write("- **Processing**: Assets currently being processed or converted\n")
        f.write("- **Import**: Recently imported assets pending organization\n")
        f.write("- **Outsourced**: Temporary storage for assets from external partners\n\n")
        f.write("## Cleanup\n\n")
        f.write("This directory can be cleaned periodically to free up disk space. Use the cleanup scripts in the Scripts/Tools directory for this purpose.\n")
    
    print(f"Created tmp directory README file: {tmp_readme_path}")
    
    # Create a cleanup script for tmp directory
    cleanup_script_dir = os.path.join(game_dir, "Scripts", "Tools")
    cleanup_script_path = os.path.join(cleanup_script_dir, "cleanup_tmp.py")
    os.makedirs(cleanup_script_dir, exist_ok=True)
    
    cleanup_script_content = '''#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import shutil
import datetime
import argparse

def cleanup_tmp_directory(project_root, dry_run=False, age_days=7, exclude_dirs=None):
    """
    Cleans up temporary files in the tmp directory that are older than specified age
    
    Args:
        project_root (str): Root directory of the project
        dry_run (bool): If True, only print what would be deleted without actually deleting
        age_days (int): Delete files older than this many days
        exclude_dirs (list): List of directories to exclude from cleanup
    """
    if exclude_dirs is None:
        exclude_dirs = ['Backups']
    
    tmp_dir = os.path.join(project_root, 'tmp')
    if not os.path.exists(tmp_dir):
        print(f"Error: Temporary directory not found at {tmp_dir}")
        return
    
    cutoff_date = datetime.datetime.now() - datetime.timedelta(days=age_days)
    cutoff_timestamp = cutoff_date.timestamp()
    
    print(f"Cleaning up files older than {cutoff_date.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'[DRY RUN] ' if dry_run else ''}Will delete files and empty directories in {tmp_dir}")
    print(f"Excluding directories: {exclude_dirs}")
    
    total_size = 0
    total_files = 0
    total_dirs = 0
    
    # Walk through all files and directories in tmp
    for root, dirs, files in os.walk(tmp_dir, topdown=False):
        # Skip excluded directories
        rel_path = os.path.relpath(root, tmp_dir)
        if rel_path == '.':
            rel_path = ''
        
        skip = False
        for exclude in exclude_dirs:
            if rel_path == exclude or rel_path.startswith(exclude + os.sep):
                skip = True
                break
        
        if skip:
            continue
        
        # Delete old files
        for file in files:
            file_path = os.path.join(root, file)
            try:
                file_stat = os.stat(file_path)
                file_mtime = file_stat.st_mtime
                
                if file_mtime < cutoff_timestamp:
                    total_size += file_stat.st_size
                    total_files += 1
                    print(f"{'[DRY RUN] ' if dry_run else ''}Deleting file: {file_path}")
                    if not dry_run:
                        os.unlink(file_path)
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
        
        # Delete empty directories
        if not os.listdir(root) and root != tmp_dir:
            total_dirs += 1
            print(f"{'[DRY RUN] ' if dry_run else ''}Removing empty directory: {root}")
            if not dry_run:
                os.rmdir(root)
    
    # Convert total size to a human-readable format
    size_str = ''
    if total_size < 1024:
        size_str = f"{total_size} bytes"
    elif total_size < 1024 * 1024:
        size_str = f"{total_size / 1024:.2f} KB"
    elif total_size < 1024 * 1024 * 1024:
        size_str = f"{total_size / (1024 * 1024):.2f} MB"
    else:
        size_str = f"{total_size / (1024 * 1024 * 1024):.2f} GB"
    
    print(f"\\nCleanup Summary:")
    print(f"{'[DRY RUN] ' if dry_run else ''}Would free up {size_str} of disk space")
    print(f"{'[DRY RUN] ' if dry_run else ''}Deleted {total_files} files and {total_dirs} directories")

def main():
    parser = argparse.ArgumentParser(description="Clean up temporary files in the project's tmp directory")
    parser.add_argument('--project-root', help='Root directory of the project')
    parser.add_argument('--dry-run', action='store_true', help='Only print what would be deleted without actually deleting')
    parser.add_argument('--age', type=int, default=7, help='Delete files older than this many days (default: 7)')
    parser.add_argument('--exclude', type=str, default='Backups', help='Comma-separated list of directories to exclude from cleanup (default: Backups)')
    
    args = parser.parse_args()
    
    # Find project root if not specified
    project_root = args.project_root
    if not project_root:
        # Try to find it by looking for the tmp directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Go up to Scripts/Tools, then up to project root
        project_root = os.path.normpath(os.path.join(current_dir, '..', '..', '..'))
        
        if not os.path.exists(os.path.join(project_root, 'tmp')):
            print("Error: Could not find project root directory. Please specify with --project-root")
            return 1
    
    exclude_dirs = [dir.strip() for dir in args.exclude.split(',')]
    
    cleanup_tmp_directory(project_root, args.dry_run, args.age, exclude_dirs)
    return 0

if __name__ == "__main__":
    sys.exit(main())
'''
    
    with open(cleanup_script_path, "w") as f:
        f.write(cleanup_script_content)
    
    # Make the cleanup script executable
    try:
        os.chmod(cleanup_script_path, 0o755)
    except:
        # Skip chmod on systems that don't support it (like Windows)
        pass
    print(f"Created tmp directory cleanup script: {cleanup_script_path}")
    
    # Create a version info file
    version_path = os.path.join(game_dir, "version_info.json")
    with open(version_path, "w") as f:
        f.write('{\n')
        f.write(f'  "name": "{game_name}",\n')
        f.write('  "version": "0.1.0",\n')
        f.write('  "status": "development",\n')
        f.write(f'  "created": "{datetime.datetime.now().isoformat()}",\n')
        f.write(f'  "engine": "{engine}",\n')
        f.write(f'  "platforms": {str(platforms).replace("\'", "\"")}\n')
        f.write('}\n')
    
    print(f"Created version info file: {version_path}")
    
    # Create a basic .gitignore file
    gitignore_path = os.path.join(game_dir, ".gitignore")
    with open(gitignore_path, "w") as f:
        f.write("# Build directories\n")
        f.write("Build/\n")
        f.write("tmp/\n\n")
        f.write("# Temporary files\n")
        f.write("*.tmp\n")
        f.write("*.temp\n")
        f.write("*.bak\n\n")
        f.write("# OS specific files\n")
        f.write(".DS_Store\n")
        f.write("Thumbs.db\n\n")
        f.write("# IDE specific files\n")
        f.write(".idea/\n")
        f.write(".vscode/\n")
        f.write("*.sublime-project\n")
        f.write("*.sublime-workspace\n\n")
        f.write("# Python specific\n")
        f.write("__pycache__/\n")
        f.write("*.py[cod]\n")
        f.write("*$py.class\n")
        f.write("venv/\n")
        f.write("env/\n")
        f.write(".env\n")
    
    print(f"Created gitignore file: {gitignore_path}")
    
    return game_dir

def create_engine_specific_structure(engine, game_dir):
    """
    Creates engine-specific directory structure
    
    Args:
        engine (str): Game engine name
        game_dir (str): Game directory root path
    
    Returns:
        list: Created engine-specific directories
    """
    engine_dirs = []
    
    # Define engine specific directory structures
    engine_structures = {
        "Unity": {
            "Assets/Prefabs": "Contains reusable Unity prefab objects.",
            "Assets/Materials": "Contains Unity material definitions.",
            "Assets/Scenes": "Contains Unity scene files.",
            "Assets/Scripts": "Contains C# scripts for Unity.",
            "Assets/Editor": "Contains Unity editor extensions and scripts.",
            "Assets/Resources": "Contains assets that need to be accessed via Resources.Load.",
            "ProjectSettings": "Contains Unity project settings.",
            "Packages": "Contains Unity package manager configuration.",
        },
        "Unreal": {
            "Content/Blueprints": "Contains Unreal Blueprint assets.",
            "Content/Materials": "Contains Unreal material definitions.",
            "Content/Levels": "Contains Unreal level files.",
            "Content/Characters": "Contains character assets and blueprints.",
            "Content/UI": "Contains UI assets and widgets.",
            "Source/[GameName]": "Contains C++ code for the game.",
            "Config/DefaultEngine.ini": "Contains engine configuration.",
            "Config/DefaultGame.ini": "Contains game configuration.",
        },
        "Godot": {
            "scenes": "Contains Godot scene files.",
            "scripts": "Contains GDScript files.",
            "assets": "Contains game assets for Godot.",
            "addons": "Contains Godot addons and plugins.",
            "project.godot": "Godot project configuration file.",
            "export_presets.cfg": "Godot export configurations.",
        },
        "Custom": {
            # No additional directories for Custom engine
        }
    }
    
    # Get the structure for the specified engine (default to empty if not found)
    engine_structure = engine_structures.get(engine, {})
    
    # Create engine-specific directories
    for directory, description in engine_structure.items():
        # Convert [GameName] placeholder if needed
        if "[GameName]" in directory:
            game_name = os.path.basename(game_dir)
            directory = directory.replace("[GameName]", game_name)
        
        dir_path = os.path.join(game_dir, directory)
        
        # Skip file paths (create parent directories only)
        if os.path.basename(directory).find('.') != -1:
            dir_path = os.path.dirname(dir_path)
            os.makedirs(dir_path, exist_ok=True)
            
            # Create the file with content
            with open(os.path.join(game_dir, directory), "w") as f:
                f.write(f"# {directory}\n\n")
                f.write(f"{description}\n")
        else:
            os.makedirs(dir_path, exist_ok=True)
            
            # Create a description.txt file in each directory
            desc_path = os.path.join(dir_path, "description.txt")
            with open(desc_path, "w") as f:
                f.write(f"# {directory}\n\n")
                f.write(f"{description}\n")
        
        engine_dirs.append(directory)
        print(f"Created engine-specific: {dir_path}")
    
    return engine_dirs

def show_examples():
    """
    Print usage examples for the tool
    """
    print("\nUsage Examples:")
    print("=" * 80)
    print("1. Basic usage (interactive):")
    print("   python game-project-directory-creator.py")
    print("")
    print("2. Basic usage with command-line arguments:")
    print("   python game-project-directory-creator.py --game-name \"My Awesome Game\" --root-dir \"C:\\Projects\"")
    print("")
    print("3. Specify game engine:")
    print("   python game-project-directory-creator.py --game-name \"My Unity Game\" --engine Unity")
    print("")
    print("4. Specify target platforms:")
    print("   python game-project-directory-creator.py --game-name \"Mobile Game\" --platforms Windows,Android,iOS")
    print("")
    print("5. Full example with all parameters:")
    print("   python game-project-directory-creator.py --game-name \"Space Adventure\" --root-dir \"D:\\Games\" --engine Unreal --platforms Windows,PlayStation,Xbox")
    print("")
    print("6. Create a project and then use the cleanup script:")
    print("   python game-project-directory-creator.py --game-name \"My Game\"")
    print("   python Scripts/Tools/cleanup_tmp.py --age 30")
    print("=" * 80)
    
    print("\nDirectory Structure Overview:")
    print("=" * 80)
    print("The generated directory structure includes:")
    print("")
    print("1. Production Pipeline Directories:")
    print("   - Pre-Production: Idea, Story, Characters, Storyboard, etc.")
    print("   - Production: Modeling, Animation, Texturing, Lighting, etc.")
    print("   - Post-Production: Compositing, Color Correction, Final Output, etc.")
    print("")
    print("2. Development Structure:")
    print("   - Source code, assets, documentation, and other standard directories")
    print("   - Engine-specific directories based on the chosen game engine")
    print("   - Platform-specific build directories")
    print("")
    print("3. Temporary Files:")
    print("   - Comprehensive tmp directory structure for all temporary assets")
    print("   - Includes specialized directories for media, renders, and workflow")
    print("   - Comes with cleanup script for managing temporary files")
    print("=" * 80)

def main():
    """
    Main function to run the tool from command line
    """
    # Define available engines
    available_engines = ["Custom", "Unity", "Unreal", "Godot"]
    
    # Define available platforms
    available_platforms = ["Windows", "MacOS", "Linux", "Android", "iOS", "PlayStation", "Xbox", "Nintendo", "Web"]
    
    # Create argument parser for command line usage
    parser = argparse.ArgumentParser(description="Create a template directory structure for game development")
    parser.add_argument("--game-name", help="Name of the game")
    parser.add_argument("--root-dir", help="Root directory where the game structure will be created")
    parser.add_argument("--engine", choices=available_engines, default="Custom", help=f"Game engine to use: {', '.join(available_engines)}")
    parser.add_argument("--platforms", help=f"Comma-separated list of target platforms (available: {', '.join(available_platforms)})")
    parser.add_argument("--examples", action="store_true", help="Show usage examples and exit")
    
    args = parser.parse_args()

def main():
    """
    Main function to run the tool from command line
    """
    # Define available engines
    available_engines = ["Custom", "Unity", "Unreal", "Godot"]
    
    # Define available platforms
    available_platforms = ["Windows", "MacOS", "Linux", "Android", "iOS", "PlayStation", "Xbox", "Nintendo", "Web"]
    
    # Create argument parser for command line usage
    parser = argparse.ArgumentParser(description="Create a template directory structure for game development")
    parser.add_argument("--game-name", help="Name of the game")
    parser.add_argument("--root-dir", help="Root directory where the game structure will be created")
    parser.add_argument("--engine", choices=available_engines, default="Custom", help=f"Game engine to use: {', '.join(available_engines)}")
    parser.add_argument("--platforms", help=f"Comma-separated list of target platforms (available: {', '.join(available_platforms)})")
    parser.add_argument("--examples", action="store_true", help="Show usage examples and exit")
    
    args = parser.parse_args()
    
    # Show examples if requested
    if args.examples:
        show_examples()
        print("\nNote: If no root directory is specified, the script will create the game directory")
        print("in the same location as the script file itself.")
        return 0
    
    # Interactive mode if arguments are not provided
    game_name = args.game_name
    root_dir = args.root_dir
    engine = args.engine
    platforms_str = args.platforms
    
    if not game_name:
        game_name = input("Enter the name of your game: ")
    
    if not root_dir:
        root_dir = input("Enter the root directory for your game project (leave empty for script directory): ")
        
        # Use script directory if none provided
        if not root_dir:
            # Get the directory where the script is located
            root_dir = os.path.dirname(os.path.abspath(__file__))
    
    if not engine or engine not in available_engines:
        print(f"Available engines: {', '.join(available_engines)}")
        engine = input(f"Select a game engine ({', '.join(available_engines)}) [default: Custom]: ")
        if not engine or engine not in available_engines:
            engine = "Custom"
    
    if not platforms_str:
        platforms_str = input(f"Enter target platforms (comma-separated) [default: Windows,MacOS,Linux]: ")
    
    # Process platforms
    if platforms_str:
        platforms = [p.strip() for p in platforms_str.split(",")]
        # Validate platforms
        for platform in platforms:
            if platform not in available_platforms:
                print(f"Warning: Unknown platform '{platform}'. Available platforms: {', '.join(available_platforms)}")
    else:
        platforms = ["Windows", "MacOS", "Linux"]
    
    # Validate inputs
    if not game_name:
        print("Error: Game name cannot be empty.")
        return 1
    
    # Ensure root directory exists
    if not os.path.exists(root_dir):
        create_dir = input(f"The directory {root_dir} does not exist. Create it? (y/n): ")
        if create_dir.lower() == 'y':
            try:
                os.makedirs(root_dir, exist_ok=True)
            except Exception as e:
                print(f"Error creating directory: {e}")
                return 1
        else:
            print("Operation cancelled.")
            return 0
    
    # Create the game directory structure
    try:
        game_dir = create_game_directory_structure(game_name, root_dir, engine, platforms)
        print(f"\nGame directory structure created successfully at: {game_dir}")
        print(f"You can now start developing {game_name}!")
        print(f"- Engine: {engine}")
        print(f"- Target Platforms: {', '.join(platforms)}")
    except Exception as e:
        print(f"Error creating game directory structure: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())