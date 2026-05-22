#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
EXAMPLES - Ví dụ sử dụng Minecraft Resource Pack Converter

File này chứa các ví dụ cách sử dụng script converter.
"""

# ═══════════════════════════════════════════════════════════════════════════
# VÍ DỤ 1: SỬ DỤNG CƠ BẢN (BASIC USAGE)
# ═══════════════════════════════════════════════════════════════════════════

def example_basic():
    """
    Ví dụ đơn giản nhất: Import và gọi hàm main.
    """
    from minecraft_resourcepack_converter import main
    
    # Chuyển đổi resource pack
    success = main(
        java_pack_path="/Users/username/Downloads/MyAwesomePack",
        output_base_path="./bedrock_packs",
        pack_name="my_awesome_bedrock_pack"
    )
    
    if success:
        print("\n✅ Chuyển đổi thành công!")
        print("📁 Kết quả: ./bedrock_packs/my_awesome_bedrock_pack/")
    else:
        print("\n❌ Chuyển đổi thất bại!")


# ═══════════════════════════════════════════════════════════════════════════
# VÍ DỤ 2: SỬ DỤNG VỚI ĐƯỜNG DẪN TUYỆT ĐỐI (ABSOLUTE PATHS)
# ═══════════════════════════════════════════════════════════════════════════

def example_absolute_paths():
    """
    Ví dụ dùng đường dẫn tuyệt đối (absolute paths).
    Hữu ích khi script nằm ở vị trí khác với resource pack.
    """
    from minecraft_resourcepack_converter import main
    import os
    
    # Windows
    if os.name == 'nt':  # Windows
        java_pack = r"C:\Users\YourName\Downloads\MyPack"
        output = r"D:\Minecraft\BedrockPacks"
    
    # macOS / Linux
    else:
        java_pack = "/Users/username/Downloads/MyPack"
        output = "/home/username/minecraft/bedrock_packs"
    
    main(
        java_pack_path=java_pack,
        output_base_path=output,
        pack_name="converted_pack"
    )


# ═══════════════════════════════════════════════════════════════════════════
# VÍ DỤ 3: BATCH CONVERSION - CHUYỂN ĐỔI NHIỀU PACK CÙNG LÚC
# ═══════════════════════════════════════════════════════════════════════════

def example_batch_conversion():
    """
    Ví dụ chuyển đổi nhiều Java Resource Pack cùng lúc.
    Hữu ích nếu bạn có collection nhiều packs.
    """
    from minecraft_resourcepack_converter import main
    from pathlib import Path
    import os
    
    # Thư mục chứa tất cả Java packs
    packs_folder = Path("./java_packs")
    output_folder = Path("./bedrock_packs")
    
    # Tạo output folder nếu chưa tồn tại
    output_folder.mkdir(parents=True, exist_ok=True)
    
    # Duyệt tất cả subfolder
    for pack_dir in packs_folder.iterdir():
        if pack_dir.is_dir() and (pack_dir / "assets").exists():
            print(f"\n{'='*70}")
            print(f"Đang chuyển đổi: {pack_dir.name}")
            print(f"{'='*70}")
            
            try:
                success = main(
                    java_pack_path=str(pack_dir),
                    output_base_path=str(output_folder),
                    pack_name=pack_dir.name.replace(" ", "_")
                )
                
                if success:
                    print(f"✅ {pack_dir.name} - Thành công")
                else:
                    print(f"❌ {pack_dir.name} - Thất bại")
                    
            except Exception as e:
                print(f"❌ {pack_dir.name} - Lỗi: {e}")
    
    print(f"\n{'='*70}")
    print(f"✅ Batch conversion hoàn thành!")
    print(f"📁 Kết quả: {output_folder}")
    print(f"{'='*70}")


# ═══════════════════════════════════════════════════════════════════════════
# VÍ DỤ 4: ADVANCED - TỰ ĐỘNG DEPLOY SANG GEYSERMC SERVER
# ═══════════════════════════════════════════════════════════════════════════

def example_auto_deploy():
    """
    Ví dụ nâng cao: Chuyển đổi THEN tự động copy sang Geyser server.
    """
    from minecraft_resourcepack_converter import main
    import shutil
    from pathlib import Path
    import subprocess
    
    # Cấu hình
    java_pack = "./my_java_pack"
    bedrock_output = "./bedrock_packs"
    pack_name = "my_custom_pack"
    
    # Đường dẫn GeyserMC server
    geyser_packs_dir = "/home/minecraft/server/plugins/Geyser-Spigot/packs"
    
    print("📦 Step 1: Chuyển đổi resource pack...")
    success = main(java_pack, bedrock_output, pack_name)
    
    if not success:
        print("❌ Chuyển đổi thất bại!")
        return
    
    # Copy sang server
    source_pack = Path(bedrock_output) / pack_name
    dest_pack = Path(geyser_packs_dir) / pack_name
    
    print(f"\n📂 Step 2: Copy sang server...")
    try:
        if dest_pack.exists():
            shutil.rmtree(dest_pack)
        shutil.copytree(source_pack, dest_pack)
        print(f"✅ Copy thành công: {dest_pack}")
    except Exception as e:
        print(f"❌ Copy thất bại: {e}")
        return
    
    # Reload GeyserMC
    print(f"\n🔄 Step 3: Reload GeyserMC...")
    try:
        # Nếu dùng Spigot/Bukkit, sử dụng RCON
        # subprocess.run(["rcon-cli", "-c", "geyser reload"], check=True)
        
        # Hoặc copy file reload trigger
        reload_file = Path(geyser_packs_dir) / ".reload"
        reload_file.touch()
        
        print("✅ GeyserMC reload command sent")
    except Exception as e:
        print(f"⚠️  Auto-reload thất bại (manual reload cần thiết): {e}")
    
    print("\n✅ Tất cả xong!")
    print(f"📁 Resource pack: {dest_pack}")
    print("💡 Hãy test bằng cách connect Bedrock client tới server")


# ═══════════════════════════════════════════════════════════════════════════
# VÍ DỤ 5: CUSTOM PROCESSING - XỬ LÝ SAU KHI CHUYỂN ĐỔI
# ═══════════════════════════════════════════════════════════════════════════

def example_custom_processing():
    """
    Ví dụ advanced: Chuyển đổi, rồi xử lý tùy chỉnh file output.
    """
    from minecraft_resourcepack_converter import main
    from pathlib import Path
    import json
    import zipfile
    
    pack_name = "my_pack"
    output_base = "./bedrock_packs"
    
    # 1. Chuyển đổi
    print("Step 1: Convert...")
    main("./java_pack", output_base, pack_name)
    
    pack_root = Path(output_base) / pack_name
    
    # 2. Modify manifest (thêm metadata custom)
    print("\nStep 2: Modify manifest...")
    manifest_file = pack_root / "manifest.json"
    
    with open(manifest_file, 'r') as f:
        manifest = json.load(f)
    
    # Thêm metadata custom
    manifest["header"]["metadata"] = {
        "author": "MyName",
        "custom_field": "custom_value"
    }
    
    with open(manifest_file, 'w') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    
    print("✅ Manifest modified")
    
    # 3. Optimize images (nếu có Pillow)
    print("\nStep 3: Optimize images...")
    try:
        from PIL import Image
        
        textures_dir = pack_root / "textures"
        for png_file in textures_dir.rglob("*.png"):
            img = Image.open(png_file)
            # Optimize (reduce color depth nếu cần)
            img.save(png_file, optimize=True, quality=95)
        
        print(f"✅ Images optimized")
    except ImportError:
        print("⚠️  Pillow not available - skipping optimization")
    
    # 4. Create ZIP package
    print("\nStep 4: Create package...")
    zip_path = Path(output_base) / f"{pack_name}.mcpack"
    
    with zipfile.ZipFile(zip_path, 'w') as zf:
        for file in pack_root.rglob("*"):
            if file.is_file():
                arcname = file.relative_to(pack_root)
                zf.write(file, arcname)
    
    print(f"✅ Package created: {zip_path}")
    print(f"   Kích thước: {zip_path.stat().st_size / (1024*1024):.2f} MB")
    
    # 5. Generate summary
    print("\nStep 5: Generate summary...")
    summary = f"""
