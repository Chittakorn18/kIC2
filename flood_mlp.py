# ฟังก์ชันอ่านไฟล์ข้อมูล
def load_data(filename):
    data = []
    with open(filename, 'r') as f:
        for line in f:
            # ข้ามบรรทัดที่เป็นหัวตารางหรือว่าง
            if line.strip() == '' or line.startswith('station') or line.startswith('t-3'):
                continue
            parts = line.strip().split()
            if len(parts) != 9:
                continue
            values = list(map(float, parts))
            data.append(values)
    return data

# ฟังก์ชัน normalize ข้อมูลให้อยู่ในช่วง 0-1
def normalize(data):
    inputs = [row[:-1] for row in data]
    outputs = [row[-1] for row in data]

    input_mins = [min(col) for col in zip(*inputs)]
    input_maxs = [max(col) for col in zip(*inputs)]

    out_min = min(outputs)
    out_max = max(outputs)

    inputs_norm = []
    for row in inputs:
        norm_row = []
        for i, val in enumerate(row):
            denom = input_maxs[i] - input_mins[i]
            if denom == 0:
                norm_row.append(0)
            else:
                norm_row.append((val - input_mins[i]) / denom)
        inputs_norm.append(norm_row)

    outputs_norm = []
    denom_out = out_max - out_min
    for val in outputs:
        if denom_out == 0:
            outputs_norm.append(0)
        else:
            outputs_norm.append((val - out_min) / denom_out)

    dataset = [(inputs_norm[i], [outputs_norm[i]]) for i in range(len(data))]
    return dataset, input_mins, input_maxs, out_min, out_max

# เริ่มอ่านไฟล์และ normalize
data_raw = load_data('Flood_dataset.txt')
dataset_norm, input_mins, input_maxs, out_min, out_max = normalize(data_raw)

# ทดสอบแสดงข้อมูล normalize แถวแรกดู
print('ข้อมูล normalize แถวแรก:', dataset_norm[0])
