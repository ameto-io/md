import os
import re
import hashlib

# Read order from the given file
def read_order_from_file(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f.readlines()]

# Convert names to a formatted title
def format_title(name):
    name = name.replace('_', ' ').replace('-', ' ')
    name = name.title()
    terms = ['Html', 'Css', 'Api', 'Mvc', 'Mongodb', 'Ql']
    replacements = {
        'Html': 'HTML',
        'Css': 'CSS',
        'Api': 'API',
        'Apis': 'APIs',
        'Mvc': 'MVC',
        'Mongodb': 'MongoDB',
        'Ql': 'SQL'
    }
    for term, replacement in replacements.items():
        name = re.sub(r'\b{}\b'.format(term), replacement, name, flags=re.I)
    name = re.sub(r'\b(and)\b', lambda pat: pat.group(1).lower(), name, flags=re.I)
    return name

# Generate a URL-friendly slug
def generate_slug(name):
    slug = re.sub(r"[^\w\s-]", "", name).strip().lower()
    slug = re.sub(r"[\s_]+", "-", slug)
    return "/" + slug

# Generate a short unique ID
def generate_id():
    return hashlib.md5(os.urandom(4)).hexdigest()[:8]

start_path = os.path.dirname(os.path.realpath(__file__))
allowed_extensions = ['.md', '.pdf']

courses_data = {"courses": []}
id_counter = 1

folder_order = read_order_from_file(os.path.join(start_path, "folder_order.txt"))
all_courses = set(os.listdir(start_path))
all_courses.difference_update(folder_order)
all_courses = folder_order + list(all_courses)

subfolder_order = read_order_from_file(os.path.join(start_path, "subfolder_order.txt"))

for course_name in all_courses:
    course_path = os.path.join(start_path, course_name)
    if os.path.isdir(course_path):
        course_data = {
            "id": id_counter,
            "title": format_title(course_name),
            "format": "md",
            "cover": generate_slug(course_name)[1:] + ".png",
            "slug": generate_slug(course_name),
            "lessons": []
        }
        id_counter += 1
        
        all_lessons = set(os.listdir(course_path))
        all_lessons.difference_update(subfolder_order)
        all_lessons = subfolder_order + list(all_lessons)

        for lesson_name in all_lessons:
            lesson_path = os.path.join(course_path, lesson_name)
            if os.path.isdir(lesson_path):
                lesson_data = {
                    "id": id_counter,
                    "title": format_title(lesson_name),
                    "slug": os.path.join(generate_slug(course_name), generate_slug(lesson_name)),
                    "sections": []
                }
                id_counter += 1
                
                for filename in sorted(os.listdir(lesson_path)):
                    file_path = os.path.join(lesson_path, filename)
                    if os.path.isfile(file_path) and os.path.splitext(filename)[1] in allowed_extensions:
                        section_data = {
                            "id": id_counter,
                            "title": format_title(filename.replace('.md', '')),
                            "file": os.path.join(generate_slug(course_name), generate_slug(lesson_name), filename.lower()),
                            "slug": os.path.join(generate_slug(course_name), generate_slug(lesson_name), generate_slug(filename.replace('.md', '')))
                        }
                        id_counter += 1
                        lesson_data["sections"].append(section_data)

                course_data["lessons"].append(lesson_data)

        courses_data["courses"].append(course_data)

# Save to courses.json
with open(os.path.join(start_path, 'courses.json'), 'w') as file:
    import json
    json.dump(courses_data, file, indent=4)

print("Generated courses data and saved to courses.json.")
