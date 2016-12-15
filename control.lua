require "map_compressed"

--Settings
local offset = {x = 8300, y = 1760} --North Belgium

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

local function get_world_tile_name(x, y)
    local code = decompressed_map_data[y % height][x % width]
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
    for y = lt.y, rb.y do
        for x = lt.x, rb.x do
            table.insert(tiles, {name=get_world_tile_name(x + offset.x, y + offset.y), position={x,y}})
        end
    end
    surface.set_tiles(tiles)
end

script.on_event(defines.events.on_chunk_generated, on_chunk_generated)
