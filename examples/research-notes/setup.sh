#!/bin/bash
# 初始化研究笔记 wiki

echo "初始化 Research Notes Wiki..."

# 初始化目录结构
python -m llm_wiki.cli init

# 复制配置模板
if [ ! -f config.yaml ]; then
    cp ../../config.yaml.example config.yaml
    echo "✓ 已创建 config.yaml，请编辑填入 API key"
fi

echo "✓ 初始化完成！"
echo ""
echo "下一步："
echo "1. 编辑 config.yaml，填入 ANTHROPIC_API_KEY"
echo "2. 将论文或笔记放入 raw/ 目录"
echo "3. 运行: python -m llm_wiki.cli ingest raw/your-file.pdf"
