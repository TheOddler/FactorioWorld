data:extend({
    {
        type = "int-setting",
        name = "map-gen-scale",
        setting_type = "runtime-global",
        minimum_value = 1,
        default_value = 6,
        --allowed_values = {6, 12, 18, 24},
        order = "a"
    },
    {
        type = "int-setting",
        name = "spawn-x",
        setting_type = "runtime-global",
        default_value = 2064,
        order = "bx"
    },
    {
        type = "int-setting",
        name = "spawn-y",
        setting_type = "runtime-global",
        default_value = 406,
        order = "by"
    },
    {
        type = "bool-setting",
        name = "use-large-map",
        setting_type = "runtime-global",
        default_value = false,
        order = "c"
    },
})
