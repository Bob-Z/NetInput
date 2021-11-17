button = {}
for i, j in  ipairs(manager.machine.ioport.ports) do
 for field_name, field in pairs(j.fields) do
  print("")
  print(field_name)
  --print("  tag", field.port.tag)
  --print("  mask", field.mask)
  --print("  type", field.type)
  id = field.port.tag .. ',' .. field.mask .. ',' .. field.type
  print("id:", id)
  button[id] = field
 end
end

dest = os.getenv("NETINPUT_ADDR")
socket = emu.file("rc") -- rwc for read, write, create
socket:open("socket." .. dest)

is_read_key = true
is_read_finished = false
key = ""
value = ""
read = ""

command = {}

function process_frame()
		read = read .. socket:read(100)
		if #read ~= 0 then
            while true do
                i, j = string.find(read, "\n")
                if i == nil then
                    break
                end

                if is_read_key == true then
                    is_read_key = false
                    key = string.sub(read, 1, i-1)
                    read = string.sub(read, j+1,-1)
                else
                    is_read_finished = true
                    value = string.sub(read, 1, i-1)
                    read = string.sub(read, j+1,-1)
                end

                if is_read_finished == true then
                    command[key] = value
                    key=""
                    value=""
                    is_read_key = true
                    is_read_finished = false
                end
            end
        end

	for k,v in pairs(command) do
		button[k]:set_value(tonumber((v)))
	end
end

emu.register_frame_done(process_frame)
