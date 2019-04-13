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
print(frames[1])

json_out = json.dumps(leap_data)

write_file(json_out)

print(LeapFrame(json_data=frames[1]))
