# Draw 600 monkeys in random colors in Blender using Python
# Pythonを使ってBlenderで600体のサルをランダムの色で描く

import bpy
from random import randint
import numpy as np

# "def HSL_2_RGB" and "def Hue_2_RGB" ported "HSL → RGB" 
# from https://www.easyrgb.com/en/math.php to Python.

def HSL_2_RGB(H, S, L): # Function to convert HLS to RGB
    # H, S and L input range = 0 - 1.0
    # R, G and B output range = 0 - 1.0  # Changed 255 to 1.0
    if S == 0 :
        R = L * 1.0     # Changed 255 to 1.0
        G = L * 1.0     # Changed 255 to 1.0
        B = L * 1.0     # Changed 255 to 1.0
    else:
        if L < 0.5 : var_2 = L * ( 1 + S )
        else : var_2 = ( L + S ) - ( S * L )
    var_1 = 2 * L - var_2
    R = 1.0 * Hue_2_RGB( var_1, var_2, H + ( 1 / 3 ) )  # Changed 255 to 1.0
    G = 1.0 * Hue_2_RGB( var_1, var_2, H )              # Changed 255 to 1.0
    B = 1.0 * Hue_2_RGB( var_1, var_2, H - ( 1 / 3 ) )  # Changed 255 to 1.0
    return R, G, B


def Hue_2_RGB( v1, v2, vH ):    # Function to convert Hue to RGB
   if vH < 0 : vH += 1
   if vH > 1 : vH -= 1
   if 6 * vH < 1 : return ( v1 + ( v2 - v1 ) * 6 * vH )
   if 2 * vH < 1 : return ( v2 )
   if 3 * vH < 2 : return ( v1 + ( v2 - v1 ) * ( ( 2 / 3 ) - vH ) * 6 )
   return ( v1 )


def materialRandomColor(materialName='') :  # Function to make material
    material = bpy.data.materials.new(materialName)
    material.use_nodes = True 
    p_BSDF = material.node_tree.nodes["Principled BSDF"] 
    R, G, B = HSL_2_RGB(np.random.rand(1), 1.0, 0.5)    # Get RGB values ​​of H = 0-1(random), S = 1, L = 0.5
    p_BSDF.inputs[0].default_value = (R, G, B, 1)       # RGBA
    p_BSDF.inputs[7].default_value = 0                  # Roughness
    p_BSDF.inputs[15].default_value = 0                 # Transmittance
    return material

# Add 600 monkeys. The first (i = 0) is at the origin,
# and the second and subsequent ones are at random locations.
number = 600
for i in range(number):
    if i == 0 : x, y, z = 0, 0, 0
    else : 
        x, y, z = randint(-30,30), randint(-30,30), randint(-30,30)
    materialName = 'Color' + str(i)
    material = materialRandomColor(materialName) 
    bpy.ops.mesh.primitive_monkey_add(location=(x,y,z))
    bpy.context.object.data.materials.append(material) 
