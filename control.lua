require "worlds/earth_atlantic_normal"
require "worlds/earth_atlantic_detailed"
require "worlds/earth_pacific_normal"
require "worlds/earth_pacific_detailed"
require "data/spawns"
require "data/worlds"

--Terrain codes should be in sync with the ConvertMap code
local terrain_codes = {
    ["_"] = "out-of-map",
    ["o"] = "deepwater",--ocean
    ["O"] = "deepwater-green",
    ["w"] = "water",
    ["W"] = "water-green",
    ["g"] = "grass-1",
    ["m"] = "grass-3",
    ["G"] = "grass-2",
    ["d"] = "dirt-3",
    ["D"] = "dirt-6",
    ["s"] = "sand-1",
    ["S"] = "sand-3"
}

local map_data = {
  ["earth_atlantic_normal"]   = map_earth_atlantic_normal,
  ["earth_atlantic_detailed"] = map_earth_atlantic_detailed,
  ["earth_pacific_normal"]    = map_earth_pacific_normal,
  ["earth_pacific_detailed"]  = map_earth_pacific_detailed
}

----
--Don't touch anything under this, unless you know what you're doing
----
--Load settings
local world_map = settings.global["world-map"].value
local map_index = worlds[world_map].map_index
local detail_factor = worlds[world_map].detail_factor
local scale = settings.global["map-gen-scale"].value
local spawn_settings = {
  position = settings.global["spawn-position"].value,
  x = settings.global["spawn-x"].value,
  y = settings.global["spawn-y"].value
}
local safe_zone_size = settings.global["safe-zone-size"].value
local repeat_map = settings.global["repeat-map"].value

local out_of_map_code = "o" -- The terrain to use for everything outside the map

-- log("~world_map: " .. world_map)
-- log("~map_index: " .. map_index)
-- log("~detail_factor: " .. detail_factor)
-- log("~scale: " .. scale)
-- log("~position: " .. spawn_settings.position)
-- log("~safe_zone: " .. safe_zone_size)

-- disable new game start stuff
script.on_init(function()
    remote.call("freeplay", "set_disable_crashsite", true) -- removes crashsite and cutscene start
    remote.call("freeplay", "set_skip_intro", true)        -- Skips popup message to press tab to start playing
  end)


script.on_event(defines.events.on_runtime_mod_setting_changed, function(event)
    game.print("You shouldn't change the world-gen settings after you started a savegame. This will break the generating for new parts of the map.")
    game.print("The change is ignored for now, but will take effect when restarting the game.")
    game.print("Return them to what they were, or risk smegging up your save!")
    game.print("Your settings were: ")
    game.print("Scale = " .. scale)
    game.print("spawn: " .. spawn_settings.position .. "; x = " .. spawn_settings.x .. ", y = " .. spawn_settings.y)
    game.print("Use large map = " .. (detail_factor and "true" or "false"))
    game.print("Repeat map = " .. (repeat_map and "true" or "false"))
end)


--Get correct world data
---filename indexes to map data variable name
local terrain_types = map_data[worlds[world_map].filename]

--Get spawn by looking up the selection and map index in 'spawns' table
local spawn = spawns[spawn_settings.position][map_index]
--If x and y are not set because 'custom' was chosen, use the x and y in the settings object, which are read from the UI
spawn = {
    x = spawn.x or spawn_settings.x,
    y = spawn.y or spawn_settings.y
}

--Scale spawn so it is roughly the same position on the map regardless of scale and wether you use detailed map 
spawn = {
    x = scale * spawn.x * detail_factor,
    y = scale * spawn.y * detail_factor
}

--The variable that will store the decompressed map
local decompressed_map_data = {}
local width = nil
local height = #terrain_types
for y = 0, #terrain_types-1 do
    decompressed_map_data[y] = {}
end

