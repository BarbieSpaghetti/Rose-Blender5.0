bl_info = {
    "name": "ROSE Online blender plugin",
    "author": "Ralph Minderhoud + BarbieSpaghetti",
    "blender": (5, 0, 1),
    "version": (0, 0, 4),
    "location": "File > Import",
    "description": "Import files from ROSE Online",
    "category": "Import-Export",
}

if "bpy" in locals():
    import importlib
    importlib.reload(import_map)
    importlib.reload(import_zms)
else:
    from . import import_map
    from . import import_zms
    import bpy

def menu(self, context):
    self.layout.separator()
    self.layout.operator(import_zms.ImportZMS.bl_idname, text=import_zms.ImportZMS.bl_label)
    self.layout.operator(import_map.ImportMap.bl_idname, text="ROSE Map (.zon)")

def register():
    bpy.utils.register_class(import_zms.ImportZMS)
    bpy.utils.register_class(import_map.ImportMap)
    bpy.types.TOPBAR_MT_file_import.append(menu)

def unregister():
    bpy.types.TOPBAR_MT_file_import.remove(menu)
    bpy.utils.unregister_class(import_zms.ImportZMS)
    bpy.utils.unregister_class(import_map.ImportMap)

if __name__ == "__main__":
    register()
