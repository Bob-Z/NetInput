button = {}
for i, j in  ipairs(manager.machine.ioport.ports) do
 for field_name, field in pairs(j.fields) do
  print(field_name)
  button[field_name] = field
 end
end


socket = emu.file("rc") -- rwc for read, write, create
socket:open("socket.127.0.0.1:1234")

is_read_key = true
is_read_finished = false
key = ""
value = ""

function process_frame()
	repeat
		local read = socket:read(1)
		if #read ~= 0 then
			if read == '\n' then
				if is_read_key == true then
					print("full key", key)
					is_read_key = false
				else
					print("full value", value)
					is_read_finished = true
				end
			else
				if is_read_key == true then
					key = key .. read
					print("key", key)
				else
					value = value .. read
					print("value", value)
				end
			end

			if is_read_finished == true then
					print("full key", key)
					print("full value", value)
				button[key]:set_value(tonumber((value)))
				key=""
				value=""
				is_read_key = true
				is_read_finished = false
socket = emu.file("rc") -- rwc for read, write, create
socket:open("socket.127.0.0.1:1234")
			end
		end

	until #read == 0

end

emu.register_frame_done(process_frame)

