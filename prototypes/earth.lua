if not mods['space-age'] or not settings.startup['only-apply-to-earth'].value then
    return
end

local asteroid_util = require("__space-age__.prototypes.planet.asteroid-spawn-definitions")

local planet_earth = data.raw.planet.earth

if not planet_earth then
    local earth = util.table.deepcopy(data.raw['planet']['nauvis'])

    earth.name = "earth"
    earth.gravity_pull = 9.8
    earth.distance = 15
    earth.orientation = 120 / 360
    earth.magnitude = 1
    earth.order = "a[earth]"
    earth.icon = "__factorio-world__/graphics/earth-icon.png"
    earth.starmap_icon = "__factorio-world__/graphics/earth.png"
    earth.starmap_icon_size = 1024
    earth.surface_properties.gravity = 9.8
    earth.subgroup = "planets"
    earth.pollutant_type = "pollution"
    earth.asteroid_spawn_influence = 1
    earth.asteroid_spawn_definitions = asteroid_util.spawn_definitions(asteroid_util.nauvis_gleba, 0.9)
    
    data:extend({earth})
    
    data.extend({
        --- space connection
        {
            type = "space-connection",
            name = "nauvis-earth",
            subgroup = "planet-connections",
            from = "nauvis",
            to = "earth",
            order = "nauvis-earth",
            length = 20000,
            asteroid_spawn_definitions = asteroid_util.spawn_definitions(asteroid_util.nauvis_gleba)
        },
        --- unlock tech
        {
            type = "technology",
            name = "planet-discovery-earth",
            icons = {
                {
                    icon = "__factorio-world__/graphics/earth-icon.png",
                    icon_size = 64,
                },
                {
                    icon = "__core__/graphics/icons/technology/constants/constant-planet.png",
                    icon_size = 128,
                    scale = 0.5,
                    shift = { 50, 50 }
                }
            },
            essential = false,
            effects = {
                {
                    type = "unlock-space-location",
                    space_location = "earth",
                    use_icon_overlay_constant = true
                },
            },
            prerequisites = { "space-platform-thruster", "landfill" },
            unit = {
                count = 1000,
                ingredients = {
                    { "automation-science-pack", 1 },
                    { "logistic-science-pack", 1 },
                    { "chemical-science-pack", 1 },
                    { "space-science-pack", 1 }
                },
                time = 60
            }
        },
    })
end