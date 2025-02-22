import tkinter as tk
from tkinter import filedialog, messagebox
import json
import re
import os
import subprocess

file_path = None
imported_obj_filename = None

# Settings Directory and Defualt Export Directory
settings_directory = 'C:\SplatoonCollisionConverter\data'

export_directory = 'C:\SplatoonCollisionConverter\exported'

# Clear the command window
os.system('cls' if os.name == 'nt' else 'clear')

# Ensure the directorys exists, create it if it doesn't
if not os.path.exists(settings_directory):
    os.makedirs(settings_directory)

if not os.path.exists(export_directory):
    os.makedirs(export_directory)

# Set the settings file path; Create settings files
settings_file = os.path.join(settings_directory, 'settings.json')

# Material mappings
material_map = {
    'COL_4007': 'Fence', 'COL_C': 'Water', 'COL_E': 'Undefined', 'COL_4': 'Glass',
    'COL_17': 'Vinyl', 'COL_80': 'Asphalt', 'COL_15': 'Vinyl', 'COL_4008': 'Fence',
    'COL_600': 'Asphalt', 'COL_41': 'Stone', 'COL_48': 'Metal', 'COL_40': 'Asphalt',
    'COL_4D': 'Carpet', 'COL_8': 'Metal', 'COL_4009': 'Fence', 'COL_609': 'Asphalt',
    'COL_2006': 'Plastic', 'COL_6': 'Plastic', 'COL_14': 'Vinyl', 'COL_2015': 'Plastic',
    'COL_4609': 'Fence', 'COL_9': 'Asphalt', 'COL_0': 'Asphalt', 'COL_603': 'Asphalt',
    'COL_22': 'Undefined', 'COL_C008': 'Undefined', 'COL_60E': 'Metal', 'COL_C8' : 'Metal',
    'COL_85' : 'Vinyl', 'COL_6009' : 'Fence', 'COL_4015' : 'Fence', 'COL_60B' : 'Asphalt',
    'COL_2008' : 'Metal', 'COL_A' : 'Vinyl', 'COL_45' : 'Wood', 'COL_88' : 'Metal', 
    'COL_46' : 'Plastic', 'COL_86' : 'Plastic', 'COL_800A' : 'Vinyl', 'COL_608' : 'Metal',
    'COL_95' : 'Plastic', 'COL_400' : 'Asphalt', 'COL_42' : 'Grass', 'COL_800B': 'Grass',
    'COL_200' : 'Asphalt', "COL_C0" : 'Stone', 'COL_C5' : 'Wood', 'COL_43' : 'Soil',
    'COL_C6' : 'Plastic', 'COL_6007' : 'Fence', 'COL_CD' : 'Plastic', 'COL_4A' : 'Rubber',
    'COL_8005' : 'Metal', 'COL_7' : 'Metal', 'COL_8045' : 'Wood', 'COL_604' : 'Asphalt',
    'COL_8040' : 'Stone', 'COL_D' : 'Vinyl', 'COL_208' : 'Plastic', 'COL_886' : 'Plastic',
    'COL_8886' : 'Plastic', 'COL_204' : 'Glass', 'COL_206' : 'Plastic', 'COL_606' : 'Plastic',
    'COL_1A' : 'Undefined', 'COL_4208' : 'Metal', 'COL_8282' : 'Grass', 'COL_8082' : 'Grass',
    'COL_5' : 'Metal', 'COL_605' : 'Wood', 'COL_400B' : 'Asphalt', 'COL_4011' : 'RopeNet',
    'COL_8008' : 'Metal', 'COL_6008' : 'Metal', 'COL_8A' : 'Rubber', 'COL_2208' : 'Fence',
    'COL_C208' : 'Fence', 'COL_8085' : 'Wood', 'COL_5C' : 'Carpet', 'COL_2004' : 'Glass',
    'COL_1' : 'Asphalt', 'COL_3' : 'Stone', 'COL_408' : 'Asphalt', 'COL_C1' : 'Asphalt',
    'COL_20' : 'Asphalt' 
}

