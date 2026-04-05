# 安装和验证清单

## 文件清单

### Python 节点文件 (4个)
- [x] `fast_groups_muter.py` - Fast Groups Muter 节点
- [x] `fast_muter.py` - Fast Muter 节点
- [x] `image_comparer.py` - Image Comparer 节点
- [x] `seed.py` - Seed 节点

### JavaScript 前端文件 (14个核心文件)
- [x] `web/js/fast_groups_muter.js` - Fast Groups Muter 完整版
- [x] `web/js/fast_groups_muter_entry.js` - Fast Groups Muter 简化版
- [x] `web/js/muter.js` - Fast Muter
- [x] `web/js/image_comparer.js` - Image Comparer
- [x] `web/js/seed.js` - Seed
- [x] `web/js/base_node.js` - 基础节点类
- [x] `web/js/base_any_input_connected_node.js` - 输入连接基类
- [x] `web/js/base_node_mode_changer.js` - 模式切换基类
- [x] `web/js/rgthree.js` - rgthree 核心
- [x] `web/js/constants.js` - 常量定义
- [x] `web/js/utils.js` - 工具函数
- [x] `web/js/utils_canvas.js` - Canvas 工具
- [x] `web/js/utils_widgets.js` - Widget 工具
- [x] `web/js/feature_import_individual_nodes.js` - 导入功能

### 共享组件 (2个)
- [x] `web/js/common/dialog.js` - 对话框
- [x] `web/js/common/shared_utils.js` - 共享工具

### 服务模块 (2个)
- [x] `web/js/services/fast_groups_service.js` - 组服务
- [x] `web/js/services/key_events_services.js` - 键盘事件

### 文档文件 (6个)
- [x] `README.md` - 主文档
- [x] `RGTHREE_NODES_README.md` - rgthree 节点详细说明
- [x] `FAST_GROUPS_MUTER_README.md` - Fast Groups Muter 详细说明
- [x] `QUICK_START.md` - 快速开始
- [x] `MIGRATION_SUMMARY.md` - 移植总结
- [x] `INSTALLATION_CHECKLIST.md` - 本文件

### 配置文件
- [x] `__init__.py` - 节点注册（已更新）
- [x] `requirements.txt` - 依赖列表

## 安装步骤

### 1. 克隆仓库
```bash
cd ComfyUI/custom_nodes
git clone https://github.com/YOUR_USERNAME/ComfyUI_Swwan
```

### 2. 安装依赖
```bash
cd ComfyUI_Swwan
pip install -r requirements.txt
```

### 3. 验证文件结构
```bash
# 检查 Python 文件
ls -la *.py | grep -E "(fast_|seed|image_comparer)"

# 检查 JavaScript 文件
ls -la web/js/*.js

# 检查子目录
ls -la web/js/common/
ls -la web/js/services/
```

### 4. 重启 ComfyUI
```bash
# 停止 ComfyUI
# 重新启动 ComfyUI
```

## 验证清单

### 启动验证
- [ ] ComfyUI 启动无错误
- [ ] 控制台没有 JavaScript 错误
- [ ] 节点菜单中出现 "rgthree" 分类

### 节点可见性验证
在节点菜单中检查以下节点：
- [ ] Fast Groups Muter (rgthree)
- [ ] Fast Muter (rgthree)
- [ ] Image Comparer (rgthree)
- [ ] Seed (rgthree)

### Fast Groups Muter 功能验证
1. [ ] 创建一个组（选择节点 → 右键 → Add Group）
2. [ ] 添加 Fast Groups Muter 节点
3. [ ] 节点显示组的开关
4. [ ] 点击开关可以切换组内节点的状态
5. [ ] 右键菜单显示批量操作选项
6. [ ] 属性面板可以配置过滤和排序

### Fast Muter 功能验证
1. [ ] 添加 Fast Muter 节点
2. [ ] 连接其他节点到 Fast Muter
3. [ ] 节点显示连接节点的开关
4. [ ] 点击开关可以切换节点状态
5. [ ] 右键菜单显示批量操作选项

### Image Comparer 功能验证
1. [ ] 添加 Image Comparer 节点
2. [ ] 连接两张图片
3. [ ] 执行工作流
4. [ ] 节点显示图片对比界面
5. [ ] Slide 模式：鼠标悬停可以滑动对比
6. [ ] 切换到 Click 模式：点击可以切换图片
7. [ ] 批次图片可以选择要对比的图片

### Seed 功能验证
1. [ ] 添加 Seed 节点
2. [ ] 连接到 KSampler
3. [ ] 点击 "🎲 Randomize Each Time" 按钮
4. [ ] 执行工作流，每次种子不同
5. [ ] 点击 "🎲 New Fixed Random" 按钮
6. [ ] 执行工作流，种子固定
7. [ ] 点击 "♻️ Use Last Queued Seed" 按钮
8. [ ] 种子恢复到上次使用的值
9. [ ] 右键菜单 → "Show/Hide Last Seed Value"
10. [ ] 显示/隐藏上次种子值

