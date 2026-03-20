# ZipCloak - zip文件混淆工具

Copyright ownership: coralhymn | 琴海奶油

Open-source protocol: GPL-2.0

Function: Perform obfuscation processing on specified file types, making a specific file recognized by the system as a folder

# Usage instructions:

## [混淆模式] (Obfuscation Mode)

1. In the 【混淆】 tab, select the source folder, output zip file location, and set the name  
2. Select the file extensions to be obfuscated  
3. Click "开始混淆" (Start Obfuscation) to generate the encrypted ZIP file  

## [恢复模式] (Recovery Mode)

1. In the 【恢复】 tab, select the obfuscated ZIP file  
2. Set the output directory and click "开始恢复" (Start Recovery) (do not select the root directory, it is recommended to create a subdirectory)  

## [配置文件] (Configuration File)

A configuration file zipcloak_config.json will be automatically generated in the software root directory upon first run. Do not delete this file. It saves your configuration information and will automatically read it next time you run.  
The file extensions added in [混淆模式] will be saved in this configuration file. To delete added extensions, simply delete this file (or modify the JSON file).  

---

This project is based on modifications to my personal project https://github.com/CoralHymn/RWMP2_Decryptor

If you need to decrypt files encrypted by [RWMP2], please do not use this tool. Use the dedicated version above!!  

Precautions:  
Do not use this tool to obfuscate important files. The developer is not responsible for any losses incurred.  
No in-depth testing has been conducted. Please back up important files before use to prevent data loss.