default_col_disable_flags = {
    'default': ["NoHit", "Unspecified", "Ground"],
    'Fence': [
        "NoHit", "SplCamera", "SplInkBullet", "SplInkBullet_FriendThrough", "SplRollerBody",
        "SplInkShield", "SplBlowerInhale", "SplInkTornado", "SplGreatBarrier", "SplSaberBombGuard",
        "SplPaintSplash", "Unspecified", "Ground", "SplPlayerSquid_NoThroughFence", "SplPlayerChariot",
        "Sight", "EnemyLarge", "Shield", "SplBall"
    ],
    'RopeNet': [
        "NoHit", "SplCamera", "SplInkBullet", "SplInkBullet_FriendThrough", "SplRollerBody",
        "SplInkShield", "SplBlowerInhale", "SplInkTornado", "SplGreatBarrier", "SplSaberBombGuard",
        "SplPaintSplash", "Unspecified", "Ground", "SplPlayerSquid_NoThroughFence", "SplPlayerChariot",
        "Sight", "EnemyLarge", "Shield", "SplBall"
    ],
    'Water': [
        "NoHit", "Water", "SplPlayer", "SplCoopEnemy", "SplSdodrEnemy", "Unspecified", 
        "Ground", "SplPlayerSquid_Invisible", "SplPlayerSquid_NoThroughFence", 
        "SplPlayerChariot", "SplPlayerChariotShield", "SplPlayerSuperHookCheck", 
        "SplSalmonBuddy", "Enemy", "SplUltraStamp", "SplBall"
    ],
    'Undefined': [
        "NoHit", "GameCustomReceiver", "Ground", "Water", "SplCamera", "SplInkBullet", 
        "SplInkBullet_FriendThrough", "SplSubstanceBullet", "SplSubstanceBullet_HitOpposite", 
        "SplSubstanceBullet_HitBullet", "SplSubstanceBullet_Lite", "SplRollerBody", 
        "SplStationedWeapon", "SplInkShield", "SplBlowerInhale", "SplBluntWeapon", 
        "SplInkFilm", "SplInkTornado", "SplGreatBarrier", "SplSaberBombGuard", 
        "SplPaintSplash", "SplObject", "MissionEnemy", "SplCoopEnemy", "SplSdodrEnemy", 
        "SplItem", "SplWallaObj", "Unspecified", "Ground"
    ]
}

default_mat_flags = {
    'Fence': ["Fence", "ForceColPaintNotPaintable"],
    'RopeNet': ["Fence", "ForceColPaintNotPaintable"],
    'Water': ["Water", "BombDead", "UltraStampDead", "TripleTornadoDeviceDead"],
    'Vinyl': ["ForceColPaintNotPaintable"],
    'Glass': ["ForceColPaintNotPaintable"]
}

