function(arr)
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
end