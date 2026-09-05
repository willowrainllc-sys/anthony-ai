import os
import shutil

def get_size(start_path='.'):
    total_size = 0
    try:
        for dirpath, dirnames, filenames in os.walk(start_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                if not os.path.islink(fp):
                    total_size += os.path.getsize(fp)
    except Exception:
        pass
    return total_size

def clear_contents(path):
    cleared = 0
    if not os.path.exists(path):
        return 0
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        try:
            size = get_size(item_path) if os.path.isdir(item_path) else os.path.getsize(item_path)
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.unlink(item_path)
                cleared += size
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
                cleared += size
        except Exception as e:
            print(f"Failed to delete {item_path}: {e}")
    return cleared

def cleanup():
    summary = []
    total_cleared = 0

    # 1. C:\AnthonyAi_Swarm\Renderings
    path1 = r'C:\AnthonyAi_Swarm\Renderings'
    c1 = clear_contents(path1)
    summary.append(f"Renderings: {c1 / (1024*1024):.2f} MB")
    total_cleared += c1

    # 2. C:\Users\willo\AppData\Local\Temp
    path2 = r'C:\Users\willo\AppData\Local\Temp'
    c2 = clear_contents(path2)
    summary.append(f"Temp: {c2 / (1024*1024):.2f} MB")
    total_cleared += c2

    # 3. C:\AnthonyAi_Swarm\Logs (over 100MB)
    path3 = r'C:\AnthonyAi_Swarm\Logs'
    c3 = 0
    if os.path.exists(path3):
        for f in os.listdir(path3):
            fp = os.path.join(path3, f)
            try:
                if os.path.isfile(fp) and os.path.getsize(fp) > 100 * 1024 * 1024:
                    size = os.path.getsize(fp)
                    os.unlink(fp)
                    c3 += size
            except Exception:
                pass
    summary.append(f"Large Logs: {c3 / (1024*1024):.2f} MB")
    total_cleared += c3

    # 4. C:\Users\willo\huggingface_cache
    path4 = r'C:\Users\willo\huggingface_cache'
    c4 = 0
    if os.path.exists(path4):
        size4 = get_size(path4)
        if size4 > 2 * 1024 * 1024 * 1024: # Clear if > 2GB
            c4 = clear_contents(path4)
            summary.append(f"Huggingface Cache (Cleared {size4/(1024*1024):.2f} MB): {c4 / (1024*1024):.2f} MB")
        else:
            summary.append(f"Huggingface Cache: Not large enough ({size4/(1024*1024):.2f} MB)")
    else:
        summary.append("Huggingface Cache: Not found")
    total_cleared += c4

    print("\n".join(summary))
    print(f"Total Cleared: {total_cleared / (1024*1024):.2f} MB")

if __name__ == '__main__':
    cleanup()