def read_obj_materials(file_path):
    materials = {}
    material_counts = {}
    current_material = None

    with open(file_path, 'r') as obj_file:
        for line in obj_file:
            if line.startswith('v '):  # Check if the line represents a vertex
                # Scale the vertex coordinates by 0.1
                vertex_coords = [float(coord) * 0.1 for coord in line.strip().split()[1:]]
                # Update the line with scaled coordinates
                line = 'v ' + ' '.join(map(str, vertex_coords)) + '\n'
            elif line.startswith('usemtl'):
                original_name = line.strip().split()[1]
                material_name = material_map.get(original_name, original_name)  # Keep original name if not in map

                count = material_counts.setdefault(material_name, 0)
                material_key = f"{material_name}{count}"
                mat_name = remove_numbers(material_name)  # Remove numbers from material name

                col_disable_flags_set = set(default_col_disable_flags.get(mat_name, default_col_disable_flags['default']))
                mat_flags_set = set(default_mat_flags.get(mat_name, []))

                # Additional flags based on original names
                if original_name in ['COL_200', 'COL_8085', 'COL_2208', 'COL_8008', 'COL_400B', 'COL_8082', 'COL_8282', 'COL_606', 'COL_604', 'COL_14', 'COL_4009', 'COL_4609', 'COL_9', 'COL_603', 'COL_600', 'COL_609', 'COL_20']:
                    mat_flags_set.add("IgnoredByMiniMap")
                if original_name in ['COL_14', 'COL_E']:
                    mat_flags_set.add("KeepOut")
                if original_name in ['COL_2004', 'COL_6008', 'COL_8005', 'COL_6007', 'COL_4008', 'COL_2015', 'COL_2006', 'COL_6009']:
                    mat_flags_set.add("Slide")
                if original_name in ['COL_8A', 'COL_6008', 'COL_8008', 'COL_400B', 'COL_605', 'COL_5', 'COL_8082', 'COL_8282', 'COL_4208', 'COL_606', 'COL_206', 'COL_886', 'COL_8886', 'COL_208','COL_604', 'COL_8005', 'COL_CD','COL_200', 'COL_800B', 'COL_400', 'COL_95', 'COL_60E', 'COL_8', 'COL_4009', 'COL_2006', 'COL_6', 'COL_2015', 'COL_609', 'COL_4609', 'COL_9', 'COL_0', 'COL_603', 'COL_C008', 'COL_60B', 'COL_2008']:
                    mat_flags_set.add("ForceColPaintNotPaintable")
                if original_name in ['COL_608']:
                    mat_flags_set.add('PlayerDead')
                if original_name in ['COL_85']:
                    mat_flags_set = set()

                current_material = material_key  # Set current material
                materials[current_material] = {
                    "col_disable_flags": list(col_disable_flags_set),
                    "mat_flags": list(mat_flags_set),
                    "mat_name": f"{mat_name}{count}",  # Rename the material with a unique identifier
                    "original_name": original_name,  # Store the original name in the materials dictionary
                    "content": ""  # Initialize content for the material
                }
                material_counts[material_name] += 1
                # Print changed material information
                print(f"Changed Material: {current_material}")
                print(f"Original Name: {original_name}")
                print(f"Renamed Name: {materials[current_material]['mat_name']}")
            elif line.startswith('f '):
                if current_material is not None:  # Check if current_material is not None
                    # Update faces with the current material
                    line_parts = line.strip().split()
                    line_parts.insert(1, f"usemtl {current_material}")
                    line = ' '.join(line_parts) + '\n'

                # Write the line to the materials list
                materials[current_material]["content"] += line

    print(f"Current Loaded OBJ: {imported_obj_filename}")

    return materials

def browse_file():
    global file_path, imported_obj_filename

    # Store the current file path and materials data
    prev_file_path = file_path
    prev_imported_obj_filename = imported_obj_filename

    settings = load_settings()
    # Load last used open directory
    open_directory = settings.get('open_directory', '')
    file_path = filedialog.askopenfilename(filetypes=[("OBJ files", "*.obj")], initialdir=open_directory)
    if file_path:
        # Store the file name without the extension
        imported_obj_filename = os.path.splitext(os.path.basename(file_path))[0]

        # Clear previous materials and associated data
        clear_material_data()

        # Clear the command window
        os.system('cls' if os.name == 'nt' else 'clear')

        materials = read_obj_materials(file_path)

        # Display materials in the text box
        materials_text.config(state=tk.NORMAL)
        materials_text.delete('1.0', tk.END)
        materials_text.insert(tk.END, f"Currently Imported OBJ: {imported_obj_filename}\n")
        materials_text.insert(tk.END, f"{imported_obj_filename} was scaled by 0.1:\n\n")
        for material, data in materials.items():
            # print(f"Material: {material}")
            # print(f"Col Disable Flags: {data['col_disable_flags']}")
            # print(f"Mat Flags: {data['mat_flags']}")
            # print(f"Mat Name: {data['mat_name']}")
            materials_text.insert(tk.END, f"{material}\n")
            materials_text.insert(tk.END, f"col_disable_flags: {data['col_disable_flags']}\n")
            materials_text.insert(tk.END, f"mat_flags: {data['mat_flags']}\n")
            materials_text.insert(tk.END, f"mat_name: {data['mat_name']}\n")
            materials_text.insert(tk.END, "\n")
        materials_text.config(state=tk.DISABLED)
        # Save the current directory as the last used open directory
        settings['open_directory'] = os.path.dirname(file_path)
        save_settings(settings)
        print("File selected successfully.")
    else:
        # Restore previous file path and materials data
        file_path = prev_file_path
        imported_obj_filename = prev_imported_obj_filename
        print("File selection canceled.")

