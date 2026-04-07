
import os

path = r"d:\Freelance\mclean_project\static\css\style.css"
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
added = False
for line in lines:
    # Look for the exact line to insert before
    if line.strip() == ".mega-menu {" and not added:
        new_lines.append(".mega-menu-wrapper {\n")
        new_lines.append("    position: relative;\n")
        new_lines.append("}\n\n")
        new_lines.append("/* Hide the default underline animation for mega trigger links */\n")
        new_lines.append(".mega-menu-wrapper > .header__nav-link::after {\n")
        new_lines.append("    display: none !important;\n")
        new_lines.append("}\n\n")
        new_lines.append("/* The mega menu panel - full width under header */\n")
        added = True
    new_lines.append(line)

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Successfully repaired style.css")