=== RESOURCE PACK CONVERSION SUMMARY ===
Name: {pack_name}
Location: {pack_root}
Package: {zip_path}

Files:
  - Total: {len(list(pack_root.rglob('*')))}
  - Textures: {len(list((pack_root / 'textures').rglob('*')))}
  - Sounds: {len(list((pack_root / 'sounds').rglob('*')))}
  - Attachables: {len(list((pack_root / 'attachables').glob('*.json')))}

Ready to distribute!
====================================
    """
    
    print(summary)
    
    summary_file = pack_root / "SUMMARY.txt"
    with open(summary_file, 'w') as f:
        f.write(summary)


# ═══════════════════════════════════════════════════════════════════════════
# VÍ DỤ 6: ERROR HANDLING - XỬ LÝ LỖI
# ═══════════════════════════════════════════════════════════════════════════

def example_error_handling():
    """
    Ví dụ xử lý lỗi gracefully.
    """
    from minecraft_resourcepack_converter import main
    from pathlib import Path
    
    java_pack = "./java_pack_that_might_not_exist"
    
    try:
        # Kiểm tra trước
        if not Path(java_pack).exists():
            raise FileNotFoundError(f"Java pack không tồn tại: {java_pack}")
        
        if not (Path(java_pack) / "assets").exists():
            raise ValueError(f"Không phải Java Resource Pack hợp lệ: {java_pack}")
        
        # Chuyển đổi
        success = main(java_pack, "./bedrock_packs", "converted")
        
        if success:
            print("✅ Thành công")
        else:
            print("❌ Thất bại (xem log trên)")
    
    except FileNotFoundError as e:
        print(f"❌ File không tìm thấy: {e}")
    except ValueError as e:
        print(f"❌ Invalid format: {e}")
    except Exception as e:
        print(f"❌ Lỗi không mong đợi: {e}")
        import traceback
        traceback.print_exc()


# ═══════════════════════════════════════════════════════════════════════════
# VÍ DỤ 7: MONITORING & LOGGING
# ═══════════════════════════════════════════════════════════════════════════

def example_monitoring():
    """
    Ví dụ thêm monitoring và logging tuỳ chỉnh.
    """
    from minecraft_resourcepack_converter import main
    import sys
    import logging
    from pathlib import Path
    
    # Setup logging
    log_file = Path("converter.log")
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    logger = logging.getLogger(__name__)
    
    logger.info("=== Bắt đầu chuyển đổi ===")
    logger.info(f"Java pack: ./java_pack")
    logger.info(f"Output: ./bedrock_packs")
    
    try:
        success = main("./java_pack", "./bedrock_packs", "converted")
        
        if success:
            logger.info("✅ Chuyển đổi thành công")
        else:
            logger.error("❌ Chuyển đổi thất bại")
    
    except Exception as e:
        logger.exception(f"Lỗi: {e}")
    
    logger.info("=== Hoàn thành ===")
    logger.info(f"Log file: {log_file}")


# ═══════════════════════════════════════════════════════════════════════════
# VÍ DỤ 8: SCHEDULER - CHUYỂN ĐỔI THEO LỊCH ĐỊNH KỲ
# ═══════════════════════════════════════════════════════════════════════════

def example_scheduled_conversion():
    """
    Ví dụ chuyển đổi theo lịch định kỳ (hàng ngày, hàng tuần...).
    Hữu ích cho monitoring thay đổi resource pack.
    """
    from minecraft_resourcepack_converter import main
    from pathlib import Path
    import schedule
    import time
    
    java_pack = "./java_pack"
    output = "./bedrock_packs_scheduled"
    
    def convert_job():
        print(f"\n⏰ Scheduled conversion started at {time.strftime('%Y-%m-%d %H:%M:%S')}")
        success = main(java_pack, output, "scheduled_pack")
        if success:
            print("✅ Conversion completed")
        else:
            print("❌ Conversion failed")
    
    # Schedule jobs
    schedule.every().day.at("02:00").do(convert_job)        # Hàng ngày lúc 2:00 AM
    schedule.every().monday.at("10:00").do(convert_job)     # Hàng tuần lúc 10:00 AM
    
    print("⏲️  Scheduler started. Waiting for scheduled times...")
    
    # Run scheduler (chạy trong background)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(60)


# ═══════════════════════════════════════════════════════════════════════════
# MAIN - CHỌN EXAMPLE ĐỂ CHẠY
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import sys
    
    print("""