def clear_material_data():
    # Clear previous materials and associated data
    materials_text.config(state=tk.NORMAL)
    materials_text.delete('1.0', tk.END)
    materials_text.config(state=tk.DISABLED)

def export_materials():
    if not file_path:
        messagebox.showwarning("No OBJ File Selected", "No materials to export. Please select an OBJ file.")
        return

    materials = read_obj_materials(file_path)
    export_materials = {}
    renamed_materials = {}

    for material, data in materials.items():
        # If material was not renamed, append the number
        if remove_numbers(data["mat_name"]) == remove_numbers(data["original_name"]):
            mat_name = f"{data['mat_name']}{materials[material]['original_name'][-1]}"
        else:
            mat_name = data["mat_name"]

        # Remove numbers from material name
        mat_name = remove_numbers(mat_name)

        # Store the original material name and its renamed name
        renamed_materials[data["original_name"]] = mat_name

    # Create a dictionary to store the count numbers for each material
    material_counts = {}

    for original_name, renamed_name in renamed_materials.items():
        # Initialize the count for the material
        material_counts[renamed_name] = 0

    settings = load_settings()
    export_directory = settings.get('export_directory', '')
    initial_dir = export_directory if os.path.isdir(export_directory) else "C:\\SplatoonCollisionConverter\\exported"
    export_path = filedialog.asksaveasfilename(defaultextension=".json", initialfile=f"{imported_obj_filename}_config.json", filetypes=[("JSON files", "*.json")], initialdir=initial_dir)

    if export_path:
        # Check if the export directory exists, create it if not
        export_dir = os.path.dirname(export_path)
        if not os.path.exists(export_dir):
            os.makedirs(export_dir)

        # Create a new dictionary excluding "original_name" and "content" fields
        for material, data in materials.items():
            export_materials[material] = {
                "col_disable_flags": data["col_disable_flags"],
                "mat_flags": data["mat_flags"],
                "mat_name": remove_numbers(data["mat_name"])  # Remove numbers from mat_name
            }

        with open(export_path, "w") as f:
            # Write the JSON data
            json.dump(export_materials, f, indent=4)
        messagebox.showinfo("Export Successful", "Collision JSON exported successfully!")

        scaled_obj_filename = f"{imported_obj_filename}_Scaled.obj"
        scaled_obj_path = os.path.join(export_dir, scaled_obj_filename)

        with open(file_path, 'r') as obj_file:
            with open(scaled_obj_path, 'w') as scaled_obj_file:
                current_material_number = 0  # Initialize current material number
                for line in obj_file:
                    if line.startswith('v '):  # Check if the line represents a vertex
                        # Scale the vertex coordinates by 0.1
                        vertex_coords = [float(coord) * 0.1 for coord in line.strip().split()[1:]]
                        # Update the line with scaled coordinates
                        line = 'v ' + ' '.join(map(str, vertex_coords)) + '\n'
                    elif line.startswith('usemtl'):
                        original_material_name = line.strip().split()[1]
                        renamed_material_name = renamed_materials.get(original_material_name, original_material_name)
                        # Get the current count number for the material
                        count = material_counts[renamed_material_name]
                        line = f'usemtl {renamed_material_name}{count}\n'
                        # Increment the count for the material
                        material_counts[renamed_material_name] += 1
                    elif line.startswith('o'):
                        original_material_name = line.strip().split()[1]
                        renamed_material_name = renamed_materials.get(original_material_name, original_material_name)
                        # Get the current count number for the material
                        count = material_counts[renamed_material_name]
                        line = f'o {renamed_material_name}{count}\n'
                    scaled_obj_file.write(line)
        messagebox.showinfo("Export Successful", "Scaled OBJ exported successfully!")

        # Open the export directory in the file explorer
        if settings.get('open_export_directory', False):
            if os.name == 'nt':  # Windows
                os.startfile(export_dir)
            elif os.name == 'posix':  # macOS or Linux
                subprocess.call(['open', export_dir] if os.uname().sysname == 'Darwin' else ['xdg-open', export_dir])

        settings['export_directory'] = export_dir
        save_settings(settings)
        
