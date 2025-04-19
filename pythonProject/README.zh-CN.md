# Gemini API 密钥检查工具

这是一个 Python 脚本，用于检查 Gemini API 密钥的有效性。它通过向 Gemini API 发送简单的请求来验证密钥是否有效，并将有效的密钥保存到输出文件中。

[English Version](README.md)

## 简介

该工具旨在帮助用户快速验证多个 Gemini API 密钥的有效性。它会读取一个包含 API 密钥的输入文件，逐一测试每个密钥，并将有效的密钥写入到一个输出文件中。工具使用了一个成本较低、响应较快的模型 `gemini-1.5-flash-latest` 进行测试，以减少资源消耗。

## 安装

1. 确保您已经安装了 Python 3。
2. 安装必要的依赖库：

   ```bash
   pip install requests
   ```

   或者使用提供的 `requirements.txt` 文件：

   ```bash
   pip install -r requirements.txt
   ```

## 使用方法

1. 创建一个名为 `gemini_key.txt` 的文本文件，将您要测试的 Gemini API 密钥逐行写入文件中，每行一个密钥。
2. 运行脚本：

   ```bash
   python check_gemini_keys.py
   ```

3. 脚本会逐一检查每个密钥，并在控制台中显示检查结果。有效的密钥将被保存到 `valid_key.txt` 文件中。

## 配置选项

脚本中包含以下配置选项，您可以根据需要修改 `check_gemini_keys.py` 文件中的相关参数：

- **INPUT_FILENAME**: 输入文件名，默认为 `gemini_key.txt`。
- **OUTPUT_FILENAME**: 输出文件名，默认为 `valid_key.txt`。
- **MODEL_NAME**: 用于测试的模型名称，默认为 `gemini-1.5-flash-latest`。
- **REQUEST_TIMEOUT**: 请求超时时间（秒），默认为 10 秒。
- **DELAY_BETWEEN_REQUESTS**: 每次请求之间的延迟（秒），默认为 0.5 秒，用于防止触发速率限制。

## 输出信息

在运行过程中，脚本会输出以下信息：

- 每个密钥的检查状态，包括是否有效以及具体的错误信息（如果有）。
- 检查完成的总结信息，显示有效密钥的数量和总检查数量。
- 有效密钥将被写入到指定的输出文件中。

## 注意事项

- 请确保在运行脚本之前已启用 Gemini API 并具有相应的权限。
- 如果遇到速率限制问题，可以尝试增加 `DELAY_BETWEEN_REQUESTS` 的值。
- 脚本会使用 ANSI 颜色代码在控制台中显示不同类型的消息（绿色表示有效，红色表示错误，黄色表示警告）。

## 许可证

本项目遵循 MIT 许可证。详情请参见 `LICENSE` 文件（如果有）。