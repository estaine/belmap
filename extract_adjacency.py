import json
from lxml import etree
from svgpathtools import parse_path
from shapely.geometry import LineString
from shapely.ops import unary_union

SVG_PATH = 'web/beldist.svg'
OUTPUT_JSON = 'district_adjacency.json'

def extract_paths(svg_file):
    parser = etree.XMLParser(huge_tree=True)
    tree = etree.parse(svg_file, parser)
    root = tree.getroot()
    ns = {'svg': 'http://www.w3.org/2000/svg'}
    paths = []
    for elem in root.xpath('.//svg:path', namespaces=ns):
        id_ = elem.attrib.get('id')
        d = elem.attrib.get('d')
        if id_ and d and id_.startswith('dist-'):
            paths.append((id_, d))
    return paths

def path_to_linestring(d):
    path = parse_path(d)
    points = []
    for seg in path:
        # Sample points along the segment for better accuracy
        for t in [i/20 for i in range(21)]:
            pt = seg.point(t)
            points.append((pt.real, pt.imag))
    # Remove consecutive duplicates
    filtered = [points[0]]
    for pt in points[1:]:
        if pt != filtered[-1]:
            filtered.append(pt)
    return LineString(filtered)

print('Parsing SVG...')
paths = extract_paths(SVG_PATH)
print(f'Found {len(paths)} district paths.')

district_lines = []
for id_, d in paths:
    try:
        line = path_to_linestring(d)
        district_lines.append((id_, line))
    except Exception as e:
        print(f'Error parsing {id_}: {e}')

adjacency = {}
for i, (id1, line1) in enumerate(district_lines):
    code1 = id1.replace('dist-', '')
    adjacency[code1] = []
    for j, (id2, line2) in enumerate(district_lines):
        if i == j:
            continue
        # Use a small buffer to account for floating point inaccuracies
        if line1.buffer(0.1).intersects(line2.buffer(0.1)):
            code2 = id2.replace('dist-', '')
            adjacency[code1].append(code2)

# Remove duplicates
for k in adjacency:
    adjacency[k] = sorted(list(set(adjacency[k])))

with open(OUTPUT_JSON, 'w') as f:
    json.dump(adjacency, f, indent=2)

print(f'Adjacency written to {OUTPUT_JSON}') 