╔════════════════════════════════════════════════════════════════════════════╗
║    MINECRAFT RESOURCE PACK CONVERTER - EXAMPLES                            ║
╚════════════════════════════════════════════════════════════════════════════╝

Chọn ví dụ để chạy:

1. Basic usage (Sử dụng cơ bản)
2. Absolute paths (Đường dẫn tuyệt đối)
3. Batch conversion (Chuyển đổi nhiều pack)
4. Auto deploy (Tự động deploy to Geyser)
5. Custom processing (Xử lý tùy chỉnh)
6. Error handling (Xử lý lỗi)
7. Monitoring (Ghi log)
8. Scheduled conversion (Chuyển đổi định kỳ)

Nhập số (1-8) hoặc 'exit' để thoát:
    """)
    
    examples = {
        "1": ("Basic usage", example_basic),
        "2": ("Absolute paths", example_absolute_paths),
        "3": ("Batch conversion", example_batch_conversion),
        "4": ("Auto deploy", example_auto_deploy),
        "5": ("Custom processing", example_custom_processing),
        "6": ("Error handling", example_error_handling),
        "7": ("Monitoring", example_monitoring),
        "8": ("Scheduled conversion", example_scheduled_conversion),
    }
    
    while True:
        choice = input("\nChọn: ").strip()
        
        if choice.lower() == 'exit':
            print("Tạm biệt!")
            break
        
        if choice in examples:
            title, func = examples[choice]
            print(f"\n{'='*70}")
            print(f"Running: {title}")
            print(f"{'='*70}\n")
            
            try:
                func()
            except Exception as e:
                print(f"\n❌ Lỗi: {e}")
                import traceback
                traceback.print_exc()
            
            print(f"\n{'='*70}\n")
        else:
            print("❌ Lựa chọn không hợp lệ. Thử lại.")