--Function to actually do the decompressing
local function decrompress_line(y)
  local decompressed_line = decompressed_map_data[y]
    if(#decompressed_line == 0) then
        --do decompression of this line
        local total_count = 0
        local line = terrain_types[y+1]
        for letter, count in string.gmatch(line, "(%a+)(%d+)") do
            for x = total_count, total_count + count do
                decompressed_line[x] = letter
            end
            total_count = total_count + count
        end
        --check width (all lines must the equal in length)
        if width == nil then
            width = total_count
        elseif width ~= total_count then
            error("Mismatching width: " .. width .. " vs " .. total_count)
        end
    end
end

--Decompress one line to we know the width
decrompress_line(0)

--Helper functions
local function add_to_total(totals, weight, code)
    if totals[code] == nil then
        totals[code] = {code=code, weight=weight}
    else
        totals[code].weight = totals[code].weight + weight
    end
end

local function get_world_tile_code_raw(x, y)
    y_wrap = y % height
    x_wrap = x % width

    if not repeat_map and (x ~= x_wrap or y ~= y_wrap)then
        return out_of_map_code
    end

    decrompress_line(y_wrap)
    return decompressed_map_data[y_wrap][x_wrap]
end

local function get_world_tile_name(x, y)
    --figure out of this is the safe-zone before screwing with x and y
    safe_zone = x >= -safe_zone_size and x < safe_zone_size and y >= -safe_zone_size and y < safe_zone_size
    -- Check spaceship
    space_ship = x >= -14 and x < 2 and y >= -10 and y < -1
    --spawn
    x = x + spawn.x
    y = y + spawn.y
    --scaling
    x = x / scale
    y = y / scale
    --get cells you're between
    local top = math.floor(y)
    local bottom = (top + 1)
    local left = math.floor(x)
    local right = (left + 1)
    --calc weights
    local sqrt2 = math.sqrt(2)
    local w_top_left = 1 - math.sqrt((top - y)*(top - y) + (left - x)*(left - x)) / sqrt2
    local w_top_right = 1 - math.sqrt((top - y)*(top - y) + (right - x)*(right - x)) / sqrt2
    local w_bottom_left = 1 - math.sqrt((bottom - y)*(bottom - y) + (left - x)*(left - x)) / sqrt2
    local w_bottom_right = 1 - math.sqrt((bottom - y)*(bottom - y) + (right - x)*(right - x)) / sqrt2
    w_top_left = w_top_left * w_top_left + math.random() / math.max(scale / 2, 10)
    w_top_right = w_top_right * w_top_right + math.random() / math.max(scale / 2, 10)
    w_bottom_left = w_bottom_left * w_bottom_left + math.random() / math.max(scale / 2, 10)
    w_bottom_right = w_bottom_right * w_bottom_right + math.random() / math.max(scale / 2, 10)
    --get codes
    local c_top_left = get_world_tile_code_raw(left, top)
    local c_top_right = get_world_tile_code_raw(right, top)
    local c_bottom_left = get_world_tile_code_raw(left, bottom)
    local c_bottom_right = get_world_tile_code_raw(right, bottom)
    --calculate total weights for codes
    local totals = {}
    add_to_total(totals, w_top_left, c_top_left)
    add_to_total(totals, w_top_right, c_top_right)
    add_to_total(totals, w_bottom_left, c_bottom_left)
    add_to_total(totals, w_bottom_right, c_bottom_right)
    --choose final code
    local code = nil
    local weight = 0
    for _, total in pairs(totals) do
        if total.weight > weight then
            code = total.code
            weight = total.weight
        end
    end
    local terrain_name = terrain_codes[code]
    --safezone
    if (safe_zone or space_ship) and string.match(terrain_name, "water") then
        terrain_name = "sand-1"
    end
    return terrain_name
end

--Chunk generation code
local function on_chunk_generated(event)
    if (event.surface.name ~= "nauvis") then
        return
    end

    local surface = event.surface
    local lt = event.area.left_top
    local rb = event.area.right_bottom

    local w = rb.x - lt.x
    local h = rb.y - lt.y

    local tiles = {}
    for y = lt.y-1, rb.y do
        for x = lt.x-1, rb.x do
            table.insert(tiles, {name=get_world_tile_name(x, y), position={x,y}})
        end
    end
    surface.set_tiles(tiles)
    local positions = {event.position}
    surface.destroy_decoratives({area = event.area})
    surface.regenerate_decorative(nil, positions)
    surface.regenerate_entity(nil, positions)
end

script.on_event(defines.events.on_chunk_generated, on_chunk_generated)

