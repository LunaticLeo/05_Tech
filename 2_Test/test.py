def decode(message_file):
    with open(message_file, 'r') as file:
        lines = file.readlines()

    data = []

    for line in lines:
        parts = line.split(' ')
        data.append((int(parts[0]),parts[1]))
    
    data.sort()

    step = 1
    sum = 0
    output = ""
    while sum< len(data):
        output += str(data[sum + step - 1][0]) + ': ' + data[sum + step - 1][1]
        sum += step
        step +=1

    return output

file_path = './test.txt'
output = decode(file_path)
print(output)