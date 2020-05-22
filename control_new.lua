require "map_compressed---8"

local scale = settings.global["map-gen-scale"].value
local spawn = {
    x = scale * settings.global["spawn-x"].value * width,
    y = scale * settings.global["spawn-y"].value * height
}

-- script.on_event(defines.events.on_runtime_mod_setting_changed, function(event)
--     if not event then return end
--     --Should prevent user from changing the settings, but will still get through if he changes it and restarts factorio :(
--     if event.setting == "map-gen-scale" then settings.global["map-gen-scale"].value = scale end
--     if event.setting == "spawn-x" then settings.global["spawn-x"].value = spawn.x end
--     if event.setting == "spawn-y" then settings.global["spawn-y"].value = spawn.y end

--     game.print("You shouldn't change the world-gen settings after you started a savegame. This will break the generating for new parts of the map.")
--     game.print("I haven't found a good way to prevent you changing them yet, so for new they are just ignored, but will take effect when restarting.")
--     game.print("Reset them to what they were, or risk fucking up your save!")
--     game.print("Your settings were: ")
--     game.print("Scale = " .. scale)
--     game.print("spawn: x = " .. spawn.x .. ", y = " .. spawn.y)
-- end)

----
--Don't touch anything under this, unless you know what you're doing
----
--Terrain codes should be in sync with the ConvertMap code

local function get_world_tile_name(x, y)
    if x > -5 and x < 5 and y > -5 and y < 5 then
        return "sand-1"
    end

    --spawn
    x = x + spawn.x
    y = y + spawn.y

    --scaling
    x = x / scale
    y = y / scale
    --normalizing
    x = math.floor(x) % width
    y = math.floor(y) % height
    --find chunk
    local chunk_size = chunk_sizes[1]
    local chunk_x = math.floor(x / chunk_size)
    local chunk_y = math.floor(y / chunk_size)
    --get chunk
    local chunk_x_count = width / chunk_size
    local chunk = data[1 + chunk_x + chunk_y * chunk_x_count]
    --game.print("chunk " .. chunk)

    --if chunk is just a single number, then use that
    if chunk == 0 then
        return "water"
    elseif chunk == 1 then
        return "sand-1"
    end

    --if not, it's a mixed chunk, so check deeper
    --move x to inside the chunk
    x = x - chunk_x * chunk_size
    y = y - chunk_y * chunk_size
    game.print("in chunk " .. x .. ", " .. y)
    --figure out the kind of tile
    local kind = chunk[x + y * chunk_size]
    if kind == 0 then
        return "water"
    else
        return "sand-1"
    end
end

local function on_chunk_generated(event)
    local surface = event.surface
    local lt = event.area.left_top
    local rb = event.area.right_bottom

    local w = rb.x - lt.x
    local h = rb.y - lt.y
    print("Chunk generated: ", lt.x, lt.y, w, h)

    local tiles = {}
    for y = lt.y-1, rb.y do
        for x = lt.x-1, rb.x do
            table.insert(tiles, {name=get_world_tile_name(x, y), position={x,y}})
        end
    end
    surface.set_tiles(tiles)
end

script.on_event(defines.events.on_chunk_generated, on_chunk_generated)
