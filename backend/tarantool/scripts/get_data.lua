function() -- get_data function in tarantool space
    local workspace = box.space.workspace
    local has_data = workspace:len()
    if has_data == 0 then
        return 0
    else
        local data = workspace:select()
        return data
    end
end