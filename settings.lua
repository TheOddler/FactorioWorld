data:extend({
    {
        type = "double-setting",
        name = "map-gen-scale",
        setting_type = "runtime-global",
        --minimum_value = 1,
        default_value = 1,
        --allowed_values = {6, 12, 18, 24},
        order = "a"
    },
    {
        type = "double-setting",
        name = "spawn-x",
        setting_type = "runtime-global",
        default_value = 0.5,
        order = "bx"
    },
    {
        type = "double-setting",
        name = "spawn-y",
        setting_type = "runtime-global",
        default_value = 0.5,
        order = "by"
    },
})
