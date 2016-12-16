require "World2"

--Choose your scale here!
local scale = 6

--Select your spawnpoint here (don't forget to take scale into account)
local spawn = {x = 2064 * scale, y = 406 * scale} -- 2064, 406 = Flanders

--For those wanting to play on a very large scale:
--You might notice that the map gets a little blocky
--I tried to limit this as much as possible, but there's only so much data
--So if you want a bit more detail, I included data for a more detailed map
--To use it do:
--  1) Change the 'require' line to require "World2_large"
--  2) Set your scale (note that the same scale for the large map results in double the size)
--  3) Fix the spawn, something like 'spawn = {x = 2068 * 2 * scale, y = 404 * 2 * scale}' (notice the '* 2')
--This will make the loading at the start of the game slower, and use some more ram,
--  but the generating should be equally fast.



----
--Don't touch anything under this, unless you know what you're doing
----
--Terrain codes should be in sync with the ConvertMap code
local terrain_codes = {
    ["_"] = "out-of-map",
    ["o"] = "deepwater",--ocean
    ["O"] = "deepwater-green",
    ["w"] = "water",
    ["W"] = "water-green",
    ["g"] = "grass",
    ["m"] = "grass-medium",
    ["G"] = "grass-dry",
    ["d"] = "dirt",
    ["D"] = "dirt-dark",
    ["s"] = "sand",
    ["S"] = "sand-dark"
}

local function decompress_map_data()
    print("Decompressing, this can take a while...")
    local decompressed = {}
    local height = #map_data
    local width = nil
    local last = -1
    for y = 0, height-1 do
        decompressed[y] = {}
        --debug info
        work = math.floor(y * 100 / height)
        if work ~= last then --so it doesn't print the same percent over and over.
            print("... ", work, "%")
        end
        last = work
        --do decompression of this line
        local total_count = 0
        local line = map_data[y+1]
        for letter, count in string.gmatch(line, "(%a+)(%d+)") do
            for x = total_count, total_count + count do
                decompressed[y][x] = letter
            end
            total_count = total_count + count
        end
        --check width (all lines must the equal in length)
        if width == nil then
            width = total_count
        elseif width ~= total_count then
            error()
        end
    end
    print("Finished decompressing")
    return decompressed, width, height
end

decompressed_map_data, width, height = decompress_map_data();

local function add_to_total(totals, weight, code)
    if totals[code] == nil then
        totals[code] = {code=code, weight=weight}
    else
        totals[code].weight = totals[code].weight + weight
    end
end

local function get_world_tile_name(x, y)
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
    local c_top_left = decompressed_map_data[top % height][left % width]
    local c_top_right = decompressed_map_data[top % height][right % width]
    local c_bottom_left = decompressed_map_data[bottom % height][left % width]
    local c_bottom_right = decompressed_map_data[bottom % height][right % width]
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
    return terrain_codes[code]
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
            table.insert(tiles, {name=get_world_tile_name(x + spawn.x, y + spawn.y), position={x,y}})
        end
    end
    surface.set_tiles(tiles)
end

script.on_event(defines.events.on_chunk_generated, on_chunk_generated)
