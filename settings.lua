require "data/spawns"
require "data/worlds"

-- Get the world names from worlds
world_names = {}
for world_name, pos in pairs(worlds) do
    table.insert(world_names, world_name)
end

-- Get only the spawn names from spawns
spawn_names = {}
for spawn_name, _ in pairs(spawns) do
    table.insert(spawn_names, spawn_name)
end

data:extend({
    {
        type = "string-setting",
        name = "world-map",
        setting_type = "runtime-global",
        default_value = world_names[1],
        allowed_values = world_names,
        order = "a"
    },
    {
        type = "double-setting",
        name = "map-gen-scale",
        setting_type = "runtime-global",
        minimum_value = 0.01,
        default_value = 6,
        --allowed_values = {6, 12, 18, 24},
        order = "b"
    },
    {
        type = "string-setting",
        name = "spawn-position",
        setting_type = "runtime-global",
        default_value = spawn_names[2],
        allowed_values = spawn_names,
        order = "cp"
    },
    {
        type = "double-setting",
        name = "spawn-x",
        setting_type = "runtime-global",
        default_value = spawns[spawn_names[2]].earth_atlantic.x,
        order = "cx"
    },
    {
        type = "double-setting",
        name = "spawn-y",
        setting_type = "runtime-global",
        default_value = spawns[spawn_names[2]].earth_atlantic.y,
        order = "cy"
    },
    {
        type = "bool-setting",
        name = "repeat-map",
        setting_type = "runtime-global",
        default_value = true,
        order = "d"
    },
    {
        type = "int-setting",
        name = "safe-zone-size",
        setting_type = "runtime-global",
        default_value = 5,
        order = "e"
    }
})
