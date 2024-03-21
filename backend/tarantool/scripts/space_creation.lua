function create_space()
    box.schema.create_space('workspace', {if_not_exists = true})
    local space = box.space.workspace
    space:create_index('primary', {type = 'TREE', unique = true, parts = {1, 'unsigned'}, if_not_exists = true})
end

create_space()