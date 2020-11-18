# Amulet-Palette-Map
 A powerful Amulet operation for mapping blocks to blocks.

## Notes
 - How to use:
   1. Add the operation into your plugins/operations folder in Amulet
   2. Define a list of mappings, one per line, in a '.txt' file
   3. Enter the path of the file in the options for the operation
   4. Run the operation
 - You can define a comment by starting a line with a '\#'
 - [Example mapping file](https://github.com/byAdam/Amulet-Palette-Map/blob/main/example_map.txt).
 - Due to the nature of the operation, the 'undo' functionality will not work. Make sure to save any changes in Amulet before using this operation.

## Mapping Format
### `OLD_BLOCK_NAME<OLD_BLOCK_PROPERTIES > NEW_BLOCK_NAME<NEW_BLOCK_PROPERTIES`

### OLD_BLOCK_NAME
 - The namespace and name of the blocks you want to replace. 
   - Example: **adam:custom_block**
 - Vanilla blocks will be in Amulet's universal_minecraft format. 
   - Example: **universal_minecraft:slab** 
 

### OLD_BLOCK_PROPERTIES
 - The properties you want to filter by for the blocks you want to replace. 
   - Example: **universal_minecraft:wool<{"color":"blue"}**
 - Vanilla blocks will be in Amulet's universal_minecraft format. 
 - Uses python dictionary syntax. 
 - Leave it blank to have no filter. 
   - Example: **universal_minecraft:wool**


### NEW_BLOCK_NAME
 - The namespace and name of the block you want to map to. 
   - Example: **minecraft:stained_hardened_clay**
 
### NEW_BLOCK_PROPERTIES
 - The properties of the block you want to map to. 
   - Example: **minecraft:stained_hardened_clay<{"color":"red"}**
 - Uses python dictionary syntax. 
 - Use '\*' to use the property value from the old block
   - Example: **minecraft:stained_hardened_clay<{"color":"*"}**
 - Use '$PROPERTY' to access a property value from the old block
   - Example: **minecraft:stained_hardened_clay<{"adam:color":"$color"}**
 - Use a '\*' instead of a dictionary to copy all propetries from the old block
   - Example: **minecraft:stained_hardened_clay<\***
