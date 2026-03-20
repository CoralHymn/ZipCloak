# ZipCloak - ZIP File Obfuscation Tool

Copyright: coralhymn | 琴海奶油

Open-source License: GPL-2.0

<div align="center">

### [🇺🇸 English](README-EN.md) | [🇨🇳 简体中文](README.md)

</div>

**Function**: Perform obfuscation processing on specified file types, making specific files recognized by the system as folders

---

# Usage Instructions:

## [Obfuscation Mode]

1. In the **Obfuscate** tab, select the source folder, output ZIP file location, and set the name
2. Select the file extensions to be obfuscated
3. Click **Start Obfuscation** to generate the obfuscated ZIP file

## [Restore Mode]

1. In the **Restore** tab, select the obfuscated ZIP file
2. Set the output directory and click **Start Restore** (do not select the root directory; it is recommended to create a subdirectory)

## [Configuration File]

Upon first run, a configuration file `zipcloak_config.json` will be automatically generated in the software root directory. **Do not delete this file** as it saves your configuration information and will be automatically read on subsequent runs.

The file extensions you add in **Obfuscation Mode** will be saved in the configuration file. If you need to delete the added file extensions, simply delete this file (or modify the JSON file directly).

---

# Multilingual Support

ZipCloak now supports multiple languages, with Chinese (zh) and English (en) provided by default.

## How to Switch Language

In the top toolbar of the application interface, you will see a language selection dropdown (🌐 Language / 语言). Click and select your desired language.

**Note:** You need to restart the application for the language switch to take full effect.

## How to Add New Language Packs

If you want to add support for another language, follow these steps:

### 1. Create a Language File

Create a new JSON file in the `lang` directory, named `{language-code}.json`.

For example, to add Japanese support, create the file `lang/jp.json`.

### 2. Copy Existing Language Pack Content

Copy the content from `zh.json` or `en.json` to your new file as a template.

### 3. Translate All Text

Translate the values in the JSON file to your target language. Make sure to keep the key names unchanged.

Example structure:

```json
{
  "app_title": "Your Language - App Title",
  "tab_obfuscate": "🔒 Obfuscate Mode",
  "tab_restore": "🔓 Restore Mode",
  ...
}
```

### 4. Test

Restart the application, and you should see your newly added language option in the language selection dropdown.

## Available Language Keys

Here is a list of all translatable keys and their descriptions:

- `app_title`: Application window title
- `tab_obfuscate`: Obfuscation mode tab title
- `tab_restore`: Restore mode tab title
- `tab_about`: About tab title
- `tab_license`: LICENSE tab title
- `status_ready`: Status bar ready text
- `status_obfuscating`: Status when obfuscating
- `status_restoring`: Status when restoring
- `status_obfuscate_done`: Obfuscation complete status
- `status_restore_done`: Restore complete status
- `status_obfuscate_fail`: Obfuscation failed status
- `status_restore_fail`: Restore failed status
- `label_source`: Source folder label
- `label_output_zip`: Output ZIP label
- `label_obf_suffix`: Obfuscation suffix label
- `label_compress`: Enable compression checkbox
- `label_input_zip`: Input ZIP label
- `label_output_dir`: Output directory label
- `label_restore_suffix`: Restore suffix label
- `label_custom`: Custom label
- `label_log`: Run log label
- `btn_browse`: Browse button
- `btn_save_as`: Save As button
- `btn_select`: Select button
- `btn_add`: Add button
- `btn_select_all`: Select All button
- `btn_clear`: Clear button
- `btn_start_obfuscate`: Start Obfuscation button
- `btn_start_restore`: Start Restore button
- `msg_param_missing`: Parameter missing message title
- `msg_fill_path`: Fill path prompt
- `msg_fill_input_output`: Fill input/output prompt
- `msg_no_suffix_title`: Confirmation dialog title
- `msg_no_suffix_obf`: No obfuscation suffix selected prompt
- `msg_no_suffix_rst`: No restore suffix selected prompt
- `msg_success`: Success message title
- `msg_obf_done`: Obfuscation complete message
- `msg_restore_done`: Restore complete message
- `msg_error`: Error message title
- `msg_obf_fail`: Obfuscation failed message
- `msg_restore_fail`: Restore failed message
- `log_add_suffix`: Add custom suffix log
- `log_error`: Error log
- `about_text`: About text
- `about_detail`: About detail text

## Contribute Your Language Pack

If you create a new language pack, feel free to submit it to the main repository via Pull Request, allowing more users to use their native language!

---

This project is based on modifications to my personal project: https://github.com/CoralHymn/RWMP2_Decryptor

**If you need to decrypt files encrypted by [RWMP2], please do not use this tool. Use the dedicated version above!**

---

# Important Notes

⚠️ **Do not use this tool to obfuscate important files. The developer is not responsible for any losses incurred.**

⚠️ **No in-depth testing has been conducted. Please back up important files before use to prevent data loss.**