## 常见问题排查

### 节点不显示
**问题**: 节点菜单中没有 rgthree 分类

**检查**:
1. [ ] 确认 `__init__.py` 已更新
2. [ ] 确认 `WEB_DIRECTORY = "./web/js"` 已添加
3. [ ] 确认所有 Python 文件存在
4. [ ] 重启 ComfyUI

**解决**:
```bash
# 检查 __init__.py
cat __init__.py | grep "WEB_DIRECTORY"

# 检查节点注册
cat __init__.py | grep "NODE_CLASS_MAPPINGS.update"
```

### JavaScript 错误
**问题**: 浏览器控制台显示 JavaScript 错误

**检查**:
1. [ ] 确认所有 JavaScript 文件已复制
2. [ ] 确认 `web/js/common/` 目录存在
3. [ ] 确认 `web/js/services/` 目录存在
4. [ ] 检查文件路径是否正确

**解决**:
```bash
# 检查文件完整性
ls -la web/js/*.js | wc -l  # 应该是 14
ls -la web/js/common/*.js | wc -l  # 应该是 2
ls -la web/js/services/*.js | wc -l  # 应该是 2
```

### Fast Groups Muter 不显示组
**问题**: Fast Groups Muter 节点是空的

**检查**:
1. [ ] 确认已创建组
2. [ ] 确认组有标题
3. [ ] 检查过滤条件（matchColors, matchTitle）

**解决**:
1. 选择一些节点
2. 右键 → "Add Group"
3. 设置组标题和颜色
4. 刷新 Fast Groups Muter 节点

### Image Comparer 不显示图片
**问题**: Image Comparer 节点不显示图片

**检查**:
1. [ ] 确认图片已生成
2. [ ] 检查浏览器控制台错误
3. [ ] 确认图片路径正确

**解决**:
1. 确保工作流已执行
2. 检查图片是否保存到临时目录
3. 尝试刷新浏览器

### Seed 值不变
**问题**: Seed 节点的值不改变

**检查**:
1. [ ] 确认没有设置为固定种子
2. [ ] 确认点击了正确的按钮
3. [ ] 检查是否有其他节点覆盖种子

**解决**:
1. 点击 "🎲 Randomize Each Time"
2. 重新执行工作流
3. 检查种子值是否变化

## 性能检查

### 启动时间
- [ ] ComfyUI 启动时间正常（< 30秒）
- [ ] 节点加载时间正常（< 5秒）

### 运行时性能
- [ ] Fast Groups Muter 响应流畅（< 100ms）
- [ ] Fast Muter 响应流畅（< 100ms）
- [ ] Image Comparer 滑动流畅（60fps）
- [ ] Seed 按钮响应即时（< 50ms）

### 内存使用
- [ ] 内存使用正常（增加 < 100MB）
- [ ] 没有内存泄漏

## 文档检查

### 文档完整性
- [ ] README.md 包含所有节点说明
- [ ] RGTHREE_NODES_README.md 详细说明每个节点
- [ ] QUICK_START.md 提供快速开始指南
- [ ] 所有文档链接正确

### 示例和教程
- [ ] 每个节点都有使用示例
- [ ] 常见用例有说明
- [ ] 故障排除指南完整

## 最终确认

### 功能完整性
- [ ] 所有 4 个节点都能正常工作
- [ ] 所有核心功能都已实现
- [ ] 所有 UI 交互都正常

### 代码质量
- [ ] Python 代码符合 PEP 8
- [ ] JavaScript 代码格式一致
- [ ] 没有明显的 bug

### 文档质量
- [ ] 所有文档都是最新的
- [ ] 说明清晰易懂
- [ ] 示例代码可运行

### 用户体验
- [ ] 节点易于查找
- [ ] 操作直观
- [ ] 错误提示清晰

## 发布前检查

### 代码仓库
- [ ] 所有文件已提交
- [ ] .gitignore 配置正确
- [ ] README.md 更新完整

### 许可证
- [ ] LICENSE 文件存在
- [ ] 致谢 rgthree-comfy

### 版本信息
- [ ] 版本号已设置
- [ ] 更新日志已创建

## 完成！

如果所有检查项都通过，恭喜！节点移植成功完成。

如有任何问题，请参考：
- `RGTHREE_NODES_README.md` - 详细说明
- `QUICK_START.md` - 快速开始
- `MIGRATION_SUMMARY.md` - 移植总结

或在 GitHub 上提交 Issue。
