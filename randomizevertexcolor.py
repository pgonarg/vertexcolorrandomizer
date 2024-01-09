import bpy
import bmesh
import random

def create_vertex_color_map(obj):
    # Create a vertex color map if it doesn't exist
    if obj.data.vertex_colors:
        vcol_layer = obj.data.vertex_colors.active
    else:
        vcol_layer = obj.data.vertex_colors.new()

    return vcol_layer

def get_linked_vertices(bm, start_vertex, found=None):
    """ Recursively find all vertices linked to the start vertex """
    if found is None:
        found = set()

    to_explore = {start_vertex}
    while to_explore:
        vertex = to_explore.pop()
        if vertex not in found:
            found.add(vertex)
            linked_vertices = {edge.other_vert(vertex) for edge in vertex.link_edges if edge.other_vert(vertex) not in found}
            to_explore.update(linked_vertices)
    return found

def paint_islands_different_colors(obj):
    mesh = obj.data

    # Create a BMesh
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bm.verts.ensure_lookup_table()

    vcol_layer = create_vertex_color_map(obj)

    visited = set()
    for vertex in bm.verts:
        if vertex not in visited:
            linked = get_linked_vertices(bm, vertex, found=set())
            visited.update(linked)
            
            # Assign a random color to all vertices in this linked set
            color = [random.random() for _ in range(3)] + [1.0]  # RGB + Alpha
            for face in bm.faces:
                for loop in face.loops:
                    if loop.vert in linked:
                        loop[bm.loops.layers.color.active] = color

    # Update the mesh
    bm.to_mesh(mesh)
    bm.free()

# Get the active object
obj = bpy.context.active_object
if obj and obj.type == 'MESH':
    paint_islands_different_colors(obj)
