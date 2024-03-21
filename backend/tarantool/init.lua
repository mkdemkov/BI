fiber = require 'fiber'

box.cfg{ listen = '127.0.0.1:3301', memtx_use_mvcc_engine = true }

box.schema.user.grant('guest', 'super', nil, nil, {if_not_exists = true})
box.schema.user.grant('admin', 'super', nil, nil, {if_not_exists = true})

box.schema.create_space('workspace', {if_not_exists = true})
local space = box.space.workspace
space:create_index('primary', {type = 'TREE', unique = true, parts = {1, 'unsigned'}, if_not_exists = true})

box.schema.func.create('insert_tuples', {body = [[function(arr)
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
end]], if_not_exists = true})

box.schema.func.create('get_data', {body = [[function() -- get_data function in tarantool space
    local workspace = box.space.workspace
    local has_data = workspace:len()
    if has_data == 0 then
        return 0
    else
        local data = workspace:select()
        return data
    end
end]], if_not_exists = true})

box.schema.func.create('remove_workspace', {body = [[function()
    box.space.workspace:truncate()
end]], if_not_exists = true})
