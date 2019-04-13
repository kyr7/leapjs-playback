import json

from python.LeapFrame import LeapFrame


def read_file(name='pinch-57fps.json'): return open(name, "r").read()


def read_json(data=read_file()): return json.loads(data)


def write_file(data, name='pinch-57fps-copy.json'):
    with open(name, 'w') as outfile:
        outfile.write(data)
        outfile.close()


leap_data = read_json()

# first frame
metadata = leap_data['metadata']
print(metadata)

frames = leap_data['frames']
# frame descriptor
print(frames[0])

# first frame
got_frame_str = str(frames[1])
print("got fr: " + got_frame_str)

json_out = json.dumps(leap_data)

write_file(json_out)

parsed_frame_str = str(LeapFrame(json_data=frames[1]))
parsed_frame_to_json_str = str(json.loads(parsed_frame_str))
print("parsed: " + parsed_frame_to_json_str)

print(got_frame_str == parsed_frame_to_json_str)
