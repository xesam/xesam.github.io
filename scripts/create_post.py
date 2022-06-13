"""
python create_post.py keil-1 keil基础 2018-06-01 computer c51
"""
import os
import sys


def get_src_dir():
    return os.path.dirname(__file__)


def get_template():
    src_dir = get_src_dir()
    template_path = os.path.join(src_dir, 'template.md')
    with open(template_path, encoding='utf-8') as in_file:
        return ''.join(list(in_file.readlines()))


def render(template, **kwargs):
    content = template.format(**kwargs)
    return content


def create_post(filename, date, category, content):
    src_dir = get_src_dir()
    proj_dir = os.path.abspath(os.path.join(src_dir, '..'))
    posts_dir = os.path.join(proj_dir, '_posts')
    post_dir = os.path.join(posts_dir, category)
    post_path = os.path.join(post_dir, f'{date}-{filename}.md')
    with open(post_path, mode='w', encoding='utf-8') as out_file:
        out_file.write(content)


if __name__ == '__main__':
    _, new_filename, title, argv_date, argv_category, tags = sys.argv
    new_content = render(get_template(),
                         title=title,
                         date=argv_date,
                         category=argv_category,
                         tags=tags)
    create_post(new_filename, argv_date, argv_category, new_content)
