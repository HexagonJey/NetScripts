import difflib
import os

# Define the paths to the two files
file_path_1 = 'first.txt'
file_path_2 = 'second.txt'

# Read the content of the two files
with open(file_path_1, 'r') as f1, open(file_path_2, 'r') as f2:
    first_file_lines = f1.readlines()
    second_file_lines = f2.readlines()

# Create an instance of HtmlDiff with wrapcolumn set to control the table width
html_diff = difflib.HtmlDiff(wrapcolumn=80)  # Adjust the wrapcolumn value as needed

# Generate the HTML diff
html_diff_output = html_diff.make_file(first_file_lines, second_file_lines)

# Add CSS styles to change the font size
css_styles = """
<style>
   .diff { 
        max-width: 100%; 
        word-wrap: break-word; 
        overflow-x: auto;
        font-size: 14px; /* Change the font size here */
    }
</style>
"""

# Inject the CSS styles into the HTML diff
html_with_css = css_styles + html_diff_output

# Write the HTML diff with CSS to a file
with open('diff.html', 'w') as f_out:
    f_out.write(html_with_css)


html_diff = html_diff.replace('<table border="1" cellpadding="3" cellspacing="0"', '<style>.diff {max-width: 100%; word-wrap: break-word; overflow-x: auto;}</style><table border="1" cellpadding="3" cellspacing="0" class="diff"')

import difflib
import os

# Define the paths to the two files
file_path_1 = 'first.txt'
file_path_2 = 'second.txt'

# Read the content of the two files
with open(file_path_1, 'r') as f1, open(file_path_2, 'r') as f2:
    first_file_lines = f1.readlines()
    second_file_lines = f2.readlines()

# Use HtmlDiff to generate the HTML diff
html_diff = difflib.HtmlDiff().make_file(first_file_lines, second_file_lines)

# Wrap the entire table in a div with specific width and overflow settings
wrapped_html_diff = f'<div style="width:800px; overflow:auto;"><pre>{html_diff}</pre></div>'

# Write the wrapped HTML diff to a file
with open('diff.html', 'w') as f_out:
    f_out.write(wrapped_html_diff)



from pathlib import Path

def extract_prefix(filepath):
    """Extracts the prefix from a filepath."""
    return Path(filepath).stem.split('_')[0]

directory = Path('/path/to/your/files')  # Replace with your actual directory path
prefixes = ['pre', 'post']  # List of prefixes to consider

matching_files = {}
for prefix in prefixes:
    matching_files[prefix] = []
    for file in directory.glob(f'*_{prefix}*'):
        if file.is_file():
            extracted_prefix = extract_prefix(file.name)
            if extracted_prefix == prefix:
                matching_files[prefix].append(file)

print("Matching files:", matching_files)

import difflib

# Assuming you have identified two files named 'pre_1.1.1.1_name_310524_1755.txt' and 'post_1.1.1.1_name_310524_1757.txt'
file1_path = matching_files['pre'][0]
file2_path = matching_files['post'][0]

with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2:
    diff = difflib.unified_diff(
        file1.readlines(),
        file2.readlines(),
        fromfile=file1_path.name,
        tofile=file2_path.name,
        lineterm=''
    )

    print("\n".join(diff))





import os
from difflib import Differ

# Define the hostname you're looking for
hostname_to_match = "Cisco1"

# Get a list of all files in the current directory
files_in_dir = os.listdir()

# Initialize lists to hold matched files
matched_pre_files = []
matched_post_files = []

# Filter files based on prefix and hostname
for file_name in files_in_dir:
    if file_name.startswith("pre_"):
        # Extract hostname from file name
        ip_hostname_date_time = file_name.split("_")[2:]
        hostname = "_".join(ip_hostname_date_time[0:2])
        
        if hostname == hostname_to_match:
            matched_pre_files.append(file_name)
    
    elif file_name.startswith("post_"):
        # Extract hostname from file name
        ip_hostname_date_time = file_name.split("_")[2:]
        hostname = "_".join(ip_hostname_date_time[0:2])
        
        if hostname == hostname_to_match:
            matched_post_files.append(file_name)

# Ensure we have matching pairs of files
if len(matched_pre_files)!= len(matched_post_files):
    print("No matching pair of files found.")
else:
    # Compare files using difflib
    for pre_file, post_file in zip(matched_pre_files, matched_post_files):
        with open(pre_file, 'r') as f1, open(post_file, 'r') as f2:
            differ = Differ()
            diff_output = differ.compare(f1.readlines(), f2.readlines())
            
            print(f"Difference between {pre_file} and {post_file}:")
            for line in diff_output:
                print(line)

        with open(pre_files[idx], 'r') as f1, open(post_files[idx_x], 'r') as f2:
            differ = Differ()
            diff_output = differ.compare(f1.readlines(), f2.readlines())