def remove_numbers(material_name):
    return re.sub(r'\d+', '', material_name)

def show_first_time_popup():
    settings = load_settings()
    popup_shown = settings.get('popup_shown', False)
    if not popup_shown:
        messagebox.showinfo("Splatoon Collision Converter", "The Splatoon Collision Converter converts the OBJ collision models from Splatoon 1 and Splatoon 2 into compatible Splatoon 3 collision JSON files to be used with fiveX. Currently, this is only a Project Redux Tool.")
        settings['popup_shown'] = True
        save_settings(settings)

def load_settings():
    if os.path.exists(settings_file):
        with open(settings_file, 'r') as f:
            return json.load(f)
    return {}

def save_settings(settings):
    with open(settings_file, 'w') as f:
        json.dump(settings, f, indent=1)

def open_export_directory():
    settings = load_settings()
    settings['open_export_directory'] = settings_menu.var.get()
    save_settings(settings)

# Create the main window
root = tk.Tk()
root.title("Splatoon Collision Converter")

# Calculate the screen's width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Determine the window's width and height
window_width = 800
window_height = 600

# Calculate the window's position
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

# Set the window's geometry and make it not resizable
root.geometry(f"{window_width}x{window_height}+{x}+{y}")
root.resizable(False, False)  # Disable resizing

# Create a frame for materials
materials_frame = tk.Frame(root)
materials_frame.pack(fill="both", padx=10, pady=10)
materials_frame.pack_propagate(0)  # Prevent resizing

# Create browse button
# browse_button = tk.Button(root, text="Select OBJ File", command=browse_file)
# browse_button.pack(anchor='n', pady=(10, 0))

# Create export button
# export_button = tk.Button(root, text="Export JSON and OBJ File", command=export_materials)
# export_button.pack(anchor='n', pady=(0, 10))

# Create text box for materials
materials_label = tk.Label(root, text="Materials:")
materials_label.pack()
materials_text = tk.Text(root, state=tk.DISABLED)  # Change state to tk.NORMAL
materials_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Create scrollbar for materials text box
scrollbar = tk.Scrollbar(root, command=materials_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
materials_text.config(yscrollcommand=scrollbar.set)

# Create Menu Bar
menu_bar = tk.Menu(root)
file_menu = tk.Menu(menu_bar, tearoff=0)
settings_menu = tk.Menu(menu_bar, tearoff=0)

# File
menu_bar.add_cascade(label='File', menu=file_menu)
file_menu.add_command(label='Open', command=browse_file, accelerator='Ctrl+O')
file_menu.add_command(label='Export', command=export_materials, accelerator='Ctrl+S')
file_menu.add_separator()
file_menu.add_command(label='Exit', command=root.quit)


# Settings
menu_bar.add_cascade(label='Settings', menu=settings_menu)
settings_menu.var = tk.BooleanVar()
settings_menu.add_checkbutton(label='Open Export Directory', variable=settings_menu.var, command=open_export_directory)
settings_menu.var.set(load_settings().get('open_export_directory', False))

root.config(menu=menu_bar)

# Keyboard Shortcuts
root.bind_all('<Control-o>', lambda event: browse_file())
root.bind_all('<Control-s>', lambda event: export_materials())

# Show the first-time pop-up
show_first_time_popup()

root.mainloop()
