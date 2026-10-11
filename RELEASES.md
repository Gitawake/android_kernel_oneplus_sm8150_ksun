# 构建成功后自动发布 Releases

下载页：https://github.com/Gitawake/android_kernel_oneplus_sm8150_ksun/releases

在 `los-23.2-ksun-v3.4.1` 分支推送代码，或手动运行 **Build LOS 23.2 KernelSU Next**。完整构建成功后，**Publish successful kernel build** 自动下载该次产物，校验固定原厂 boot 与 WLAN、核对 412 个模块符号 CRC、回包，再创建独立预发布版本。

标签格式为 `hotdog-los23.2-ksun-v3.4.1-构建编号-构建尝试次数`。每次成功构建有单独版本；失败或取消不发布。重跑发布工作流不会覆盖已经公开的同一版本；附件未传完的版本留在草稿中，全部上传成功后才公开。

源码标签使用此仓库专用的可写部署密钥推送，私钥加密保存在 Actions Secret `KSUN_RELEASE_DEPLOY_KEY`。这是为了解决 GitHub 临时令牌无法为包含工作流变更的历史提交创建标签的问题；Release 附件发布仍使用临时 `GITHUB_TOKEN`。将工作流复制到其他仓库时，需要为那个仓库单独配置部署密钥和同名 Secret。

附件包括：

- `boot-los-23.2-20260925-ksun-v3.4.1.img`：可临时启动测试的 unsigned boot。
- `kernel-build.tar.gz`：Image、模块、原始配置及构建来源资料。
- `kernel.config`、`Module.symvers`：配置及符号版本。
- `boot-repack-verification.json`、`wlan-abi.json`：回包和模块 ABI 校验。
- `kernel-commit.txt`、`ksun-commit.txt`、`toolchain.txt`：源码及工具链来源。
- `SHA256SUMS`：附件校验值。

自动发布不代表实机测试通过。只有构建 38128218220 的镜像已在本机完成启动、Root、Enforcing、Wi-Fi 和永久刷入验证，说明会单独标注；其他版本默认未实测，先备份、核对解锁和槽位、临时启动，再决定是否写入。

适用 LOS 基线固定为 **23.2-20260925-NIGHTLY-hotdog**。固定原厂材料在 `release-inputs` 分支，工作流引用不可变提交并校验解压后的 SHA-256。未来 LOS OTA 更新需要同时更新内核基线、原厂材料提交、哈希和版本说明；自动生成 Release 并不意味着自动适配新 OTA。

如发布阶段网络故障，可手动运行 **Publish successful kernel build**，输入已成功的内核构建 Run ID。发布工作流会验证仓库、分支、构建工作流路径、成功状态及产物提交，不能把失败产物当作成功版本发布。

充电 IRQ 警告在匹配 LOS 原厂内核也复现；memcg 负计数在移植测试中出现，原因仍待确认。长期稳定、Warp 快充和耗电仍需测试。
