# TengYoda Logistics — English-only website

这是 `https://tengyodalogistics.com` 的纯英文主仓库文件。

## 目录说明

- `site/`：英文网站页面、样式、脚本和图片。
- `articles/`：英文 Markdown 博文。
- `pages/`：英文 About、Contact 和进口商落地页内容。
- `article-images/`：博文配图。
- `tools/`：把 Markdown 自动生成网页的脚本。
- `.github/workflows/`：GitHub Pages 自动部署配置。

网站不再使用 `articles-zh/`、`pages-zh/` 或语言切换脚本。

部署流程会读取 GitHub Pages 当前的站点路径：使用仓库预览地址时自动兼容
`/仓库名/`，以后绑定独立域名时自动切换为根目录，无需重新修改网站链接。

## 发布新英文博文

1. 在 `articles/` 中新建英文文件，例如 `shipping-cost-guide.md`。
2. 参照已有文章填写标题、日期、摘要、分类、关键词、封面和正文。
3. `language` 必须填写 `en`。
4. 提交到 `main` 分支后，GitHub Actions 会自动生成博文并部署。

## 修改主要英文页面

编辑 `pages/` 内对应文件：

- `about.md`：关于我们。
- `contact.md`：联系我们。
- 其他文件：面向进口商的服务与关键词页面。

提交后 GitHub Actions 会自动发布，无需手动修改生成后的 HTML。

## 首次上传

应把本压缩包解压后，将里面的所有文件和文件夹上传到仓库根目录。`.github` 是部署所需目录，不能遗漏。
