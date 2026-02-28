import re
import os

def parse_readme():
    input_file = '/Users/s2993348/workspace/github/awesome-instruction-editing/README.md'
    output_file = '/Users/s2993348/workspace/github/awesome-instruction-editing.github.io/index.html'

    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    html_rows = []
    current_category = None
    in_table = False

    for line in lines:
        if line.startswith('## Approaches for Image Editing'):
            current_category = 'Image Editing'
        elif line.startswith('## Approaches for Media Editing'):
            current_category = 'Media Editing'
        elif line.startswith('## Datasets'):
            # Stop parsing approaches
            break
        
        if line.startswith('| [') and current_category:
            parts = [p.strip() for p in line.split('|')[1:-1]]
            if len(parts) >= 4:
                # | [Title](Link) | Year | Venue | Features | Code |
                
                # Title and Link
                title_link_match = re.match(r'\[(.*)\]\((.*)\)', parts[0])
                if title_link_match:
                    title, link = title_link_match.groups()
                else:
                    title = parts[0]
                    link = '#'

                year = parts[1]
                venue = parts[2]
                features = parts[3]
                
                # Code might be missing or empty
                code_html = '-'
                if len(parts) >= 5:
                    code_match = re.match(r'\[Code\]\((.*)\)', parts[4])
                    if code_match:
                        code_link = code_match.group(1)
                        code_html = f'<a href="{code_link}">[Code]</a>'

                html_row = f'''
                                                <tr>
                                                    <td><a href="{link}">{title}</a></td>
                                                    <td>{venue}</td>
                                                    <td>{year}</td>
                                                    <td>{code_html}</td>
                                                    <td>{features}</td>
                                                    <td>{current_category}</td>
                                                </tr>'''
                html_rows.append(html_row)

    # Now read the index.html template and insert the rows
    with open(output_file, 'r', encoding='utf-8') as f:
        template = f.read()

    # Replace the rows in the template
    start_tag = '<!-- TABLE_CONTENT_START -->'
    end_tag = '<!-- TABLE_CONTENT_END -->'
    
    start_idx = template.find(start_tag)
    end_idx = template.find(end_tag)
    
    if start_idx != -1 and end_idx != -1:
        new_content = template[:start_idx + len(start_tag)] + '\n' + '\n'.join(html_rows) + '\n' + template[end_idx:]
        
        # update total rows count
        new_content = re.sub(r'Total number of rows: \d+', f'Total number of rows: {len(html_rows)}', new_content)

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Successfully generated {len(html_rows)} rows into index.html.")
    else:
        print("Error: Could not find table output markers in index.html")

if __name__ == '__main__':
    parse_readme()
