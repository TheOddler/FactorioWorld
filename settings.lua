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
        type = "double-setting",
        name = "spawn-x",
        setting_type = "runtime-global",
        default_value = 2064,
        order = "bx"
    },
    {
        type = "double-setting",
        name = "spawn-y",
        setting_type = "runtime-global",
        default_value = 406,
        order = "by"
    },
    {
        type = "bool-setting",
        name = "use-large-map",
        setting_type = "runtime-global",
        default_value = true,
        order = "c"
    },
    {
        type = "int-setting",
        name = "safe-zone-size",
        setting_type = "runtime-global",
        default_value = 5,
        order = "c"
    },
})
