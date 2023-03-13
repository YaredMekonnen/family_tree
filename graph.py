import plotly.graph_objects as go
import json

class Graph:
    def __init__(self):
        self.vertices = {}
        self.edges = []
    
    def add_person(self, name):
        if name not in self.vertices:
            self.vertices[name] = []
    
    def add_relationship(self, person1, relationship, person2):
        self.add_person(person1)
        self.add_person(person2)
        self.vertices[person1].append((person2, relationship))
        self.vertices[person2].append((person1, relationship))
        self.edges.append((person1, person2, relationship))
    
    def save_tree(self, filename):
        fig = self.display_tree()
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        with open(filename, "w") as f:
            f.write(f"var graphJSON = {graphJSON};")
    
    def display_tree(self):
        fig = go.Figure()
        pos = self.get_node_positions()
        for edge in self.edges:
            x = [pos[edge[0]][0], pos[edge[1]][0], None]
            y = [pos[edge[0]][1], pos[edge[1]][1], None]
            fig.add_trace(go.Scatter(x=x, y=y, mode='lines', line=dict(color='rgb(210,210,210)', width=1), hoverinfo='skip'))
        for name in pos:
            x_pos, y_pos, edges = pos[name]
            edge_text = "<br>".join([f"{edge[0]}: {edge[1]}" for edge in edges])
            fig.add_trace(go.Scatter(x=[x_pos], y=[y_pos], mode='markers+text', marker=dict(size=20), text=f"{name}<br>{edge_text}", textposition='top center', hoverinfo='text'))
        fig.update_layout(showlegend=False)
        return fig

    
    def get_node_positions(self):
        if not self.vertices:
            return {}

        root = next(iter(self.vertices.keys()))

        visited = set()
        node_positions = {}

        def dfs(node, level, x_pos):
            if node in visited:
                return
            visited.add(node)

            # Calculate y position based on level
            y_pos = level * -1

            # Store node position
            node_positions[node] = (x_pos, y_pos, [(edge[1], edge[2]) for edge in self.edges if edge[0] == node])

            # Recursively visit children
            children = self.vertices[node]
            num_children = len(children)
            if num_children > 1:
                space = 2 / (num_children - 1)
                x_offset = -1
                for child in children:
                    dfs(child[0], level - 1, x_pos + x_offset)
                    x_offset += space
            elif num_children == 1:
                dfs(children[0][0], level - 1, x_pos)

        dfs(root, 0, 0)
        return node_positions


    
    def get_node_positions_recursive(self, node, node_positions, level, left_angle, right_angle):
        if len(self.vertices[node]) == 1:
            return
        angle = (left_angle + right_angle) / 2
        angle_diff = (right_angle - left_angle) / (len(self.vertices[node]) - 1)
        for i, edge in enumerate(self.vertices[node]):
            if edge[0] not in node_positions:
                node_positions[edge[1]] = (level * 100 * round(2 ** 0.5, 1) * round((i - (len(self.vertices[node]) - 1) / 2) * 0.2, 1) * round(2 ** (level - 1), 1))


# g = Graph()
# g.add_relationship("Alice", "mother", "Bob")
# g.add_relationship("Bob", "father", "Charlie")
# g.add_relationship("Bob", "father", "David")
# g.add_relationship("Charlie", "father", "Eve")
# g.add_relationship("David", "mother", "Frank")
# g.add_relationship("David", "father", "Grace")
# g.display_tree()
# create a graph object
family_tree = Graph()

# add vertices (people)
family_tree.add_person("Person1")
family_tree.add_person("Person2")
family_tree.add_person("Person3")
family_tree.add_person("Person4")
family_tree.add_person("Person5")
family_tree.add_person("Person6")

# add edges (relationships)
family_tree.add_relationship("Person1", "parent", "Person2")
family_tree.add_relationship("Person2", "child", "Person1")
family_tree.add_relationship("Person2", "parent", "Person3")
family_tree.add_relationship("Person3", "child", "Person2")
family_tree.add_relationship("Person2", "parent", "Person4")
family_tree.add_relationship("Person4", "child", "Person2")
family_tree.add_relationship("Person3", "parent", "Person5")
family_tree.add_relationship("Person5", "child", "Person3")
family_tree.add_relationship("Person4", "parent", "Person6")
family_tree.add_relationship("Person6", "child", "Person4")

# display the family tree graph
family_tree.display_tree()
