import bpy
from bpy.props import StringProperty
from bpy_extras.io_utils import ImportHelper
from .rose.zms import ZMS


class ImportZMS(bpy.types.Operator, ImportHelper):
    """Import ROSE Online ZMS mesh file"""
    bl_idname = "import_mesh.zms"
    bl_label = "Import ROSE mesh (.zms)"
    bl_options = {'PRESET', 'UNDO'}
    
    filename_ext = ".zms"
    filter_glob: StringProperty(default="*.zms;*.ZMS", options={'HIDDEN'})

    def execute(self, context):
        try:
            # Load ZMS file
            zms = ZMS(self.filepath)
            
            # Create mesh data
            vertices = []
            faces = []
            
            # Extract vertex positions
            for v in zms.vertices:
                vertices.append((v.position.x, v.position.y, v.position.z))
            
            # Extract face indices
            for idx in zms.indices:
                faces.append((idx.x, idx.y, idx.z))
            
            # Create mesh and object
            mesh_name = bpy.path.display_name_from_filepath(self.filepath)
            mesh = bpy.data.meshes.new(mesh_name)
            obj = bpy.data.objects.new(mesh_name, mesh)
            
            # Link object to scene
            context.collection.objects.link(obj)
            
            # Create mesh from data
            mesh.from_pydata(vertices, [], faces)
            
            # Add UV maps if present
            if zms.uv1_enabled():
                uv_layer = mesh.uv_layers.new(name="UVMap")
                for face_idx, face in enumerate(mesh.polygons):
                    for vert_idx, loop_idx in zip(face.vertices, face.loop_indices):
                        uv = zms.vertices[vert_idx].uv1
                        uv_layer.data[loop_idx].uv = (uv.x, uv.y)
            
            if zms.uv2_enabled():
                uv_layer2 = mesh.uv_layers.new(name="UVMap2")
                for face_idx, face in enumerate(mesh.polygons):
                    for vert_idx, loop_idx in zip(face.vertices, face.loop_indices):
                        uv = zms.vertices[vert_idx].uv2
                        uv_layer2.data[loop_idx].uv = (uv.x, uv.y)
            
            # Add vertex colors if present
            if zms.colors_enabled():
                color_layer = mesh.vertex_colors.new(name="Color")
                for face in mesh.polygons:
                    for vert_idx, loop_idx in zip(face.vertices, face.loop_indices):
                        color = zms.vertices[vert_idx].color
                        color_layer.data[loop_idx].color = (color.r, color.g, color.b, color.a)
            
            # Add normals if present
            if zms.normals_enabled():
                normals = []
                for v in zms.vertices:
                    normals.append((v.normal.x, v.normal.y, v.normal.z))
                # In Blender 5.0+, custom normals are set directly without use_auto_smooth
                mesh.normals_split_custom_set_from_vertices(normals)
            
            # Update mesh
            mesh.update()
            mesh.validate()
            
            # Select the new object
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            context.view_layer.objects.active = obj
            
            self.report({'INFO'}, f"Imported {mesh_name}: {len(vertices)} vertices, {len(faces)} faces")
            return {'FINISHED'}
            
        except Exception as e:
            self.report({'ERROR'}, f"Failed to import ZMS: {str(e)}")
            return {'CANCELLED'}
