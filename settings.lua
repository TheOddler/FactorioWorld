require "spawns"

-- Get only the spawn names from spawns
spawn_names = {}
for name, pos in pairs(spawns) do
    table.insert(spawn_names, name)
end

data:extend({
    {
        type = "double-setting",
        name = "map-gen-scale",
        setting_type = "runtime-global",
        minimum_value = 0.01,
        default_value = 6,
        --allowed_values = {6, 12, 18, 24},
        order = "a"
    },
    {
        type = "string-setting",
        name = "spawn-position",
        setting_type = "runtime-global",
        default_value = spawn_names[1],
        allowed_values = spawn_names,
        order = "ba"
    },
    {
        type = "double-setting",
        name = "spawn-x",
        setting_type = "runtime-global",
        default_value = spawns[spawn_names[2]].x,
        order = "bx"
    },
    {
        type = "double-setting",
        name = "spawn-y",
        setting_type = "runtime-global",
        default_value = spawns[spawn_names[2]].y,
        order = "by"
    },
    {
        type = "bool-setting",
        name = "repeat-map",
        setting_type = "runtime-global",
        default_value = true,
        order = "c"
    },
    {
        type = "bool-setting",
        name = "use-large-map",
        setting_type = "runtime-global",
        default_value = false,
        order = "d"
    },
    {
        type = "int-setting",
        name = "safe-zone-size",
        setting_type = "runtime-global",
        default_value = 5,
        order = "e"
    },
    {
        type = "bool-setting",
        name = "only-apply-to-earth",
        setting_type = "startup",
        default_value = false,
        order = "a"
    }
})