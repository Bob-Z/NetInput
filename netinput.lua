button = {}
for i, j in  ipairs(manager.machine.ioport.ports) do
 for field_name, field in pairs(j.fields) do
  print(field_name)
  button[field_name] = field
 end
end

dest = os.getenv("NETINPUT_ADDR")
socket = emu.file("rc") -- rwc for read, write, create
socket:open("socket." .. dest)

is_read_key = true
is_read_finished = false
key = ""
value = ""

command = {}

function process_frame()
	--repeat
		local read = socket:read(100)
		while #read ~= 0 do
			print("read")
			char = read:sub(1, 1)
			if char == '\n' then
				if is_read_key == true then
					print("full key", key)
					is_read_key = false
				else
					print("full value", value)
					is_read_finished = true
				end
			else
				if is_read_key == true then
					key = key .. char
					--print("key", key)
				else
					value = value .. char
					--print("value", value)
				end
			end

			if is_read_finished == true then
				print("full key", key)
				print("full value", value)
				command[key] = value
				key=""
				value=""
				is_read_key = true
				is_read_finished = false
--socket = emu.file("rc") -- rwc for read, write, create
--socket:open("socket.127.0.0.1:1234")
			end

			read = read:sub(2)
		end

	--until #read == 0

	for k,v in pairs(command) do
		--print("** push", k, v)
		button[k]:set_value(tonumber((v)))
	end
end

emu.register_frame_done(process_frame)

