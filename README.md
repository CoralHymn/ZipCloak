# ZipCloak - zip文件混淆工具

版权所属:coralhymn | 琴海奶油

开源协议:GPL-2.0

<div align="center">

### [🇺🇸 English](README-EN.md) | [🇨🇳 简体中文](README.md)

</div>

功能：对指定类型的文件进行混淆处理，使得某个文件被系统认为是文件夹

# 使用说明：

## [混淆模式]

1. 在【混淆】选项卡中选择源文件夹和输出zip文件位置与设置名称

2. 选择需要混淆的文件扩展名

3. 点击开始混淆生成加密的 ZIP 文件

## [恢复模式]

1. 在【恢复】选项卡中选择混淆后的 ZIP 文件

2. 设置输出目录并点击开始恢复（请不要选择根目录，建议自行创建一个子目录）

## [配置文件]

在首次运行时，会在软件根目录自动生成一个配置文件zipcloak_config.json，请勿随意删除此文件，此文件将保存您的配置信息，下次运行时将自动读取此文件

您在[混淆模式]中添加的文件扩展名将保存在配置文件中，若需要删除您添加的文件扩展名请删除该文件即可（也可以对json文件进行修改）

---

# 多语言支持说明

ZipCloak 现已支持多语言功能，默认提供中文 (zh) 和英文 (en) 两种语言。

## 如何切换语言

在应用程序界面顶部工具栏中，您会看到一个语言选择下拉框（🌐 Language / 语言），点击并选择您需要的语言即可。

**注意：** 切换语言后需要重启应用以完全生效。

## 如何添加新的语言包

如果您想添加其他语言的支持，可以按照以下步骤操作：

### 1. 创建语言文件

在 `lang` 目录下创建一个新的 JSON 文件，命名为 `{语言代码}.json`。

例如，要添加日语支持，创建文件 `lang/jp.json`。

### 2. 复制现有语言包内容

复制 `zh.json` 或 `en.json` 的内容到您的新文件中作为模板。

### 3. 翻译所有文本

将 JSON 文件中的值翻译成您的目标语言。确保保持键名不变。

示例结构：

```json
{
  "app_title": "Your Language - App Title",
  "tab_obfuscate": "🔒 Obfuscate Mode",
  "tab_restore": "🔓 Restore Mode",
  ...
}
```

### 4. 测试

重启应用程序，在语言选择下拉框中应该能看到您新添加的语言选项。

## 可用的语言键位

以下是所有可翻译的键位列表及其说明：

- `app_title`: 应用程序窗口标题
- `tab_obfuscate`: 混淆模式选项卡标题
- `tab_restore`: 恢复模式选项卡标题
- `tab_about`: 关于选项卡标题
- `tab_license`: LICENSE 选项卡标题
- `status_ready`: 状态栏就绪文本
- `status_obfuscating`: 正在混淆时的状态
- `status_restoring`: 正在恢复时的状态
- `status_obfuscate_done`: 混淆完成状态
- `status_restore_done`: 恢复完成状态
- `status_obfuscate_fail`: 混淆失败状态
- `status_restore_fail`: 恢复失败状态
- `label_source`: 源文件夹标签
- `label_output_zip`: 输出 ZIP 标签
- `label_obf_suffix`: 混淆后缀标签
- `label_compress`: 启用压缩复选框
- `label_input_zip`: 混淆 ZIP 标签
- `label_output_dir`: 输出目录标签
- `label_restore_suffix`: 恢复后缀标签
- `label_custom`: 自定义标签
- `label_log`: 运行日志标签
- `btn_browse`: 浏览按钮
- `btn_save_as`: 保存为按钮
- `btn_select`: 选择按钮
- `btn_add`: 添加按钮
- `btn_select_all`: 全选按钮
- `btn_clear`: 清空按钮
- `btn_start_obfuscate`: 开始混淆按钮
- `btn_start_restore`: 开始恢复按钮
- `msg_param_missing`: 参数缺失消息标题
- `msg_fill_path`: 填写路径提示
- `msg_fill_input_output`: 填写输入输出提示
- `msg_no_suffix_title`: 确认对话框标题
- `msg_no_suffix_obf`: 未选择混淆后缀提示
- `msg_no_suffix_rst`: 未选择恢复后缀提示
- `msg_success`: 成功消息标题
- `msg_obf_done`: 混淆完成消息
- `msg_restore_done`: 恢复完成消息
- `msg_error`: 错误消息标题
- `msg_obf_fail`: 混淆失败消息
- `msg_restore_fail`: 恢复失败消息
- `log_add_suffix`: 添加自定义后缀日志
- `log_error`: 错误日志
- `about_text`: 关于文本
- `about_detail`: 关于详细文本

## 贡献您的语言包

如果您创建了新的语言包，欢迎通过 Pull Request 提交到主仓库，让更多用户能够使用他们的母语！




---

本项目基于我的个人项目 https://github.com/CoralHymn/RWMP2_Decryptor 的基础上进行修改

若您是需要对[RWMP2]加密的文件进行解密请勿使用此工具，请使用上方的专属版本！！




注意事项：

请勿使用此工具对重要文件进行混淆处理、本人对产生的损失不负任何责任

本人未进行深度测试，在使用此工具时请对重要文件进行备份处理，防止文件丢失
