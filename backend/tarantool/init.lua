fiber = require 'fiber'

MEMORY = 268435456 -- bytes
box.cfg{ listen = '127.0.0.1:3301', memtx_use_mvcc_engine = true, memtx_memory = MEMORY }

box.schema.user.grant('guest', 'super', nil, nil, {if_not_exists = true})
box.schema.user.grant('admin', 'super', nil, nil, {if_not_exists = true})

box.schema.create_space('workspace', {if_not_exists = true})
local space = box.space.workspace
space:create_index('primary', {type = 'TREE', unique = true, parts = {1, 'unsigned'}, if_not_exists = true})

function recreate_function(name, body)
    if box.schema.func.exists(name) then
        box.schema.func.drop(name)
    end
    box.schema.func.create(name, {body = body, if_not_exists = true})
end

recreate_function('insert_tuples', [[function(arr)
    box.begin() -- start of transaction
    local fiber = require('fiber')
    local workspace = box.space.workspace
    local counter = 0
    for _, tuple in ipairs(arr) do
        workspace:insert(tuple)
        counter = counter + 1
        if counter > 10000 then
            fiber.yield() -- yield fiber after 10000 iterations
            counter = 0
        end
    end
    box.commit() -- end of transaction
end]])

recreate_function('get_data', [[function() -- get_data function in tarantool space
    local workspace = box.space.workspace
    local has_data = workspace:len()
    if has_data == 0 then
        return 0
    else
        local data = workspace:select()
        return data
    end
end]])

recreate_function('remove_workspace', [[function()
    box.space.workspace:truncate()
end]])

recreate_function('multiply_data', [[function(num, col)
    local space = box.space.workspace
    tt_col = col + 2
    for _, tuple in space:pairs() do
        if tt_col <= #tuple and type(tuple[tt_col]) == "number" then
            local new_value = tuple[tt_col] * num
            local new_tuple = tuple:totable()
            new_tuple[tt_col] = new_value
            space:put(new_tuple)
        end
    end
end]])

recreate_function('select_optimal', [[function()
    local space = box.space.workspace
    local len = space:len()
    if len == 0 then
        return 0
    else
        if len <= 10 then
            return space:select()
        else
            local first_five = space:select({}, {limit = 5})
            local last_five = space:select({}, {limit = 5, offset = len - 5})
            return {first_five, last_five}
        end
    end
end]])

recreate_function('divide_data', [[function(num, col)
    local space = box.space.workspace
    tt_col = col + 2
    if num == 0 then
        return 'Division by zero'
    end
    for _, tuple in space:pairs() do
        if tt_col <= #tuple then
            local value = tuple[tt_col]
            if type(value) == "number" then
                local new_value = math.floor(value / num)
                local new_tuple = tuple:totable()
                new_tuple[tt_col] = new_value
                space:put(new_tuple)
            end
        end
    end
end]])

recreate_function('diff_data', [[function(num, col)
    local space = box.space.workspace
    tt_col = col + 2
    for _, tuple in space:pairs() do
        if tt_col <= #tuple then
            local value = tuple[tt_col]
            if type(value) == "number" then
                local new_value = value - num
                local new_tuple = tuple:totable()
                new_tuple[tt_col] = new_value
                space:put(new_tuple)
            end
        end
    end
end]])

recreate_function('sum_data', [[function(num, col)
    local space = box.space.workspace
    tt_col = col + 2
    for _, tuple in space:pairs() do
        if tt_col <= #tuple then
            local value = tuple[tt_col]
            if type(value) == "number" then
                local new_value = value + num
                local new_tuple = tuple:totable()
                new_tuple[tt_col] = new_value
                space:put(new_tuple)
            end
        end
    end
end]])

recreate_function('divide_mod_data', [[function(num, col)
    local space = box.space.workspace
    tt_col = col + 2

    if num == 0 then
        return 'Division by zero'
    end
    for _, tuple in space:pairs() do
        if tt_col <= #tuple then
            local value = tuple[tt_col]
            if type(value) == "number" then
                local new_value = value % num
                local new_tuple = tuple:totable()
                new_tuple[tt_col] = new_value
                space:put(new_tuple)
            end
        end
    end
end]])