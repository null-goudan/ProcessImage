import os
import glob
from PIL import Image
import shutil

def compress_and_convert_to_jpg(folder_path, output_folder=None, quality=85, prefix='image'):
    """
    压缩图片并转换为JPG格式，同时按顺序重命名
    
    参数:
    - folder_path: 原始图片文件夹路径
    - output_folder: 输出文件夹路径 (如果为None，则在原文件夹创建compressed_jpg子文件夹)
    - quality: 图片质量 (1-100, 推荐85)
    - prefix: 重命名前缀
    """
    
    # 支持的图片格式
    supported_formats = ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.tiff', '*.webp', '*.gif']
    
    # 获取所有图片文件
    image_files = []
    for format in supported_formats:
        image_files.extend(glob.glob(os.path.join(folder_path, format)))
        image_files.extend(glob.glob(os.path.join(folder_path, format.upper())))
    
    # 按文件名排序
    image_files.sort()
    
    if not image_files:
        print("在指定文件夹中未找到图片文件")
        return
    
    # 创建输出文件夹
    if output_folder is None:
        output_folder = os.path.join(folder_path, 'compressed_jpg')
    
    os.makedirs(output_folder, exist_ok=True)
    
    print(f"找到 {len(image_files)} 个图片文件")
    print(f"输出文件夹: {output_folder}")
    
    # 处理每个图片文件
    for i, image_path in enumerate(image_files, 1):
        try:
            # 打开图片
            with Image.open(image_path) as img:
                # 获取原始格式
                original_format = img.format
                
                # 转换为RGB模式（如果是RGBA等模式）
                if img.mode in ('RGBA', 'LA', 'P'):
                    # 创建白色背景
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                    img = background
                elif img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # 生成新文件名
                new_filename = f"{i}.jpg"
                output_path = os.path.join(output_folder, new_filename)
                
                # 保存为JPG格式
                img.save(output_path, 'JPEG', quality=quality, optimize=True, progressive=True)
                
                # 获取文件大小信息
                original_size = os.path.getsize(image_path)
                compressed_size = os.path.getsize(output_path)
                compression_ratio = (1 - compressed_size / original_size) * 100
                
                print(f"处理: {os.path.basename(image_path)} ({original_format}) -> {new_filename}")
                print(f"  大小: {original_size/1024:.1f}KB -> {compressed_size/1024:.1f}KB "
                      f"(压缩率: {compression_ratio:.1f}%)")
                
        except Exception as e:
            print(f"处理文件 {image_path} 时出错: {str(e)}")
    
    print(f"\n处理完成! 所有文件已转换为JPG并保存到: {output_folder}")

def compress_with_options(folder_path, output_folder=None, quality=85, 
                         target_format='JPEG', prefix='image'):
    """
    通用压缩函数，可选择输出格式
    
    参数:
    - folder_path: 原始图片文件夹路径
    - output_folder: 输出文件夹路径
    - quality: 图片质量 (1-100)
    - target_format: 目标格式 ('JPEG', 'PNG', 'WEBP')
    - prefix: 重命名前缀
    """
    
    # 支持的图片格式
    supported_formats = ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.tiff', '*.webp', '*.gif']
    
    # 获取所有图片文件
    image_files = []
    for format in supported_formats:
        image_files.extend(glob.glob(os.path.join(folder_path, format)))
        image_files.extend(glob.glob(os.path.join(folder_path, format.upper())))
    
    # 按文件名排序
    image_files.sort()
    
    if not image_files:
        print("在指定文件夹中未找到图片文件")
        return
    
    # 创建输出文件夹
    if output_folder is None:
        folder_name = 'compressed_jpg' if target_format == 'JPEG' else f'compressed_{target_format.lower()}'
        output_folder = os.path.join(folder_path, folder_name)
    
    os.makedirs(output_folder, exist_ok=True)
    
    print(f"找到 {len(image_files)} 个图片文件")
    print(f"输出格式: {target_format}")
    print(f"输出文件夹: {output_folder}")
    
    # 处理每个图片文件
    for i, image_path in enumerate(image_files, 1):
        try:
            # 打开图片
            with Image.open(image_path) as img:
                original_format = img.format
                
                # 转换为RGB模式（如果是RGBA等模式且目标格式为JPEG）
                if target_format == 'JPEG' and img.mode in ('RGBA', 'LA', 'P'):
                    # 创建白色背景
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                    img = background
                elif target_format == 'JPEG' and img.mode != 'RGB':
                    img = img.convert('RGB')
                elif target_format != 'JPEG' and img.mode == 'P':
                    img = img.convert('RGBA')
                
                # 生成新文件名
                if target_format == 'JPEG':
                    file_extension = '.jpg'
                else:
                    file_extension = f'.{target_format.lower()}'
                
                new_filename = f"{prefix}_{i:04d}{file_extension}"
                output_path = os.path.join(output_folder, new_filename)
                
                # 保存图片
                if target_format == 'JPEG':
                    img.save(output_path, target_format, quality=quality, optimize=True, progressive=True)
                elif target_format == 'PNG':
                    img.save(output_path, target_format, optimize=True)
                elif target_format == 'WEBP':
                    img.save(output_path, target_format, quality=quality, method=6)
                else:
                    img.save(output_path, target_format, quality=quality)
                
                # 获取文件大小信息
                original_size = os.path.getsize(image_path)
                compressed_size = os.path.getsize(output_path)
                compression_ratio = (1 - compressed_size / original_size) * 100
                
                print(f"处理: {os.path.basename(image_path)} ({original_format}) -> {new_filename}")
                print(f"  大小: {original_size/1024:.1f}KB -> {compressed_size/1024:.1f}KB "
                      f"(压缩率: {compression_ratio:.1f}%)")
                
        except Exception as e:
            print(f"处理文件 {image_path} 时出错: {str(e)}")
    
    print(f"\n处理完成! 所有文件已保存到: {output_folder}")

