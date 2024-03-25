import matplotlib.pyplot as plt
import pandas as pd

def size_to_bytes(size_str):
    units = {"B": 1, "K": 1024, "M": 1024**2, "G": 1024**3, "T": 1024**4}
    if size_str == '0':
        return 0
    try:
        number, unit = size_str[:-1].replace(',', '.'), size_str[-1]
        return int(float(number) * units.get(unit.upper(), 0))
    except ValueError:
        return None

def process_file_data(file_path):
    file_sizes = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.split()
            if len(parts) >= 2:
                size_str = parts[0]
                bytes_size = size_to_bytes(size_str)
                if bytes_size is not None:
                    file_sizes.append(bytes_size)
    return file_sizes

file_path = 'D:\\Downloads\\result.txt'

sizes = process_file_data(file_path)

if sizes:
    df_sizes = pd.DataFrame(sizes, columns=['File Size'])

    plt.figure(figsize=(10, 6))
    density, bins, _ = plt.hist(df_sizes['File Size'], bins=30, density=True, alpha=0.5)
    plt.close()
    plt.figure(figsize=(10, 6))
    plt.plot(bins[1:], density, drawstyle='steps')
    plt.title('Графік щільності розмірів файлів')
    plt.xlabel('Розмір файлу (байти)')
    plt.ylabel('Щільність')
    plt.grid(True)
    plt.show()

    bins = [0, 10, 100, 1000, 10000, 100000, 1000000, 10000000, float('inf')]
    labels = ['<10B', '10-100B', '100B-1KB', '1-10KB', '10-100KB', '100KB-1MB', '1-10MB', '>10MB']
    df_sizes['Category'] = pd.cut(df_sizes['File Size'], bins=bins, labels=labels, right=False)
    category_counts = df_sizes['Category'].value_counts(sort=False)
    plt.figure(figsize=(10, 8))
    pie = plt.pie(category_counts, startangle=140, autopct='%1.1f%%', pctdistance=0.85)
    plt.title('File Size Distribution')
    plt.legend(pie[0], labels, title="File Size", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
    plt.setp(pie[2], size=8, weight="bold", color="white")
    plt.show()

else:
    print("No valid file sizes to display.")
