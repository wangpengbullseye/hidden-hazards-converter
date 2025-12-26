"""
煤矿采空区数据集转换Web应用
基于Streamlit构建的CSV到JSON转换工具

版本: 1.0.0
"""

import streamlit as st
import pandas as pd
import json
import zipfile
from io import BytesIO
from pathlib import Path
import sys

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from ToJson import ToJson
from Validator import Validator

# 页面配置
st.set_page_config(
    page_title="煤矿采空区数据集转换工具",
    page_icon="⛏️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 标题
st.title("⛏️ 煤矿采空区数据集转换工具")
st.markdown("**将CSV格式的采空区普查数据转换为JSON格式，符合KAT 22.2-2024标准**")

# 侧边栏
with st.sidebar:
    st.header("📋 使用说明")
    st.markdown("""
    ### 步骤：
    1. 输入煤矿名称
    2. 上传CSV文件（最多10个表）
    3. 点击"转换为JSON"
    4. 下载转换结果
    
    ### 支持的表：
    - 采空区基本信息
    - 采空区积水信息
    - 采空区积气信息
    - 自燃发火信息
    - 采空区悬顶信息
    - 采空区塌陷信息
    - 地裂缝信息
    - 废弃井筒信息
    - 密闭墙信息
    - 采空区治理信息
    """)
    
    st.divider()
    st.markdown("**版本**: 1.0.0")
    st.markdown("**标准**: KAT 22.2-2024")

# 主界面
tab1, tab2, tab3 = st.tabs(["📤 数据转换", "✅ 数据验证", "📖 帮助文档"])

# Tab 1: 数据转换
with tab1:
    st.header("数据转换")
    
    # 输入煤矿名称
    mine_name = st.text_input(
        "煤矿名称",
        placeholder="例如：河西联办煤矿",
        help="请输入煤矿的完整名称"
    )
    
    # 文件上传
    st.subheader("上传CSV文件")
    uploaded_files = st.file_uploader(
        "选择CSV文件（可多选）",
        type=['csv'],
        accept_multiple_files=True,
        help="支持上传1-10个CSV文件"
    )
    
    if uploaded_files:
        st.success(f"已上传 {len(uploaded_files)} 个文件")
        
        # 显示上传的文件
        with st.expander("查看上传的文件"):
            for file in uploaded_files:
                st.text(f"📄 {file.name}")
    
    # 转换按钮
    if st.button("🚀 转换为JSON", type="primary", disabled=not (mine_name and uploaded_files)):
        with st.spinner("正在转换..."):
            try:
                # 保存上传的文件到临时目录
                temp_dir = Path("temp_upload")
                temp_dir.mkdir(exist_ok=True)
                
                for file in uploaded_files:
                    file_path = temp_dir / file.name
                    with open(file_path, 'wb') as f:
                        f.write(file.getbuffer())
                
                # 转换
                converter = ToJson(data_dir=str(temp_dir))
                result = converter.convert_mine(mine_name)
                
                # 显示统计
                st.success("✅ 转换成功！")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("总记录数", sum(result['statistics'].values()))
                with col2:
                    st.metric("表数量", len([v for v in result['statistics'].values() if v > 0]))
                with col3:
                    st.metric("数据版本", result['mine_info']['data_version'])
                
                # 显示详细统计
                with st.expander("📊 详细统计"):
                    stats_df = pd.DataFrame([
                        {"表名": k, "记录数": v}
                        for k, v in result['statistics'].items()
                    ])
                    st.dataframe(stats_df, use_container_width=True)
                
                # 下载按钮
                json_str = json.dumps(result, ensure_ascii=False, indent=2)
                st.download_button(
                    label="📥 下载JSON文件",
                    data=json_str,
                    file_name=f"{mine_name}-采空区数据集.json",
                    mime="application/json"
                )
                
                # 清理临时文件
                import shutil
                shutil.rmtree(temp_dir)
                
            except Exception as e:
                st.error(f"❌ 转换失败: {str(e)}")

# Tab 2: 数据验证
with tab2:
    st.header("数据验证")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("上传CSV文件")
        csv_files = st.file_uploader(
            "选择CSV文件",
            type=['csv'],
            accept_multiple_files=True,
            key="validator_csv"
        )
    
    with col2:
        st.subheader("上传JSON文件")
        json_file = st.file_uploader(
            "选择JSON文件",
            type=['json'],
            key="validator_json"
        )
    
    if st.button("🔍 验证数据", disabled=not (csv_files and json_file)):
        with st.spinner("正在验证..."):
            try:
                # 保存文件
                temp_dir = Path("temp_validate")
                temp_dir.mkdir(exist_ok=True)
                
                # 保存CSV
                for file in csv_files:
                    file_path = temp_dir / file.name
                    with open(file_path, 'wb') as f:
                        f.write(file.getbuffer())
                
                # 保存JSON
                json_path = temp_dir / json_file.name
                with open(json_path, 'wb') as f:
                    f.write(json_file.getbuffer())
                
                # 验证
                validator = Validator()
                
                # 从文件名提取煤矿名称
                mine_name_val = json_file.name.split('-')[0]
                
                csv_result = validator.validate_csv(mine_name_val, str(temp_dir))
                json_result = validator.validate_json(str(json_path))
                compare_result = validator.compare_csv_json(mine_name_val, str(json_path), str(temp_dir))
                
                # 显示结果
                if compare_result['match']:
                    st.success("✅ 验证通过！CSV和JSON数据一致。")
                else:
                    st.error("❌ 验证失败！CSV和JSON数据不一致。")
                
                # 详细结果
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("CSV表数", f"{csv_result['found_tables']}/10")
                with col2:
                    st.metric("CSV记录数", csv_result['total_records'])
                with col3:
                    st.metric("JSON记录数", json_result['total_records'])
                
                # 比对详情
                with st.expander("📋 比对详情"):
                    for table_cn, details in compare_result['table_comparison'].items():
                        status_icon = "✅" if details['match'] else "❌"
                        st.text(f"{status_icon} {table_cn}: CSV={details['csv_records']}, JSON={details['json_records']}")
                
                # 错误和警告
                if csv_result['errors'] or json_result['errors'] or compare_result['errors']:
                    with st.expander("⚠️ 错误信息"):
                        for error in csv_result['errors'] + json_result['errors'] + compare_result['errors']:
                            st.error(error)
                
                # 清理
                import shutil
                shutil.rmtree(temp_dir)
                
            except Exception as e:
                st.error(f"❌ 验证失败: {str(e)}")

# Tab 3: 帮助文档
with tab3:
    st.header("帮助文档")
    
    st.markdown("""
    ## 📖 使用指南
    
    ### 1. 数据转换
    
    #### 步骤：
    1. 在"数据转换"标签页输入煤矿名称
    2. 上传CSV文件（支持1-10个文件）
    3. 点击"转换为JSON"按钮
    4. 下载生成的JSON文件
    
    #### 文件命名规范：
    CSV文件必须遵循以下命名格式：
    ```
    {煤矿名称}-{表名}.csv
    ```
    
    例如：
    - 河西联办煤矿-采空区基本信息.csv
    - 河西联办煤矿-采空区积水信息.csv
    
    ### 2. 数据验证
    
    #### 步骤：
    1. 在"数据验证"标签页上传CSV文件
    2. 上传对应的JSON文件
    3. 点击"验证数据"按钮
    4. 查看验证结果
    
    ### 3. 支持的表
    
    本工具支持以下10个表：
    
    | 表名 | 说明 |
    |------|------|
    | 采空区基本信息 | 采空区形成时间、埋深、位置、面积等 |
    | 采空区积水信息 | 积水面积、水位标高、水质、积水量等 |
    | 采空区积气信息 | 瓦斯及有毒有害气体成分等 |
    | 自燃发火信息 | 火区位置、范围、温度、气体成分等 |
    | 采空区悬顶信息 | 顶板垮落情况、悬顶位置及面积等 |
    | 采空区塌陷信息 | 地表塌陷情况 |
    | 地裂缝信息 | 裂缝位置、深度、长度、宽度等 |
    | 废弃井筒信息 | 井筒形式、位置、封闭方法等 |
    | 密闭墙信息 | 密闭分布位置、规格情况等 |
    | 采空区治理信息 | 治理工程信息 |
    
    ### 4. JSON格式
    
    转换后的JSON文件包含三个部分：
    
    ```json
    {
      "mine_info": {
        "mine_id": "...",
        "mine_name": "...",
        "standard": "KAT 22.2-2024"
      },
      "statistics": {
        "goaf_basic_info": 29,
        ...
      },
      "data": {
        "goaf_basic_info": [...],
        ...
      }
    }
    ```
    
    ### 5. 注意事项
    
    - ✅ CSV文件必须使用UTF-8编码（工具支持自动检测多种编码）
    - ✅ 文件命名必须符合规范
    - ✅ 部分表缺失时仍可转换（缺失的表将为空数组）
    - ✅ 空值会自动转换为JSON的null
    
    ### 6. 标准依据
    
    本工具符合 **KAT 22.2-2024 矿山隐蔽致灾因素普查规范 第2部分：煤矿** 标准。
    
    ---
    
    ## 🔗 相关链接
    
    - [GitHub仓库](#)
    - [技术文档](#)
    - [问题反馈](#)
    """)

# 页脚
st.divider()
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>煤矿采空区数据集转换工具 v1.0.0 | 符合 KAT 22.2-2024 标准</p>
    <p>© 2024 煤矿采空区普查数据标准化工作组</p>
</div>
""", unsafe_allow_html=True)