def get_folder_size(folder_path):
    """计算文件夹总大小"""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            total_size += os.path.getsize(filepath)
    return total_size

def main():
    # 用户输入文件夹路径
    folder_path = input("请输入图片文件夹路径: ").strip().strip('"')
    
    if not os.path.exists(folder_path):
        print("文件夹不存在!")
        return
    
    # 选择功能模式
    print("\n请选择功能模式:")
    print("1. 压缩并转换为JPG格式 (推荐)")
    print("2. 压缩并选择输出格式")
    
    mode_choice = input("请选择模式 (1-2, 默认1): ").strip()
    
    if mode_choice == "2":
        # 显示压缩选项
        print("\n压缩选项:")
        print("1. 高质量 (质量: 90, 文件较大)")
        print("2. 平衡 (质量: 85, 推荐)")
        print("3. 高压缩 (质量: 75, 文件较小)")
        print("4. 超高压缩 (质量: 50, 文件最小)")

        choice = input("请选择压缩级别 (1-4, 默认2): ").strip()
        quality_options = {'1': 90, '2': 85, '3': 75, '4': 50}
        quality = quality_options.get(choice, 85)
        
        # 格式选择
        print("\n输出格式:")
        print("1. JPEG (通用性好)")
        print("2. PNG (支持透明, 无损)")
        print("3. WEBP (现代格式, 压缩率高)")
        
        format_choice = input("请选择输出格式 (1-3, 默认1): ").strip()
        format_options = {'1': 'JPEG', '2': 'PNG', '3': 'WEBP'}
        target_format = format_options.get(format_choice, 'JPEG')
        
        # 前缀输入
        prefix = input("请输入文件前缀 (默认: image): ").strip()
        if not prefix:
            prefix = 'image'
        
        # 执行压缩和重命名
        original_size = get_folder_size(folder_path)
        compress_with_options(folder_path, output_folder="./result_1/", quality=quality, 
                             target_format=target_format, prefix=prefix)
        
        # 计算压缩效果
        folder_name = 'compressed_jpg' if target_format == 'JPEG' else f'compressed_{target_format.lower()}'
        compressed_folder = os.path.join(folder_path, folder_name)
        
    else:
        # 默认模式：压缩并转换为JPG
        print("\n压缩选项:")
        print("1. 高质量 (质量: 90, 文件较大)")
        print("2. 平衡 (质量: 85, 推荐)")
        print("3. 高压缩 (质量: 75, 文件较小)")
        print("4. 超高压缩 (质量: 50, 文件最小)")

        choice = input("请选择压缩级别 (1-4, 默认2): ").strip()
        quality_options = {'1': 90, '2': 85, '3': 75, '4': 50}
        quality = quality_options.get(choice, 85)
        
        # 前缀输入
        prefix = input("请输入文件前缀 (默认: image): ").strip()
        if not prefix:
            prefix = 'image'
        
        # 执行压缩和重命名
        original_size = get_folder_size(folder_path)
        compress_and_convert_to_jpg(folder_path, output_folder="./result_1/", quality=quality, prefix=prefix)

        # 计算压缩效果
        compressed_folder = os.path.join(folder_path, 'compressed_jpg')
    
    if os.path.exists(compressed_folder):
        compressed_size = get_folder_size(compressed_folder)
        total_compression_ratio = (1 - compressed_size / original_size) * 100
        print(f"\n总体压缩效果:")
        print(f"原始总大小: {original_size/1024/1024:.2f}MB")
        print(f"压缩后总大小: {compressed_size/1024/1024:.2f}MB")
        print(f"总体压缩率: {total_compression_ratio:.1f}%")

if __name__ == "__main__":
    main()