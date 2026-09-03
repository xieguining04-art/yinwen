# 纯英文网站维护说明

## 日常更新博文

只维护 `articles/` 内的英文 Markdown 文件。每篇文件名使用小写英文字母、数字和连字符，例如：

`how-to-import-from-china.md`

文章头部 `language` 必须为 `en`。封面图片可上传到 `article-images/`，并在文章中使用 `/article-images/图片名.webp`。

## 更新 About 或 Contact

编辑 `pages/about.md` 或 `pages/contact.md`，然后直接提交到 `main` 分支。

## 不应重新添加的内容

- `articles-zh/`
- `pages-zh/`
- `site/assets/bilingual.js`
- 中文语言选择按钮

这些内容会重新引入双语状态和页面滚动兼容问题。

## 部署结果

提交后打开仓库的 `Actions`，最新一条任务显示绿色勾号即代表发布完成。请检查首页、About、Contact、Services 和 Blog 的鼠标滚轮及移动端菜单。
