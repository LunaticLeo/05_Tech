// 汉字 [\u4e00-\u9fa5]

const fs = require('fs');

async function main() {
	const filePath = 'test.txt'; // 你需要替换成你的文件路径
	const fileContent = fs.readFileSync(filePath, 'utf-8');

	// 使用正则表达式以数字+“章”为分隔符进行分割
	const chapters = fileContent.split(/[0-9]+章/).filter(chapter => chapter.trim() !== '');
	// 计算每个章节的长度
	for (let i = 0; i < chapters.length; i++) {
		const chapterText = chapters[i].trim();
		const chapterLength = chapterText.length;

		if (chapterLength < 1000) {
			console.log(`第${i + 1}章长度: ${chapterLength}字符`);
			console.log(chapterText);
		}
	}
}

main();
