import os
import argparse
from pathlib import Path
import hashlib
import math
import json

# Global configuration parameters
NODE_WIDTH = 220
NODE_HEIGHT = 40
NODE_RADIUS = 10
VERTICAL_GAP = 45
HORIZONTAL_GAP = 45
MIN_COLOR = (0, 128, 0)  # Green
MID_COLOR = (255, 255, 0)  # Yellow
MAX_COLOR = (200, 0, 0)  # Red
CONNECTOR_COLOR = "#AAAAAA"
TEXT_COLOR = "#FFFFFF"
BG_COLOR = "#2A2A2A"

class DirectorySVGGenerator:
    def __init__(self, root_dir):
        self.root_dir = os.path.abspath(root_dir)
        self.root_name = os.path.basename(self.root_dir)
        self.nodes = []
        self.connections = []
        self.dir_sizes = {}
        self.directory_tree = {}
        self.node_width = NODE_WIDTH
        self.node_height = NODE_HEIGHT
        self.node_radius = NODE_RADIUS
        self.vertical_gap = VERTICAL_GAP
        self.horizontal_gap = HORIZONTAL_GAP
        self.min_color = MIN_COLOR
        self.mid_color = MID_COLOR
        self.max_color = MAX_COLOR
        self.connector_color = CONNECTOR_COLOR
        self.text_color = TEXT_COLOR
        self.bg_color = BG_COLOR
        self.level_positions = {}
        self.max_level = 0
        self.max_width = 0
        self.max_height = 0
        self.max_dir_size = 1
        self.min_dir_size = float('inf')

    def calculate_dir_size(self, directory):
        total_size = 0
        try:
            for dirpath, dirnames, filenames in os.walk(directory):
                for filename in filenames:
                    file_path = os.path.join(dirpath, filename)
                    try:
                        total_size += os.path.getsize(file_path)
                    except (FileNotFoundError, PermissionError):
                        pass
        except (PermissionError, FileNotFoundError):
            return 0
        return total_size

    def scan_directory_sizes(self, directory=None):
        if directory is None:
            directory = self.root_dir
        try:
            subdirs = [os.path.join(directory, item) for item in os.listdir(directory) 
                       if os.path.isdir(os.path.join(directory, item))]
        except (PermissionError, FileNotFoundError):
            return
        dir_size = self.calculate_dir_size(directory)
        self.dir_sizes[directory] = dir_size
        if dir_size > 0:
            self.min_dir_size = min(self.min_dir_size, dir_size)
        self.max_dir_size = max(self.max_dir_size, dir_size)
        for subdir in subdirs:
            self.scan_directory_sizes(subdir)

    def get_color_for_size(self, size):
        if self.max_dir_size <= self.min_dir_size or self.min_dir_size == float('inf'):
            return f"#{int(self.mid_color[0]):02x}{int(self.mid_color[1]):02x}{int(self.mid_color[2]):02x}"  # Yellow
        normalized_size = (size - self.min_dir_size) / (self.max_dir_size - self.min_dir_size)
        normalized_size = max(0, min(1, normalized_size))
        if normalized_size <= 0.5:
            factor = normalized_size * 2
            r = int(self.min_color[0] + factor * (self.mid_color[0] - self.min_color[0]))
            g = int(self.min_color[1] + factor * (self.mid_color[1] - self.min_color[1]))
            b = int(self.min_color[2] + factor * (self.mid_color[2] - self.min_color[2]))
        else:
            factor = (normalized_size - 0.5) * 2
            r = int(self.mid_color[0] + factor * (self.max_color[0] - self.mid_color[0]))
            g = int(self.mid_color[1] + factor * (self.max_color[1] - self.mid_color[1]))
            b = int(self.mid_color[2] + factor * (self.max_color[2] - self.min_color[2]))
        return f"#{r:02x}{g:02x}{b:02x}"

    def format_size(self, size_bytes):
        if size_bytes == 0:
            return "0 B"
        size_names = ["B", "KB", "MB", "GB", "TB"]
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return f"{s} {size_names[i]}"

    def build_directory_tree(self, directory=None, parent_id=None):
        if directory is None:
            directory = self.root_dir
        dir_id = self._generate_id(directory)
        dir_name = os.path.basename(directory)
        dir_size = self.dir_sizes.get(directory, 0)
        node_data = {
            'id': dir_id,
            'name': dir_name,
            'path': directory,
            'size': dir_size,
            'formatted_size': self.format_size(dir_size),
            'children': [],
            'color': self.get_color_for_size(dir_size),
            'parent': parent_id
        }
        self.directory_tree[dir_id] = node_data
        try:
            subdirs = sorted([item for item in os.listdir(directory) 
                              if os.path.isdir(os.path.join(directory, item))])
            for subdir in subdirs:
                subdir_path = os.path.join(directory, subdir)
                subdir_id = self._generate_id(subdir_path)
                self.build_directory_tree(subdir_path, dir_id)
                node_data['children'].append(subdir_id)
        except (PermissionError, FileNotFoundError):
            pass
        return dir_id

    def generate_interactive_svg(self):
        svg_width = 1600
        svg_height = 1200
        svg = []
        svg.append('<!DOCTYPE html>')
        svg.append('<html>')
        svg.append('<head>')
        svg.append('<meta charset="UTF-8">')
        svg.append('<title>Interactive Directory Structure</title>')
        svg.append('<style>')
        svg.append('  body { margin: 0; padding: 0; background-color: #1a1a1a; overflow: auto; }')
        svg.append('  #svg-container { width: 100%; height: 100vh; overflow: auto; }')
        svg.append('  svg { display: block; width: 100%; height: auto; }')
        svg.append('  .node { cursor: pointer; }')
        svg.append('  .node-text { pointer-events: none; }')
        svg.append('  .connector { pointer-events: none; }')
        svg.append('  .toggle-icon { cursor: pointer; fill: #ffffff; }')
        svg.append('  .controls { position: fixed; top: 10px; right: 20px; background: rgba(0,0,0,0.7); padding: 10px; border-radius: 5px; color: white; }')
        svg.append('  .zoom-button { background: #444; color: white; border: none; padding: 5px 10px; margin: 0 5px; cursor: pointer; border-radius: 3px; }')
        svg.append('  input[type="number"], input[type="text"] { background: #444; color: white; border: none; padding: 5px; border-radius: 3px; }')
        svg.append('  label { margin-right: 5px; }')
        svg.append('  .legend { margin-top: 10px; }')
        svg.append('  .legend-bar { width: 150px; height: 20px; background: linear-gradient(to right, #008000, #FFFF00, #C80000); border-radius: 3px; }')
        svg.append('  .legend-labels { display: flex; justify-content: space-between; font-size: 12px; margin-top: 2px; }')
        svg.append('</style>')
        svg.append('</head>')
        svg.append('<body>')
        svg.append('<div class="controls">')
        svg.append('  <button class="zoom-button" id="zoom-in">Zoom In (+)</button>')
        svg.append('  <button class="zoom-button" id="zoom-out">Zoom Out (-)</button>')
        svg.append('  <button class="zoom-button" id="zoom-reset">Reset Zoom</button>')
        svg.append('  <div style="margin-top: 10px;">')
        svg.append('    <label>Vertical Gap: </label>')
        svg.append('    <input type="number" id="vertical-gap-input" min="45" max="500" step="5" style="width: 60px;">')
        svg.append('  </div>')
        svg.append('  <div style="margin-top: 5px;">')
        svg.append('    <label>Horizontal Gap: </label>')
        svg.append('    <input type="number" id="horizontal-gap-input" min="45" max="500" step="5" style="width: 60px;">')
        svg.append('  </div>')
        svg.append('  <div style="margin-top: 10px;">')  # Arama kutusu ekleniyor
        svg.append('    <label>Search: </label>')
        svg.append('    <input type="text" id="search-input" placeholder="Enter directory name..." style="width: 150px;">')
        svg.append('  </div>')
        svg.append('  <div class="legend">')
        svg.append('    <div class="legend-bar"></div>')
        svg.append(f'    <div class="legend-labels"><span>Small ({self.format_size(self.min_dir_size)})</span><span>Large ({self.format_size(self.max_dir_size)})</span></div>')
        svg.append('  </div>')
        svg.append('</div>')
        svg.append('<div id="svg-container">')
        svg.append(f'<svg id="directory-tree" viewBox="0 0 {svg_width} {svg_height}" preserveAspectRatio="xMinYMin meet">')
        svg.append(f'<rect width="100%" height="100%" fill="{self.bg_color}"/>')
        svg.append('<g id="diagram">')
        svg.append('<g id="connections"></g>')
        svg.append('<g id="nodes"></g>')
        svg.append('</g>')
        svg.append('</svg>')
        svg.append('</div>')
        svg.append('<script>')
        svg.append(f'''
        const nodeWidth = {self.node_width};
        const nodeHeight = {self.node_height};
        const nodeRadius = {self.node_radius};
        let verticalGap = {self.vertical_gap};
        let horizontalGap = {self.horizontal_gap};
        ''')
        svg.append('const treeData = ' + json.dumps(self.directory_tree) + ';')
        svg.append('''
        const svg = document.getElementById('directory-tree');
        const svgContainer = document.getElementById('svg-container');
        const diagram = document.getElementById('diagram');
        const nodesGroup = document.getElementById('nodes');
        const connectionsGroup = document.getElementById('connections');
        const nodeStates = {};
        let currentZoom = 0.5;
        let zoomIncrement = 0.1;
        let rootId = Object.keys(treeData).find(id => !treeData[id].parent);
        Object.keys(treeData).forEach(id => {
            nodeStates[id] = { expanded: id === rootId, visible: false };
        });
        if (rootId) {
            nodeStates[rootId].visible = true;
            treeData[rootId].children.forEach(childId => {
                nodeStates[childId].visible = true;
            });
        }
        renderTree();
        zoomOut();  // İlk yüklenmede zoom out
        svg.addEventListener('wheel', handleWheel);
        document.getElementById('zoom-in').addEventListener('click', () => {
            zoomIn();
        });
        document.getElementById('zoom-out').addEventListener('click', () => {
            zoomOut();
        });
        document.getElementById('zoom-reset').addEventListener('click', () => {
            resetZoom();
        });
        const verticalGapInput = document.getElementById('vertical-gap-input');
        const horizontalGapInput = document.getElementById('horizontal-gap-input');
        verticalGapInput.value = verticalGap;
        horizontalGapInput.value = horizontalGap;
        verticalGapInput.addEventListener('input', (e) => {
            verticalGap = parseInt(e.target.value) || 100;
            renderTree();
        });
        horizontalGapInput.addEventListener('input', (e) => {
            horizontalGap = parseInt(e.target.value) || 300;
            renderTree();
        });
        document.getElementById('search-input').addEventListener('input', (e) => {
            const searchTerm = e.target.value.toLowerCase();
            searchNodes(searchTerm);
            renderTree();
        });
        function zoomIn() {
            currentZoom += zoomIncrement;
            updateZoom();
        }
        function zoomOut() {
            currentZoom = Math.max(0.1, currentZoom - zoomIncrement);
            updateZoom();
        }
        function resetZoom() {
            currentZoom = 1;
            updateZoom();
        }
        function updateZoom() {
            diagram.setAttribute('transform', `scale(${currentZoom})`);
        }
        function handleWheel(e) {
            const container = document.getElementById('svg-container');
            const scrollSpeed = 50;
           if (e.deltaY < 0) {
                container.scrollTop -= scrollSpeed;
            } else {
                container.scrollTop += scrollSpeed;
            }
        }
        function updateSVGSize() {
            const nodes = document.querySelectorAll('.node');
            if (nodes.length === 0) return;
            let maxX = 0;
            let maxY = 0;
            nodes.forEach(node => {
                const rect = node.querySelector('rect');
                const x = parseFloat(rect.getAttribute('x')) + nodeWidth;
                const y = parseFloat(rect.getAttribute('y')) + nodeHeight;
                maxX = Math.max(maxX, x);
                maxY = Math.max(maxY, y);
            });
            maxX += 100;
            maxY += 150;
            svg.setAttribute('viewBox', `0 0 ${maxX} ${maxY}`);
            svg.setAttribute('width', maxX);
            svg.setAttribute('height', maxY);
        }
        function renderTree() {
            nodesGroup.innerHTML = '';
            connectionsGroup.innerHTML = '';
            calculateNodePositions();
            renderConnections();
            renderNodes();
            updateSVGSize();
        }
                   
        function calculateNodePositions() {
            const visibleNodes = [];
            function traverseVisible(nodeId, level = 0, position = 0) {
                const node = treeData[nodeId];
                if (!nodeStates[nodeId].visible) return position;
                node.level = level;
                node.y = position * verticalGap + 45;
                visibleNodes.push(node);
                position++;
                if (nodeStates[nodeId].expanded) {
                    for (const childId of node.children) {
                        if (nodeStates[childId].visible) {  // Yalnızca görünür çocukları işle
                            position = traverseVisible(childId, level + 1, position);
                        }
                    }
                }
                return position;
            }
            if (rootId) {
                traverseVisible(rootId);
            }
            const levelPositions = {};
            const maxLevel = Math.max(...visibleNodes.map(n => n.level), 0);
            levelPositions[0] = 45;
            for (let level = 1; level <= maxLevel; level++) {
                levelPositions[level] = levelPositions[level-1] + nodeWidth + horizontalGap;
            }
            visibleNodes.forEach(node => {
                node.x = levelPositions[node.level];
            });
        }
        function renderConnections() {
            for (const nodeId in treeData) {
                const node = treeData[nodeId];
                if (!nodeStates[nodeId].visible) continue;
                if (!nodeStates[nodeId].expanded || !node.children.length) continue;
                for (const childId of node.children) {
                    if (!nodeStates[childId].visible) continue;
                    const child = treeData[childId];
                    const startX = node.x + nodeWidth;
                    const startY = node.y + (nodeHeight / 2);
                    const endX = child.x;
                    const endY = child.y + (nodeHeight / 2);
                    const controlX1 = startX + (endX - startX) * 0.4;
                    const controlX2 = startX + (endX - startX) * 0.6;
                    const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
                    path.setAttribute('d', `M ${startX} ${startY} C ${controlX1} ${startY}, ${controlX2} ${endY}, ${endX} ${endY}`);
                    path.setAttribute('stroke', '#AAAAAA');
                    path.setAttribute('stroke-width', '2');
                    path.setAttribute('fill', 'none');
                    path.setAttribute('class', 'connector');
                    connectionsGroup.appendChild(path);
                }
            }
        }
        function renderNodes() {
            for (const nodeId in treeData) {
                const node = treeData[nodeId];
                if (!nodeStates[nodeId].visible) continue;
                const nodeGroup = document.createElementNS('http://www.w3.org/2000/svg', 'g');
                nodeGroup.setAttribute('class', 'node');
                nodeGroup.setAttribute('data-id', nodeId);
                nodeGroup.addEventListener('click', (e) => toggleNode(nodeId, e));
                const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
                rect.setAttribute('x', node.x);
                rect.setAttribute('y', node.y);
                rect.setAttribute('width', nodeWidth);
                rect.setAttribute('height', nodeHeight);
                rect.setAttribute('rx', nodeRadius);
                rect.setAttribute('ry', nodeRadius);
                rect.setAttribute('fill', node.highlight ? '#FF4500' : node.color);  // Arama vurgusu
                nodeGroup.appendChild(rect);
                const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
                circle.setAttribute('cx', node.x + 15);
                circle.setAttribute('cy', node.y + nodeHeight / 2);
                circle.setAttribute('r', '5');
                circle.setAttribute('fill', '#FFD700');
                nodeGroup.appendChild(circle);
                const textName = document.createElementNS('http://www.w3.org/2000/svg', 'text');
                textName.setAttribute('x', node.x + 30);
                textName.setAttribute('y', node.y + nodeHeight / 2 - 5);
                textName.setAttribute('font-family', 'Arial');
                textName.setAttribute('font-size', '14px');
                textName.setAttribute('fill', '#FFFFFF');
                textName.setAttribute('class', 'node-text');
                textName.textContent = node.name;
                nodeGroup.appendChild(textName);
                const textSize = document.createElementNS('http://www.w3.org/2000/svg', 'text');
                textSize.setAttribute('x', node.x + 30);
                textSize.setAttribute('y', node.y + nodeHeight / 2 + 15);
                textSize.setAttribute('font-family', 'Arial');
                textSize.setAttribute('font-size', '12px');
                textSize.setAttribute('fill', '#FFFFFF');
                textSize.setAttribute('class', 'node-text');
                textSize.textContent = node.formatted_size;
                nodeGroup.appendChild(textSize);
                if (node.children.length > 0) {
                    const toggleIcon = document.createElementNS('http://www.w3.org/2000/svg', 'text');
                    toggleIcon.setAttribute('x', node.x + nodeWidth - 20);
                    toggleIcon.setAttribute('y', node.y + nodeHeight / 2 + 5);
                    toggleIcon.setAttribute('font-family', 'Arial');
                    toggleIcon.setAttribute('font-size', '18px');
                    toggleIcon.setAttribute('fill', '#FFFFFF');
                    toggleIcon.setAttribute('class', 'toggle-icon');
                    toggleIcon.textContent = nodeStates[nodeId].expanded ? '−' : '+';
                    toggleIcon.addEventListener('click', (e) => {
                        toggleNode(nodeId, e);
                        e.stopPropagation();
                    });
                    nodeGroup.appendChild(toggleIcon);
                }
                nodesGroup.appendChild(nodeGroup);
            }
        }
        function collapseSubtree(nodeId) {
            const node = treeData[nodeId];
            nodeStates[nodeId].expanded = false;
            node.children.forEach(childId => {
                nodeStates[childId].visible = false;
                collapseSubtree(childId);
            });
        }
        function toggleNode(nodeId, event) {
            nodeStates[nodeId].expanded = !nodeStates[nodeId].expanded;
            if (!nodeStates[nodeId].expanded) {
                collapseSubtree(nodeId);
            } else {
                treeData[nodeId].children.forEach(childId => {
                    nodeStates[childId].visible = true;
                });
            }
            renderTree();
        }
                   
        function searchNodes(searchTerm) {
            // Tüm düğümleri sıfırla
            Object.keys(treeData).forEach(id => {
                treeData[id].highlight = false;  // Vurgulamayı sıfırla
                nodeStates[id].visible = false;  // Tüm düğümleri görünmez yap
                nodeStates[id].expanded = false; // Tüm düğümleri kapat
            });

            if (searchTerm.trim() === '') {
                // Arama terimi boşsa, sadece kök düğümü ve çocuklarını aç
                if (rootId) {
                    nodeStates[rootId].expanded = true;
                    nodeStates[rootId].visible = true;
                    treeData[rootId].children.forEach(childId => {
                        nodeStates[childId].visible = true;
                    });
                }
                return;
            }

            // Eşleşen düğümleri bul ve genişlet
            Object.keys(treeData).forEach(id => {
                const node = treeData[id];
                if (node.name.toLowerCase().includes(searchTerm)) {
                    node.highlight = true;  // Eşleşen düğümü vurgula
                    nodeStates[id].expanded = true;  // Eşleşen düğümü genişlet
                    nodeStates[id].visible = true;   // Görünür yap
                    // Üst düğümleri de genişlet
                    let parentId = node.parent;
                    while (parentId) {
                        nodeStates[parentId].expanded = true;
                        nodeStates[parentId].visible = true;
                        parentId = treeData[parentId].parent;
                    }
                } else {
                    node.highlight = false;
                }
            });
        }
        </script>
        ''')
        svg.append('</body>')
        svg.append('</html>')
        return '\n'.join(svg)

    def _generate_id(self, path):
        return "node_" + hashlib.md5(path.encode()).hexdigest()[:8]

    def save_svg(self, output_path):
        self.scan_directory_sizes()
        self.build_directory_tree()
        html_content = self.generate_interactive_svg()
        if not os.path.isabs(output_path):
            output_path = os.path.join(self.root_dir, output_path)
        if output_path.endswith('.svg'):
            output_path = output_path[:-4] + '.html'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        return output_path

def main():
    parser = argparse.ArgumentParser(description='Generate an interactive SVG visualization of directory structure with collapsible nodes')
    parser.add_argument('directory', nargs='?', default=os.path.dirname(os.path.abspath(__file__)), 
                        help='Directory to visualize (defaults to script directory)')
    parser.add_argument('-o', '--output', default='directory_structure.html', help='Output HTML file path')
    args = parser.parse_args()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if not os.path.isabs(args.directory):
        args.directory = os.path.join(script_dir, args.directory)
    if not os.path.isdir(args.directory):
        print(f"Error: '{args.directory}' is not a valid directory.")
        return
    generator = DirectorySVGGenerator(args.directory)
    output_path = generator.save_svg(args.output)
    print(f"Generated visualization at: {output_path}")

if __name__ == "__main__":
    main()